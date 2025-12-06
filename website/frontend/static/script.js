// ВСЬО САМ СУКА
// --- Керуємо scroll restoration ---
if ("scrollRestoration" in history) {
  history.scrollRestoration = "auto";
}

console.log(window.Telegram.WebApp.initData)

const selectSortBy = document.getElementById("selectSortBy")

console.log(sessionStorage)

// позначаємо reload
window.addEventListener("beforeunload", () => {
  sessionStorage.setItem("was_reloaded", "1");
});

// після завантаження перевіряємо
window.addEventListener("DOMContentLoaded", () => {
  const wasReloaded = sessionStorage.getItem("was_reloaded");
  if (wasReloaded === "1") {
    sessionStorage.removeItem("was_reloaded");
    window.scrollTo(0, 0); // тепер точно зверху
		selectSortBy.value = "likes"
  }
});


// --- Конфіг ---
const POSTS_PER_PAGE = 50;
const CACHE_KEY = "cachedPosts";
const CACHE_TTL_MS = 5000; // 10 секунд
//
let loading = false;
let noMorePosts = false;
//
//
//
//
//
function saveToCache(posts) {
  const cacheData = {
    posts,
    timestamp: Date.now(),
  };
  localStorage.setItem(CACHE_KEY, JSON.stringify(cacheData));
}

function loadFromCache() {
  const raw = localStorage.getItem(CACHE_KEY);
  if (!raw) return null;
//
  const jsonchik = JSON.parse(raw);
	const timestamp = jsonchik["timestamp"];
	const posts = jsonchik["posts"];
	// if time till cache dies have passed
  if (Date.now() - timestamp > CACHE_TTL_MS) {
    localStorage.removeItem(CACHE_KEY);
    return null;
  }
//
  renderPosts(posts, true);
	return posts;
}
//
function renderPosts(posts, replace = false) {
  const feed = document.getElementById("feed");
  if (replace) feed.innerHTML = "";

  posts.forEach((post, index) => {
    const div = document.createElement("div");
    div.className = "post";
		let last_post = feed.lastChild;
		div.setAttribute("index", last_post == null ? 1 : parseInt(last_post.getAttribute("index")) + 1);

    const previewText =
      post.text.length === 200 ? post.text + "..." : post.text;

    div.innerHTML = `
      <a href="/post/${post.id}" class="post-link" 
         data-id="${post.id}"
         data-title="${encodeURIComponent(post.title)}" 
         data-text="${encodeURIComponent(post.text)}"
         style="text-decoration:none;color:inherit;">
        <strong>${post.title}</strong><br>
        <span class="preview-text">${previewText}</span>
      </a>

			<div class="post-likes">
        <span>👍 ${post.likes}</span>
        <span>👎 ${post.dislikes}</span>
      </div>

			`;
    feed.appendChild(div);
  });
}


async function loadFeedChunk(sort_by="likes") {

	if (loading || noMorePosts) return;
  loading = true;
	let posts = null
	try {
		const posts_feed = document.getElementById("feed");
		
		const last_post = posts_feed.lastChild;
		console.log(last_post);
		let last_post_index = 0;
		if (last_post != null){
			last_post_index = last_post.getAttribute("index");
		}
    console.log(last_post_index);
		const res = await fetch("/api/api_v1/posts",{
            method:"POST", 
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({"limit": POSTS_PER_PAGE,"offset":last_post_index, "sort_by":sort_by,})
        });

		posts = await res.json();

		if (posts.length === 0) {
			noMorePosts = true;
		}
		renderPosts(posts);
  } catch (err) {
    console.error("Error loading posts", err);
  }

	loading = false;
	return posts;
}

function showConfirmationModal() {
  const overlay = document.getElementById("confirmationOverlay");
  overlay.style.display = "flex";
  overlay.style.opacity = "0";

  requestAnimationFrame(() => {
    overlay.style.transition = "opacity 0.3s ease";
    overlay.style.opacity = "1";
  });

  // авто-закриття через 1.8 секунди або клік мимо
  setTimeout(() => closeConfirmationModal(), 1800);

  overlay.addEventListener(
    "click",
    (e) => {
      if (e.target === overlay) closeConfirmationModal();
    },
    { once: true }
  );
}

function closeConfirmationModal() {
  const overlay = document.getElementById("confirmationOverlay");
  overlay.style.opacity = "0";
  setTimeout(() => {
    overlay.style.display = "none";
  }, 300);
}

// викликати після сабміту
async function submitPost() {
  // ... твій код відправки ...
  showConfirmationModal();
}


