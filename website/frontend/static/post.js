let commentStart = 0;
let loadingComments = false;
let noMoreComments = false;
const commentsPerChunk = 10;
let lastCommentLoadTime = 0;
const commentLoadCooldown = 7000;

// --- Безопасный рендер комментариев ---
function renderComments(comments) {
  const container = document.getElementById('comments');

  comments.forEach(comment => {
    const div = document.createElement('div');
    div.classList.add('comment');

    // header
    const header = document.createElement('div');
    header.classList.add('comment-header');

    const avatar = document.createElement('img');
    avatar.src = "/static/images/avatar.png";
    avatar.alt = "User";
    avatar.classList.add('comment-avatar');

    const author = document.createElement('span');
    author.classList.add('comment-author');
    author.textContent = "Anon User";

    header.appendChild(avatar);
    header.appendChild(author);

    // body
    const body = document.createElement('div');
    body.classList.add('comment-body');
    body.textContent = comment.text; // безопасно

    div.appendChild(header);
    div.appendChild(body);

    container.appendChild(div);
  });
}

// --- Загрузка комментариев по чанкам ---
async function loadCommentChunk(postId) {
  if (loadingComments) return;
  loadingComments = true;

  try {
    const res = await fetch(`/api/api_v1/comments?post_id=${postId}&start=${commentStart}&amount=${commentsPerChunk}`);
    const comments = await res.json();

    if (commentStart === 0) {
      document.getElementById('comments').innerHTML = '';
    }

    if (comments.length < commentsPerChunk) {
      noMoreComments = true;
    } else {
      noMoreComments = false;
    }

    renderComments(comments);
    commentStart += comments.length;
  } catch (err) {
    console.error('Error loading comments:', err);
    document.getElementById('comments').innerHTML = `
      <p style="text-align: center; color: red;">Failed to load comments 😢</p>
    `;
  }

  loadingComments = false;
}

// --- Скролл для подгрузки ---
window.addEventListener('scroll', () => {
  const now = Date.now();
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
    const post = JSON.parse(sessionStorage.getItem('post_data'));
    if (!post) return;

    if (noMoreComments) {
      if (now - lastCommentLoadTime >= commentLoadCooldown) {
        lastCommentLoadTime = now;
        loadCommentChunk(post.id);
      }
    } else {
      loadCommentChunk(post.id);
    }
  }
});

// --- Модалка ---
function openCommentModal() {
  document.getElementById('overlay').style.display = 'flex';
  document.getElementById('feed').classList.add('blurred');
  document.querySelector('footer').classList.add('blurred');
  document.body.style.overflow = 'hidden';

  setTimeout(() => autoGrow(document.getElementById('commentText')), 0);
}

function closeCommentModal() {
  document.getElementById('overlay').style.display = 'none';
  document.getElementById('feed').classList.remove('blurred');
  document.querySelector('footer').classList.remove('blurred');
  document.body.style.overflow = '';
}

document.getElementById('overlay')?.addEventListener('click', (e) => {
  if (e.target.id === 'overlay') closeCommentModal();
});

// --- Отправка комментария ---
function submitComment() {
  const text = document.getElementById("commentText").value.trim();
  const post = JSON.parse(sessionStorage.getItem("post_data"));

  if (!text) return alert("Порожній коментар");

  fetch("/api/api_v1/comment", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ post_id: post.id, text })
  })
  .then(res => {
    if (!res.ok) throw new Error("Failed");
    return res.json();
  })
  .then(() => {
    closeCommentModal();
    document.getElementById("commentText").value = '';
    commentStart = 0;
    noMoreComments = false;
    loadCommentChunk(post.id); // безопасная перезагрузка комментариев
  })
  .catch(err => {
    alert("Помилка при надсиланні");
    console.error(err);
  });
}

// --- Автозростання textarea ---
function autoGrowDesktop(elem) {
  const modal = document.getElementById('modal');
  const maxModalHeight = window.innerHeight * 0.95;
  const paddingHeight = 82;
  const maxTextareaHeight = maxModalHeight - paddingHeight;
  const minModalHeight = 200;

  const prevScrollTop = elem.scrollTop;
  elem.style.height = 'auto';
  const newScrollHeight = elem.scrollHeight;

  if (newScrollHeight <= maxTextareaHeight) {
    elem.style.height = newScrollHeight + 'px';
    elem.style.overflowY = 'hidden';
    modal.style.height = Math.max(minModalHeight, newScrollHeight + paddingHeight) + 'px';
    modal.style.overflowY = 'hidden';
  } else {
    elem.style.height = maxTextareaHeight + 'px';
    elem.style.overflowY = 'auto';
    modal.style.height = maxModalHeight + 'px';
    modal.style.overflowY = 'auto';
  }

  elem.scrollTop = prevScrollTop;
}

function autoGrowMobile(elem) {
  elem.style.height = 'auto';
  elem.style.height = elem.scrollHeight + 'px';
}

function isMobileDevice() {
  return /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
}

function autoGrow(elem) {
  if (isMobileDevice()) autoGrowMobile(elem);
  else autoGrowDesktop(elem);
}

// --- Рендер поста на странице ---
document.addEventListener("DOMContentLoaded", () => {
  const post = JSON.parse(sessionStorage.getItem('post_data'));

  if (!post) {
    window.location.href = "/";
    return;
  }

  const main = document.getElementById('feed');
  main.innerHTML = ''; // очищаем контейнер

  // создаем элементы вручную для безопасного рендеринга
  const postDiv = document.createElement('div');
  postDiv.classList.add('post');

  const titleH2 = document.createElement('h2');
  titleH2.style.fontSize = '2rem';
  titleH2.style.marginTop = '0';
  titleH2.textContent = post.title; // безопасно

  const textP = document.createElement('p');
  textP.style.marginTop = '1rem';
  textP.style.whiteSpace = 'pre-line';
  textP.textContent = post.text; // безопасно

  postDiv.appendChild(titleH2);
  postDiv.appendChild(textP);
  main.appendChild(postDiv);

  // секция комментариев
  const commentsSection = document.createElement('div');
  commentsSection.classList.add('comments-section');
  commentsSection.style.marginTop = '1.5rem';

  const commentsHeader = document.createElement('h3');
  commentsHeader.style.textAlign = 'center';
  commentsHeader.style.fontFamily = "'Dancing Script', cursive";
  commentsHeader.style.fontSize = '2.2rem';
  commentsHeader.style.color = '#333';
  commentsHeader.style.marginBottom = '1rem';
  commentsHeader.textContent = 'Comments';

  const commentsContainer = document.createElement('div');
  commentsContainer.id = 'comments';
  const loadingMsg = document.createElement('p');
  loadingMsg.style.textAlign = 'center';
  loadingMsg.style.color = '#777';
  loadingMsg.textContent = 'Loading comments...';
  commentsContainer.appendChild(loadingMsg);

  commentsSection.appendChild(commentsHeader);
  commentsSection.appendChild(commentsContainer);
  main.appendChild(commentsSection);

  loadCommentChunk(post.id);
});
