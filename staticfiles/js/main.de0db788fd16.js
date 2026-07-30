/* =============================================
   KAMPUNG SIPIAS - MAIN JAVASCRIPT
   ============================================= */

// ===== NAVBAR SCROLL EFFECT =====
const navbar = document.getElementById('navbar');
if (navbar) {
  const handleScroll = () => {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  };
  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();
}

// ===== MOBILE NAVBAR TOGGLE =====
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');
if (navToggle && navMenu) {
  navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('open');
    const spans = navToggle.querySelectorAll('span');
    if (navMenu.classList.contains('open')) {
      spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
      spans[1].style.opacity = '0';
      spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
    } else {
      spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    }
  });
  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
      navMenu.classList.remove('open');
      const spans = navToggle.querySelectorAll('span');
      spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    }
  });
}

// ===== AUTO-DISMISS MESSAGES =====
const messages = document.querySelectorAll('.message');
messages.forEach((msg) => {
  setTimeout(() => {
    msg.style.animation = 'slideOut 0.4s ease forwards';
    setTimeout(() => msg.remove(), 400);
  }, 5000);
});

// Add slideOut keyframe dynamically
const style = document.createElement('style');
style.textContent = `
  @keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
  }
`;
document.head.appendChild(style);

// ===== COUNTER ANIMATION =====
const animateCounter = (el, target, duration = 2000) => {
  const start = 0;
  const increment = target / (duration / 16);
  let current = start;
  const timer = setInterval(() => {
    current += increment;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    el.textContent = Math.floor(current).toLocaleString('id-ID');
  }, 16);
};

// Trigger counters on scroll into view
const counterEls = document.querySelectorAll('[data-count]');
if (counterEls.length > 0) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const target = parseInt(entry.target.dataset.count) || 0;
        if (target > 0) animateCounter(entry.target, target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });
  counterEls.forEach(el => observer.observe(el));
}

// ===== SCROLL REVEAL ANIMATION =====
const revealEls = document.querySelectorAll('.card, .stat-item, .org-card, .galeri-item, .kontak-info-item');
if (revealEls.length > 0) {
  const revealStyle = document.createElement('style');
  revealStyle.textContent = `
    .reveal-hidden { opacity: 0; transform: translateY(30px); transition: opacity 0.6s ease, transform 0.6s ease; }
    .reveal-visible { opacity: 1; transform: translateY(0); }
  `;
  document.head.appendChild(revealStyle);

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.classList.add('reveal-visible');
          entry.target.classList.remove('reveal-hidden');
        }, i * 80);
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  revealEls.forEach(el => {
    el.classList.add('reveal-hidden');
    revealObserver.observe(el);
  });
}

// ===== SMOOTH ANCHOR SCROLL =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    const target = document.querySelector(anchor.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ===== FORM VALIDATION FEEDBACK =====
const forms = document.querySelectorAll('form');
forms.forEach(form => {
  form.addEventListener('submit', (e) => {
    const btn = form.querySelector('button[type="submit"]');
    if (btn) {
      btn.textContent = '⏳ Memproses...';
      btn.disabled = true;
      setTimeout(() => {
        btn.disabled = false;
        btn.textContent = btn.dataset.originalText || btn.textContent;
      }, 5000);
    }
  });
});

console.log('🌿 Website Kampung Sipias loaded successfully!');
