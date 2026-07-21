/* ═══════════════════════════════════════════════════════════════
   DH2026 Workshop — 공용 UI (테마 · 언어 토글)

   · 테마 : dark / light   — 처음엔 시스템 설정을 따른다
   · 언어 : ko / en        — 처음엔 브라우저 언어를 따른다
   · 선택은 localStorage 에 남아 다음 방문에도 유지된다
   · 자료 사이를 오갈 때도 같은 선택이 유지된다 (키가 공통)

   HTML 쪽 규칙
   · 이중언어 텍스트는  <span lang="ko">…</span><span lang="en">…</span>
   · 전환은 CSS 가 한다 (theme.css). 이 스크립트는 html[data-*] 만 바꾼다.
   · 스크립트로 만드는 문구는 L('한국어','English') 를 쓴다.
   ═══════════════════════════════════════════════════════════════ */

(function () {
  var KT = 'dh2026-theme', KL = 'dh2026-lang';
  var root = document.documentElement;

  function initialTheme() {
    var s = localStorage.getItem(KT);
    if (s === 'light' || s === 'dark') return s;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches
      ? 'light' : 'dark';
  }
  function initialLang() {
    var s = localStorage.getItem(KL);
    if (s === 'ko' || s === 'en') return s;
    return (navigator.language || 'ko').toLowerCase().indexOf('ko') === 0 ? 'ko' : 'en';
  }

  root.dataset.theme = initialTheme();
  root.dataset.lang = initialLang();

  /* 스크립트가 만드는 문구용 — L('한국어','English') */
  window.L = function (ko, en) { return root.dataset.lang === 'en' ? en : ko; };

  /* 언어가 바뀌면 다시 그려야 하는 곳에서 쓴다 */
  var listeners = [];
  window.onLangChange = function (fn) { listeners.push(fn); };

  function setTheme(v) {
    root.dataset.theme = v;
    localStorage.setItem(KT, v);
    paint();
  }
  function setLang(v) {
    root.dataset.lang = v;
    localStorage.setItem(KL, v);
    document.documentElement.setAttribute('lang', v);
    paint();
    listeners.forEach(function (fn) { try { fn(v); } catch (e) {} });
  }

  function paint() {
    var dark = root.dataset.theme === 'dark';
    var ko = root.dataset.lang === 'ko';
    var t = document.getElementById('tgTheme');
    var l = document.getElementById('tgLang');
    if (t) {
      t.innerHTML = '<span class="ic">' + (dark ? '☾' : '☀') + '</span>'
        + (dark ? 'Dark' : 'Light');
      t.title = dark ? '밝은 화면으로 / Switch to light' : '어두운 화면으로 / Switch to dark';
    }
    if (l) {
      l.innerHTML = '<span class="' + (ko ? 'on' : 'off') + '">한</span>'
        + '<span class="sep">/</span>'
        + '<span class="' + (ko ? 'off' : 'on') + '">EN</span>';
      l.title = ko ? 'Read in English' : '한국어로 보기';
    }
  }

  /* 머리띠에 토글을 꽂는다 */
  function mount() {
    var bar = document.querySelector('.topbar');
    if (!bar) return;
    var g = document.createElement('div');
    g.className = 'tgroup';
    g.innerHTML = '<button class="tg" id="tgTheme"></button>'
                + '<button class="tg" id="tgLang"></button>';
    var back = bar.querySelector('.back');
    if (back) bar.insertBefore(g, back); else bar.appendChild(g);
    document.getElementById('tgTheme').addEventListener('click', function () {
      setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark');
    });
    document.getElementById('tgLang').addEventListener('click', function () {
      setLang(root.dataset.lang === 'ko' ? 'en' : 'ko');
    });
    paint();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }

  window.DHUI = { setTheme: setTheme, setLang: setLang };
})();
