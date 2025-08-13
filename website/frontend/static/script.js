let start = 0;
let loading = false;
let noMorePosts = false;
const postPixelHeight = 120;
let lastLoadTime = 0;
const loadCooldown = 7000; // 7 секунд
const CACHE_KEY = 'cachedPosts';
const CACHE_TTL_MS = 1000 * 60 * 5; // 5 хвилин

function estimatePostsForScreen(multiplier = 1) {
  const screenHeight = window.innerHeight;
  const header = document.querySelector('header').offsetHeight;
  const footer = document.querySelector('footer').offsetHeight;
  const available = screenHeight - header - footer;
  return Math.ceil((available / postPixelHeight) * multiplier);
}

function renderPosts(posts) {
  const feed = document.getElementById('feed');
  posts.forEach(post => {
    const div = document.createElement('div');
    div.className = 'post';
    const previewText = post.text.length > 200 ? post.text.slice(0, 200) + '...' : post.text;

    div.innerHTML = `
  <a href="/post/${post.id}" class="post-link" data-id="${post.id}" data-title="${encodeURIComponent(post.title)}" data-text="${encodeURIComponent(post.text)}" style="text-decoration:none;color:inherit;">
    <strong>${post.title}</strong><br>
    <span class="preview-text">${previewText}</span>
  </a>`;
    feed.appendChild(div);
  });
}

function saveToCache(posts) {
  const cacheData = {
    posts: posts,
    timestamp: Date.now()
  };
  localStorage.setItem(CACHE_KEY, JSON.stringify(cacheData));
}

function loadFromCache() {
  const raw = localStorage.getItem(CACHE_KEY);
  if (!raw) return;

  const { posts, timestamp } = JSON.parse(raw);
  if (Date.now() - timestamp > CACHE_TTL_MS) {
    localStorage.removeItem(CACHE_KEY);
    return;
  }

  renderPosts(posts);
  start = posts.length;
}

async function loadFeedChunk(multiplier = 1) {
  if (loading) return;
  loading = true;

  try {
    const amount = estimatePostsForScreen(multiplier);
    const res = await fetch(`/api/api_v1/posts?start=${start}&amount=${amount}`);
    const posts = await res.json();

    if (posts.length < amount) noMorePosts = true;
    else noMorePosts = false;

    renderPosts(posts);
    saveToCache(posts);
    start += posts.length;
  } catch (err) {
    console.error('Error loading posts', err);
  }

  loading = false;
}

async function submitPost() {
  const title = document.getElementById('postTitle').value.trim();
  const text = document.getElementById('postText').value.trim();
  if (!title || !text) return;

  try {
    const res = await fetch('/api/api_v1/post', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, text })
    });

    if (res.ok) {
      noMorePosts = false;
      document.getElementById('postTitle').value = '';
      document.getElementById('postText').value = '';
      document.getElementById('titleError').textContent = '';
      document.getElementById('titleError').style.display = 'none';

      localStorage.removeItem(CACHE_KEY); // скидаємо кеш
      closeModal();
      document.getElementById('feed').innerHTML = '';
      start = 0;
      await loadFeedChunk(1.5);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  } catch (err) {
    console.error('Post failed', err);
  }
}

function openModal() {
  document.getElementById('overlay').style.display = 'flex';
  document.getElementById('feed').classList.add('blurred');
  document.querySelector('footer').classList.add('blurred');
  document.body.style.overflow = 'hidden';
  document.getElementById('titleError').textContent = '';
  document.getElementById('titleError').style.display = 'none';

  setTimeout(() => {
    autoGrow(document.getElementById('postText'));
  }, 0);
}

function closeModal() {
  document.getElementById('overlay').style.display = 'none';
  document.getElementById('feed').classList.remove('blurred');
  document.querySelector('footer').classList.remove('blurred');
  document.body.style.overflow = '';
}

function autoGrowDesktop(elem) {
  const modal = document.getElementById('modal');
  const error = document.getElementById('titleError');
  const errorHeight = error.offsetHeight && error.style.display !== 'none' ? error.offsetHeight : 0;
  const maxModalHeight = window.innerHeight * 0.95;
  const paddingHeight = 200 + errorHeight;
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

document.getElementById('postTitle').addEventListener('input', function () {
  const maxLength = 40;
  const error = document.getElementById('titleError');

  if (this.value.length > maxLength) {
    this.value = this.value.slice(0, maxLength);
    error.textContent = 'Максимум 40 символів';
    error.classList.add('visible');
  } else {
    error.textContent = '';
    error.classList.remove('visible');
  }
});

window.addEventListener('scroll', () => {
  const now = Date.now();
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
    if (noMorePosts) {
      if (now - lastLoadTime >= loadCooldown) {
        lastLoadTime = now;
        loadFeedChunk(1);
      }
    } else {
      loadFeedChunk(1);
    }
  }
});

document.getElementById('overlay').addEventListener('click', (e) => {
  if (e.target.id === 'overlay') closeModal();
});

document.addEventListener('click', (e) => {
  const link = e.target.closest('.post-link');
  if (link) {
    const id = link.dataset.id;
    const title = decodeURIComponent(link.dataset.title);
    const text = decodeURIComponent(link.dataset.text);

    sessionStorage.setItem('post_data', JSON.stringify({ id, title, text }));
  }
});

// 🧠 Спочатку — з кешу
loadFromCache();
loadFeedChunk(1.5);
