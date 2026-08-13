/* ============================================================
   SMART AI FORECASTING - Shared Interactions
   ============================================================ */
(function () {
  'use strict';

  /* ---------- Auth Guard ---------- */
  // Only run guard on app pages (not on landing or auth itself)
  var _page = window.location.pathname.split('/').pop();
  var _appPages = ['dashboard.html', 'inventory.html', 'forecast.html', 'alerts.html'];
  if (_appPages.indexOf(_page) !== -1) {
    var _session = localStorage.getItem('saf_user');
    var _valid = false;
    if (_session) {
      try { JSON.parse(_session); _valid = true; } catch (e) { localStorage.removeItem('saf_user'); }
    }
    if (!_valid) {
      window.location.replace('auth.html');
      return; // stop execution
    }
  }

  /* ---------- Demo Data Store (localStorage) ---------- */
  var STORE_KEY = 'saf_store_v1';

  var seedProducts = [
    { id: 1, name: 'Lays Classic', sku: 'SKU-001', category: 'Chips', stock: 40, price: 20, supplier: 'ABC Dist.', leadTime: 3, minStock: 15 },
    { id: 2, name: 'Cheetos', sku: 'SKU-002', category: 'Snacks', stock: 12, price: 15, supplier: 'XYZ Corp.', leadTime: 5, minStock: 20 },
    { id: 3, name: 'Pepsi 750ml', sku: 'SKU-003', category: 'Beverages', stock: 150, price: 35, supplier: 'PQR Ltd.', leadTime: 2, minStock: 30 },
    { id: 4, name: 'Doritos', sku: 'SKU-004', category: 'Chips', stock: 25, price: 25, supplier: 'ABC Dist.', leadTime: 3, minStock: 15 },
    { id: 5, name: 'Coca-Cola 500ml', sku: 'SKU-005', category: 'Beverages', stock: 80, price: 30, supplier: 'PQR Ltd.', leadTime: 2, minStock: 25 },
    { id: 6, name: 'Maggi Noodles', sku: 'SKU-006', category: 'Instant Food', stock: 9, price: 14, supplier: 'XYZ Corp.', leadTime: 4, minStock: 20 },
    { id: 7, name: 'Parle-G Biscuits', sku: 'SKU-007', category: 'Snacks', stock: 220, price: 10, supplier: 'ABC Dist.', leadTime: 3, minStock: 40 },
    { id: 8, name: 'Kurkure', sku: 'SKU-008', category: 'Snacks', stock: 55, price: 15, supplier: 'XYZ Corp.', leadTime: 4, minStock: 18 },
    { id: 9, name: 'Sprite 600ml', sku: 'SKU-009', category: 'Beverages', stock: 18, price: 32, supplier: 'PQR Ltd.', leadTime: 2, minStock: 20 },
    { id: 10, name: 'Dairy Milk', sku: 'SKU-010', category: 'Confectionery', stock: 62, price: 50, supplier: 'ABC Dist.', leadTime: 3, minStock: 25 },
    { id: 11, name: 'Fanta 750ml', sku: 'SKU-011', category: 'Beverages', stock: 140, price: 35, supplier: 'PQR Ltd.', leadTime: 2, minStock: 30 },
    { id: 12, name: 'Balaji Wafers', sku: 'SKU-012', category: 'Chips', stock: 22, price: 20, supplier: 'XYZ Corp.', leadTime: 5, minStock: 18 },
    { id: 13, name: 'Bournville', sku: 'SKU-013', category: 'Confectionery', stock: 7, price: 120, supplier: 'ABC Dist.', leadTime: 4, minStock: 12 },
    { id: 14, name: 'Nescafe 50g', sku: 'SKU-014', category: 'Beverages', stock: 38, price: 95, supplier: 'PQR Ltd.', leadTime: 3, minStock: 15 },
    { id: 15, name: 'Haldiram Bhujia', sku: 'SKU-015', category: 'Snacks', stock: 45, price: 28, supplier: 'XYZ Corp.', leadTime: 4, minStock: 20 },
    { id: 16, name: 'Good Day Biscuits', sku: 'SKU-016', category: 'Snacks', stock: 68, price: 20, supplier: 'ABC Dist.', leadTime: 3, minStock: 25 },
    { id: 17, name: 'Mountain Dew', sku: 'SKU-017', category: 'Beverages', stock: 12, price: 32, supplier: 'PQR Ltd.', leadTime: 2, minStock: 20 },
    { id: 18, name: 'Cadbury Gems', sku: 'SKU-018', category: 'Confectionery', stock: 30, price: 45, supplier: 'ABC Dist.', leadTime: 3, minStock: 15 },
    { id: 19, name: 'Slice Mango', sku: 'SKU-019', category: 'Beverages', stock: 175, price: 30, supplier: 'PQR Ltd.', leadTime: 2, minStock: 30 },
    { id: 20, name: '5 Star', sku: 'SKU-020', category: 'Confectionery', stock: 88, price: 25, supplier: 'ABC Dist.', leadTime: 3, minStock: 30 },
    { id: 21, name: 'Sting Energy', sku: 'SKU-021', category: 'Beverages', stock: 5, price: 25, supplier: 'PQR Ltd.', leadTime: 2, minStock: 15 },
    { id: 22, name: 'Lays Chips Masala', sku: 'SKU-022', category: 'Chips', stock: 34, price: 20, supplier: 'ABC Dist.', leadTime: 3, minStock: 15 },
    { id: 23, name: 'Bingo Mad Angles', sku: 'SKU-023', category: 'Chips', stock: 28, price: 20, supplier: 'XYZ Corp.', leadTime: 5, minStock: 15 },
    { id: 24, name: 'Nutrela Soya', sku: 'SKU-024', category: 'Instant Food', stock: 40, price: 60, supplier: 'XYZ Corp.', leadTime: 4, minStock: 15 }
  ];

  var seedResolved = [
    { id: 1, product: 'Doritos', level: 'low', title: 'Stock levels are optimal', desc: 'Current stock meets predicted demand for the next 30 days.', date: 'Jan 12, 2026', status: 'resolved' }
  ];

  function getStore() {
    var raw = localStorage.getItem(STORE_KEY);
    if (raw) {
      try {
        return JSON.parse(raw);
      } catch (e) { /* ignore */ }
    }
    var store = { products: seedProducts, resolved: seedResolved };
    localStorage.setItem(STORE_KEY, JSON.stringify(store));
    return store;
  }

  function saveStore(store) {
    localStorage.setItem(STORE_KEY, JSON.stringify(store));
  }

  window.SAF = {
    getStore: getStore,
    saveStore: saveStore,
    productStatus: function (p) {
      var ratio = p.stock / Math.max(p.minStock, 1);
      var forecast = SAF.predictedDemand(p);
      if (p.stock < p.minStock || p.stock < forecast * 0.5) return { key: 'low', label: 'Low Stock', emoji: '🔴', cls: 'status-low', level: 'high' };
      if (p.stock > p.minStock * 3) return { key: 'overstock', label: 'Overstock', emoji: '🟡', cls: 'status-overstock', level: 'medium' };
      return { key: 'healthy', label: 'Healthy', emoji: '🟢', cls: 'status-healthy', level: 'low' };
    },
    predictedDemand: function (p) {
      var seed = (p.id * 13 + p.sku.length * 7) % 60;
      return Math.max(seed + Math.round(p.minStock * 1.2), 10);
    },
    currency: function (n) {
      return '\u20B9' + Number(n).toLocaleString('en-IN');
    }
  };

  /* ---------- Toast notifications ---------- */
  function ensureToastContainer() {
    var c = document.querySelector('.toast-container');
    if (!c) {
      c = document.createElement('div');
      c.className = 'toast-container';
      c.setAttribute('aria-live', 'polite');
      c.setAttribute('aria-atomic', 'false');
      document.body.appendChild(c);
    }
    return c;
  }

  function toast(message, type, title) {
    var map = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
    var t = document.createElement('div');
    t.className = 'toast ' + (type || 'info');
    t.setAttribute('role', 'status');
    t.innerHTML =
      '<span class="toast-icon">' + (map[type] || map.info) + '</span>' +
      '<div><div class="toast-title">' + (title || (type === 'success' ? 'Success' : type === 'error' ? 'Error' : 'Heads up')) + '</div>' +
      '<div class="toast-message">' + message + '</div></div>';
    ensureToastContainer().appendChild(t);
    setTimeout(function () {
      t.classList.add('leaving');
      setTimeout(function () { t.remove(); }, 320);
    }, 4000);
  }

  window.SAF.toast = toast;

  /* ---------- Modal helpers ---------- */
  function openModal(el) {
    if (!el) return;
    el.classList.add('open');
    document.body.style.overflow = 'hidden';
    var focusTarget = el.querySelector('input, select, button');
    setTimeout(function () { if (focusTarget) focusTarget.focus(); }, 150);
  }

  function closeModal(el) {
    if (!el) return;
    el.classList.remove('open');
    document.body.style.overflow = '';
  }

  document.addEventListener('click', function (e) {
    var closer = e.target.closest('[data-close-modal]');
    if (closer) {
      var modal = closer.closest('.modal-overlay');
      closeModal(modal);
    }
    if (e.target.classList && e.target.classList.contains('modal-overlay') && !e.target.dataset.keepOpen) {
      closeModal(e.target);
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-overlay.open').forEach(closeModal);
    }
  });

  document.addEventListener('click', function (e) {
    var opener = e.target.closest('[data-modal-open]');
    if (opener) {
      var id = opener.getAttribute('data-modal-open');
      openModal(document.getElementById(id));
    }
  });

  /* ---------- Sidebar (mobile) ---------- */
  document.addEventListener('click', function (e) {
    var toggle = e.target.closest('[data-sidebar-toggle]');
    if (toggle) {
      document.getElementById('sidebar').classList.toggle('open');
      document.getElementById('sidebarOverlay').classList.toggle('show');
      return;
    }
    if (e.target.classList && e.target.classList.contains('sidebar-overlay')) {
      document.getElementById('sidebar').classList.remove('open');
      document.getElementById('sidebarOverlay').classList.remove('show');
    }
  });

  /* ---------- Skeleton loading simulation ---------- */
  function skeletonShow(selector, ms, callback) {
    var els = document.querySelectorAll(selector);
    els.forEach(function (el) { el.classList.add('skeleton'); });
    setTimeout(function () {
      els.forEach(function (el) { el.classList.remove('skeleton'); });
      if (callback) callback();
    }, ms);
  }
  window.SAF.skeletonShow = skeletonShow;

  /* ---------- Upload zone (drag & drop) ---------- */
  function initUpload(zoneId, inputId, statusId, onFile) {
    var zone = document.getElementById(zoneId);
    var input = document.getElementById(inputId);
    var status = document.getElementById(statusId);
    if (!zone || !input) return;

    function setStatus(msg, type) {
      if (!status) return;
      status.className = 'upload-status ' + type;
      status.innerHTML = (type === 'success' ? '✅ ' : type === 'error' ? '❌ ' : '⏳ ') + msg;
    }

    function handle(files) {
      if (!files || !files.length) return;
      var file = files[0];
      if (!/\.csv$/i.test(file.name)) {
        setStatus('Please upload a valid .csv file.', 'error');
        return;
      }
      setStatus('Uploading ' + file.name + '...', 'info');
      var bar = document.querySelector('.progress-bar');
      var pct = 0;
      var timer = setInterval(function () {
        pct += 15;
        if (bar) bar.style.width = Math.min(pct, 100) + '%';
        if (pct >= 100) {
          clearInterval(timer);
          setStatus(file.name + ' uploaded successfully! ' + file.size.toLocaleString() + ' bytes.', 'success');
          if (onFile) onFile(file);
        }
      }, 120);
    }

    zone.addEventListener('click', function () { input.click(); });
    input.addEventListener('change', function () { handle(input.files); });
    ['dragenter', 'dragover'].forEach(function (ev) {
      zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.add('dragover'); });
    });
    ['dragleave', 'drop'].forEach(function (ev) {
      zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.remove('dragover'); });
    });
    zone.addEventListener('drop', function (e) { handle(e.dataTransfer.files); });
  }
  window.SAF.initUpload = initUpload;

  /* ---------- Form validation helper ---------- */
  function bindValidation(formEl) {
    if (!formEl) return;
    formEl.querySelectorAll('[data-validate]').forEach(function (field) {
      field.addEventListener('blur', function () { validateField(field); });
      field.addEventListener('input', function () {
        if (field.closest('.form-group') && field.closest('.form-group').classList.contains('invalid')) {
          validateField(field);
        }
      });
    });
  }

  function validateField(field) {
    var group = field.closest('.form-group');
    if (!group) return true;
    var valid = true;
    var val = field.value.trim();
    var rules = (field.dataset.validate || '').split(' ');
    if (rules.indexOf('required') !== -1 && !val) valid = false;
    if (rules.indexOf('email') !== -1 && val && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) valid = false;
    if (rules.indexOf('min6') !== -1 && val && val.length < 6) valid = false;
    if (rules.indexOf('number') !== -1 && val && isNaN(Number(val))) valid = false;
    if (rules.indexOf('positive') !== -1 && val && Number(val) < 0) valid = false;
    group.classList.toggle('invalid', !valid);
    group.classList.toggle('valid', valid);
    return valid;
  }

  function validateForm(formEl) {
    if (!formEl) return true;
    var ok = true;
    formEl.querySelectorAll('[data-validate]').forEach(function (field) {
      if (!validateField(field)) ok = false;
    });
    return ok;
  }
  window.SAF.validateForm = validateForm;

  /* ---------- Buttons with loading spinner ---------- */
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-loading]');
    if (!btn) return;
    var label = btn.getAttribute('data-loading');
    var original = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> ' + label;
    var done = btn.dataset.done;
    setTimeout(function () {
      if (done === 'false') {
        btn.disabled = false;
        btn.innerHTML = original;
      }
    }, 1800);
  });

  /* ---------- Logout ---------- */
  document.addEventListener('click', function (e) {
    var logout = e.target.closest('[data-logout]');
    if (logout) {
      e.preventDefault();
      localStorage.removeItem('saf_user');
      window.location.href = 'auth.html';
    }
  });

  /* ---------- Store current user ---------- */
  function currentUser() {
    try {
      var u = localStorage.getItem('saf_user');
      if (u) {
        var parsed = JSON.parse(u);
        return {
          name: parsed.name || 'Store Manager',
          email: parsed.email || 'manager@store.com',
          store: parsed.store || 'My Store',
          role: parsed.role || 'Store Manager'
        };
      }
    } catch (e) { /* ignore */ }
    return { name: 'Store Manager', email: 'manager@store.com', store: 'My Store', role: 'Store Manager' };
  }
  window.SAF.currentUser = currentUser;

  /* ---------- Active nav highlight ---------- */
  document.addEventListener('DOMContentLoaded', function () {
    var page = window.location.pathname.split('/').pop() || 'dashboard.html';
    document.querySelectorAll('.sidebar-link').forEach(function (a) {
      if (a.getAttribute('href') === page) a.classList.add('active');
    });
    // Greeting
    var greet = document.getElementById('userName');
    if (greet) greet.textContent = currentUser().name.split(' ')[0];
    var avatar = document.getElementById('userAvatar');
    if (avatar) {
      var nm = currentUser().name;
      avatar.textContent = nm.split(' ').map(function (w) { return w[0]; }).join('').slice(0, 2).toUpperCase();
    }
  });

  /* ---------- Chart.js helpers ---------- */
  var PALETTE = {
    primary: '#FF6B35',
    primaryLight: '#FF8A5C',
    success: '#48BB78',
    danger: '#F56565',
    warning: '#ED8936',
    info: '#4299E1',
    ai: '#7C3AED',
    gray: '#A0AEC0'
  };

  function defaultChartOptions(extra) {
    var base = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#718096', font: { family: 'Inter, sans-serif', size: 12 }, usePointStyle: true } }
      }
    };
    return Object.assign({}, base, extra || {});
  }

  function renderLineChart(canvasId, labels, datasets, extra) {
    var ctx = document.getElementById(canvasId);
    if (!ctx || typeof Chart === 'undefined') return;
    new Chart(ctx, {
      type: 'line',
      data: { labels: labels, datasets: datasets },
      options: defaultChartOptions(Object.assign({
        scales: {
          x: { grid: { color: 'rgba(226,232,240,0.5)' }, ticks: { color: '#A0AEC0' } },
          y: { grid: { color: 'rgba(226,232,240,0.5)' }, ticks: { color: '#A0AEC0' }, beginAtZero: true }
        },
        interaction: { mode: 'index', intersect: false },
        animation: { duration: 900, easing: 'easeOutQuart' }
      }, extra))
    });
  }

  function renderDoughnutChart(canvasId, labels, data, colors) {
    var ctx = document.getElementById(canvasId);
    if (!ctx || typeof Chart === 'undefined') return;
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{ data: data, backgroundColor: colors, borderWidth: 2, borderColor: '#fff' }]
      },
      options: defaultChartOptions({
        cutout: '62%',
        plugins: { legend: { position: 'bottom' } },
        animation: { animateRotate: true, duration: 900 }
      })
    });
  }

  function renderBarChart(canvasId, labels, datasets, extra) {
    var ctx = document.getElementById(canvasId);
    if (!ctx || typeof Chart === 'undefined') return;
    new Chart(ctx, {
      type: 'bar',
      data: { labels: labels, datasets: datasets },
      options: defaultChartOptions(Object.assign({
        scales: {
          x: { grid: { display: false }, ticks: { color: '#A0AEC0' } },
          y: { grid: { color: 'rgba(226,232,240,0.5)' }, ticks: { color: '#A0AEC0' }, beginAtZero: true }
        },
        animation: { duration: 900, easing: 'easeOutQuart' }
      }, extra))
    });
  }

  window.SAF.charts = {
    palette: PALETTE,
    line: renderLineChart,
    doughnut: renderDoughnutChart,
    bar: renderBarChart,
    options: defaultChartOptions
  };

})();
