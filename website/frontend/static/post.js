const postContainer = document.getElementById("post-container");
const commentsContainer = document.getElementById("comments-container");

const postId = window.location.pathname.split("/").pop();
let loading = false;
let noMoreComments = false;

// ------------------- РЕНДЕР ПОСТА -------------------
async function fetchPost(id) {
  const res = await fetch(`/api/api_v1/post?id=${id}`);
  if (!res.ok) throw new Error("Не удалось получить пост");
  return await res.json();
}

function renderPost(post) {
  postContainer.innerHTML = `
    <div class="post">
      <strong>${post.title}</strong>
      <p class="preview-text">${post.text}</p>
      <div class="post-likes">
        <button class="like-btn" data-id="${post.id}">👍 ${post.likes}</button>
        <button class="dislike-btn" data-id="${post.id}">👎 ${post.dislikes}</button>
      </div>
    </div>
  `;

  const likeBtn = postContainer.querySelector(".like-btn");
  const dislikeBtn = postContainer.querySelector(".dislike-btn");

  likeBtn.addEventListener("click", () => handleReaction(post.id, "like"));
  dislikeBtn.addEventListener("click", () => handleReaction(post.id, "dislike"));
}

// ------------------- ЛАЙКИ / ДИЗЛАЙКИ -------------------
async function handleReaction(postId, action) {
  const key = `reaction_${postId}`;
  const previous = localStorage.getItem(key);

  if (previous === action) return alert("Ти вже це оцінив 😉");

  try {
    const likeBtn = postContainer.querySelector(".like-btn");
    const dislikeBtn = postContainer.querySelector(".dislike-btn");

    let likeCount = parseInt(likeBtn.textContent.replace(/[^\d]/g, ""));
    let dislikeCount = parseInt(dislikeBtn.textContent.replace(/[^\d]/g, ""));

    if (action === "like") {
      if (previous === "dislike") {
        await fetch(`/api/api_v1/dislike_post?post_id=${postId}&action=minus`, { method: "PUT" });
        dislikeCount = Math.max(0, dislikeCount - 1);
      }
      const res = await fetch(`/api/api_v1/like_post?post_id=${postId}`, { method: "PUT" });
      likeCount = await res.json();
      localStorage.setItem(key, "like");
    } else {
      if (previous === "like") {
        await fetch(`/api/api_v1/like_post?post_id=${postId}&action=minus`, { method: "PUT" });
        likeCount = Math.max(0, likeCount - 1);
      }
      const res = await fetch(`/api/api_v1/dislike_post?post_id=${postId}`, { method: "PUT" });
      dislikeCount = await res.json();
      localStorage.setItem(key, "dislike");
    }

    likeBtn.textContent = `👍 ${likeCount}`;
    dislikeBtn.textContent = `👎 ${dislikeCount}`;
  } catch (err) {
    console.error(err);
  }
}

// ------------------- КОМЕНТЫ -------------------
let lastCommentIdx = 0; 
const COMMENTS_AMOUNT = 50;

async function fetchComments() {
	// const comments_container = document.getElementById("comments-container");
	// const lastComment = comments_container.lastChild;
	// let lastCommentId = 0; 
	// // if last comment exists, rewrite lastCommentId to it's id
	// if (lastComment != null) {
	// 	lastCommentId = lastComment.getAttribute("index")
	// }
	if (loading || noMoreComments) return;
  loading = true;

	try {
		const res = await fetch(`/api/api_v1/comments?post_id=${postId}&amount=${COMMENTS_AMOUNT}&start=${lastCommentIdx}`);
		if (!res.ok) throw new Error("Не удалось получить комментарии");
		const comments = await res.json();
		
		comments.forEach((comment) => {
			renderComment(comment,false);
		});

		if (comments.length === 0) {
			noMoreComments = true;
		}
		lastCommentIdx += comments.length; 
	} catch (err) {
    console.error("Error loading comments", err);
	}
	loading = false;
}

function renderComment(comment, insert = false) {
  const div = document.createElement("div");
  div.className = "post new-comment";
  div.innerHTML = `
		<div class="comment-header">
			<img class="comment-avatar" src="/static/images/avatar.png"></img>
			<p class="comment-author">Anonim user</p>
		</div>
    <p class="preview-text">${comment.text}</p>
  `;
	if (insert) {
		commentsContainer.insertBefore(div,commentsContainer.firstChild);
	}
	else {
		commentsContainer.appendChild(div);
	}
}

window.addEventListener("scroll", () => {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
    fetchComments();
  }
});


function isMobile() {
  return /Android|iPhone|iPad|iPod|Opera Mini|IEMobile|WPDesktop/i.test(navigator.userAgent);
}

