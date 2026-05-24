/* ============================================================
   MOLINARI FORGE — MAIN JS
   UI interactions: sidebar, toasts, modals, animations
   ============================================================ */

'use strict';

// ── SIDEBAR TOGGLE ─────────────────────────────────────────
const Sidebar = (() => {
  const sidebar  = document.getElementById('sidebar');
  const overlay  = document.getElementById('sidebarOverlay');
  const mainContent = document.getElementById('mainContent');
  const navbar = document.getElementById('navbarForge');
  const toggleBtn = document.getElementById('sidebarToggle');
  const collapsedKey = 'mf_sidebar_collapsed';

  const isMobile = () => window.innerWidth < 992;

  function open() {
    sidebar?.classList.add('open');
    overlay?.classList.add('show');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    sidebar?.classList.remove('open');
    overlay?.classList.remove('show');
    document.body.style.overflow = '';
  }

  function collapse() {
    sidebar?.classList.add('collapsed');
    mainContent?.classList.add('sidebar-collapsed');
    navbar?.classList.add('sidebar-collapsed');
    localStorage.setItem(collapsedKey, '1');
  }

  function expand() {
    sidebar?.classList.remove('collapsed');
    mainContent?.classList.remove('sidebar-collapsed');
    navbar?.classList.remove('sidebar-collapsed');
    localStorage.setItem(collapsedKey, '0');
  }

  function toggle() {
    if (isMobile()) {
      sidebar?.classList.contains('open') ? close() : open();
    } else {
      sidebar?.classList.contains('collapsed') ? expand() : collapse();
    }
  }

  function init() {
    if (!sidebar) return;
    // restore state
    if (!isMobile() && localStorage.getItem(collapsedKey) === '1') collapse();

    toggleBtn?.addEventListener('click', toggle);
    overlay?.addEventListener('click', close);
    window.addEventListener('resize', () => { if (!isMobile()) close(); });

    // Active link detection
    const links = sidebar.querySelectorAll('.sidebar-link');
    links.forEach(link => {
      if (link.href && window.location.pathname.startsWith(new URL(link.href, location.href).pathname) && link.href !== window.location.origin + '/') {
        link.classList.add('active');
      }
    });
  }

  return { init, open, close, toggle, collapse, expand };
})();


// ── TOAST SYSTEM ───────────────────────────────────────────
const Toast = (() => {
  let container;

  function getContainer() {
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container-forge';
      document.body.appendChild(container);
    }
    return container;
  }

  const icons = {
    success: '✓',
    error:   '✕',
    info:    'ℹ',
    warning: '⚠',
  };

  function show({ title = '', message = '', type = 'info', duration = 4000 } = {}) {
    const c = getContainer();
    const el = document.createElement('div');
    el.className = `toast-forge toast-${type}`;
    el.innerHTML = `
      <span class="toast-icon">${icons[type] || icons.info}</span>
      <div class="toast-body">
        ${title ? `<div class="toast-title">${title}</div>` : ''}
        ${message ? `<div class="toast-msg">${message}</div>` : ''}
      </div>
      <button class="toast-close" aria-label="Close">&times;</button>
    `;

    el.querySelector('.toast-close').addEventListener('click', () => dismiss(el));
    c.appendChild(el);

    if (duration > 0) setTimeout(() => dismiss(el), duration);
    return el;
  }

  function dismiss(el) {
    el.style.transition = 'opacity 0.3s, transform 0.3s';
    el.style.opacity = '0';
    el.style.transform = 'translateX(40px)';
    setTimeout(() => el.remove(), 300);
  }

  return {
    show,
    success: (title, message, opts) => show({ title, message, type: 'success', ...opts }),
    error:   (title, message, opts) => show({ title, message, type: 'error',   ...opts }),
    info:    (title, message, opts) => show({ title, message, type: 'info',    ...opts }),
    warning: (title, message, opts) => show({ title, message, type: 'warning', ...opts }),
  };
})();


// ── XP BARS ────────────────────────────────────────────────
function animateXpBars() {
  document.querySelectorAll('.xp-bar-fill[data-percent]').forEach(bar => {
    const pct = Math.min(100, Math.max(0, parseFloat(bar.dataset.percent)));
    bar.style.width = '0%';
    requestAnimationFrame(() => {
      setTimeout(() => { bar.style.width = pct + '%'; }, 100);
    });
  });
}

// ── ANALYTICS BARS ─────────────────────────────────────────
function animateAnalyticsBars() {
  document.querySelectorAll('.ab-fill[data-pct]').forEach(bar => {
    const pct = Math.min(100, parseFloat(bar.dataset.pct));
    bar.style.width = '0%';
    requestAnimationFrame(() => {
      setTimeout(() => { bar.style.width = pct + '%'; }, 200);
    });
  });
}

// ── COUNTER ANIMATION ──────────────────────────────────────
function animateCounters() {
  document.querySelectorAll('[data-counter]').forEach(el => {
    const target = parseFloat(el.dataset.counter);
    const duration = 1200;
    const start = performance.now();
    const isFloat = target !== Math.floor(target);

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const val = target * eased;
      el.textContent = isFloat ? val.toFixed(1) : Math.round(val).toLocaleString();
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });
}


