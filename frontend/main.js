/* ============================================================
   SMART AI FORECASTING - Shared Interactions
   ============================================================ */
(function () {
  'use strict';

  /* ---------- API CONFIGURATION ---------- */
  function normalizeApiHost(host) {
    if (!host) return 'localhost';
    var trimmed = String(host).trim();
    if (['localhost', '127.0.0.1', '0.0.0.0', '::1'].indexOf(trimmed) !== -1) {
      return 'localhost';
    }
    return trimmed.indexOf(':') !== -1 && trimmed.indexOf('[') !== 0 ? '[' + trimmed + ']' : trimmed;
  }

  function resolveApiBase() {
    if (window.__SMART_AI_API_BASE__) {
      return String(window.__SMART_AI_API_BASE__).replace(/\/$/, '');
    }
    var currentHost = window.location.hostname || 'localhost';
    var currentProtocol = window.location.protocol || 'http:';
    if (['localhost', '127.0.0.1', '0.0.0.0', '::1'].indexOf(currentHost) !== -1) {
      return 'http://localhost:8001/api';
    }
    return (window.location.origin || (currentProtocol + '//' + normalizeApiHost(currentHost))) + '/api';
  }

  var API_BASE = resolveApiBase();
  var DEMO_EMAIL = 'demo.user@test.com';
  var DEMO_PASSWORD = 'Password123!';
  var AUTH_TOKEN_KEY = 'saf_auth_token';
  var USER_KEY = 'saf_user';

  function clearInvalidSession() {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }

  function isValidAuthToken(token) {
    if (!token || token === 'local-demo-token') {
      return false;
    }
    try {
      var parts = String(token).split('.');
      if (parts.length !== 3) {
        return false;
      }
      var payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')));
      if (payload && typeof payload.exp === 'number' && payload.exp * 1000 < Date.now()) {
        return false;
      }
      return true;
    } catch (e) {
      return false;
    }
  }

  function getStoredUsers() {
    try {
      return JSON.parse(localStorage.getItem('saf_users') || '[]');
    } catch (e) {
      return [];
    }
  }

  function saveStoredUsers(users) {
    localStorage.setItem('saf_users', JSON.stringify(users));
  }

  function ensureDemoUser() {
    var users = getStoredUsers();
    var emails = ['demo.user@test.com', 'manager@store.com'];
    var hasDemo = users.some(function (u) {
      return emails.indexOf(String(u.email || '').toLowerCase()) !== -1;
    });
    if (!hasDemo) {
      users.push({
        firstName: 'Demo',
        lastName: 'User',
        email: DEMO_EMAIL,
        store: 'Demo Store',
        password: DEMO_PASSWORD,
        createdAt: Date.now()
      });
      saveStoredUsers(users);
    }
    return users;
  }

  function localDemoAuth(email, password, mode) {
    var users = ensureDemoUser();
    var normalizedEmail = String(email || '').toLowerCase();
    var user = users.find(function (u) {
      return String(u.email || '').toLowerCase() === normalizedEmail ||
        (normalizedEmail === 'manager@store.com' && String(u.email || '').toLowerCase() === DEMO_EMAIL);
    });
    if (!user) {
      throw new Error(mode === 'signup' ? 'An account with this email already exists.' : 'No account found with this email. Please register first.');
    }
    var expectedPassword = String(user.password || '');
    if (expectedPassword !== String(password)) {
      throw new Error('Incorrect password. Please try again.');
    }
    var session = {
      name: (user.firstName || '') + ' ' + (user.lastName || '').trim(),
      email: user.email,
      store: user.store || 'Demo Store',
      role: 'Store Manager',
      loginTime: Date.now()
    };
    localStorage.removeItem(AUTH_TOKEN_KEY);
    localStorage.setItem(USER_KEY, JSON.stringify(session));
    return {
      access_token: null,
      user: session
    };
  }

  /* ---------- Auth Guard ---------- */
  var _page = window.location.pathname.split('/').pop();
  var _appPages = ['dashboard.html', 'inventory.html', 'forecast.html', 'alerts.html'];
  if (_appPages.indexOf(_page) !== -1) {
    var _token = localStorage.getItem(AUTH_TOKEN_KEY);
    if (!isValidAuthToken(_token)) {
      clearInvalidSession();
      window.location.replace('auth.html');
      return;
    }
  }

  /* ========== API FUNCTIONS ========== */
  function getAuthHeaders() {
    var token = localStorage.getItem(AUTH_TOKEN_KEY);
    if (!isValidAuthToken(token)) {
      clearInvalidSession();
      return {
        'Content-Type': 'application/json'
      };
    }
    return {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    };
  }

  var API = {
    login: async function(email, password) {
      try {
        var res = await fetch(API_BASE + '/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        var data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Login failed');
        localStorage.setItem(AUTH_TOKEN_KEY, data.access_token);
        localStorage.setItem(USER_KEY, JSON.stringify(data.user));
        return data;
      } catch (e) {
        console.warn('Login API unavailable, attempting local demo login:', e);
        try {
          return localDemoAuth(email, password, 'login');
        } catch (demoError) {
          console.error('Login error:', demoError);
          throw demoError;
        }
      }
    },

    signup: async function(email, password, name) {
      try {
        var res = await fetch(API_BASE + '/auth/signup', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password, name, role: 'store_manager' })
        });
        var data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Signup failed');
        localStorage.setItem(AUTH_TOKEN_KEY, data.access_token);
        localStorage.setItem(USER_KEY, JSON.stringify(data.user));
        return data;
      } catch (e) {
        console.warn('Signup API unavailable, attempting local demo signup:', e);
        try {
          var users = getStoredUsers();
          if (users.find(function (u) { return String(u.email || '').toLowerCase() === String(email || '').toLowerCase(); })) {
            throw new Error('An account with this email already exists. Try signing in.');
          }
          users.push({
            firstName: (name || 'Store').split(' ')[0],
            lastName: (name || 'Manager').split(' ').slice(1).join(' ') || 'Manager',
            email: email,
            store: 'Demo Store',
            password: password,
            createdAt: Date.now()
          });
          saveStoredUsers(users);
          var session = {
            name: name || 'Store Manager',
            email: email,
            store: 'Demo Store',
            role: 'Store Manager',
            loginTime: Date.now()
          };
          localStorage.removeItem(AUTH_TOKEN_KEY);
          localStorage.setItem(USER_KEY, JSON.stringify(session));
          return { access_token: null, user: session };
        } catch (demoError) {
          console.error('Signup error:', demoError);
          throw demoError;
        }
      }
    },

    logout: function() {
      localStorage.removeItem(AUTH_TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
      window.location.href = 'index.html';
    },

    getProducts: async function() {
      try {
        var res = await fetch(API_BASE + '/products', {
          method: 'GET',
          headers: getAuthHeaders()
        });
        var data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Failed to fetch products');
        return data.items || [];
      } catch (e) {
        console.error('Get products error:', e);
        throw e;
      }
    },

    createProduct: async function(product) {
      try {
        var res = await fetch(API_BASE + '/products', {
          method: 'POST',
          headers: getAuthHeaders(),
          body: JSON.stringify(product)
        });
        var data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Failed to create product');
        return data.product;
      } catch (e) {
        console.error('Create product error:', e);
        throw e;
      }
    },

    getDashboard: async function() {
      try {
        var res = await fetch(API_BASE + '/dashboard', {
          method: 'GET',
          headers: getAuthHeaders()
        });
        var data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Failed to fetch dashboard');
        return data;
      } catch (e) {
        console.error('Get dashboard error:', e);
        throw e;
      }
    },

    getAIInsights: async function(products) {
      try {
        var res = await fetch(API_BASE + '/dashboard/ai-insights', {
          method: 'POST',
          headers: getAuthHeaders(),
          body: JSON.stringify({ products: products })
        });
        var data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Failed to get AI insights');
        return data.insights || data.analysis || {
          stockout_risk: '⚠️ Unable to analyze inventory at this time.',
          reorder_recommendation: '📋 Check your inventory manually.',
          overstock_analysis: '📊 Monitor stock levels regularly.'
        };
      } catch (e) {
        console.error('Get AI insights error:', e);
        return {
          stockout_risk: '⚠️ Unable to analyze inventory at this time.',
          reorder_recommendation: '📋 Check your inventory manually.',
          overstock_analysis: '📊 Monitor stock levels regularly.'
        };
      }
    },

    uploadCSV: async function(file) {
      var token = localStorage.getItem(AUTH_TOKEN_KEY);
      if (!isValidAuthToken(token)) {
        clearInvalidSession();
        throw new Error('Your session expired. Please log in again.');
      }
      var formData = new FormData();
      formData.append('file', file);
      var res = await fetch(API_BASE + '/upload/csv', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + token },
        body: formData
      });
      var data = await res.json();
      if (!res.ok) throw new Error(data.detail || data.message || 'Upload failed');
      return data;
    }
  };

  window.SAF_API = API;

  function defaultProducts() {
    return [];
  }

  function normalizeProduct(product) {
    if (!product) return null;
    var normalized = Object.assign({}, product);
    normalized.minStock = Number(product.minStock || product.min_stock || 0);
    normalized.leadTime = Number(product.leadTime || product.lead_time || 3);
    normalized.min_stock = normalized.minStock;
    normalized.stock = Number(product.stock || 0);
    normalized.price = Number(product.price || 0);
    return normalized;
  }

  window.SAF = {
    currency: function (n) {
      return '\u20B9' + Number(n).toLocaleString('en-IN');
    },
    getStore: function () {
      try {
        var raw = localStorage.getItem('saf_store');
        if (!raw) {
          var initial = { products: defaultProducts() };
          localStorage.setItem('saf_store', JSON.stringify(initial));
          return initial;
        }
        var parsed = JSON.parse(raw);
        if (!parsed || !Array.isArray(parsed.products)) {
          parsed = { products: defaultProducts() };
          localStorage.setItem('saf_store', JSON.stringify(parsed));
        }
        parsed.products = (parsed.products || []).map(normalizeProduct).filter(Boolean);
        return parsed;
      } catch (e) {
        return { products: defaultProducts() };
      }
    },
    setStore: function (store) {
      try {
        var payload = store || { products: defaultProducts() };
        payload.products = (payload.products || []).map(normalizeProduct).filter(Boolean);
        localStorage.setItem('saf_store', JSON.stringify(payload));
        return payload;
      } catch (e) {
        return store || { products: defaultProducts() };
      }
    },
    clearStore: function () {
      localStorage.removeItem('saf_store');
      return { products: defaultProducts() };
    },
    predictedDemand: function (p) {
      if (!p) return 0;
      var product = normalizeProduct(p);
      var stock = Number(product.stock || 0);
      var min = Number(product.minStock || 0);
      var lead = Number(product.leadTime || 3);
      var base = Math.max(10, stock + Math.max(0, min * 0.9));
      var volatility = Math.max(8, lead * 3 + 10);
      return Math.max(0, Math.round((base + volatility) / 2));
    },
    productStatus: function (p) {
      if (!p) return { key: 'healthy', label: 'Healthy', emoji: '🟢', cls: 'status-healthy', level: 'low' };
      var product = normalizeProduct(p);
      var stock = product.stock || 0;
      var minStock = product.minStock || 0;
      if (stock < minStock) return { key: 'low', label: 'Low Stock', emoji: '🔴', cls: 'status-low', level: 'high' };
      if (stock > minStock * 3) return { key: 'overstock', label: 'Overstock', emoji: '🟡', cls: 'status-overstock', level: 'medium' };
      return { key: 'healthy', label: 'Healthy', emoji: '🟢', cls: 'status-healthy', level: 'low' };
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
      setStatus('SMART AI processing ' + file.name + '...', 'info');

      if (typeof SAF_API !== 'undefined' && SAF_API.uploadCSV) {
        SAF_API.uploadCSV(file).then(function (data) {
          var inserted = data.records_inserted || data.products_inserted || 0;
          var typeLabel = data.data_type === 'sales' ? 'sales records' : 'products';
          setStatus(
            inserted + ' ' + typeLabel + ' saved to database via SMART AI.',
            'success'
          );
          if (onFile) onFile(file, data);
        }).catch(function (err) {
          setStatus(err.message || 'Upload failed.', 'error');
        });
      } else {
        setStatus(file.name + ' uploaded successfully! ' + file.size.toLocaleString() + ' bytes.', 'success');
        if (onFile) onFile(file);
      }
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
      if (confirm('Are you sure you want to logout?')) {
        API.logout();
      }
    }
  });

  /* ---------- Set user info in header ---------- */
  function updateUserInfo() {
    var user = JSON.parse(localStorage.getItem(USER_KEY) || '{}');
    if (user && user.name) {
      var nameEl = document.getElementById('userName');
      if (nameEl) nameEl.textContent = user.name.split(' ')[0];
      var avatarEl = document.getElementById('userAvatar');
      if (avatarEl) {
        var initials = (user.name || 'U').split(' ').map(function(n) { return n[0]; }).join('').toUpperCase();
        avatarEl.textContent = initials;
      }
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateUserInfo);
  } else {
    updateUserInfo();
  }
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

  // Color palette array for charts
  var COLORS = [
    '#FF6B35', '#4299E1', '#48BB78', '#ED8936', '#7C3AED', '#10B981',
    '#EC4899', '#F59E0B', '#06B6D4', '#8B5CF6', '#EF4444', '#14B8A6'
  ];

  // Generate colors array for any number of categories
  function generateColors(count) {
    var result = [];
    for (var i = 0; i < count; i++) {
      result.push(COLORS[i % COLORS.length]);
    }
    return result;
  }

  var chartRegistry = {}; // Store chart instances globally

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
    // Destroy existing chart if present
    if (chartRegistry[canvasId]) {
      chartRegistry[canvasId].destroy();
    }
    chartRegistry[canvasId] = new Chart(ctx, {
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
    // Destroy existing chart if present
    if (chartRegistry[canvasId]) {
      chartRegistry[canvasId].destroy();
    }
    chartRegistry[canvasId] = new Chart(ctx, {
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
    // Destroy existing chart if present
    if (chartRegistry[canvasId]) {
      chartRegistry[canvasId].destroy();
    }
    chartRegistry[canvasId] = new Chart(ctx, {
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
    colors: COLORS,
    generateColors: generateColors,
    line: renderLineChart,
    doughnut: renderDoughnutChart,
    bar: renderBarChart,
    options: defaultChartOptions,
    registry: chartRegistry  // Expose registry for debugging
  };

  // Also expose chartRegistry globally for access
  window.chartRegistry = chartRegistry;

})();
