/* =============================================
   KAMPUNG SIPIAS - MAIN JAVASCRIPT (PERFORMANCE OPTIMIZED)
   ============================================= */

// ===== NAVBAR SCROLL EFFECT (THROTTLED WITH RAF FOR HIGH PERFORMANCE) =====
const navbar = document.getElementById('navbar');
if (navbar) {
  let isTicking = false;
  const handleScroll = () => {
    const isScrolled = window.scrollY > 40;
    if (navbar.classList.contains('scrolled') !== isScrolled) {
      navbar.classList.toggle('scrolled', isScrolled);
    }
    isTicking = false;
  };

  window.addEventListener('scroll', () => {
    if (!isTicking) {
      window.requestAnimationFrame(handleScroll);
      isTicking = true;
    }
  }, { passive: true });

  handleScroll();
}

// ===== MOBILE NAVBAR TOGGLE =====
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');

if (navToggle && navMenu) {
  navToggle.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = navMenu.classList.toggle('open');
    const spans = navToggle.querySelectorAll('span');
    if (isOpen) {
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
  }, { passive: true });
}

// ===== DROPDOWN CLICK TOGGLE =====
const navDropdowns = document.querySelectorAll('.nav-dropdown');
navDropdowns.forEach(dropdown => {
  const toggleBtn = dropdown.querySelector('.dropdown-toggle');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      navDropdowns.forEach(other => {
        if (other !== dropdown) other.classList.remove('open');
      });
      dropdown.classList.toggle('open');
    });
  }
});

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
  navDropdowns.forEach(dropdown => {
    if (!dropdown.contains(e.target)) {
      dropdown.classList.remove('open');
    }
  });
}, { passive: true });

// ===== AUTO-DISMISS MESSAGES =====
const messages = document.querySelectorAll('.message');
messages.forEach((msg) => {
  setTimeout(() => {
    msg.style.animation = 'slideOut 0.3s cubic-bezier(0.4, 0, 0.2, 1) forwards';
    setTimeout(() => msg.remove(), 300);
  }, 5000);
});

// Add slideOut keyframe dynamically
if (!document.getElementById('slideOutStyle')) {
  const style = document.createElement('style');
  style.id = 'slideOutStyle';
  style.textContent = `
    @keyframes slideOut {
      from { transform: translate3d(0, 0, 0); opacity: 1; }
      to { transform: translate3d(100%, 0, 0); opacity: 0; }
    }
  `;
  document.head.appendChild(style);
}

// ===== COUNTER ANIMATION (OPTIMIZED RAF) =====
const animateCounter = (el, target, duration = 1500) => {
  const start = 0;
  const startTime = performance.now();
  
  const updateCounter = (currentTime) => {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // Ease out quad formula for smooth decelerating animation
    const easeProgress = 1 - (1 - progress) * (1 - progress);
    const current = Math.floor(start + (target - start) * easeProgress);
    
    el.textContent = current.toLocaleString('id-ID');
    
    if (progress < 1) {
      requestAnimationFrame(updateCounter);
    } else {
      el.textContent = target.toLocaleString('id-ID');
    }
  };

  requestAnimationFrame(updateCounter);
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
  }, { threshold: 0.2 });
  counterEls.forEach(el => observer.observe(el));
}

// ===== HARDWARE-ACCELERATED SCROLL REVEAL =====
const revealEls = document.querySelectorAll('.card, .stat-item, .org-card, .galeri-item, .kontak-info-item');
if (revealEls.length > 0) {
  if (!document.getElementById('revealStyle')) {
    const revealStyle = document.createElement('style');
    revealStyle.id = 'revealStyle';
    revealStyle.textContent = `
      .reveal-hidden { 
        opacity: 0; 
        transform: translate3d(0, 20px, 0); 
        will-change: opacity, transform;
        transition: opacity 0.4s cubic-bezier(0.16, 1, 0.3, 1), transform 0.4s cubic-bezier(0.16, 1, 0.3, 1); 
      }
      .reveal-visible { 
        opacity: 1; 
        transform: translate3d(0, 0, 0); 
        will-change: auto;
      }
    `;
    document.head.appendChild(revealStyle);
  }

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal-visible');
        entry.target.classList.remove('reveal-hidden');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.05, rootMargin: '0px 0px -40px 0px' });

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

console.log('🌿 Website Kampung Sipias (Mobile Performance Optimized) loaded!');