// --- Сабміт ---
async function submitPost() {
  const title = document.getElementById("postTitle").value.trim();
  const text = document.getElementById("postText").value.trim();
  if (!title || !text) return;

  try {
		let url = "/api/api_v1/submit_post";
		const tg = window.Telegram.WebApp;
		let userId = tg.initDataUnsafe?.user?.id;

        let http_body = {title: title, text: text}

		if (userId !== undefined) {
            http_body["telegram_user_id"] = userId.toString();
		}
		
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(http_body),
    });

    if (res.ok) {
      document.getElementById("postTitle").value = "";
      document.getElementById("postText").value = "";
      document.getElementById("titleError").textContent = "";
      document.getElementById("titleError").style.display = "none";

      closeModal();
      showConfirmationModal();
    }
  } catch (err) {
    console.error("Post failed", err);
  }
}
//
// --- Модалка ---
function openModal() {
  document.getElementById("overlay").style.display = "flex";
  document.getElementById("feed").classList.add("blurred");
  document.getElementById("dock").classList.add("blurred");
  document.body.style.overflow = "hidden";
  document.getElementById("titleError").textContent = "";
  document.getElementById("titleError").style.display = "none";

  setTimeout(() => {
    autoGrow(document.getElementById("postText"));
  }, 0);
}
//
function closeModal() {
  document.getElementById("overlay").style.display = "none";
  document.getElementById("feed").classList.remove("blurred");
  document.getElementById("dock").classList.remove("blurred");
  document.body.style.overflow = "";
}

// --- AutoGrow ---
function autoGrowDesktop(elem) {
  const modal = document.getElementById("modal");
  const error = document.getElementById("titleError");
  const errorHeight =
    error.offsetHeight && error.style.display !== "none"
      ? error.offsetHeight
      : 0;
  const maxModalHeight = window.innerHeight * 0.95;
  const paddingHeight = 200 + errorHeight;
  const maxTextareaHeight = maxModalHeight - paddingHeight;
  const minModalHeight = 200;

  const prevScrollTop = elem.scrollTop;
  elem.style.height = "auto";
  const newScrollHeight = elem.scrollHeight;

  if (newScrollHeight <= maxTextareaHeight) {
    elem.style.height = newScrollHeight + "px";
    elem.style.overflowY = "hidden";
    modal.style.height =
      Math.max(minModalHeight, newScrollHeight + paddingHeight) + "px";
    modal.style.overflowY = "hidden";
  } else {
    elem.style.height = maxTextareaHeight + "px";
    elem.style.overflowY = "auto";
    modal.style.height = maxModalHeight + "px";
    modal.style.overflowY = "auto";
  }

  elem.scrollTop = prevScrollTop;
}

function autoGrowMobile(elem) {
  elem.style.height = "auto";
  elem.style.height = elem.scrollHeight + "px";
}

function isMobileDevice() {
  return /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
}

function autoGrow(elem) {
  if (isMobileDevice()) autoGrowMobile(elem);
  else autoGrowDesktop(elem);
}
//
// --- Валідація title ---
document.getElementById("postTitle").addEventListener("input", function () {
  const maxLength = 40;
  const error = document.getElementById("titleError");

  if (this.value.length > maxLength) {
    this.value = this.value.slice(0, maxLength);
    error.textContent = "Максимум 40 символів";
    error.classList.add("visible");
  } else {
    error.textContent = "";
    error.classList.remove("visible");
  }
});

//

//
document.getElementById("add").addEventListener("click", () => {
  openModal();
});
//
document.getElementById("overlay").addEventListener("click", (e) => {
  if (e.target.id === "overlay") closeModal();
});


document.getElementById("up").addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});
//
document.getElementById("down").addEventListener("click", () => {
  const feed = document.getElementById("feed");
  const lastPost = feed.lastElementChild;
  if (lastPost) {
    lastPost.scrollIntoView({ behavior: "smooth" });
  }
});

document.getElementById("home").addEventListener("click", () => {
	window.location.href = `${window.location.origin}/`;
});


selectSortBy.onchange = function() {
  start = 0;
  noMorePosts = false;
  document.getElementById("feed").innerHTML = "";
	const selectedValue = selectSortBy.value;

	loadFeedChunk(selectedValue);
	window.localStorage.clear();
	window.scrollTo({ top: 0, behavior: "smooth" });
}

window.addEventListener("scroll", () => {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
		const selectedValue = selectSortBy.value;
    loadFeedChunk(selectedValue);
  }
});



if (!loadFromCache()) {
	loadFeedChunk().then((posts) => {;
		if (posts != null) {
			saveToCache(posts);
		}
	});
}