// ── ONBOARDING QUIZ ────────────────────────────────────────
const Onboarding = (() => {
  function init() {
    document.querySelectorAll('.ob-option').forEach(opt => {
      opt.addEventListener('click', function () {
        const group = this.closest('[data-question]');
        if (group) {
          group.querySelectorAll('.ob-option').forEach(o => o.classList.remove('selected'));
          this.classList.add('selected');
          const check = this.querySelector('.ob-opt-check');
          if (check) check.textContent = '✓';
          // re-clear others
          group.querySelectorAll('.ob-option:not(.selected) .ob-opt-check').forEach(c => { c.textContent = ''; });
        }
      });
    });

    // Step progress
    const nextBtns = document.querySelectorAll('[data-ob-next]');
    nextBtns.forEach(btn => {
      btn.addEventListener('click', function () {
        const currentStep = parseInt(this.dataset.obNext);
        const steps = document.querySelectorAll('[data-step]');
        steps.forEach(s => {
          s.style.display = 'none';
          if (parseInt(s.dataset.step) === currentStep + 1) s.style.display = 'block';
        });
        updateDots(currentStep + 1);
      });
    });
  }

  function updateDots(current) {
    document.querySelectorAll('.step-dot').forEach((dot, i) => {
      dot.classList.remove('done', 'current');
      if (i < current - 1) dot.classList.add('done');
      else if (i === current - 1) dot.classList.add('current');
    });
  }

  return { init };
})();


// ── REQUESTS: APPROVE / REJECT ─────────────────────────────
function initRequestActions() {
  document.querySelectorAll('[data-action="approve"]').forEach(btn => {
    btn.addEventListener('click', function () {
      const card = this.closest('.request-card');
      if (!card) return;
      card.style.transition = 'opacity 0.4s, transform 0.4s';
      card.style.opacity = '0';
      card.style.transform = 'translateX(20px)';
      setTimeout(() => card.remove(), 400);
      Toast.success('Request approved', 'The student has been notified.');
    });
  });

  document.querySelectorAll('[data-action="reject"]').forEach(btn => {
    btn.addEventListener('click', function () {
      const card = this.closest('.request-card');
      if (!card) return;
      card.style.transition = 'opacity 0.4s, transform 0.4s';
      card.style.opacity = '0';
      card.style.transform = 'translateX(-20px)';
      setTimeout(() => card.remove(), 400);
      Toast.error('Request rejected', 'The student has been notified.');
    });
  });
}


// ── LEADERBOARD FILTER TABS ────────────────────────────────
function initLbFilters() {
  document.querySelectorAll('.lb-filter-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      document.querySelectorAll('.lb-filter-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      // HTMX or fetch would go here — for now just a UI toggle
    });
  });
}


// ── NOTIFICATION PILLS ─────────────────────────────────────
function initNotifPills() {
  document.querySelectorAll('.notif-pill').forEach(pill => {
    pill.addEventListener('click', function () {
      document.querySelectorAll('.notif-pill').forEach(p => p.classList.remove('active'));
      this.classList.add('active');
    });
  });
}


// ── REQUESTS TABS ──────────────────────────────────────────
function initRequestsTabs() {
  document.querySelectorAll('.requests-tab').forEach(tab => {
    tab.addEventListener('click', function () {
      document.querySelectorAll('.requests-tab').forEach(t => t.classList.remove('active'));
      this.classList.add('active');
    });
  });
}


// ── KEYBOARD SHORTCUT: search ──────────────────────────────
function initSearchShortcut() {
  document.addEventListener('keydown', e => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      const search = document.querySelector('.navbar-search input');
      if (search) search.focus();
    }
  });
}


// ── REWARD CARDS ───────────────────────────────────────────
function initRewardCards() {
  document.querySelectorAll('.reward-card:not(.reward-owned)').forEach(card => {
    card.addEventListener('click', function () {
      const title = this.querySelector('.reward-title')?.textContent || 'reward';
      const price = this.querySelector('.reward-price')?.textContent?.trim() || '';
      // In production: open confirm modal
      Toast.info('Confirm purchase', `Redeem "${title}" for ${price}?`);
    });
  });
}


// ── STAGGERED CARD ENTRANCE ────────────────────────────────
function initPageAnimations() {
  const cards = document.querySelectorAll('.stat-card, .card-glass, .house-card, .reward-card, .request-card');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        const delay = Array.from(cards).indexOf(entry.target) * 60;
        entry.target.style.animationDelay = delay + 'ms';
        entry.target.classList.add('animate-fadeup');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.05 });

  cards.forEach(card => observer.observe(card));
}


// ── COPY TEXT ──────────────────────────────────────────────
function initCopyBtns() {
  document.querySelectorAll('[data-copy]').forEach(btn => {
    btn.addEventListener('click', function () {
      navigator.clipboard.writeText(this.dataset.copy).then(() => {
        Toast.success('Copied!', '', { duration: 2000 });
      });
    });
  });
}


// ── INIT ALL ───────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  Sidebar.init();
  animateXpBars();
  animateAnalyticsBars();
  animateCounters();
  Onboarding.init();
  initRequestActions();
  initLbFilters();
  initNotifPills();
  initRequestsTabs();
  initSearchShortcut();
  initRewardCards();
  initPageAnimations();
  initCopyBtns();
});

// Expose for inline usage
window.MF = { Toast, Sidebar };