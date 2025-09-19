// ВСЬО САМ СУКА


// // === Конфіги ===
// const COMMENTS_PER_CHUNK = 20;
// const CACHE_TTL_MS = 10000; // 10 секунд
// let commentStart = 0;
// let loadingComments = false;
// let noMoreComments = false;
//
// // === КЕШ ===
// function cacheKey(postId) { return `comments_cache_${postId}`; }
//
// function saveCommentsToCache(postId, comments) {
//   const data = { timestamp: Date.now(), comments };
//   localStorage.setItem(cacheKey(postId), JSON.stringify(data));
// }
//
// function loadCommentsFromCache(postId) {
//   const raw = localStorage.getItem(cacheKey(postId));
//   if (!raw) return null;
//   try {
//     const data = JSON.parse(raw);
//     if (Date.now() - data.timestamp > CACHE_TTL_MS) return null;
//     return data.comments;
//   } catch { return null; }
// }
//
// // === Рендер ===
// function renderComments(comments, reset = false) {
//   const container = document.getElementById('comments');
//   if (reset) container.innerHTML = '';
//
//   comments.forEach(comment => {
//     const div = document.createElement('div');
//     div.classList.add('comment');
//
//     const header = document.createElement('div');
//     header.classList.add('comment-header');
//
//     const avatar = document.createElement('img');
//     avatar.src = "/static/images/avatar.png";
//     avatar.alt = "User";
//     avatar.classList.add('comment-avatar');
//
//     const author = document.createElement('span');
//     author.classList.add('comment-author');
//     author.textContent = "Anon User";
//
//     header.appendChild(avatar);
//     header.appendChild(author);
//
//     const body = document.createElement('div');
//     body.classList.add('comment-body');
//     body.textContent = comment.text;
//
//     div.appendChild(header);
//     div.appendChild(body);
//     container.appendChild(div);
//   });
// }
//
// // === Fetch коментарів ===
// async function fetchComments(postId, start, amount) {
//   const res = await fetch(`/api/api_v1/comments?post_id=${postId}&start=${start}&amount=${amount}`);
//   if (!res.ok) throw new Error("Failed to fetch comments");
//   return await res.json();
// }
//
// // === Lazy Load / Підвантаження ===
// async function loadCommentChunk(postId) {
//   if (loadingComments || noMoreComments) return;
//   loadingComments = true;
//
//   try {
//     const comments = await fetchComments(postId, commentStart, COMMENTS_PER_CHUNK);
//
//     renderComments(comments);
//     const cached = loadCommentsFromCache(postId) || [];
//     saveCommentsToCache(postId, cached.concat(comments));
//
//     commentStart += comments.length;
//     if (comments.length < COMMENTS_PER_CHUNK) noMoreComments = true;
//   } catch (err) {
//     console.error(err);
//   } finally {
//     loadingComments = false;
//   }
// }
//
// // === Fetch нових коментів при протуханні кешу ===
// async function checkForNewComments(postId) {
//   const cached = loadCommentsFromCache(postId) || [];
//   const res = await fetch(`/api/api_v1/comments?post_id=${postId}&start=0&amount=${COMMENTS_PER_CHUNK}`);
//   if (!res.ok) return;
//   const latest = await res.json();
//
//   // перевіряємо, чи з’явились нові
//   const cachedIds = new Set(cached.map(c => c.id));
//   const newComments = latest.filter(c => !cachedIds.has(c.id));
//   if (newComments.length === 0) return;
//
//   // додаємо кнопку
//   addNewCommentButton(postId, newComments, cached);
// }
//
// function addNewCommentButton(postId, newComments, oldComments) {
//   let btn = document.getElementById('newCommentsBtn');
//   if (!btn) {
//     btn = document.createElement('button');
//     btn.id = 'newCommentsBtn';
//     btn.textContent = `Перейти до ${newComments.length} нових коментарів`;
//     btn.style.position = 'fixed';
//     btn.style.top = '80px';
//     btn.style.right = '20px';
//     btn.style.zIndex = '1000';
//     btn.style.padding = '0.5rem 1rem';
//     document.body.appendChild(btn);
//
//     btn.addEventListener('click', () => {
//       const container = document.getElementById('comments');
//       renderComments(newComments, false);
//       saveCommentsToCache(postId, newComments.concat(oldComments));
//       commentStart = newComments.length + oldComments.length;
//       btn.remove();
//       window.scrollTo({ top: 0, behavior: 'smooth' });
//     });
//   }
// }
//
// // === Scroll ===
// window.addEventListener('scroll', () => {
//   const post = JSON.parse(sessionStorage.getItem('post_data'));
//   if (!post) return;
//
//   const cached = loadCommentsFromCache(post.id);
//   if (cached && (Date.now() - cached.timestamp < CACHE_TTL_MS)) return; // кеш живий
//
//   if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
//     loadCommentChunk(post.id);
//   }
// });
//
// // === Init ===
// document.addEventListener('DOMContentLoaded', async () => {
//   const post = JSON.parse(sessionStorage.getItem('post_data'));
//   if (!post) { window.location.href = "/"; return; }
//
//   const main = document.getElementById('feed');
//   main.innerHTML = '';
//
//   // пост
//   const postDiv = document.createElement('div');
//   postDiv.classList.add('post');
//   const titleH2 = document.createElement('h2'); titleH2.textContent = post.title;
//   const textP = document.createElement('p'); textP.textContent = post.text;
//   postDiv.appendChild(titleH2); postDiv.appendChild(textP);
//   main.appendChild(postDiv);
//
//   // секція коментарів
//   const commentsSection = document.createElement('div');
//   commentsSection.classList.add('comments-section');
//   commentsSection.style.marginTop = '1.5rem';
//   const commentsHeader = document.createElement('h3');
//   commentsHeader.textContent = 'Comments'; commentsHeader.style.textAlign = 'center';
//   const commentsContainer = document.createElement('div'); commentsContainer.id = 'comments';
//   commentsContainer.innerHTML = `<p style="text-align: center; color: #777;">Loading comments...</p>`;
//   commentsSection.appendChild(commentsHeader); commentsSection.appendChild(commentsContainer);
//   main.appendChild(commentsSection);
//
//   // перевірка кешу
//   const cached = loadCommentsFromCache(post.id);
//   if (cached) {
//     renderComments(cached, true);
//     commentStart = cached.length;
//     noMoreComments = false;
//   } else {
//     await loadCommentChunk(post.id);
//   }
//
//   // таймер на перевірку нових коментів
//   setInterval(() => {
//     checkForNewComments(post.id);
//   }, CACHE_TTL_MS + 500); // перевірка трохи після TTL
// });
//
// // === Модалка коментарів ===
// function openCommentModal() {
//   document.getElementById('overlay').style.display = 'flex';
//   document.getElementById('feed').classList.add('blurred');
//   document.querySelector('footer').classList.add('blurred');
//   document.body.style.overflow = 'hidden';
//   setTimeout(() => autoGrow(document.getElementById('commentText')), 0);
// }
// function closeCommentModal() {
//   document.getElementById('overlay').style.display = 'none';
//   document.getElementById('feed').classList.remove('blurred');
//   document.querySelector('footer').classList.remove('blurred');
//   document.body.style.overflow = '';
// }
// function submitComment() {
//   const text = document.getElementById("commentText").value.trim();
//   const post = JSON.parse(sessionStorage.getItem("post_data"));
//   if (!text) return alert("Порожній коментар");
//
//   fetch("/api/api_v1/comment", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ post_id: post.id, text })
//   })
//   .then(res => res.ok ? res.json() : Promise.reject())
//   .then(comment => {
//     closeCommentModal();
//     document.getElementById("commentText").value = '';
//     commentStart = 0;
//     noMoreComments = false;
//     loadCommentChunk(post.id);
//   })
//   .catch(err => console.error(err));
// }
//
// // === AutoGrow ===
// function autoGrow(elem) {
//   elem.style.height = 'auto';
//   elem.style.height = elem.scrollHeight + 'px';
// }
