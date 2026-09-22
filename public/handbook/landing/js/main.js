/* AI 阻詐訓練平台 · 精準守護
   Signature：金色守護線畫過「看穩聽問守」+ 數據跳動
   其餘：安靜的短距淡入（各區塊只出現一次，不重複套版） */

gsap.registerPlugin(ScrollTrigger);

const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (prefersReduced) {
  gsap.set("[data-hero], [data-fade], [data-step], .cred-in", { opacity: 1, y: 0, clearProps: "transform" });
  gsap.set(".track-gold", { strokeDashoffset: 0 });
} else {
  initAnimations();
}

function initAnimations() {

  /* ---- Hero：lead-follow，標題先落定，其餘依序跟上，圖卡最後浮入 ---- */
  gsap.set("[data-hero]", { opacity: 0, y: 18 });
  gsap.timeline({ defaults: { ease: "power2.out", duration: 0.7 } })
    .to(".hero-pill",  { opacity: 1, y: 0, duration: 0.5 })
    .to(".hero-title", { opacity: 1, y: 0, duration: 0.9 }, "-=0.25")
    .to(".hero-sub",   { opacity: 1, y: 0 }, "-=0.5")
    .to(".hero-cta",   { opacity: 1, y: 0 }, "-=0.45")
    .to(".hero-tag",   { opacity: 1, y: 0, duration: 0.5 }, "-=0.4")
    .to(".hero-phase", { opacity: 1, y: 0, duration: 0.5 }, "-=0.3")
    .to(".hero-media", { opacity: 1, y: 0, duration: 0.7 }, "-=0.85");

  /* ---- Signature：金色守護線隨捲動畫過五步驟 ---- */
  const goldPath = document.querySelector(".track-gold");
  if (goldPath) {
    const len = goldPath.getTotalLength();
    gsap.set(goldPath, { strokeDasharray: len, strokeDashoffset: len });
    gsap.to(goldPath, {
      strokeDashoffset: 0,
      ease: "none",
      scrollTrigger: {
        trigger: ".track",
        start: "top 78%",
        end: "bottom 45%",
        scrub: 0.6
      }
    });
    /* 五張卡片依序點亮，跟著線走（from:"start"，方向有意義） */
    gsap.from("[data-step]", {
      opacity: 0,
      y: 14,
      duration: 0.5,
      ease: "power2.out",
      stagger: { each: 0.14, from: "start" },
      scrollTrigger: { trigger: ".steps", start: "top 80%", once: true }
    });
  }

  /* ---- 其餘區塊：安靜的短距淡入，不搶戲 ---- */
  gsap.utils.toArray("[data-fade]").forEach(el => {
    gsap.from(el, {
      opacity: 0,
      y: 12,
      duration: 0.45,
      ease: "power1.out",
      scrollTrigger: { trigger: el, start: "top 86%", once: true }
    });
  });
}

/* 字型與圖片載入完成後重算 ScrollTrigger 位置 */
if (document.fonts && document.fonts.ready) {
  document.fonts.ready.then(() => ScrollTrigger.refresh());
}
window.addEventListener("load", () => ScrollTrigger.refresh());
