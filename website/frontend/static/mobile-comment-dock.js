const dock = document.getElementById("mobile-dock");
const textarea = document.getElementById("commentInput");
const sendBtn = document.getElementById("sendComment");

// авто-зростання textarea
textarea.addEventListener("input", () => {
  textarea.style.height = "auto";
  textarea.style.height = Math.min(textarea.scrollHeight, 120) + "px";
});

// слухаємо появу / зникнення клавіатури через visualViewport
if (window.visualViewport) {
  const updateDockPosition = () => {
    const viewport = window.visualViewport;
    const keyboardHeight = window.innerHeight - viewport.height - viewport.offsetTop;

    if (keyboardHeight > 100) {
      // клавіатура відкрита — піднімаємо док
      dock.style.transform = `translateY(-${keyboardHeight}px)`;
    } else {
      // клавіатура схована — повертаємо док вниз
      dock.style.transform = "translateY(0)";
    }
  };

  visualViewport.addEventListener("resize", updateDockPosition);
  visualViewport.addEventListener("scroll", updateDockPosition);
}

// при фокусі — показуємо док вище
textarea.addEventListener("focus", () => {
  dock.classList.add("raised");
});

// натиснув поза доком — ховаємо клаву і опускаємо док
document.addEventListener("touchstart", (e) => {
  if (!dock.contains(e.target)) {
    textarea.blur();
    dock.classList.remove("raised");
  }
});

// натиснув “відправити”
sendBtn.addEventListener("click", () => {
  const text = textarea.value.trim();
  if (!text) return;

  console.log("Відправляємо коментар:", text);

  textarea.value = "";
  textarea.style.height = "40px";
  textarea.blur();
  dock.classList.remove("raised");
});
