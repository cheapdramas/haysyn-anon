let commentStart = 0;
let loadingComments = false;
let noMoreComments = false;
const commentsPerChunk = 10;
let lastCommentLoadTime = 0;
const commentLoadCooldown = 7000;

function renderComments(comments) {
  const container = document.getElementById('comments');

  comments.forEach(comment => {
    const div = document.createElement('div');
    div.classList.add('comment');

    div.innerHTML = `
      <div class="comment-header">
        <img src="/static/images/avatar.png" alt="User" class="comment-avatar">
        <span class="comment-author">Anon User</span>
      </div>
      <div class="comment-body">${comment.text}</div>
    `;

    container.appendChild(div);
  });
}

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

window.addEventListener('scroll', () => {
  const now = Date.now();
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
    if (noMoreComments) {
      if (now - lastCommentLoadTime >= commentLoadCooldown) {
        lastCommentLoadTime = now;
        const post = JSON.parse(sessionStorage.getItem('post_data'));
        loadCommentChunk(post.id);
      }
    } else {
      const post = JSON.parse(sessionStorage.getItem('post_data'));
      loadCommentChunk(post.id);
    }
  }
});

function openCommentModal() {
	document.getElementById('overlay').style.display = 'flex';
	document.getElementById('feed').classList.add('blurred');
	document.querySelector('footer').classList.add('blurred');
	document.body.style.overflow = 'hidden';
  
	setTimeout(() => {
	  autoGrow(document.getElementById('commentText'));
	}, 0);
}
  
function closeCommentModal() {
	document.getElementById('overlay').style.display = 'none';
	document.getElementById('feed').classList.remove('blurred');
	document.querySelector('footer').classList.remove('blurred');
	document.body.style.overflow = '';
}
  
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
	.then(() => window.location.reload())
	.catch(err => {
	  alert("Помилка при надсиланні");
	  console.error(err);
	});
}
document.getElementById('overlay')?.addEventListener('click', (e) => {
	if (e.target.id === 'overlay') closeCommentModal();
});


 
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


document.addEventListener("DOMContentLoaded", () => {
	const post = JSON.parse(sessionStorage.getItem('post_data'));
  
	if (!post) {
	  window.location.href = "/";
	  return;
	}
  
	const main = document.getElementById('feed');
	main.innerHTML = `
	  <div class="post">
		<h2 style="font-size: 2rem; margin-top: 0;">${post.title}</h2>
		<p style="margin-top: 1rem; white-space: pre-line;">${post.text}</p>
	  </div>
  
	  <div class="comments-section" style="margin-top: 1.5rem;">
		<h3 style="
		  text-align: center;
		  font-family: 'Dancing Script', cursive;
		  font-size: 2.2rem;
		  color: #333;
		  margin-bottom: 1rem;
		">
		  Comments
		</h3>
		<div id="comments">
		  <p style="text-align: center; color: #777;">Loading comments...</p>
		</div>
	  </div>
	`;
		loadCommentChunk(post.id);
  });
  
