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
  // Navbar shadow on scroll and active underline sync
  const navbar = document.querySelector('.navbar');
  const links = document.querySelectorAll('.nav-links a');
  const setScrolled = () => {
    if (!navbar) return;
    if (window.scrollY > 10) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  };
  setScrolled();
  window.addEventListener('scroll', setScrolled);

  // Smooth scroll for internal links
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', (e) => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target){
        e.preventDefault();
        target.scrollIntoView({behavior: 'smooth', block: 'start'});
      }
    });
  });
});

// IntersectionObserver fallback animations for category cards and generic elements
(function(){
  const els = document.querySelectorAll('.animate-on-scroll');
  if (!('IntersectionObserver' in window) || els.length === 0) return;
  const io = new IntersectionObserver((entries)=>{
    entries.forEach(entry=>{
      if (entry.isIntersecting){
        entry.target.classList.add('animated');
        io.unobserve(entry.target);
      }
    })
  }, {threshold: 0.15});
  els.forEach(el=>io.observe(el));
})();


