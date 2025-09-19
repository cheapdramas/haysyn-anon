// ВСЬО САМ СУКА

// --- Конфіг ---
const POSTS_PER_PAGE = 20;
const CACHE_KEY = "cachedPosts";
const CACHE_TTL_MS = 10000; // 10 секунд
//
let start = 0;
let loading = false;
let noMorePosts = false;
//
//
function saveToCache(posts, start) {
  const cacheData = {
    posts,
    start,
    timestamp: Date.now(),
  };
  localStorage.setItem(CACHE_KEY, JSON.stringify(cacheData));
}

function loadFromCache() {
  const raw = localStorage.getItem(CACHE_KEY);
  if (!raw) return null;
//
  const { posts, start: cachedStart, timestamp } = JSON.parse(raw);
	// if time till cache dies have passed
  if (Date.now() - timestamp > CACHE_TTL_MS) {
    localStorage.removeItem(CACHE_KEY);
    return null;
  }
//
  renderPosts(posts, true);
  start = cachedStart;
  return posts;
}
//
function renderPosts(posts, replace = false) {
  const feed = document.getElementById("feed");
  if (replace) feed.innerHTML = "";

  posts.forEach((post) => {
    const div = document.createElement("div");
    div.className = "post";

    const previewText =
      post.text.length > 200 ? post.text.slice(0, 200) + "..." : post.text;

    div.innerHTML = `
      <a href="/post/${post.id}" class="post-link" 
         data-id="${post.id}" 
         data-title="${encodeURIComponent(post.title)}" 
         data-text="${encodeURIComponent(post.text)}"
         style="text-decoration:none;color:inherit;">
        <strong>${post.title}</strong><br>
        <span class="preview-text">${previewText}</span>
      </a>`;
    feed.appendChild(div);
  });
}


async function loadFeedChunk() {

	if (loading || noMorePosts) return;
  loading = true;

	try {
    const res = await fetch(`/api/api_v1/posts?start=${start}&amount=${POSTS_PER_PAGE}`);
		const posts = await res.json();

		if (posts.length === 0) {
			noMorePosts = true;
		}
		renderPosts(posts);
		start += posts.length;
		// saveToCache(posts)
  } catch (err) {
    console.error("Error loading posts", err);
  }

	loading = false;
}

//
// // --- Завантаження ---
// async function loadFeedChunk() {
  
//
//   try {
//     const res = await fetch(`/api/api_v1/posts?start=${start}&amount=${POSTS_PER_PAGE}`);
//     const posts = await res.json();
//
//     if (posts.length === 0) {
//       noMorePosts = true;
//     } else {
//       renderPosts(posts);
//       start += posts.length;
//       saveToCache(posts, start);
//     }
//   } catch (err) {
//     console.error("Error loading posts", err);
//   }
//
//   loading = false;
// }
//
// // --- Сабміт ---
// async function submitPost() {
//   const title = document.getElementById("postTitle").value.trim();
//   const text = document.getElementById("postText").value.trim();
//   if (!title || !text) return;
//
//   try {
//     const res = await fetch("/api/api_v1/post", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ title, text }),
//     });
//
//     if (res.ok) {
//       document.getElementById("postTitle").value = "";
//       document.getElementById("postText").value = "";
//       document.getElementById("titleError").textContent = "";
//       document.getElementById("titleError").style.display = "none";
//
//       localStorage.removeItem(CACHE_KEY);
//       closeModal();
//
//       start = 0;
//       noMorePosts = false;
//       document.getElementById("feed").innerHTML = "";
//       await loadFeedChunk();
//       window.scrollTo({ top: 0, behavior: "smooth" });
//     }
//   } catch (err) {
//     console.error("Post failed", err);
//   }
// }
//
// // --- Модалка ---
// function openModal() {
//   document.getElementById("overlay").style.display = "flex";
//   document.getElementById("feed").classList.add("blurred");
//   document.querySelector("footer").classList.add("blurred");
//   document.body.style.overflow = "hidden";
//   document.getElementById("titleError").textContent = "";
//   document.getElementById("titleError").style.display = "none";
//
//   setTimeout(() => {
//     autoGrow(document.getElementById("postText"));
//   }, 0);
// }
//
// function closeModal() {
//   document.getElementById("overlay").style.display = "none";
//   document.getElementById("feed").classList.remove("blurred");
//   document.querySelector("footer").classList.remove("blurred");
//   document.body.style.overflow = "";
// }
//
// // --- AutoGrow ---
// function autoGrowDesktop(elem) {
//   const modal = document.getElementById("modal");
//   const error = document.getElementById("titleError");
//   const errorHeight =
//     error.offsetHeight && error.style.display !== "none"
//       ? error.offsetHeight
//       : 0;
//   const maxModalHeight = window.innerHeight * 0.95;
//   const paddingHeight = 200 + errorHeight;
//   const maxTextareaHeight = maxModalHeight - paddingHeight;
//   const minModalHeight = 200;
//
//   const prevScrollTop = elem.scrollTop;
//   elem.style.height = "auto";
//   const newScrollHeight = elem.scrollHeight;
//
//   if (newScrollHeight <= maxTextareaHeight) {
//     elem.style.height = newScrollHeight + "px";
//     elem.style.overflowY = "hidden";
//     modal.style.height =
//       Math.max(minModalHeight, newScrollHeight + paddingHeight) + "px";
//     modal.style.overflowY = "hidden";
//   } else {
//     elem.style.height = maxTextareaHeight + "px";
//     elem.style.overflowY = "auto";
//     modal.style.height = maxModalHeight + "px";
//     modal.style.overflowY = "auto";
//   }
//
//   elem.scrollTop = prevScrollTop;
// }
//
// function autoGrowMobile(elem) {
//   elem.style.height = "auto";
//   elem.style.height = elem.scrollHeight + "px";
// }
//
// function isMobileDevice() {
//   return /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
// }
//
// function autoGrow(elem) {
//   if (isMobileDevice()) autoGrowMobile(elem);
//   else autoGrowDesktop(elem);
// }
//
// // --- Валідація title ---
// document.getElementById("postTitle").addEventListener("input", function () {
//   const maxLength = 40;
//   const error = document.getElementById("titleError");
//
//   if (this.value.length > maxLength) {
//     this.value = this.value.slice(0, maxLength);
//     error.textContent = "Максимум 40 символів";
//     error.classList.add("visible");
//   } else {
//     error.textContent = "";
//     error.classList.remove("visible");
//   }
// });
//
//
window.addEventListener("scroll", () => {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
    loadFeedChunk();
  }
});
//
// document.getElementById("overlay").addEventListener("click", (e) => {
//   if (e.target.id === "overlay") closeModal();
// });
//
// document.addEventListener("click", (e) => {
//   const link = e.target.closest(".post-link");
//   if (link) {
//     const id = link.dataset.id;
//     const title = decodeURIComponent(link.dataset.title);
//     const text = decodeURIComponent(link.dataset.text);
//
//     sessionStorage.setItem("post_data", JSON.stringify({ id, title, text }));
//   }
// });
//
if (!loadFromCache()) {
	loadFeedChunk();
}