// ------------------- СТВОРЮЄМО ФОРМУ КОМЕНТАРЯ -------------------
function createCommentForm() {
  if (isMobile()) return; // ❌ не показуємо на мобілці

  const container = document.getElementById("comment-form-container");
  if (!container) return;

  const form = document.createElement("div");
  form.className = "comment-form";

  form.innerHTML = `
    <textarea id="comment-input" placeholder="Напишіть коментар..." rows="1"></textarea>
    <div class="comment-actions">
      <button id="send-comment-btn">Відправити</button>
      <button id="cancel-comment-btn">Скасувати</button>
    </div>
  `;

  container.appendChild(form);

  const textarea = form.querySelector("#comment-input");
  const sendBtn = form.querySelector("#send-comment-btn");
  const cancelBtn = form.querySelector("#cancel-comment-btn");

  // Автозростання textarea вниз
  textarea.addEventListener("input", () => {
    textarea.style.height = "auto"; // скидаємо перед підрахунком
    textarea.style.height = textarea.scrollHeight + "px"; // росте вниз
  });

  cancelBtn.addEventListener("click", () => {
    textarea.value = "";
    textarea.style.height = "auto";
  });

	sendBtn.addEventListener("click", async () => {
		const text = textarea.value.trim();
		if (!text) return alert("Порожній коментар 🤔");

		try {
			const res = await fetch("/api/api_v1/comment", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ post_id: postId, text })
			});
			if (!res.ok) throw new Error("Не вдалося відправити");

			const newComment = await res.json();
			renderComment(newComment, true);  // Рендеримо новий коментар


			textarea.value = "";
			textarea.style.height = "auto";
		} catch (err) {
			console.error(err);
			alert("Помилка при відправці коментаря");
		}
	});
};

function autoGrow(e) {
  const textarea = e.target;
  textarea.style.height = "auto";
  textarea.style.height = textarea.scrollHeight + "px";
}




// const dock = document.getElementById('dock');
const addCommentBtn = document.getElementById('add-comment');
const refreshBtn = document.getElementById('refresh');
const homeBtn = document.getElementById('home');
const mobileDock = document.getElementById('mobile-dock');
const commentInput = document.getElementById('commentInput');
const test = document.getElementById('test');
const sendCommentBtn = document.getElementById('sendComment');
const closeDockCommentBtn = document.getElementById('closeDock');
const MAX_HEIGHT = 180;


function closeDockComment() {
	document.getElementById("mobile-dock").classList.add("hidden")
	document.getElementById("commentInput").blur();

	document.getElementById("dock").classList.remove("hidden")
	document.getElementById("home").classList.remove("hidden")
	document.getElementById("refresh").classList.remove("hidden")
	document.getElementById("add-comment").classList.remove("hidden")

}

async function sendComment() {
  const textarea = document.getElementById("commentInput");
  const text = textarea.value.trim();
  if (!text) return;

  try {
    const res = await fetch(`/api/api_v1/comment`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, post_id: postId }),
    });
    if (!res.ok) throw new Error("Помилка при надсиланні коментаря");

    const comment = await res.json();
    renderComment(comment, true);
    textarea.value = "";
    textarea.style.height = "auto";
  } catch (err) {
    console.error(err);
  }

	closeDockComment();
}


homeBtn.addEventListener("click", () => {
	if (history.length > 1) {
		history.back()
	}
	else {
		window.location.href = `${window.location.origin}/`;
	}
});

refreshBtn.addEventListener("click", () => {
	window.location.href = `${window.location.origin}/post/${postId}`;
});



// MOBILE DOCK behavior
test.addEventListener('touchstart', () => {
	if (document.activeElement == commentInput){
		commentInput.blur(); // ховаємо клаву
	}
})
commentInput.addEventListener('input', () => {
    commentInput.style.height = 'auto'; // скидаємо висоту для перерахунку
    const scrollHeight = commentInput.scrollHeight;
    const newHeight = Math.min(scrollHeight, MAX_HEIGHT);
    commentInput.style.height = newHeight + 'px';
    mobileDock.style.height = newHeight + 40 + 'px'; // padding dock

    commentInput.style.overflowY = scrollHeight > MAX_HEIGHT ? 'auto' : 'hidden';
    
    // щоб текст не зникав
    if (scrollHeight > MAX_HEIGHT) {
        commentInput.scrollTop = commentInput.scrollHeight;
    }
});
addCommentBtn.addEventListener("click", () => {
  // якщо на десктопі — прокручуємо до textarea під постом
  const commentInputDesktop = document.getElementById("comment-input");
  if (!isMobile()) {
    commentInputDesktop.scrollIntoView({ behavior: "smooth", block: "center" });
    commentInputDesktop.focus({ preventScroll: true });
    return;
  }

  // === Мобільний режим ===
  addCommentBtn.classList.add('hidden');
  refreshBtn.classList.add('hidden');
  homeBtn.classList.add('hidden');

  mobileDock.classList.remove("hidden");

  commentInput.focus({ preventScroll: true });
});
sendCommentBtn.addEventListener("click", () =>{
	sendComment();	
});
closeDockCommentBtn.addEventListener("click", () =>{
	closeDockComment();
	
	

});


// ------------------- ІНІЦІАЛІЗАЦІЯ -------------------
(async function init() {
  try {
    const post = await fetchPost(postId);
    renderPost(post);
    createCommentForm();
    await fetchComments();
  } catch (err) {
    console.error(err);
    postContainer.innerHTML = "<p>Не удалось загрузить пост</p>";
  }
})();
