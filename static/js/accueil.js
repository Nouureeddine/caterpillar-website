// Page-specific JS for accueil

// Typing effect for headline
(function typingEffect(){
  const el = document.querySelector('.typing');
  if (!el) return;
  const raw = el.getAttribute('data-typing-target') || '';
  const phrases = raw.split('|').map(s => s.trim()).filter(Boolean);
  if (phrases.length === 0) return;

  let phraseIndex = 0;
  let charIndex = 0;
  let deleting = false;
  const basePrefix = '';

  const span = document.createElement('span');
  span.className = 'typing-span';
  el.innerHTML = '';
  el.appendChild(span);

  function tick(){
    const current = phrases[phraseIndex];
    if (!deleting){
      charIndex++;
      if (charIndex >= current.length){
        setTimeout(() => { deleting = true; }, 1200);
      }
    } else {
      charIndex--;
      if (charIndex <= 0){
        deleting = false;
        phraseIndex = (phraseIndex + 1) % phrases.length;
      }
    }
    span.textContent = basePrefix + current.substring(0, Math.max(0, charIndex));
    const delay = deleting ? 45 : 70;
    setTimeout(tick, delay);
  }
  tick();
})();

// GSAP scroll animations if available
window.addEventListener('load', () => {
  if (window.gsap && window.ScrollTrigger){
    gsap.utils.toArray('.value-card, .brand-card, .stat-item').forEach((el) => {
      gsap.fromTo(el, {opacity: 0, y: 24}, {opacity: 1, y: 0, duration: 0.6, ease: 'power2.out', scrollTrigger: {trigger: el, start: 'top 85%'}});
    });
    gsap.fromTo('.solutions-swiper', {opacity: 0, scale: 0.98}, {opacity: 1, scale: 1, duration: 0.6, ease: 'power2.out', scrollTrigger: {trigger: '.solutions-swiper', start: 'top 85%'}});
  }
});


