/* ═══════════════════════════════════════════════════════
   huayan_collection — 共享JS (common.js)
   华严宗·法脉全景 — 公共函数库
   ═══════════════════════════════════════════════════════ */

(function () {
  'use strict';

  /* ═══════════════════════════════════════════════════════
     1. Error Catching
     ═══════════════════════════════════════════════════════ */

  window.onerror = function (msg, src, line, col, err) {
    if (document.getElementById('js-error-bar')) return;
    var bar = document.createElement('div');
    bar.id = 'js-error-bar';
    bar.style.cssText =
      'position:fixed;top:0;left:0;right:0;z-index:99999;' +
      'background:#c46b5d;color:#fff;padding:10px 16px;' +
      'font:12px/1.5 monospace;white-space:pre-wrap;cursor:pointer';
    bar.textContent = 'JS ERROR: ' + msg + '\nFile: ' + (src || '?') +
      ' at line ' + (line || '?');
    bar.title = 'Click to dismiss';
    bar.addEventListener('click', function () {
      if (bar.parentNode) bar.parentNode.removeChild(bar);
    });
    document.body.appendChild(bar);
  };

  /* ═══════════════════════════════════════════════════════
     2. Comment System
     ═══════════════════════════════════════════════════════ */

  var COMMENT_TABS = ['lineage', 'gap', 'jiaoxing', 'practice', 'frontier', 'cosmology'];

  /**
   * Submit a comment for a given tab.
   * Saves to localStorage, optionally syncs to GitHub Issue if a PAT is configured.
   * Falls back to opening a GitHub Issue form for unauthenticated users.
   * @param {string} tab — tab identifier
   */
  window.submitComment = function (tab) {
    var textarea = document.getElementById('cmt-input-' + tab);
    if (!textarea || !textarea.value.trim()) return;
    var text = textarea.value.trim();
    var now = new Date();
    var ts =
      now.getFullYear() +
      '-' + String(now.getMonth() + 1).padStart(2, '0') +
      '-' + String(now.getDate()).padStart(2, '0') +
      ' ' + String(now.getHours()).padStart(2, '0') +
      ':' + String(now.getMinutes()).padStart(2, '0') +
      ':' + String(now.getSeconds()).padStart(2, '0');
    var token = localStorage.getItem('gh_pat_v4');
    var user = '访客';

    function saveComment(ip) {
      var comments = [];
      try {
        comments = JSON.parse(localStorage.getItem('huayan_cmt_' + tab) || '[]');
      } catch (e) { /* ignore */ }
      comments.push({ d: ts, t: text, u: user, ip: ip || '' });
      localStorage.setItem('huayan_cmt_' + tab, JSON.stringify(comments));
      textarea.value = '';
      window.renderComments(tab);

      if (token) {
        var labels =
          tab === 'jiaoxing' ? ['华严教行'] :
          tab === 'practice' ? ['行法'] :
          tab === 'lineage' ? ['法脉'] :
          tab === 'gap' ? ['文献'] :
          tab === 'cosmology' ? ['世主妙严'] :
          ['前沿'];
        var body =
          '**' + user + '** · ' + ts +
          (ip ? ' · IP:' + ip : '') +
          '\n\n---\n\n标签: ' + tab + '\n\n' + text;
        fetch('https://api.github.com/repos/LengyanReader/huayan_collection/issues', {
          method: 'POST',
          headers: {
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/vnd.github+json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            title: '💬 [' + labels[0] + '] ' + text.substring(0, 60),
            body: body,
            labels: labels
          })
        })
          .then(function (r) { return r.json(); })
          .then(function (d) {
            if (d.html_url) {
              var box = document.getElementById('cmt-' + tab);
              if (box) {
                var h4 = box.querySelector('h4');
                if (h4) {
                  h4.innerHTML +=
                    ' ✅<a href=' + d.html_url +
                    ' target=_blank style="font-size:0.8em">#' + d.number + '</a>';
                }
              }
            }
          })
          .catch(function () { /* silent */ });
      } else {
        // Fallback: open GitHub Issue form
        var title = '💬 [' + tab + '] ' + text.substring(0, 60);
        var fallbackBody = '**' + user + '** · ' + ts + '\n\n---\n\n' + text;
        var url =
          'https://github.com/LengyanReader/huayan_collection/issues/new?title=' +
          encodeURIComponent(title) + '&body=' + encodeURIComponent(fallbackBody);
        window.open(url, '_blank');
      }
    }

    // Resolve username & IP
    if (token) {
      var cachedUser = localStorage.getItem('gh_username');
      if (cachedUser) {
        user = cachedUser;
        tryGetIP(saveComment);
      } else {
        fetch('https://api.github.com/user', {
          headers: { 'Authorization': 'Bearer ' + token }
        })
          .then(function (r) { return r.json(); })
          .then(function (u) {
            if (u.login) {
              user = u.login;
              localStorage.setItem('gh_username', u.login);
            }
            tryGetIP(saveComment);
          })
          .catch(function () { tryGetIP(saveComment); });
      }
    } else {
      tryGetIP(saveComment);
    }

    function tryGetIP(cb) {
      fetch('https://api.ipify.org?format=json')
        .then(function (r) { return r.json(); })
        .then(function (d) { cb(d.ip || ''); })
        .catch(function () { cb(''); });
    }
  };

  /**
   * Render the comment list for a tab. Builds HTML including inline
   * data:image processing (splits on `![alt](data:image/...)` markup
   * and injects real <img> elements).
   * @param {string} tab
   */
  window.renderComments = function (tab) {
    var box = document.getElementById('cmt-' + tab);
    if (!box) return;
    var comments = [];
    try {
      comments = JSON.parse(localStorage.getItem('huayan_cmt_' + tab) || '[]');
    } catch (e) { /* ignore */ }
    var token = !!localStorage.getItem('gh_pat_v4');

    var h = '<h4>💬 评论与建议 (' + comments.length + ')</h4>';
    h += '<div class="c-list">';

    comments.slice(-8).forEach(function (c, i) {
      var idx = comments.length - 8 + i;
      if (idx < 0) idx = 0;
      var who =
        c.u && c.u !== '访客'
          ? '<b style="color:#5e8b9e">@' + c.u + '</b> '
          : '';
      var ts = c.d || '';
      var ip = c.ip ? ' · ' + c.ip : '';

      // Process inline images: replace ![alt](data:image/...) with <img>
      var ct = c.t;
      var buf = '', pos = 0;
      while (pos < ct.length) {
        var s = ct.indexOf('](data:image/', pos);
        if (s < 0) { buf += ct.substring(pos); break; }
        var start = ct.lastIndexOf('![', s);
        if (start < 0 || start < pos) {
          buf += ct.substring(pos, s + 2);
          pos = s + 2;
          continue;
        }
        var alt = ct.substring(start + 2, s);
        var uriEnd = s + 2;
        var depth = 1;
        while (uriEnd < ct.length && depth > 0) {
          if (ct[uriEnd] === '(') depth++;
          else if (ct[uriEnd] === ')') depth--;
          uriEnd++;
        }
        uriEnd--;
        var uri = ct.substring(s + 2, uriEnd);
        buf += ct.substring(pos, start);
        buf +=
          '<div style="text-align:center;margin:6px 0">' +
          '<img src="' + uri + '" alt="' + alt +
          '" style="max-width:200px;max-height:200px;border-radius:6px;' +
          'box-shadow:0 1px 4px rgba(0,0,0,0.1)" loading="lazy"></div>';
        pos = uriEnd + 1;
      }
      ct = buf;

      h +=
        '<div class="c-item">' +
        who +
        '<span style="font-size:0.7em;color:var(--text2)">' + ts + ip + '</span><br>' +
        ct +
        (token
          ? '<button onclick="deleteComment(\'' + tab + '\',' + idx +
            ')" style="background:none;border:none;color:#c46b5d;cursor:pointer;' +
            'font-size:0.9em" title="删除">×</button>'
          : '') +
        '</div>';
    });
    h += '</div>';

    // Textarea + submit
    h +=
      '<textarea id="cmt-input-' + tab +
      '" placeholder="输入文本或直接Ctrl+V贴图…" rows="2"></textarea>';
    h += '<button onclick="submitComment(\'' + tab + '\')">提交</button> ';

    // Image file picker
    h +=
      '<label style="font-size:0.7em;color:var(--text2);cursor:pointer;' +
      'border:1px solid var(--line);border-radius:4px;padding:2px 6px;margin-left:4px">' +
      '🖼 选图' +
      '<input type="file" accept="image/*" style="display:none" ' +
      'onchange="pickImage(this,\'' + tab + '\')"></label>';

    if (!token) {
      h +=
        '<p style="font-size:0.65em;color:var(--text2);margin-top:2px">' +
        '💡 配置Token后可同步评论至GitHub Issue并可删除</p>';
    }
    box.innerHTML = h;
  };

  /**
   * Canvas-based image compression for comment area.
   * Resizes to max 600px width, JPEG 65% quality.
   * @param {HTMLInputElement} input — file input element
   * @param {string} tab
   */
  window.pickImage = function (input, tab) {
    var file = input.files && input.files[0];
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function (ev) {
      var img = new Image();
      img.onload = function () {
        var dataUri = ev.target.result;
        if (img.width > 600) {
          var ratio = 600 / img.width;
          var w = 600;
          var h = Math.round(img.height * ratio);
          var canvas = document.createElement('canvas');
          canvas.width = w;
          canvas.height = h;
          canvas.getContext('2d').drawImage(img, 0, 0, w, h);
          dataUri = canvas.toDataURL('image/jpeg', 0.65);
        }
        var textarea = document.getElementById('cmt-input-' + tab);
        if (!textarea) return;
        textarea.value += '\n![图片](' + dataUri + ')\n';
      };
      img.src = ev.target.result;
    };
    reader.readAsDataURL(file);
    input.value = '';  // allow re-selecting the same file
  };

  /**
   * Delete a comment from localStorage by index.
   * @param {string} tab
   * @param {number} idx
   */
  window.deleteComment = function (tab, idx) {
    var comments = [];
    try {
      comments = JSON.parse(localStorage.getItem('huayan_cmt_' + tab) || '[]');
    } catch (e) { /* ignore */ }
    if (idx >= 0 && idx < comments.length) {
      comments.splice(idx, 1);
      localStorage.setItem('huayan_cmt_' + tab, JSON.stringify(comments));
      window.renderComments(tab);
    }
  };

  /* ═══════════════════════════════════════════════════════
     3. Image Paste Support (for comment textareas)
     ═══════════════════════════════════════════════════════ */

  document.addEventListener('paste', function (e) {
    var textarea = e.target.closest('textarea[id^="cmt-input-"]');
    if (!textarea) return;
    var items = e.clipboardData && e.clipboardData.items;
    if (!items) return;

    for (var i = 0; i < items.length; i++) {
      if (items[i].type.indexOf('image') === 0) {
        e.preventDefault();
        var blob = items[i].getAsFile();
        var reader = new FileReader();
        reader.onload = function (ev) {
          var img = new Image();
          img.onload = function () {
            var dataUri = ev.target.result;
            // Compress large images via canvas before storing
            if (img.width > 600) {
              var ratio = 600 / img.width;
              var w = 600;
              var h = Math.round(img.height * ratio);
              var canvas = document.createElement('canvas');
              canvas.width = w;
              canvas.height = h;
              canvas.getContext('2d').drawImage(img, 0, 0, w, h);
              dataUri = canvas.toDataURL('image/jpeg', 0.65);
            }
            var tag = '![图片](' + dataUri + ')';
            var s = textarea.selectionStart;
            var end = textarea.selectionEnd;
            textarea.value =
              textarea.value.substring(0, s) + '\n' + tag + '\n' +
              textarea.value.substring(end);
            textarea.focus();
          };
          img.src = ev.target.result;
        };
        reader.readAsDataURL(blob);
        break;
      }
    }
  });

  /* ═══════════════════════════════════════════════════════
     4. GitHub Integration (heart* functions)
     ═══════════════════════════════════════════════════════ */

  var GH_OWNER = 'LengyanReader';
  var GH_REPO = 'huayan_collection';
  var STORAGE_KEY = 'gh_pat_v4';

  /**
   * Prompt for a GitHub Personal Access Token and validate it against the API.
   */
  window.heartLogin = function () {
    var msg =
      'GitHub Fine-grained Token（仅存浏览器）:\n\n' +
      '生成: GitHub → Settings → Developer settings → Fine-grained tokens\n' +
      '→ Repository: ' + GH_OWNER + '/' + GH_REPO + '\n' +
      '→ Permissions: Contents → Read and Write\n\n粘贴Token:';
    var token = prompt(msg, localStorage.getItem(STORAGE_KEY) || '');
    if (!token || !token.trim()) return;
    var trimmed = token.trim();
    localStorage.setItem(STORAGE_KEY, trimmed);

    fetch('https://api.github.com/user', {
      headers: {
        'Authorization': 'Bearer ' + trimmed,
        'Accept': 'application/vnd.github+json'
      }
    })
      .then(function (r) { return r.json(); })
      .then(function (u) {
        if (u.login) {
          localStorage.setItem('gh_username', u.login);
          window.heartToast && window.heartToast('✅ 已授权: @' + u.login);
        } else {
          window.heartToast && window.heartToast('⚠ 授权失败，请检查Token');
        }
      })
      .catch(function () {
        window.heartToast && window.heartToast('⚠ 网络错误，Token已保存');
      });
  };

  /**
   * Clear the stored GitHub token and cached username.
   */
  window.heartLogout = function () {
    localStorage.removeItem(STORAGE_KEY);
    localStorage.removeItem('gh_username');
    window.heartToast && window.heartToast('🔓 已退出');
  };

  /**
   * Export all huayan_* and gh_* localStorage entries as a downloadable JSON file.
   */
  window.heartExport = function () {
    var dump = {};
    for (var i = 0; i < localStorage.length; i++) {
      var key = localStorage.key(i);
      if (key && (key.indexOf('huayan_') === 0 || key.indexOf('gh_') === 0)) {
        try {
          dump[key] = JSON.parse(localStorage.getItem(key));
        } catch (e) {
          dump[key] = localStorage.getItem(key);
        }
      }
    }
    var blob = new Blob([JSON.stringify(dump, null, 2)], { type: 'application/json' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'huayan_backup_' + new Date().toISOString().slice(0, 10) + '.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.heartToast && window.heartToast('💾 已导出 JSON');
  };

  /**
   * Import a JSON backup file and restore localStorage entries.
   */
  window.heartImport = function () {
    var input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = function (e) {
      var file = e.target.files[0];
      if (!file) return;
      var reader = new FileReader();
      reader.onload = function (ev) {
        try {
          var data = JSON.parse(ev.target.result);
          var count = 0;
          Object.keys(data).forEach(function (key) {
            if (key.indexOf('huayan_') === 0 || key.indexOf('gh_') === 0) {
              localStorage.setItem(key,
                typeof data[key] === 'string' ? data[key] : JSON.stringify(data[key]));
              count++;
            }
          });
          window.heartToast &&
            window.heartToast('📥 已导入 ' + count + ' 项 · 刷新页面生效');
        } catch (ex) {
          window.heartToast && window.heartToast('❌ JSON格式错误');
        }
      };
      reader.readAsText(file);
    };
    input.click();
  };

  /**
   * Flash a temporary toast notification at the bottom center of the screen.
   * @param {string} msg
   * @param {boolean} [quiet] — if true, suppress the toast
   */
  window.heartToast = function (msg, quiet) {
    if (quiet) return;
    var toast = document.createElement('div');
    toast.style.cssText =
      'position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:99999;' +
      'background:#3d3427;color:#fefdf9;padding:8px 20px;border-radius:20px;' +
      'font-size:0.82em;transition:opacity 0.3s;pointer-events:none';
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(function () {
      toast.style.opacity = '0';
      setTimeout(function () {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 300);
    }, 2000);
  };

  /**
   * Copy an element's text content to the clipboard.
   * @param {string} elId — element id (without '#')
   */
  window.heartCopy = function (elId) {
    var el = document.getElementById(elId);
    if (!el) return;
    var text = el.textContent || el.innerText || '';
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () {
        window.heartToast && window.heartToast('✅ 已复制');
      }).catch(function () {
        // Fallback for permission denied
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.style.cssText = 'position:fixed;left:-9999px';
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand('copy'); } catch (e) { /* silent */ }
        document.body.removeChild(ta);
      });
    } else {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.cssText = 'position:fixed;left:-9999px';
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand('copy');
        window.heartToast && window.heartToast('✅ 已复制');
      } catch (e) {
        window.heartToast && window.heartToast('❌ 复制失败');
      }
      document.body.removeChild(ta);
    }
  };

  /* ═══════════════════════════════════════════════════════
     5. Scroll-to-Top Button
     ═══════════════════════════════════════════════════════ */

  /**
   * Create and inject a floating scroll-to-top button if a .back-to-top
   * element exists in the DOM. Wires its visibility to window scroll position.
   */
  window.createScrollTopButton = function () {
    var btn = document.querySelector('.back-to-top');
    if (!btn) return;
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (!ticking) {
        requestAnimationFrame(function () {
          btn.classList.toggle('visible', window.scrollY > 300);
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  };

  /* ═══════════════════════════════════════════════════════
     6. Sidebar Scroll-Spy
     ═══════════════════════════════════════════════════════ */

  /**
   * Wire up scroll-spy behavior on the page/window, highlighting the sidebar
   * nav-link corresponding to the currently-visible section.
   *
   * Sidebar links use `data-section` attributes pointing to the id of the
   * target section in the content area.
   *
   * @param {Object} [opts]
   * @param {string} [opts.sidebarSelector='#sidebar'] — sidebar container
   * @param {string} [opts.linkSelector='.nav-link'] — nav links inside sidebar
   * @param {number} [opts.offset=80] — px offset from top
   */
  window.initSidebarScrollSpy = function (opts) {
    opts = opts || {};
    var sidebarSel = opts.sidebarSelector || '#sidebar';
    var linkSel = opts.linkSelector || '.nav-link';
    var offset = (opts.offset != null) ? opts.offset : 80;

    var sidebar = document.querySelector(sidebarSel);
    if (!sidebar) return;

    var links = sidebar.querySelectorAll(linkSel);
    if (!links.length) return;

    // Click handler: smooth scroll to target section
    links.forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        var sectionId = link.getAttribute('data-section');
        if (!sectionId) return;
        var target = document.getElementById(sectionId) ||
          document.querySelector('[id*="' + sectionId + '"]');
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });

    // Scroll-spy: highlight the active nav-link
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (!ticking) {
        requestAnimationFrame(function () {
          var scrollPos = window.scrollY + offset;

          links.forEach(function (link) {
            var sectionId = link.getAttribute('data-section');
            if (!sectionId) return;
            var target = document.getElementById(sectionId) ||
              document.querySelector('[id*="' + sectionId + '"]');
            if (!target) return;

            var top = target.offsetTop;
            var bottom = top + target.offsetHeight;

            if (scrollPos >= top && scrollPos < bottom) {
              links.forEach(function (l) { l.classList.remove('active'); });
              link.classList.add('active');
            }
          });

          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  };

  /* ═══════════════════════════════════════════════════════
     7. Auto-Initialize: render comments for existing boxes
     ═══════════════════════════════════════════════════════ */

  COMMENT_TABS.forEach(function (tab) {
    if (document.getElementById('cmt-' + tab)) {
      try { window.renderComments(tab); } catch (e) { /* DOM not ready yet */ }
    }
  });

  /* ═══════════════════════════════════════════════════════
     8. Sidebar Collapsible Groups (accordion)
     ═══════════════════════════════════════════════════════ */
  window.toggleSidebarGroup = function (link) {
    var group = link.closest('.sidebar-group');
    if (!group || !group.classList.contains('has-subs')) return true; // proceed normally
    var wasOpen = group.classList.contains('open');
    // Close all siblings
    document.querySelectorAll('.sidebar-group.open').forEach(function (g) {
      if (g !== group) g.classList.remove('open');
    });
    if (wasOpen) {
      group.classList.remove('open');
      return false; // suppress original onclick
    } else {
      group.classList.add('open');
      return true; // allow original onclick to fire
    }
  };

  /* ═══════════════════════════════════════════════════════
     9. Global Reading-Language Toggle (中英对照 ⇄ 仅中文)
     统一开关：仅中文偏好为「会话级」（sessionStorage，'0' = 仅中文）。
     . 默认恒为中英对照：新会话/次次打开页面时英文默认显示，避免误触后
       英文在全站「永久消失」（不再交由 localStorage 持久状态决定）。
     . '仅中文' 仅影响当前浏览器标签页会话，标签页关闭即恢复默认。
     . 顺带清理历史 localStorage 'site_lang' 旧值，使旧偏好不再静默生效。
       作用于全站所有页面的英文对应块（.en-line / .en-block / .en-note / .en-cell）。
     ═══════════════════════════════════════════════════════ */

  /**
   * Apply the reading-language preference to the current page.
   * 阅读语言默认中英对照（zh-only 关闭）；仅中文为会话级、绝不跨会话持久隐藏英文。
   */
  /**
   * 英文对应块打标（全站通用，供「仅中文」隐藏）。
   * 文档渲染路径（_mdDocEmbed / gap.js 专题研究视图 / article.js）产出的英文对应块
   * 均为 <blockquote>，须先加 .en-block 类，common.css 的 body.zh-only 规则方能命中。
   * 幂等：可反复调用，动态插入的内容亦可即时补标。
   */
  window._markEnBlocks = function (root) {
    var sc = root || document;
    var bqs = sc.querySelectorAll ? sc.querySelectorAll('blockquote') : [];
    for (var i = 0; i < bqs.length; i++) {
      var t = (bqs[i].textContent || '').replace(/\s+/g, ' ').trim();
      if (/^(英译对读|EN对应|EN\s*corresponding|EN\s*note|EN\s*register|EN\s*block|🔑|术语格义|主题对读注|卷末批注)/i.test(t)) bqs[i].classList.add('en-block');
    }
  };

  window._applySiteLang = function () {
    try { window._markEnBlocks(); } catch (e) {}
    var zh = (sessionStorage.getItem('site_lang') || '') === '0';
    document.body.classList.toggle('zh-only', zh);
    var btn = document.getElementById('lang-toggle');
    if (btn) {
      btn.textContent = zh ? '🌐 仅中文' : '🌐 中·EN';
      btn.classList.toggle('zh', zh);
      btn.setAttribute('aria-pressed', zh ? 'true' : 'false');
    }
  };

  /**
   * Toggle between '中英对照' (bilingual, default) and '仅中文' (Chinese only).
   * 会话级切换：写入 sessionStorage，并清除历史 localStorage 旧值。
   */
  window.toggleSiteLang = function () {
    var nowZh = (sessionStorage.getItem('site_lang') || '') === '0';
    sessionStorage.setItem('site_lang', nowZh ? '1' : '0');
    localStorage.removeItem('site_lang');
    window._applySiteLang();
  };

  /* ═══════════════════════════════════════════════════════
     10. 共享参考文献渲染器 renderRefList（单源·全站复用）
     ───────────────────────────────────────────────────────
     华严文献 / 教海行云 / 禅门实迹 各页 references 的**唯一渲染源**，
     取代此前散落于 practice.js / gap.js / cosmology.js 及 build.py 内联
     CHAN_TRACES_RENDER / GAP_TOPICS_RENDER 的重复 `refs.forEach(r=>'<li>'+r)`。
     入参 refs 兼容三种形态：
       · 字符串数组（旧格式，向后兼容，原样成条）；
       · 对象数组 {label|cite|text|fmt, tier:'A'|'B'|'C', url, note}；
       · 「类目 → 上述数组」映射（分组渲染）。
     opts: { fmt: 逐条文本格式化函数(如 _dynMD), md: 用全局 mdToHTML, legend:false 关图例 }。
     A/B/C 信度分级 + 🔗核对（指向可回查原页）；无 url 不臆造、留空即不显链接。
     ═══════════════════════════════════════════════════════ */
  var REF_TIER = {
    A: ['一手 · 权威', 'var(--gold)'],
    B: ['专著 · 学位论文', 'var(--blue)'],
    C: ['线索 · 待核', '#d98a00']
  };
  function refItem(r, fmt) {
    if (r == null) return '';
    if (typeof r === 'string') return '<li style="margin:2px 0">' + (fmt ? fmt(r) : r) + '</li>';
    if (typeof r === 'object') {
      var lb = r.label || r.cite || r.text || r.fmt || ''; lb = fmt ? fmt(lb) : lb;
      var bd = '';
      if (r.tier && REF_TIER[r.tier]) {
        bd = '<span title="信度 ' + REF_TIER[r.tier][0] + '" style="display:inline-block;min-width:13px;text-align:center;padding:0 4px;margin-right:5px;border:1px solid ' + REF_TIER[r.tier][1] + ';border-radius:3px;color:' + REF_TIER[r.tier][1] + ';font-weight:700;font-size:0.88em">' + r.tier + '</span>';
      }
      var nt = r.note ? ' <span style="color:var(--text2)">— ' + (fmt ? fmt(r.note) : r.note) + '</span>' : '';
      var lk = r.url ? ' <a href="' + r.url + '" target="_blank" rel="noopener" style="color:var(--blue);text-decoration:none;white-space:nowrap">🔗核对</a>' : '';
      return '<li style="margin:2px 0">' + bd + lb + nt + lk + '</li>';
    }
    return '<li style="margin:2px 0">' + String(r) + '</li>';
  }
  window._refItem = refItem;
  window.renderRefList = function (refs, opts) {
    opts = opts || {};
    if (!refs) return '';
    var fmt = opts.fmt || (opts.md && typeof mdToHTML === 'function' ? mdToHTML : null);
    var legend = (opts.legend === false) ? '' :
      '<div style="font-size:0.9em;color:var(--text2);margin:2px 0 6px">🔖 信度分级：<b style="color:var(--gold)">A</b> 一手/权威 · <b style="color:var(--blue)">B</b> 专著/学位论文 · <b style="color:#d98a00">C</b> 线索/待核 &nbsp;·&nbsp; 🔗核对 = 指向可回查原页</div>';
    var body = '';
    var isMap = !Array.isArray(refs) && typeof refs === 'object';
    if (isMap) {
      Object.keys(refs).forEach(function (k) {
        var arr = refs[k] || [];
        body += '<li style="list-style:none;margin:6px 0 2px;padding-left:0"><b>' + k +
                '</b><ul style="margin:0;padding-left:18px">' +
                arr.map(function (r) { return refItem(r, fmt); }).join('') + '</ul></li>';
      });
      return legend + '<ul style="margin:0;padding-left:12px">' + body + '</ul>';
    }
    return legend + '<ul style="margin:0;padding-left:18px">' +
      refs.map(function (r) { return refItem(r, fmt); }).join('') + '</ul>';
  };

})();

// ═══ Global markdown-lite converter ═══
function mdToHTML(s) {
  if (!s) return '';
  return String(s)
    .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
    .replace(/(^|[^*])\*([^*]+?)\*(?!\*)/g, '$1<i>$2</i>');
}

// ═══ Full-document markdown → HTML (headings/quotes/hr/lists/tables/fences) ═══
// Shared by gap.js (专题/祖师全文) 与 article.js (独立文章页)。
function _mdFullToHTML(text) {
  if (!text) return '';
  var lines = text.split('\n');
  var out = [];
  var i = 0;
  while (i < lines.length) {
    var l = lines[i];
    // blank line
    if (!l.trim()) { i++; continue; }
    // horizontal rule
    if (/^---+$/.test(l.trim())) { out.push('<hr style="border:none;border-top:1px solid var(--line);margin:14px 0">'); i++; continue; }
    // headings
    var mh = l.match(/^(#{1,4})\s+(.*)$/);
    if (mh) {
      var lv = mh[1].length;
      out.push('<h' + lv + ' style="color:var(--gold);margin:' + (lv===1?'18px':'14px') + ' 0 8px;font-size:' + [0,'1.15em','1.02em','0.95em','0.88em'][lv] + ';line-height:1.5">' + _mdInline(mh[2]) + '</h' + lv + '>');
      i++; continue;
    }
    // blockquote
    if (l.trim().indexOf('>') === 0) {
      var q = [];
      while (i < lines.length && lines[i].trim().indexOf('>') === 0) {
        q.push(lines[i].trim().replace(/^>\s?/, ''));
        i++;
      }
      // 引用块内若含表格，须按块级 markdown 递归渲染（否则表格会被当作纯文本转义显示）
      var _bq = q.join('\n');
      var _bqBlock = /^[ \t]*\|/m.test(_bq);
      out.push('<blockquote style="border-left:3px solid var(--gold);background:rgba(184,134,60,0.06);padding:8px 12px;margin:10px 0;font-size:0.82em;line-height:1.8;color:var(--text2);' + (_bqBlock ? '' : 'white-space:pre-line') + '">' + (_bqBlock ? _mdFullToHTML(_bq) : _mdInline(_bq)) + '</blockquote>');
      continue;
    }
    // table
    if (l.trim().indexOf('|') === 0 && (i+1 < lines.length) && lines[i+1].indexOf('---') >= 0) {
      var header = l.split('|').filter(function(c){return c.trim();});
      out.push('<table class=v-table style="font-size:0.78em;margin:8px 0"><tr>' + header.map(function(c){return '<th>' + _mdInline(c.trim()) + '</th>';}).join('') + '</tr>');
      i += 2;
      while (i < lines.length && lines[i].trim().indexOf('|') === 0) {
        var cells = lines[i].split('|').filter(function(c){return c.trim();});
        out.push('<tr>' + cells.map(function(c){return '<td>' + _mdInline(c.trim()) + '</td>';}).join('') + '</tr>');
        i++;
      }
      out.push('</table>');
      continue;
    }
    // ordered list
    var mo = l.match(/^\s*\d+\.\s+(.*)$/);
    if (mo) {
      out.push('<ol style="margin:6px 0 6px 18px;font-size:0.8em;line-height:1.8">');
      while (i < lines.length && /^\s*\d+\.\s/.test(lines[i])) {
        out.push('<li>' + _mdInline(lines[i].replace(/^\s*\d+\.\s/, '')) + '</li>');
        i++;
      }
      out.push('</ol>');
      continue;
    }
    // unordered list
    var mu = l.match(/^\s*[-•·]\s+(.*)$/);
    if (mu) {
      out.push('<ul style="margin:6px 0 6px 18px;font-size:0.8em;line-height:1.8">');
      while (i < lines.length && /^\s*[-•·]\s/.test(lines[i])) {
        var item = lines[i].replace(/^\s*[-•·]\s/, '');
        out.push('<li>' + _mdInline(item) + '</li>');
        i++;
      }
      out.push('</ul>');
      continue;
    }
    // block-level HTML passthrough: <details>/<figure>/<svg>/<div>/… 原样透出，
    // 内文仍按 markdown 递归渲染。不走此路则会被段落分支包进 <p>，块级元素即失效。
    var mh2 = l.match(/^\s*<(\/?)(details|figure|svg|div|picture|section|aside)\b/i);
    if (mh2 && !mh2[1]) {
      var tag = mh2[2].toLowerCase();
      var endRe = new RegExp('</' + tag + '\\s*>', 'i');
      var raw = [];
      var cut = -1;
      for (var j = i; j < lines.length; j++) {
        raw.push(lines[j]);
        if (endRe.test(lines[j])) { cut = j; break; }
      }
      if (cut >= 0) {
        var blk = raw.join('\n');
        i = cut + 1;
        if (tag === 'details') {
          // 折叠块：summary 走 inline（可含强调），正文递归按 markdown 渲染；默认收起
          var isOpen = /<details\b[^>]*\bopen\b/i.test(raw[0]);
          var dcls = (raw[0].match(/<details\b[^>]*\bclass="([^"]*)"/i) || [, ''])[1];
          var inner = raw.slice(1, -1);
          var sm = '';
          var smIdx = -1;
          for (var k = 0; k < inner.length; k++) {
            if (/<summary>/i.test(inner[k])) { smIdx = k; break; }
          }
          if (smIdx >= 0) {
            var smTxt = inner[smIdx].replace(/<summary>/i, '').replace(/<\/summary>/i, '');
            inner.splice(smIdx, 1);
            while (inner.length && /^\s*<\/summary>\s*$/i.test(inner[0])) inner.shift();
            for (var m2 = 0; m2 < inner.length; m2++) inner[m2] = inner[m2].replace(/<\/summary>/i, '');
            sm = _mdInline(smTxt.trim());
          }
          out.push('<details class="fold' + (dcls ? ' ' + dcls : '') + '"' + (isOpen ? ' open' : '') + '>'
            + '<summary>' + sm + '</summary><div class="fold-body">'
            + _mdFullToHTML(inner.join('\n')) + '</div></details>');
        } else {
          out.push(blk);   // figure/svg/div 等：整块原样透出
        }
        continue;
      }
      // 未见闭合标签 → 退回段落分支（避免误吞余下全文）
    }
    // code fence (```)
    if (l.trim().indexOf('```') === 0) {
      var code = [];
      i++;
      while (i < lines.length && lines[i].trim().indexOf('```') !== 0) { code.push(lines[i]); i++; }
      if (i < lines.length) i++; // skip closing fence
      out.push('<pre style="background:rgba(94,139,158,0.08);border:1px solid var(--line);border-radius:8px;padding:10px 12px;font-size:0.78em;line-height:1.5;overflow-x:auto;margin:8px 0;white-space:pre">' + code.join('\n').replace(/&/g,'&amp;').replace(/</g,'&lt;') + '</pre>');
      continue;
    }
    // paragraph (collect consecutive lines)
    var para = [l];
    i++;
    while (i < lines.length && lines[i].trim() && !/^(#{1,4}\s|---+$|>\s|\||\s*\d+\.\s|\s*[-•·]\s|\s*<\/?(details|figure|svg|div|picture|section|aside)\b)/.test(lines[i].trim())) {
      para.push(lines[i]); i++;
    }
    out.push('<p style="font-size:0.8em;line-height:1.9;margin:6px 0">' + _mdInline(para.join('<br>')) + '</p>');
  }
  return out.join('');
}

// ═══ Inline markdown (code/bold/italic/link) ═══
function _mdInline(t) {
  t = t.replace(/`([^`]+)`/g, '<code style="font-family:monospace;font-size:0.92em;background:rgba(94,139,158,0.12);padding:1px 5px;border-radius:4px">$1</code>');
  t = t.replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
  t = t.replace(/\*(.+?)\*/g, '<i>$1</i>');
  t = t.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target=_blank style="color:var(--blue)">$1</a>');
  return t;
}

// ═══ 整篇 markdown 文档嵌入（标题加锚点 id + 生成目录；剥离 HTML 注释）═══
function _mdDocEmbed(md) {
  if (!md) return {html:'', toc:[]};
  md = md.replace(/<!--[\s\S]*?-->/g, '');
  // 目录：源标题行（h2-h4；h1 为文档标题，不入目录）
  var toc = [], m;
  var reT = /^[#]{2,4}\s+(.*)$/gm;
  while ((m = reT.exec(md)) !== null) {
    var lv = m[0].match(/^#+/)[0].length;
    toc.push({lv: lv, id: 'mdh-' + (toc.length + 1), text: m[1].replace(/\*\*(.+?)\*\*/g, '$1').trim()});
  }
  // 渲染后为每个 h2-h4 注入同名 id（顺序一致）
  var html = _mdFullToHTML(md);
  var counter = 0;
  html = html.replace(/<h([234])([^>]*)>/g, function(u, lv, attrs) {
    counter++;
    return '<h' + lv + ' id="mdh-' + counter + '" ' + attrs + '>';
  });
  return {html: html, toc: toc};
}

// ═══ 独立文章入口条（ARTICLES 由 build.py 内嵌在各 Tab 页）═══
// view 为当前子视图 id；containerSel 为本视图容器（如 '#gv-topic-zhenwei'）。
// 命中 articles 登记中的 views 时，在容器顶部插入「独立文章页」入口（独立地址，点击即进入）。

// 由子视图 id 反查独立文章页的（相对本页面）href；无则返回空串。
// 用于祖师/专题总览卡片、侧栏等「一点击即进入独立页面」的入口。
function articlePageHref(view){
  if(typeof ARTICLES==='undefined'||!ARTICLES) return '';
  for(var i=0;i<ARTICLES.length;i++){
    var a=ARTICLES[i];
    if((a.views||[]).indexOf(view)>=0)
      return (a.file.indexOf('../')===0)?a.file:'../'+a.file;
  }
  return '';
}

function articleChip(view, containerSel){
  if(typeof ARTICLES==='undefined'||!ARTICLES) return;
  var arts=ARTICLES.filter(function(x){return (x.views||[]).indexOf(view)>=0;});
  if(!arts.length) return;
  var el=document.querySelector(containerSel);
  if(!el) return;
  if(document.querySelector(containerSel+' .article-chip')) return;
  var chip=document.createElement('div');
  chip.className='article-chip';
  var links=[];
  arts.forEach(function(a){
    var href=(a.file.indexOf('../')===0)?a.file:'../'+a.file;
    links.push('<a href="'+href+'" title="打开完整文章独立地址">'+(a.icon?a.icon+' ':'')+a.title+' ↗</a>');
  });
  chip.innerHTML=links.join(' · ');
  el.insertBefore(chip, el.firstChild);
}

// ═══ 独立文章目录入口（sidebar 底部小链接，build.py 生成的目录）═══
function articlesIndexLink(){
  var nav=document.querySelector('#sidebar');
  if(!nav) return;
  if(nav.querySelector('.articles-index-link')) return;
  var el=document.createElement('div');
  el.className='articles-index-link';
  el.style.cssText='margin-top:14px;padding-top:10px;border-top:1px solid var(--line);font-size:0.74em';
  el.innerHTML='<a href="../articles/index.html" style="color:var(--blue);text-decoration:none">📚 独立文章目录</a>';
  nav.appendChild(el);
}

  /**
   * 动态内容补标：Tab 视图切换、专题研究渲染、文章渲染均为运行时就地插入 DOM，
   * 须在插入后重跑打标，否则「仅中文」下这些英文对应块不会被隐藏。
   * 仅观察 childList（不观察 attributes），故打标自身不会触发回调、无循环之虞。
   */
  (function () {
    if (typeof MutationObserver === 'undefined' || !document.body) return;
    var pending = false;
    var run = function () {
      pending = false;
      try { window._markEnBlocks && window._markEnBlocks(); } catch (e) {}
    };
    new MutationObserver(function () {
      if (pending) return;
      pending = true;
      (window.requestAnimationFrame || window.setTimeout)(run, 16);
    }).observe(document.body, { childList: true, subtree: true });
  })();

// ═══ 悬浮目录 (floating TOC) ═══
// 长文（独立文章页）阅读用：右侧可折叠目录 rail，随滚动高亮当前节，附阅读进度。
// 目录项**从正文标题派生**（扫描容器内 h2-h4，缺 id 者就地补 id），不硬编码任何条目，
// 故任何长文页面（doc 型与 data_source 型皆然）自动受益。
// 激活条件：页内存在 #article-root（独立文章页）；Tab 页不注入。
function _initFloatingToc(containerSel) {
  var root = document.querySelector(containerSel || '#article-root');
  if (!root) return;
  if (document.querySelector('.floating-toc')) return;   // 已注入，勿重复

  // sticky 页头实高（据实量取，不写死像素）；另留 8px 呼吸位
  function stickyGap() {
    var top = document.getElementById('page-top');
    return (top ? top.offsetHeight : 0) + 8;
  }

  // ── 收集标题（h2-h4，跳过 h2 内的按钮等非文本节点由 _flatText 处理）──
  var heads = Array.prototype.slice.call(root.querySelectorAll('h2, h3, h4'));
  heads = heads.filter(function (h) {
    // 排除页面自身的装饰性标题（导览/目录等，渲染器以 data-chrome / data-skip-toc 标出）
    if (h.hasAttribute('data-skip-toc')) return false;
    if (h.closest && h.closest('[data-chrome]')) return false;
    // 文本为空或仅含图标者不入目录
    var t = _flatText(h);
    return t && t.length > 1;
  });
  if (heads.length < 3) return;   // 标题太少，悬浮目录反成累赘，不注入

  // ── 补 id（数据驱动页之标题未必有 id）──
  var items = heads.map(function (h, i) {
    if (!h.id) h.id = 'ftoc-h' + (i + 1);
    return {
      id: h.id,
      lv: parseInt(h.tagName.charAt(1), 10),
      text: _flatText(h).slice(0, 60)
    };
  });

  // ── 结构：收态＝竖向窄轨（进度＋当前节）；展态＝标题条＋完整目录 ──
  var rail = document.createElement('nav');
  rail.className = 'floating-toc';
  rail.setAttribute('aria-label', '悬浮目录');
  var list = items.map(function (t) {
    return '<a href="#' + t.id + '" class="ftoc-lv' + t.lv + '" data-tid="' + t.id + '">' +
             _escHtml(t.text) + '</a>';
  }).join('');
  rail.innerHTML =
    '<div class="ftoc-rail" title="点此钉住目录／再点取消；鼠标移入亦可展开">' +
      '<span class="fr-icon">🧭</span>' +
      '<span class="fr-track"><i class="fr-fill"></i></span>' +
      '<span class="fr-label"></span>' +
    '</div>' +
    '<div class="ftoc-bar" title="点此钉住目录／再点取消；移开即收起">' +
      '<span class="ftoc-title">🧭 目录</span>' +
      '<span class="ftoc-count">' + items.length + ' 节</span>' +
      '<span class="ftoc-progress"><i></i></span>' +
      '<button class="ftoc-toggle" type="button" title="钉住／取消钉住">📌</button>' +
    '</div>' +
    '<div class="ftoc-list">' + list + '</div>';
  document.body.appendChild(rail);

  // 窄屏浮层钮（宽屏隐藏）
  var tab = document.createElement('button');
  tab.className = 'floating-toc-tab';
  tab.type = 'button';
  tab.title = '目录';
  tab.innerHTML = '🧭';
  tab.addEventListener('click', function () { rail.classList.toggle('is-mobile-open'); });
  document.body.appendChild(tab);

  // ── 钉住：默认随鼠标进出开合（不遮正文）；点窄轨／条／钮可钉住供持续可见 ──
  var bar = rail.querySelector('.ftoc-bar');
  var narrow = rail.querySelector('.ftoc-rail');
  var btn = rail.querySelector('.ftoc-toggle');
  function togglePinned() {
    var on = rail.classList.toggle('is-open');
    btn.textContent = on ? '📌' : '📍';
    btn.title = on ? '取消钉住' : '钉住目录';
  }
  narrow.addEventListener('click', togglePinned);
  bar.addEventListener('click', function (e) {
    if (e.target === btn) return;      // 按钮自身已绑 togglePinned
    togglePinned();
  });
  btn.addEventListener('click', function (e) { e.stopPropagation(); togglePinned(); });
  // 触屏无 hover：以窄轨为展开把手（点一次钉住，Esc 或再点收起）
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') rail.classList.remove('is-open', 'is-mobile-open');
  });

  // ── 点击锚点：先展开被折叠的祖先节，再平滑滚动，避开顶部 sticky 页头 ──
  rail.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
    if (!a) return;
    var id = a.getAttribute('href').slice(1);
    var el = document.getElementById(id);
    if (!el) return;
    e.preventDefault();
    if (window._reveal && (typeof _skipReveal === 'undefined' || !_skipReveal)) window._reveal(el);
    window.scrollTo({ top: topOf(el) - stickyGap(), behavior: 'smooth' });
    if (history.replaceState) history.replaceState(null, '', '#' + id);
    // 释放焦点，令 :focus-within 随之解除 → 未钉住时面板即随鼠标移开而收起
    a.blur();
  });

  // ── 当前节高亮 + 阅读进度（滚动时取「视口上缘之上最末一个标题」）──
  var links = {};
  items.forEach(function (t) {
    var el = document.getElementById(t.id);
    if (el) links[t.id] = rail.querySelector('a[data-tid="' + t.id + '"]');
  });
  var prog = rail.querySelector('.ftoc-progress i');
  var railFill = rail.querySelector('.ftoc-rail .fr-fill');
  var railLabel = rail.querySelector('.ftoc-rail .fr-label');
  var listBox = rail.querySelector('.ftoc-list');
  var cur = null, ticking = false;

  function topOf(el) {
    return el.getBoundingClientRect().top + window.pageYOffset;
  }

  // 幂等重算：可由 rAF 与定时器重复调用，结果一致，故双轨调度互为保险
  // （rAF 在后台标签页与部分嵌入 webview 会被节流，单靠 rAF 会漏更新）。
  function update() {
    ticking = false;
    var y = window.pageYOffset + 150;
    var idx = -1;
    for (var i = 0; i < items.length; i++) {
      var el = document.getElementById(items[i].id);
      if (!el) continue;
      if (topOf(el) <= y) idx = i; else break;
    }
    // 滚到底：强制高亮末节；尚未越过首节（页头/横幅区）：高亮首节
    if (window.innerHeight + window.pageYOffset >= document.body.scrollHeight - 4)
      idx = items.length - 1;
    if (idx < 0) idx = 0;
    if (idx >= 0 && items[idx].id !== cur) {
      if (cur && links[cur]) links[cur].classList.remove('is-active');
      cur = items[idx].id;
      if (links[cur]) {
        links[cur].classList.add('is-active');
        // 高亮项保持在可视区内
        if (listBox) {
          var lt = links[cur].offsetTop, lb = lt + links[cur].offsetHeight;
          if (lt < listBox.scrollTop || lb > listBox.scrollTop + listBox.clientHeight)
            listBox.scrollTop = lt - listBox.clientHeight / 2;
        }
      }
      // 收态窄轨亦示当前节（否则读者不知身在何处）
      if (railLabel && idx >= 0) railLabel.textContent = (idx + 1) + '·' + items[idx].text;
    }
    if (prog) {
      var h = document.body.scrollHeight - window.innerHeight;
      var pct = (h > 0 ? Math.min(100, Math.max(0, window.pageYOffset / h * 100)) : 0);
      prog.style.width = pct + '%';
      if (railFill) railFill.style.height = pct + '%';
    }
  }

  function onScroll() {
    if (ticking) return;
    ticking = true;
    (window.requestAnimationFrame || window.setTimeout)(update, 16);
    setTimeout(update, 200);   // rAF 未被调度时的保险（幂等）
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  // 深链直达（#锚点）：浏览器原生跳转会停在 y=0 而被 sticky 页头遮住标题，
  // 故按页头实高下移校正；载入时与运行时 hashchange 皆适用。
  function applyHashOffset() {
    if (!location.hash) return;
    var el = document.getElementById(location.hash.slice(1));
    if (!el) return;
    window.scrollTo({ top: Math.max(0, topOf(el) - stickyGap()), behavior: 'auto' });
    onScroll();
  }
  if (location.hash) setTimeout(applyHashOffset, 120);
  window.addEventListener('hashchange', function () { setTimeout(applyHashOffset, 0); });
}

function _flatText(el) {
  return (el && el.textContent ? el.textContent : '').replace(/\s+/g, ' ').trim();
}

function _escHtml(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ═══ 术语标注 · 弹窗 · 知识图谱面板 ═══
// 数据源：data/translation/article_knowledge/<article_id>.yaml
//   → import_all_to_sqlite.py → SQLite(article_terms/article_term_links)
//   → db_reader.load_article_knowledge() → build.py 内嵌 var ARTICLE_GRAPH
// 命中两种方式：①正文自动扫描 term_zh + aliases ②显式标记 [[显示文本|term_id]]。
// 信度分级：A1 经文直证 · A2 古注明证 · B 文献转述 · C 单一来源待考 · D 疑讹不采用。

var _AG = null;   // {title, terms[], links[]}
var _AGi = null;  // term_id -> term（terms 已带 out/in 邻接）

function _agInit() {
  if (_AG !== null) return _AG;
  _AG = (typeof ARTICLE_GRAPH !== 'undefined' && ARTICLE_GRAPH) ? ARTICLE_GRAPH : null;
  if (!_AG) return null;
  _AGi = {};
  (_AG.terms || []).forEach(function (t) { _AGi[t.id] = t; });
  return _AG;
}

// 依长度降序排比，避免「摩竭提」先于「摩竭提國」命中
function _agNames() {
  if (_agInit() && _agNames._all) return _agNames._all;
  var map = {};
  (_AG.terms || []).forEach(function (t) {
    [t.zh].concat(t.aliases || []).forEach(function (n) {
      if (n && n.length >= 2) map[n] = t.id;
    });
  });
  var re = new RegExp(
    Object.keys(map).sort(function (a, b) { return b.length - a.length; })
      .map(function (n) { return n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); })
      .join('|'), 'g');
  _agNames._all = { re: re, map: map };
  return _agNames._all;
}

function _agSkip(el) {
  for (var n = el; n && n.nodeType === 1; n = n.parentNode) {
    if (n.tagName === 'SCRIPT' || n.tagName === 'STYLE' || n.tagName === 'TEXTAREA') return true;
    if (n.classList && (n.classList.contains('term-ref') || n.classList.contains('term-modal'))) return true;
  }
  return false;
}

function _agWrap(txt, id) {
  var t = _AGi[id];
  var cls = 'term-ref' + (t && t.status === 'rejected' ? ' is-rejected' : '');
  var s = document.createElement('span');
  s.className = cls;
  s.dataset.termId = id;
  s.setAttribute('role', 'button');
  s.tabIndex = 0;
  s.textContent = txt;
  return s;
}

// ═══ 文物 · 艺术品 · 壁画 · 考古资料（默认折叠，需时点开）═══
// 数据源：data/translation/article_artifacts/<article_id>.yaml
//   → import_all_to_sqlite.py → SQLite(article_artifacts)
//   → db_reader.load_article_artifacts() → build.py 内嵌 var ARTICLE_ARTIFACTS
//   → renderArticleArtifacts()（仅 status=confirmed 入页；pending/rejected 留库待审）
// 版权与溯源底线：href（原藏品页）必填、source/许可必填、未复核者一律不进页面。
var _AA = null;
function _aaInit() {
  if (_AA !== null) return _AA;
  _AA = (typeof ARTICLE_ARTIFACTS !== 'undefined' && ARTICLE_ARTIFACTS) ? ARTICLE_ARTIFACTS : null;
  return _AA;
}
// 依信度徽章配色沿用 grade-A1…；加图例注记于 summary 行。
var _AA_CAT_ICON = { mural: '🖼', sculpture: '🗿', painting_scroll: '🧻', manuscript: '📜', print: '🪵', architecture: '🏛', relic: '🪔', archaeology: '⛏' };

function renderArticleArtifacts(containerSel) {
  if (!_aaInit()) return 0;
  var items = _AA.items || [];
  if (!items.length) return 0;
  var root = typeof containerSel === 'string' ? document.querySelector(containerSel) : containerSel;
  if (!root) return 0;
  var cat = {};
  items.forEach(function (it) { cat[_AA_CAT_ICON[it.category] || '🏺'] = (cat[_AA_CAT_ICON[it.category] || '🏺'] || 0) + 1; });
  var cats = Object.keys(cat).map(function (k) { return k + cat[k]; }).join(' · ');
  var h = '<details class="fold artifacts-fold" id="article-artifacts-fold">'
    + '<summary>🖼 相关艺术品 · 文物 · 壁画 · 考古（' + items.length + ' 项 · ' + cats + '）<span style="font-weight:400;color:var(--text2)"> · 默认折叠，点开查看</span></summary>'
    + '<div class="fold-body"><div class="artifact-grid">';
  items.forEach(function (it) {
    var g = it.grade || 'C';
    h += '<div class="artifact-card" data-grade="' + g + '">';
    if (it.thumb) h += '<a href="' + _escHtml(it.href) + '" target="_blank" rel="noopener"><img class="ac-thumb" loading="lazy" src="' + _escHtml(it.thumb) + '" alt="' + _escHtml(it.title) + '"></a>';
    h += '<div class="ac-title">' + _escHtml(it.title)
      + ' <span class="grade-badge grade-' + g + '" style="margin-left:4px">' + g + '</span></div>';
    if (it.title_en) h += '<div class="ac-en en-line">' + _escHtml(it.title_en) + '</div>';
    var meta = [];
    if (it.era) meta.push(_escHtml(it.era));
    if (it.location) meta.push(_escHtml(it.location));
    if (it.category) meta.push(_escHtml(it.category));
    if (meta.length) h += '<div class="ac-meta">' + meta.join(' · ') + '</div>';
    if (it.relevance) h += '<div class="ac-relevance">🔗 ' + _mdInline(it.relevance) + '</div>';
    if (it.relevance_en) h += '<div class="en-line">' + _mdInline(it.relevance_en) + '</div>';
    h += '<div class="ac-foot">';
    h += '<div>📖 出处：' + _mdInline(it.source) + '</div>';
    h += '<div>© 许可：' + _escHtml(it.license) + '</div>';
    if (it.note) h += '<div>⚠️ ' + _escHtml(it.note) + '</div>';
    h += '<div><a href="' + _escHtml(it.href) + '" target="_blank" rel="noopener">查看原始藏品页 ↗</a></div>';
    h += '</div></div>';
  });
  h += '</div></div></details>';
  root.insertAdjacentHTML('beforeend', h);
  var n = items.length;
  _aaGather();
  return n;
}

// 预留钩子：如需对卡片内文本做统一语言开关/术语标注在此展开。
function _aaGather() { }

// ═══════════════════════════════════════════════════════════════
// 会众名号数据剖面（EDA）· articles/shizhu-miaoyan.html
// 数据源：build.py 自 SQLite 内嵌 ARTICLE_EDA（词素切分/语义域/群组/网络，编辑性析构）
//        与 ARTICLE_ASSEMBLY（40 类 414 名之经文事实：类名/成员原名/所主/誓愿/数量表达）
// 分源之要：经文事实与编辑析构分居两表，页面须明示二者性质不同——
//        名称与誓愿出经文，词素切分与百分比则为本站析构，非经文所有。
// 本函数不含任何硬编码数据：一切取自 ARTICLE_EDA.payload。
// ═══════════════════════════════════════════════════════════════
var _EDA_DOMCOLOR = {};   // domain key → color（取自 payload.domains，运行时建立）
var _EDA_DOMZH = {};      // domain key → 中文名
var _EDA_DOMEN = {};      // domain key → 英文名
var _EDA_GRPZH = {};      // group key → 中文名
var _EDA_M = null;

function _edaInit() {
  if (typeof ARTICLE_EDA === 'undefined' || !ARTICLE_EDA || !ARTICLE_EDA.payload) return 0;
  var p = ARTICLE_EDA.payload;
  _EDA_M = ARTICLE_EDA.metrics || p.metrics || {};
  (p.domains || []).forEach(function (d) {
    _EDA_DOMCOLOR[d.key] = d.color || '#888';
    _EDA_DOMZH[d.key] = d.zh || d.key;
    _EDA_DOMEN[d.key] = d.en || '';
  });
  (p.groups || []).forEach(function (g) { _EDA_GRPZH[g.key] = g.zh || g.key; });
  return 1;
}

// 词素徽标（着色 + 判读置信度）
function _edaMorph(zh, domain, conf) {
  var col = _EDA_DOMCOLOR[domain] || '#888';
  var op = conf === 'high' ? 1 : (conf === 'medium' ? 0.72 : 0.5);
  var t = '<span class="eda-morph" style="background:' + col + op
    + ';border-color:' + col + '" title="' + _escHtml(_EDA_DOMZH[domain] || domain || '')
    + (conf && conf !== 'high' ? '（判读：' + (conf === 'medium' ? '中' : '待考') + '）' : '')
    + '">' + _escHtml(zh) + '</span>';
  return t;
}

// 数值格
function _edaStat(label, val, sub) {
  return '<div class="eda-stat"><div class="eda-stat-v">' + val + '</div>'
    + '<div class="eda-stat-l">' + label + '</div>'
    + (sub ? '<div class="eda-stat-s">' + sub + '</div>' : '') + '</div>';
}

function _edaBar(pct, color) {
  var w = Math.max(0, Math.min(100, pct || 0));
  return '<span class="eda-bar"><i style="width:' + w.toFixed(1) + '%;background:'
    + (color || 'var(--gold)') + '"></i></span>';
}

function renderArticleEDA(containerSel) {
  if (!_edaInit()) return 0;
  var root = typeof containerSel === 'string' ? document.querySelector(containerSel) : containerSel;
  if (!root) return 0;
  var p = ARTICLE_EDA.payload, m = _EDA_M;
  var asm = (typeof ARTICLE_ASSEMBLY !== 'undefined' && ARTICLE_ASSEMBLY) ? ARTICLE_ASSEMBLY : null;
  var byIdx = {};   // class idx → 经文事实（供逐类节回链类名/成员原名/所主/誓愿）
  if (asm && asm.classes) asm.classes.forEach(function (c) { byIdx[c.idx] = c; });
  // 核名（剥类尾）由「经文原名 − 派生类尾」在渲染时现算，不取自 EDA 投影：
  // EDA 侧刻意不存 core/tail（其分析投影不夹带经文事实字段），故此处于 join 之后推得。
  var tailOf = {};
  var tailOfCat = {};
  (p.class_tails_derived || []).forEach(function (t) {
    tailOf[t.idx] = t.tail || '';
    tailOfCat[t.cat] = t.tail || '';
  });
  function _edaCore(idx, name) {
    var t = tailOf[idx];
    var core = '';
    if (t && name.length > t.length && name.slice(-t.length) === t) {
      core = name.slice(0, name.length - t.length);
    }
    // 剥后与类名全同者（天子／月天子之属）亦无可析之核
    if (core && byIdx[idx] && core === byIdx[idx].cat) core = '';
    return core;
  }
  var h = '';

  h += '<h2>🔬 会众名号 · 数据剖面</h2>';

  // ── 体例声明：编辑性析构 vs 经文事实 ──
  h += '<div class="eda-declare">';
  h += '<div class="eda-declare-t">⚠️ 体例：以下为<b>编辑性析构</b>，非经文原文</div>';
  h += '<div>经文事实（类名、成员原名、所主、誓愿、数量表达）与本站分析（词素切分、语义域归属、'
    + '百分比、群组剖面、网络图）<b>分属两表</b>：前者出《世主妙严品》本文，后者依 '
    + '<code>miaoyan_eda_lexicon.yaml</code> 词素表析构。切分与百分比供比较之用，'
    + '一字一句之义，仍以经文为准。</div>';
  if (p.method) {
    h += '<details class="fold"><summary>📐 切分方法与限度（点开查看）</summary><div class="fold-body">';
    h += '<table class="eda-tbl"><tbody>';
    ['segmentation', 'segmentation_alt', 'domain_assignment', 'class_tail',
      'n_named_caveat', 'caveat'].forEach(function (k) {
        if (p.method[k]) h += '<tr><th style="width:170px">' + k + '</th><td>' + _mdInline(p.method[k]) + '</td></tr>';
      });
    h += '</tbody></table></div></details>';
  }
  h += '<div style="font-size:0.74em;color:var(--text2);margin-top:6px">生成：<code>'
    + _escHtml(p.generated_by || '') + '</code> · 源：<code>' + _escHtml(p.source || '') + '</code></div>';
  h += '</div>';

  // ── 指标总览 ──
  h += '<h3>📊 指标总览</h3><div class="eda-stats">';
  h += _edaStat('类', m.classes || 0, 'classes');
  h += _edaStat('明列名号', m.named_total || 0, 'named');
  h += _edaStat('词素位', m.tokens_total || 0, 'tokens');
  h += _edaStat('不同词素', m.distinct_tokens || 0, 'distinct');
  h += _edaStat('覆盖率', (m.coverage_pct || 0) + '%', 'coverage');
  h += _edaStat('待补字次', m.unsegmented_chars || 0, 'unsegmented');
  h += _edaStat('多字词', m.word_hits || 0, 'words');
  h += _edaStat('判读存疑', m.medconf_hits + m.lowconf_hits, 'medlow');
  h += _edaStat('低置信位', m.lowconf_hits || 0, 'lowconf');
  h += _edaStat('待归域积压', m.unassigned_backlog_segs || 0, 'backlog');
  h += '</div>';
  h += '<div style="font-size:0.76em;color:var(--text2);margin:6px 0 14px">'
    + '覆盖率 100% 仅表示每个字皆已收入词素表，<b>不等于语义皆已核定</b>——'
    + '词素位 <code>c</code> 分三级：high ' + (m.tokens_total - m.medconf_hits - m.lowconf_hits)
    + '、medium ' + (m.medconf_hits || 0) + '、low ' + (m.lowconf_hits || 0) + '。'
    + '<b>仅 low 者前端须显示〔待考〕</b>；「判读存疑」为 medium 与 low 之合计，'
    + '供群间比较之需，二者口径不同，勿相混。涉存疑位之比较结论宜从缓。</div>'
    + '<div style="font-size:0.76em;color:var(--text2);margin:0 0 14px">'
    + '<b>「未定域」不等于「待办」</b>——未定域共 <b>' + (m.unassigned_segs || 0) + '</b> 段，须分三类读：'
    + '<b>①专名／音译 ' + (m.unassigned_lexeme_segs || 0) + ' 段</b>（已注册为多字词，注册目的正是阻止逐字强析，'
    + '强行归域反属臆造）；<b>②不可归域 ' + (m.unassigned_unresolved_glyph_segs || 0) + ' 段</b>'
    + '（底本罕字，字义不可判读，已考订而止步）；'
    + '<b>③待归域 ' + (m.unassigned_backlog_segs || 0) + ' 段</b>——唯③方可推进，本批已归零。'
    + '三类皆<b>不得</b>为凑「未定→0」而强并。</div>';

  // ── 群组纵深（5 群剖面）──
  var gps = p.group_profiles || [];
  if (gps.length) {
    h += '<h3>👥 群组纵深 · 五群剖面</h3>';
    h += '<div class="eda-note" style="font-size:0.78em;color:var(--text2);margin-bottom:8px">'
      + '各群之量（名数/类数/词素/判读）皆由脚本实算；群之一句定位与判读出 '
      + '<code>miaoyan_eda_lexicon.yaml ▸ group_profiles</code>，页面不另生数据。</div>';
    gps.forEach(function (g) {
      h += '<div class="eda-gp">';
      h += '<div class="eda-gp-h"><b>' + _escHtml(g.zh) + '</b>'
        + '<span class="en-line"> · ' + _escHtml(g.en || '') + '</span>'
        + '<span class="eda-gp-n">' + g.n_named + ' 名／' + g.n_classes + ' 类／'
        + g.n_tokens + ' 词素位</span></div>';
      if (g.character) h += '<div class="eda-gp-c">' + _mdInline(g.character) + '</div>';
      h += '<div class="eda-gp-m">核名均值 ' + g.core_len_mean + '（' + g.core_len_min + '–'
        + g.core_len_max + ' 字）· 词素 ' + g.n_distinct_morph + ' · 多字词 ' + g.n_word_hits
        + ' · 判读存疑 ' + (g.n_medconf + g.n_lowconf) + '（'
        + (Math.round((g.medconf_pct + g.lowconf_pct) * 10) / 10) + '%）'
        + ' · low ' + g.n_lowconf + '</div>';
      // 语义域分布
      h += '<div class="eda-doms">';
      (g.domains || []).slice(0, 8).forEach(function (d) {
        h += '<div class="eda-dom"><span class="eda-dom-k" style="color:'
          + (_EDA_DOMCOLOR[d.domain] || '#888') + '">' + _escHtml(d.domain_zh || d.domain)
          + '</span>' + _edaBar(d.pct, _EDA_DOMCOLOR[d.domain])
          + '<span class="eda-dom-v">' + d.n + '／' + d.pct + '%</span></div>';
      });
      h += '</div>';
      // 高频词素 + 冠字/尾字
      h += '<div class="eda-line"><b>高频词素</b>：' + (g.top_morphs || []).slice(0, 12)
        .map(function (x) { return _edaMorph(x.zh, x.domain, x.c); }).join(' ') + '</div>';
      if ((g.top_heads || []).length) h += '<div class="eda-line"><b>冠字</b>：'
        + g.top_heads.slice(0, 10).map(function (x) { return _escHtml(x.zh) + '×' + x.n; }).join(' · ') + '</div>';
      if ((g.exclusive_morphs || []).length) h += '<div class="eda-line"><b>本群特有</b>：'
        + g.exclusive_morphs.map(function (x) { return _edaMorph(x.zh, x.domain, x.c) + '<span style="opacity:.6">×' + x.n + '</span>'; }).join(' ')
        + '</div>';
      else h += '<div class="eda-line" style="color:var(--text2)"><b>本群特有</b>：（无）'
        + '——其词素全部见于他群，与他群共用同一语料池。</div>';
      if ((g.class_tails || []).length) h += '<div class="eda-line"><b>类尾</b>：'
        + g.class_tails.map(function (t) { return '<code>' + _escHtml(t) + '</code>'; }).join('、') + '</div>';
      if (g.note) h += '<div class="eda-gp-n2">' + _mdInline(g.note) + '</div>';
      if (g.note_en) h += '<div class="eda-gp-n2 en-line">' + _mdInline(g.note_en) + '</div>';
      h += '</div>';
    });

    // 群间对比
    var prs = p.group_pairs || [];
    if (prs.length) {
      h += '<h4>🔀 群间对比（十对）</h4>';
      h += '<div class="scroll-x"><table class="eda-tbl"><thead><tr><th>群 A</th><th>群 B</th>'
        + '<th>共有词素</th><th>Jaccard</th><th>域分布距离</th><th>共有高频词素</th></tr></thead><tbody>';
      prs.forEach(function (q) {
        h += '<tr><td>' + _escHtml(q.a_zh) + '</td><td>' + _escHtml(q.b_zh) + '</td>'
          + '<td style="text-align:right">' + q.shared + '</td>'
          + '<td style="text-align:right">' + q.jaccard + '</td>'
          + '<td style="text-align:right">' + q.domain_dist + '%</td>'
          + '<td>' + (q.top_shared || []).slice(0, 6).map(function (x) {
            return _escHtml(x.zh) + '<span style="opacity:.55">(' + x.n_a + '/' + x.n_b + ')</span>';
          }).join(' ') + '</td></tr>';
      });
      h += '</tbody></table></div>';
    }
  }

  // ── 群 × 语义域 热力矩阵 ──
  var heat = p.heat_matrix || [];
  if (heat.length) {
    h += '<h3>🌡 群 × 语义域 · 热力矩阵</h3>';
    h += '<div style="font-size:0.76em;color:var(--text2);margin-bottom:6px">'
      + '格内为该群之词素位落于该域之百分比（分母为该群词素位数，故各行合计≈100%）。</div>';
    h += '<div class="scroll-x"><table class="eda-tbl eda-heat"><thead><tr><th>群＼域</th>';
    var doms = (heat[0].cells || []).map(function (c) { return c; });
    doms.forEach(function (c) {
      h += '<th style="color:' + (_EDA_DOMCOLOR[c.domain] || '#888') + '">' + _escHtml(c.domain_zh) + '</th>';
    });
    h += '</tr></thead><tbody>';
    heat.forEach(function (row) {
      h += '<tr><th style="text-align:left;white-space:nowrap">' + _escHtml(row.group_zh) + '</th>';
      (row.cells || []).forEach(function (c) {
        var col = _EDA_DOMCOLOR[c.domain] || '#888';
        var a = c.n ? Math.min(0.55, 0.06 + c.pct / 40) : 0;
        h += '<td style="text-align:center;background:' + col + a + '">' + (c.n ? c.pct : '·') + '</td>';
      });
      h += '</tr>';
    });
    h += '</tbody></table></div>';
    h += '<div style="font-size:0.74em;color:var(--text2);margin-top:4px">'
      + '（格内数字为百分比；空白「·」表示该群无词素落此域。着色深浅随占比。）</div>';
  }

  // ── 高频词素 × 群 矩阵 ──
  var mm = p.morph_matrix || [];
  if (mm.length) {
    h += '<h3>🧬 高频词素 × 群（前 ' + mm.length + '）</h3>';
    h += '<div class="scroll-x"><table class="eda-tbl"><thead><tr><th>词素</th><th>域</th>';
    (p.groups || []).forEach(function (g) { h += '<th>' + _escHtml(g.zh) + '</th>'; });
    h += '<th>合计</th></tr></thead><tbody>';
    mm.forEach(function (x) {
      h += '<tr><td>' + _edaMorph(x.zh, x.domain, x.c) + '</td><td style="color:'
        + (_EDA_DOMCOLOR[x.domain] || '#888') + ';font-size:.86em">' + _escHtml(x.domain_zh || '') + '</td>';
      (p.groups || []).forEach(function (g) {
        var v = (x.by_group || {})[g.key] || 0;
        h += '<td style="text-align:right' + (v ? ';color:var(--gold);font-weight:600' : ';opacity:.28') + '">'
          + (v || '·') + '</td>';
      });
      h += '<td style="text-align:right;font-weight:600">' + x.total + '</td></tr>';
    });
    h += '</tbody></table></div>';
  }

  // ── 逐类：经文事实 × 词素切分（此节是「分源」之要：左经文、右析构）──
  var ecs = p.eda_classes || [];
  if (ecs.length) {
    h += '<h3>📚 逐类详解 · 经文事实 × 词素切分</h3>';
      h += '<div style="font-size:0.76em;color:var(--text2);margin-bottom:8px">'
      + '每类一节：上为经文所载（类名、所主、誓愿、明列名号），下为本站切分（每名之核名与词素序列）。'
      + '两者并列而不相混。核名 <b>∅</b> 者有二：一为剥除类尾后与类名全同者（<code>日天子</code>／<code>月天子</code> 之属）；'
      + '一为经文原名带省文记号（<code>……</code>，CBETA 原卷如此）而尾字不全者。'
      + '二者皆无可析之核，其词素序列即全名。</div>';
    ecs.forEach(function (ec) {
      var f = byIdx[ec.idx] || {};
      var open = (ec.idx === 0);
      h += '<details class="fold eda-cls"' + (open ? ' open' : '') + '>';
      h += '<summary>🧩 ' + _escHtml(f.cat || ec.cat)
        + '<span style="font-weight:400;color:var(--text2)"> · ' + _escHtml(f.group_zh || _EDA_GRPZH[ec.group] || '')
        + ' · ' + (f.n_named || 0) + ' 名 · 核名 ' + ec.n_char_total + ' 字'
        + (ec.n_word_hits ? ' · 多字词 ' + ec.n_word_hits : '')
        + (ec.n_unsegmented ? ' · <span style="color:var(--red)">待补 ' + ec.n_unsegmented + '</span>' : '')
        + '</span></summary>';
      h += '<div class="fold-body">';
      // 经文事实
      h += '<div class="eda-src"><b>经文</b>';
      var facts = [];
      if (f.domain) facts.push('所主：' + _escHtml(f.domain));
      if (f.realm) facts.push('界：' + _escHtml(f.realm));
      if (f.count_expr) facts.push('数量：<code>' + _escHtml(f.count_expr) + '</code>');
      if (f.collective) facts.push('总称：' + _escHtml(f.collective));
      if (f.leader) facts.push('上首：' + _escHtml(f.leader));
      if (facts.length) h += '<div>' + facts.join(' · ') + '</div>';
      if (f.vow) h += '<div class="eda-vow">誓愿：' + _mdInline(f.vow) + '</div>';
      if (f.source) h += '<div style="font-size:.76em;color:var(--text2)">出处：' + _mdInline(f.source) + '</div>';
      h += '</div>';
      // 逐名切分
      h += '<table class="eda-tbl eda-seg"><thead><tr><th style="width:44px">#</th><th>经文名号</th>'
        + '<th>核名（剥类尾）</th><th>词素序列</th></tr></thead><tbody>';
      (ec.members || []).forEach(function (mm2) {
        var a2 = (f.members || []).filter(function (x) { return x.i === mm2.i; })[0] || {};
          h += '<tr><td style="text-align:right;opacity:.5">' + mm2.i + '</td>'
          + '<td style="white-space:nowrap">' + _escHtml(a2.name || '') + (a2.is_leader ? ' <span class="eda-lead">上首</span>' : '') + '</td>'
          + '<td style="color:var(--gold);white-space:nowrap">' + _escHtml(_edaCore(ec.idx, a2.name || '') || '∅') + '</td>'
          + '<td>' + (mm2.segs || []).map(function (s) {
            return _edaMorph(s.zh, s.domain, s.c);
          }).join('') + '</td></tr>';
      });
      h += '</tbody></table>';
      h += '</div></details>';
    });
  }

  // ── 共现网络（词素—词素 二部网络之投影 + 类—词素 二部图）──
  var g = p.graph || {};
  if ((g.lex_nodes || []).length) {
    h += '<h3>🕸 词素共现网络</h3>';
    h += '<div style="font-size:0.76em;color:var(--text2);margin-bottom:8px">'
      + '节点为词素（按域着色，边宽为共现次数），连线示同一名号内二词素相邻之频。'
      + '共 ' + (g.lex_nodes || []).length + ' 节点／' + (g.lex_edges || []).length + ' 边；'
      + '另有类—词素二部边 ' + (g.bipartite_edges || []).length + ' 条（逐名归类，见逐类节）。</div>';
    h += '<details class="fold"><summary>🕸 展开网络（' + (g.lex_edges || []).length + ' 条共现边）</summary><div class="fold-body">';
    h += '<div class="scroll-x"><table class="eda-tbl"><thead><tr><th>词素 A</th><th>词素 B</th><th>共现</th><th>合成词</th></tr></thead><tbody>';
    (g.lex_edges || []).slice(0, 120).forEach(function (e) {
      var pair = e.source.replace('m:', '') + e.target.replace('m:', '');
      var word = (p.word_hits || []).filter(function (w) { return w.zh === pair; })[0];
      h += '<tr><td>' + _escHtml(e.source.replace('m:', '')) + '</td><td>'
        + _escHtml(e.target.replace('m:', '')) + '</td><td style="text-align:right">' + e.n + '</td>'
        + '<td style="font-size:.82em;color:var(--text2)">' + (word ? _escHtml(word.gloss || '') : '（未收为多字词）') + '</td></tr>';
    });
    h += '</tbody></table></div></details>';
  }

  // ── 多字词 / 固定搭配 ──
  if ((p.word_hits || []).length) {
    h += '<h3>🔗 多字词与固定搭配</h3><div class="eda-line">';
    h += p.word_hits.map(function (w) { return _edaMorph(w.zh, w.domain, w.c) + '<span style="opacity:.6">×' + w.n + '</span>'; }).join(' ');
    h += '</div>';
  }

  // ── 跨类重名（同一核名分属多类）──
  if ((p.core_duplicates || []).length) {
    h += '<h3>🔁 跨类重名（同一核名分属多类）</h3>';
    h += '<div style="font-size:.76em;color:var(--text2);margin-bottom:6px">'
      + '剥类尾后核名相同而类名不同者——示名号之 epithet 语料跨类共用。</div><table class="eda-tbl"><thead><tr><th>核名</th><th>类</th></tr></thead><tbody>';
    (p.core_duplicates || []).forEach(function (d) {
      h += '<tr><td style="color:var(--gold);white-space:nowrap">' + _escHtml(d.core) + '</td><td>'
        + d.classes.map(function (c) { return _escHtml(c); }).join('、') + '</td></tr>';
    });
    h += '</tbody></table>';
  }

  // ── 跨类同赞词（剥「主X」所主槽后；整核比较测不到者）──
  var eps = p.epithet_sharing;
  if (eps && (eps.groups || []).length) {
    h += '<h3>🏷️ 跨类同赞词（剥所主槽后）</h3>';
    if (eps.note) h += '<div class="eda-line" style="margin-bottom:6px">' + _mdInline(eps.note) + '</div>';
    if (eps.note_en) h += '<div class="eda-line en-line" style="margin-bottom:6px">' + _mdInline(eps.note_en) + '</div>';
    h += '<div style="font-size:.76em;color:var(--text2);margin-bottom:6px">'
      + '可析 ' + (eps.n_members_parsed || 0) + ' 名（十九类神 150 名），跨类共用 <b>'
      + (eps.groups || []).length + '</b> 组。</div>'
      + '<div class="scroll-x"><table class="eda-tbl"><thead><tr><th>赞词</th><th>名数</th><th>所主槽（分属各类）</th></tr></thead><tbody>';
    (eps.groups || []).forEach(function (g) {
      h += '<tr><td style="color:var(--gold);white-space:nowrap">' + _escHtml(g.epithet) + '</td>'
        + '<td style="text-align:right">' + g.n + '</td><td>'
        + (g.members || []).map(function (m) {
            // 成员原名属经文事实，只在 assembly 一处；此处由赞词＋所主槽＋类尾现拼
            var tn = tailOfCat[m.cat] || '';
            return _escHtml(g.epithet) + '主' + _escHtml(m.domain) + _escHtml(tn)
              + '<span class="eda-dim">（' + _escHtml(m.cat) + '）</span>';
          }).join('、')
        + '</td></tr>';
    });
    h += '</tbody></table></div>';
  }
  // ── 主X神 句式 ──
  if (p.zhu_formula && (p.zhu_formula.classes || []).length) {
    var z = p.zhu_formula;
    h += '<h3>🧩 「主X神」句式</h3>';
    if (z.note) h += '<div class="eda-line" style="margin-bottom:8px">' + _mdInline(z.note) + '</div>';
    if (z.note_en) h += '<div class="eda-line en-line" style="margin-bottom:8px">' + _mdInline(z.note_en) + '</div>';
    h += '<div class="scroll-x"><table class="eda-tbl"><thead><tr><th>类</th><th>明列</th><th>合句式</th><th>比率</th></tr></thead><tbody>';
    (z.classes || []).forEach(function (c) {
      h += '<tr><td>' + _escHtml(c.cat) + '</td><td style="text-align:right">' + c.n_named
        + '</td><td style="text-align:right">' + c.n_formula + '</td><td>' + c.pct + '%</td></tr>';
    });
    h += '</tbody></table></div>';
  }

  // ── 异体字 / 判读词素 ──
  if ((p.glyph_variants || []).length) {
    h += '<h3>🔠 异体字对照</h3><table class="eda-tbl"><thead><tr><th>CBETA 字形</th><th>通行字形</th><th>本篇用次</th></tr></thead><tbody>';
    (p.glyph_variants || []).forEach(function (v) {
      h += '<tr><td>' + _escHtml(v.cbeta) + '</td><td>' + _escHtml(v.common) + '</td><td style="text-align:right">'
        + v.n_cbeta + '</td></tr>';
    });
    h += '</tbody></table>';
  }

  // ── 词素表待考 ──
  if ((p.unsegmented || []).length) {
    h += '<h3>❓ 待补判读</h3><table class="eda-tbl"><thead><tr><th>字</th><th>域</th><th>注</th></tr></thead><tbody>';
    (p.unsegmented || []).forEach(function (u) {
      h += '<tr><td>' + _escHtml(u.zh) + '</td><td>' + _escHtml(u.domain || '') + '</td><td style="font-size:.84em">'
        + _escHtml(u.note || '') + '</td></tr>';
    });
    h += '</tbody></table>';
  }
  if ((p.lexicon_notes || []).length) {
    h += '<h3>📝 词素表注记</h3><ul class="eda-ul">';
    (p.lexicon_notes || []).forEach(function (n) { h += '<li>' + _mdInline(n) + '</li>'; });
    h += '</ul>';
  }

  root.insertAdjacentHTML('beforeend', h);
  return 1;
}


function _markTermRefs(rootSel) {
  if (!_agInit()) return 0;
  var root = typeof rootSel === 'string' ? document.querySelector(rootSel) : rootSel;
  if (!root) return 0;
  // 显式标记先于自动扫描：若 [[显示文本|id]] 的显示文本恰是别名（如 [[普贤|…]]），
  // 自动扫描先行会把 [[…]] 拆散成多段文本节点，显式解析将无法跨节点匹配。
  _agExplicit(root);
  var N = _agNames();
  var n = 0;
  var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode: function (node) {
      if (_agSkip(node.parentNode) || !node.nodeValue) return NodeFilter.FILTER_REJECT;
      N.re.lastIndex = 0;
      return N.re.test(node.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
    }
  });
  var texts = [];
  for (var t = walker.nextNode(); t; t = walker.nextNode()) texts.push(t);
  texts.forEach(function (node) {
    var s = node.nodeValue, last = 0, m;
    N.re.lastIndex = 0;
    while ((m = N.re.exec(s)) !== null) {
      if (m.index > last) node.parentNode.insertBefore(document.createTextNode(s.slice(last, m.index)), node);
      var id = N.map[m[0]];
      node.parentNode.insertBefore(_agWrap(m[0], id), node);
      last = m.index + m[0].length;
      n++;
    }
    if (last < s.length) node.parentNode.insertBefore(document.createTextNode(s.slice(last)), node);
    node.parentNode.removeChild(node);
  });
  if (n) _agMount();
  return n;
}

// 显式标记：[[显示文本|term_id]]。必须在自动扫描前处理，理由见 _markTermRefs。
function _agExplicit(root) {
  var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode: function (node) {
      if (_agSkip(node.parentNode) || !node.nodeValue) return NodeFilter.FILTER_REJECT;
      return /\[\[[^\]]+\|[^\]]+\]\]/.test(node.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
    }
  });
  var texts = [];
  for (var t = walker.nextNode(); t; t = walker.nextNode()) texts.push(t);
  texts.forEach(function (node) {
    var s = node.nodeValue;
    if (s.indexOf('[[') < 0) return;
    var frag = document.createDocumentFragment(), last = 0, re = /\[\[([^\]|]+)\|([^\]]+)\]\]/g, m;
    while ((m = re.exec(s)) !== null) {
      if (m.index > last) frag.appendChild(document.createTextNode(s.slice(last, m.index)));
      if (_AGi[m[2]]) frag.appendChild(_agWrap(m[1], m[2]));
      else frag.appendChild(document.createTextNode(m[0]));
      last = m.index + m[0].length;
    }
    if (last < s.length) frag.appendChild(document.createTextNode(s.slice(last)));
    node.parentNode.replaceChild(frag, node);
  });
}

function _agMount() {
  if (document.getElementById('term-modal')) return;
  var d = document.createElement('div');
  d.className = 'term-modal';
  d.id = 'term-modal';
  d.innerHTML = '<div class="tm-box" role="dialog" aria-modal="true">'
    + '<div class="tm-head"><h3 id="tm-title"></h3>'
    + '<button class="tm-close" type="button" aria-label="关闭">✕</button></div>'
    + '<div class="tm-body" id="tm-body"></div></div>';
  document.body.appendChild(d);
  d.addEventListener('click', function (e) { if (e.target === d) closeTermModal(); });
  d.querySelector('.tm-close').addEventListener('click', closeTermModal);
  var tip = document.createElement('div');
  tip.className = 'term-tip';
  tip.id = 'term-tip';
  document.body.appendChild(tip);
}

function openTermModal(id, anchorEl) {
  if (!_agInit()) return;
  var t = _AGi[id];
  if (!t) return;
  _agMount();
  var gradeCls = 'grade-' + (t.grade || 'C');
  var h = '<div class="tm-meta">'
    + '<span class="grade-badge ' + gradeCls + '">' + _escHtml(t.grade) + '</span>'
    + '<span>' + _escHtml(t.status) + '</span>'
    + '<span>' + _escHtml(t.category) + '</span>';
  if (t.aliases && t.aliases.length) h += '<span>别称：' + _escHtml(t.aliases.join('、')) + '</span>';
  h += '</div>';
  h += '<div class="en-line">📖 ' + _mdInline(t.def_en || '') + '</div>';
  if (t.source) {
    h += '<div class="tm-src">出处：' + _mdInline(t.source)
      + (t.source_url ? ' <a href="' + _escHtml(t.source_url) + '" target="_blank" rel="noopener">回查</a>' : '') + '</div>';
  }
  if (t.note) h += '<div class="tm-src">注记：' + _mdInline(t.note) + '</div>';

  var rel = (t.out || []).map(function (o) {
    var clickable = (o.to_type === 'term')
      ? ' data-term-id="' + _escHtml(o.to_ref) + '" style="cursor:pointer" title="查看该节点"'
      : '';
    return '<span class="rel-chip"' + clickable + '><b>' + _escHtml(o.rel) + '</b> ' + _escHtml(o.to_label) + '</span>';
  }).join('');
  if (rel) h += '<div class="tm-rel"><span style="font-size:0.82em;color:var(--text2)">关联 →</span>' + rel + '</div>';

  document.getElementById('tm-title').textContent = t.zh;
  document.getElementById('tm-body').innerHTML = h;
  document.getElementById('term-modal').classList.add('is-open');
  _agTip(anchorEl, t);
  if (window._markEnBlocks) try { window._markEnBlocks(); } catch (e) {}
}

function closeTermModal() {
  var m = document.getElementById('term-modal');
  if (m) m.classList.remove('is-open');
  var tip = document.getElementById('term-tip');
  if (tip) tip.classList.remove('is-on');
}

function _agTip(anchorEl, t) {
  var tip = document.getElementById('term-tip');
  if (!tip || !anchorEl) return;
  tip.innerHTML = '<b>' + _escHtml(t.zh) + '</b><div class="tt-def">' + _escHtml((t.def_zh || t.def_en || '').slice(0, 110)) + '</div>';
  var r = anchorEl.getBoundingClientRect();
  tip.classList.add('is-on');
  var top = r.bottom + 8 + window.scrollY;
  if (top + 100 > document.documentElement.scrollHeight) top = r.top + 8 + window.scrollY;
  tip.style.top = top + 'px';
  tip.style.left = Math.max(8, Math.min(r.left + window.scrollX, window.innerWidth - 320)) + 'px';
}

// ═══ 正文配图：缩略图 + 点击看原图 ═══
// 需求：文中图片原本可达 720px 宽，喧宾夺主且挤占版面，故一律以缩略图呈现，
// 点击后于灯箱中显示原图，并附「在新标签页打开」以便自行缩放/存档。
// 尺寸与外观全由 CSS 决定（杜绝硬编码），本层只负责行为：
//   ① 扫出正文配图并挂 .doc-img（文物卡 .ac-thumb 等自带尺寸者不在此列）
//   ② 原图地址：优先取作者显式给的 data-full；否则按 Wikimedia 缩略图路径还原原图
//   ③ 灯箱：点图开启，✕／点击遮罩／Esc 皆可关闭
function _imgFullUrl(src) {
  if (!src) return '';
  // upload.wikimedia.org/wikipedia/commons/thumb/a/ab/NAME.jpg/960px-NAME.jpg
  //   → .../wikipedia/commons/a/ab/NAME.jpg
  var m = /^(https?:\/\/upload\.wikimedia\.org\/.+?)\/thumb\/(.+?)\/\d+px-([^/]+)$/.exec(src);
  if (m) return m[1] + '/' + m[2] + '/' + m[3];
  return src;   // 非缩略图链接（如本地/直链）：原图即其本身
}

function initDocImages(rootSel) {
  var root = typeof rootSel === 'string' ? document.querySelector(rootSel) : rootSel;
  if (!root) return 0;
  var imgs = root.querySelectorAll('img');
  var n = 0;
  Array.prototype.forEach.call(imgs, function (im) {
    if (im.closest && im.closest('.artifact-card, .ac-thumb, .figure-fold')) return;  // 文物卡等自有版式
    if (im.dataset.imgInit) return;
    im.dataset.imgInit = '1';
    im.classList.add('doc-img');
    if (!im.dataset.full) im.dataset.full = _imgFullUrl(im.getAttribute('src'));
    im.setAttribute('role', 'button');
    im.setAttribute('tabindex', '0');
    im.title = '点击看原图';
    n++;
  });
  return n;
}

function openImageLightbox(src, alt) {
  if (!src) return;
  var lb = document.getElementById('img-lightbox');
  if (!lb) {
    lb = document.createElement('div');
    lb.className = 'img-lightbox';
    lb.id = 'img-lightbox';
    lb.innerHTML = '<button class="lb-close" type="button" aria-label="关闭">✕</button>'
      + '<figure class="lb-fig"><img id="lb-img" alt=""><figcaption id="lb-cap"></figcaption></figure>';
    document.body.appendChild(lb);
    lb.addEventListener('click', function (e) {
      // 点遮罩或 ✕ 关闭；点图/说明文字本身不关（便于看图）
      if (e.target === lb || e.target.classList.contains('lb-close')
          || e.target.classList.contains('lb-fig')) closeImageLightbox();
    });
    lb.querySelector('.lb-close').addEventListener('click', closeImageLightbox);
  }
  lb.querySelector('#lb-img').src = src;
  lb.querySelector('#lb-img').alt = alt || '';
  var cap = lb.querySelector('#lb-cap');
  cap.innerHTML = (alt ? _escHtml(alt) + ' · ' : '')
    + '<a href="' + _escHtml(src) + '" target="_blank" rel="noopener">在新标签页打开原图 ↗</a>';
  lb.classList.add('is-on');
  document.body.style.overflow = 'hidden';
}

function closeImageLightbox() {
  var lb = document.getElementById('img-lightbox');
  if (lb) lb.classList.remove('is-on');
  document.body.style.overflow = '';
}

(function () {
  document.addEventListener('click', function (e) {
    var im = e.target.closest && e.target.closest('img.doc-img');
    if (im) { e.preventDefault(); openImageLightbox(im.dataset.full || im.getAttribute('src'), im.alt); return; }
    if (e.key === 'Escape') { /* 见 keydown */ }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && e.target.tagName === 'IMG' && e.target.classList.contains('doc-img')) {
      e.preventDefault();
      openImageLightbox(e.target.dataset.full || e.target.getAttribute('src'), e.target.alt);
    }
    if (e.key === 'Escape') closeImageLightbox();
  });
})();

// ═══ 实体百科 · 众/菩萨/金刚神/龙/八部/诸神/佛 ═══
// 数据源：data/encyclopedia/beings.yaml
//   → import_all_to_sqlite.py → SQLite(entities/entity_claims/entity_relations)
//   → db_reader.load_entity_registry() → build.py 内嵌 var ENTITY_REGISTRY
// 与 ARTICLE_GRAPH（名相·会处，article-scoped）之别：
//   名相层管「法义」（业变力、教轮…）；实体层管「有名有姓之存在」（善化天王、文殊师利…）。
//   二者不重复登记：实体之关系可指向名相（to_type='term'）。
// 断言级信度：实体总 grade 只管名号；小传每条事实之可信度由 claims[].grade 逐条判定，
//   故「名号 A1 而梵名 C」并存不悖——卡内逐条显示徽标与出处，不以总信度掩盖未考之处。
// 泛称禁令：龙/天/王/菩萨 等单字泛称 auto_link=0，永不作自动命中（否则满篇皆蓝）；
//   命中一律取最长名，且经 meta.stoplist 过滤。
var _EN = null;    // ENTITY_REGISTRY
var _ENi = null;   // entity_id -> entity
var _ENnames = null;

function _enInit() {
  if (_EN !== null) return _EN;
  _EN = (typeof ENTITY_REGISTRY !== 'undefined' && ENTITY_REGISTRY) ? ENTITY_REGISTRY : null;
  if (!_EN) return null;
  _ENi = {};
  (_EN.entities || []).forEach(function (e) { _ENi[e.id] = e; });
  return _EN;
}

// 名称 → id 映射（按长度降序比对，故「善化天王众」先于「善化天王」命中）
function _enNames() {
  if (_ENnames !== null) return _ENnames;
  var reg = _enInit();
  if (!reg) return (_ENnames = { re: null, map: {} });
  var stop = {};
  (reg.stoplist || []).forEach(function (s) { stop[s] = 1; });
  var map = {};
  (_EN.entities || []).forEach(function (e) {
    if (e.status === 'rejected' || e.status === 'pending') return;  // 待核/疑讹不作正文命中
    if (!e.auto_link) return;                                        // 泛称或易误命中者显式关闭
    [e.zh].concat(e.aliases || []).forEach(function (n) {
      if (!n || n.length < 2 || stop[n]) return;
      map[n] = e.id;
    });
  });
  var re = Object.keys(map).length ? new RegExp(
    Object.keys(map).sort(function (a, b) { return b.length - a.length; })
      .map(function (n) { return n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); })
      .join('|'), 'g') : null;
  _ENnames = { re: re, map: map };
  return _ENnames;
}

function _enSkip(el) {
  for (var n = el; n && n.nodeType === 1; n = n.parentNode) {
    if (n.tagName === 'SCRIPT' || n.tagName === 'STYLE' || n.tagName === 'TEXTAREA') return true;
    // 已标注者不再重入；名相标注之内也不再插入实体标注（避免两层可点文字互相嵌套）
    if (n.classList && (n.classList.contains('entity-ref') || n.classList.contains('term-ref')
                        || n.classList.contains('term-modal') || n.classList.contains('entity-modal'))) return true;
  }
  return false;
}

function _enWrap(txt, id) {
  var t = _ENi[id];
  var s = document.createElement('span');
  s.className = 'term-ref entity-ref';
  s.dataset.entityId = id;
  s.setAttribute('role', 'button');
  s.tabIndex = 0;
  s.title = t ? ('实体卡：' + t.zh) : '实体卡';
  s.textContent = txt;
  return s;
}

function markEntityRefs(rootSel) {
  var N = _enNames();
  if (!N.re) return 0;
  var root = typeof rootSel === 'string' ? document.querySelector(rootSel) : rootSel;
  if (!root) return 0;
  var n = 0;
  var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode: function (node) {
      if (_enSkip(node.parentNode) || !node.nodeValue) return NodeFilter.FILTER_REJECT;
      N.re.lastIndex = 0;
      return N.re.test(node.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
    }
  });
  var texts = [];
  for (var t = walker.nextNode(); t; t = walker.nextNode()) texts.push(t);
  texts.forEach(function (node) {
    var s = node.nodeValue, last = 0, m;
    N.re.lastIndex = 0;
    while ((m = N.re.exec(s)) !== null) {
      if (m.index > last) node.parentNode.insertBefore(document.createTextNode(s.slice(last, m.index)), node);
      node.parentNode.insertBefore(_enWrap(m[0], N.map[m[0]]), node);
      last = m.index + m[0].length;
      n++;
    }
    if (last < s.length) node.parentNode.insertBefore(document.createTextNode(s.slice(last)), node);
    node.parentNode.removeChild(node);
  });
  return n;
}

function _enMount() {
  if (document.getElementById('entity-modal')) return;
  var d = document.createElement('div');
  d.className = 'term-modal entity-modal';
  d.id = 'entity-modal';
  // 结构与名相弹窗同构，复用既有样式；id 独立以免二者互相关闭
  d.innerHTML = '<div class="tm-box" role="dialog" aria-modal="true">'
    + '<div class="tm-head"><h3 id="em-title"></h3>'
    + '<button class="tm-close" type="button" aria-label="关闭">✕</button></div>'
    + '<div class="tm-body" id="em-body"></div></div>';
  document.body.appendChild(d);
  d.addEventListener('click', function (e) { if (e.target === d) closeEntityCard(); });
  d.querySelector('.tm-close').addEventListener('click', closeEntityCard);
}

function openEntityCard(id, anchorEl) {
  if (!_enInit()) return;
  var e = _ENi[id];
  if (!e) return;
  _enMount();
  var g = e.grade || 'C';
  var cnt = {};
  (e.claims || []).forEach(function (c) { cnt[c.grade] = (cnt[c.grade] || 0) + 1; });
  var h = '<div class="tm-meta">'
    + '<span class="grade-badge grade-' + g + '">' + _escHtml(g) + '</span>'
    + '<span>' + _escHtml(e.category || '') + '</span>'
    + (e.status && e.status !== 'used' ? '<span>' + _escHtml(e.status) + '</span>' : '')
    + (e.aliases && e.aliases.length ? '<span>别称：' + _escHtml(e.aliases.join('、')) + '</span>' : '')
    + '</div>';
  if (e.name_full) h += '<div class="tm-src">全称：' + _mdInline(e.name_full) + '</div>';
  if (e.name_sa) h += '<div class="tm-src">梵名：<i>' + _escHtml(e.name_sa) + '</i></div>';
  if (e.bio_zh) h += '<div>' + _mdInline(e.bio) + '</div>';
  if (e.bio_en) h += '<div class="en-line">📖 ' + _mdInline(e.bio_en) + '</div>';

  // 逐条考据：每条自带信度与出处，未考者如实见其徽标
  if ((e.claims || []).length) {
    var dist = ['A1', 'A2', 'B', 'C', 'D'].filter(function (k) { return cnt[k]; })
      .map(function (k) { return '<span class="grade-badge grade-' + k + '">' + k + ' ' + cnt[k] + '</span>'; }).join(' ');
    h += '<div style="margin-top:10px"><div style="font-size:0.86em;color:var(--gold);margin-bottom:4px">'
      + '考据 ' + (e.claims || []).length + ' 条 · ' + dist + '</div><ul class="en-claims">';
    e.claims.forEach(function (c) {
      h += '<li><span class="grade-badge grade-' + (c.grade || 'C') + '">' + _escHtml(c.grade || 'C') + '</span> '
        + _mdInline(c.text || '');
      if (c.source) h += ' <span class="tm-src">〔' + _mdInline(c.source) + '〕</span>';
      if (c.note) h += ' <span class="tm-src">注：' + _mdInline(c.note) + '</span>';
      h += '</li>';
    });
    h += '</ul></div>';
  }
  if (e.source) {
    h += '<div class="tm-src">出处：' + _mdInline(e.source)
      + (e.source_url ? ' <a href="' + _escHtml(e.source_url) + '" target="_blank" rel="noopener">回查</a>' : '') + '</div>';
  }
  if (e.note) h += '<div class="tm-src">注记：' + _mdInline(e.note) + '</div>';

  var rel = (e.out || []).map(function (o) {
    var clickable = (o.to_type === 'entity' && _ENi[o.to_ref])
      ? ' data-entity-id="' + _escHtml(o.to_ref) + '" style="cursor:pointer" title="查看该实体"'
      : (o.to_type === 'term' && typeof openTermModal === 'function'
         ? ' data-term-id="' + _escHtml(o.to_ref) + '" style="cursor:pointer" title="查看该名相"' : '');
    return '<span class="rel-chip"' + clickable + '><b>' + _escHtml(o.rel) + '</b> '
      + _escHtml(o.to_label || o.to_ref) + '</span>';
  }).join('');
  if (rel) h += '<div class="tm-rel"><span style="font-size:0.82em;color:var(--text2)">关联 →</span>' + rel + '</div>';

  document.getElementById('em-title').textContent = e.zh;
  document.getElementById('em-body').innerHTML = h;
  document.getElementById('entity-modal').classList.add('is-open');
  if (window._markEnBlocks) try { window._markEnBlocks(); } catch (err) {}
  // 二层互斥：实体卡与名相窗不并立，免得叠窗遮读
  if (typeof closeTermModal === 'function') closeTermModal();
}

function closeEntityCard() {
  var m = document.getElementById('entity-modal');
  if (m) m.classList.remove('is-open');
}

(function () {
  // 实体点击 / 关联节点跳转 → 开卡；点击卡外或 Esc → 关闭
  document.addEventListener('click', function (e) {
    var ref = e.target.closest && e.target.closest('[data-entity-id]');
    if (ref && ref.dataset.entityId) { e.stopPropagation(); openEntityCard(ref.dataset.entityId, ref); return; }
    if (!(e.target.closest && e.target.closest('.entity-modal'))) closeEntityCard();
  }, true);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeEntityCard();
    if (e.key === 'Enter' && e.target.dataset && e.target.dataset.entityId) {
      openEntityCard(e.target.dataset.entityId, e.target);
    }
  });
})();

(function () {
  // 术语点击 / 关联节点跳转 → 开窗；点击弹窗外或 Esc → 关闭
  document.addEventListener('click', function (e) {
    var ref = e.target.closest && e.target.closest('.term-ref, [data-term-id]');
    if (ref && ref.dataset.termId) { openTermModal(ref.dataset.termId, ref); return; }
    if (!(e.target.closest && e.target.closest('.term-modal'))) closeTermModal();
  }, true);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeTermModal();
    if (e.key === 'Enter' && e.target.dataset && e.target.dataset.termId) {
      openTermModal(e.target.dataset.termId, e.target);
    }
  });
})();

// 知识图谱面板：按 category 分组列出全部节点与边（数据驱动，零硬编码）
function openGraphPanel() {
  if (!_agInit()) { return; }
  _agMount();
  var cats = {}, order = [];
  (_AG.terms || []).forEach(function (t) {
    var c = t.category || 'other';
    if (!cats[c]) { cats[c] = []; order.push(c); }
    cats[c].push(t);
  });
  var cnt = { A1: 0, A2: 0, B: 0, C: 0, D: 0 };
  (_AG.terms || []).forEach(function (t) { cnt[t.grade] = (cnt[t.grade] || 0) + 1; });
  var h = '<div class="tm-meta">'
    + '<span>节点 ' + (_AG.terms || []).length + '</span>'
    + '<span>边 ' + (_AG.links || []).length + '</span>'
    + '<span class="grade-badge grade-A1">A1 ' + cnt.A1 + '</span>'
    + '<span class="grade-badge grade-A2">A2 ' + cnt.A2 + '</span>'
    + (cnt.B ? '<span class="grade-badge grade-B">B ' + cnt.B + '</span>' : '')
    + (cnt.C ? '<span class="grade-badge grade-C">C ' + cnt.C + '</span>' : '')
    + (cnt.D ? '<span class="grade-badge grade-D">D ' + cnt.D + '</span>' : '')
    + '</div>';
  order.forEach(function (c) {
    h += '<div style="margin-top:12px"><div style="font-size:0.86em;color:var(--gold);margin-bottom:6px">' + _escHtml(c) + '</div>';
    cats[c].forEach(function (t) {
      h += '<div style="margin:3px 0"><span class="term-ref" data-term-id="' + _escHtml(t.id) + '" role="button" tabindex="0"'
        + (t.status === 'rejected' ? ' style="text-decoration:line-through"' : '') + '>'
        + _escHtml(t.zh) + '</span> <span class="grade-badge grade-' + _escHtml(t.grade) + '">' + _escHtml(t.grade) + '</span></div>';
    });
    h += '</div>';
  });
  document.getElementById('tm-title').textContent = '🕸 名相会处 · 知识图谱';
  document.getElementById('tm-body').innerHTML = h;
  document.getElementById('term-modal').classList.add('is-open');
  if (window._markEnBlocks) try { window._markEnBlocks(); } catch (e) {}
}

(function(){
  // 长文页：正文渲染后标注术语（与悬浮目录同样轮询待 #article-root 就绪）
  function boot(){
    try{
      _markTermRefs('#article-full') || _markTermRefs('#article-root');
    }catch(e){}
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
  (function poll(tries){
    if (document.querySelector('.term-ref')) return;
    if (tries <= 0) return;
    setTimeout(function(){ boot(); poll(tries-1); }, 150);
  })(24);
})();

(function(){
  // 各 Tab 页侧栏底部自动追加「独立文章目录」入口（lineage 无侧栏则跳过）
  try{ articlesIndexLink(); }catch(e){}
  // 全局阅读语言切换：按 localStorage 恢复站点语言偏好（common.js 位于 header 之后加载）
  try{ window._applySiteLang && window._applySiteLang(); }catch(e){}
  // 长文页：注入悬浮目录（内容运行时插入，故轮询至标题就绪）
  function bootToc(){ try{ _initFloatingToc('#article-root'); }catch(e){} }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bootToc);
  else bootToc();
  // 页面正文由 article.js / 各 RENDER 脚本于其后同步或异步写入 #article-root，
  // common.js 载入时容器尚空，故短程轮询待其就绪（标题不足则自然不再注入，非错误）。
  (function pollToc(tries) {
    if (document.querySelector('.floating-toc')) return;
    if (tries <= 0) return;
    setTimeout(function () { bootToc(); pollToc(tries - 1); }, 120);
  })(24);
})();

// ═══ 章节级折叠（独立文章页 · h2/h3/h4/h5 层级，默认全部折叠）═══
// 长文经各级标题分组为可折叠章节；点击标题或 ▾ 号折叠/展开该节，
// 每节顶部提供「全部折叠 / 全部展开」工具栏；
// 跳转目录/深链锚点前自动展开祖先节（_reveal），故折叠不影响导航。
// 依站点设置：所有标题层次默认折叠（含数据剖面），故 foldDefault 默认 true。

// 展开包裹 el 的折叠祖先节（目录/锚点跳转前调用，防止目标「藏在折叠体内」）
window._reveal = function (el) {
  var p = el;
  while (p) {
    var body = (p.closest ? p.closest('.secfold-body') : null) ||
               (p.classList && p.classList.contains('secfold-body') ? p : null);
    if (!body) break;
    var owner = body.previousElementSibling;
    if (owner && owner.classList && owner.classList.contains('secfold')) {
      owner.classList.remove('is-folded');
    }
    p = body.parentElement;
  }
  // 另向上升开沿途 <details>（表折叠/图折叠/交互面板折叠壳 panel-fold 皆属之）：
  // 锚点跳转的目标若藏在默认折叠的 <details> 内，浏览器不会自动展开，须手动 open。
  var q = el;
  while (q && q !== document.body) {
    if (q.tagName === 'DETAILS') q.setAttribute('open', 'open');
    q = q.parentElement;
  }
  return el;
};

// 滚至某 id 元素，并先展开其沿途所有 <details>（供页头「文本分析层/叙事动画」等入口按钮用）。
// 目标 id 传入时不带 '#'。返回是否命中元素。
window._scrollReveal = function (id) {
  var el = document.getElementById(id);
  if (!el) return false;
  if (el.closest) {
    var d = el.closest('details');
    while (d) { d.setAttribute('open', 'open'); d = d.parentElement ? d.parentElement.closest('details') : null; }
  }
  el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  return true;
};

// 载入章节折叠。rootSel：长文容器；opts：{foldDefault(默认 true), label(工具栏前缀)}。
// 结束返回 {h2, h3, h4, h5, groups, total} 或 0。
window._foldDoc = function (rootSel, opts) {
  var o = opts || {};
  var root = typeof rootSel === 'string' ? document.querySelector(rootSel) : rootSel;
  if (!root) return 0;
  if (root.dataset.sfDone === '1') return 0;
  root.dataset.sfDone = '1';
  var counts = { 2: 0, 3: 0, 4: 0, 5: 0 }, groups = 0, total = 0;
  var LV = 'h2, h3, h4, h5';
  var SEL = 'h2.secfold, h3.secfold, h4.secfold, h5.secfold';

  function caret() { return '<span class="secfold-caret" aria-hidden="true">▾</span>'; }

  function setFolded(h, folded) {
    h.classList.toggle('is-folded', !!folded);
    if (folded) h.setAttribute('aria-expanded', 'false');
    else h.setAttribute('aria-expanded', 'true');
  }

  // 1) 标记全部可折叠标题（跳过 data-skip-toc 之页头性标题）
  root.querySelectorAll(LV).forEach(function (h) {
    if (h.hasAttribute('data-skip-toc')) return;
    if (h.classList.contains('secfold')) return;
    var lv = +h.tagName.charAt(1);
    h.classList.add('secfold');
    h.dataset.fh = lv;
    if (!h.tabIndex) h.tabIndex = 0;
    h.insertAdjacentHTML('afterbegin', caret());
    h.addEventListener('click', function (e) {
      var c = e.target && e.target.closest && e.target.closest('.secfold-caret');
      if (c) e.stopPropagation();
      setFolded(h, !h.classList.contains('is-folded'));
    });
    h.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); setFolded(h, !h.classList.contains('is-folded')); }
    });
    counts[lv] = (counts[lv] || 0) + 1;
    total++;
  });

  // 2) 依层级递归（2→3→4→5）把下级标题及其正文包入 .secfold-body（标题与 body 相邻兄弟）
  function wrapLevel(container, level) {
    if (level > 5) return;
    var kids = Array.prototype.slice.call(container.children);
    for (var i = 0; i < kids.length; i++) {
      var el = kids[i];
      if (!el.classList || !el.classList.contains('secfold')) continue;
      if ((el.dataset.fh | 0) !== level) continue;
      if (el.dataset.sfDone === '1') continue;
      var slice = [];
      for (var k = i + 1; k < kids.length; k++) {
        var nx = kids[k];
        var nlv = (nx.classList && nx.classList.contains('secfold')) ? (nx.dataset.fh | 0) : 99;
        if (nlv <= level) break;
        slice.push(nx);
      }
      if (!slice.length) { el.dataset.sfDone = '1'; continue; }
      var body = document.createElement('div');
      body.className = 'secfold-body';
      slice.forEach(function (x) { body.appendChild(x); });
      el.insertAdjacentElement('afterend', body);
      el.dataset.sfDone = '1';
      groups++;
      wrapLevel(body, level + 1);
    }
  }

  wrapLevel(root, 2);

  // 3) 依设置置默认状态：全部折叠（可由 opts.foldDefault === false 退回展开）
  var foldDefault = (o.foldDefault === undefined) ? true : !!o.foldDefault;
  if (total) {
    root.querySelectorAll(SEL).forEach(function (h) { setFolded(h, foldDefault); });
  }

  // 4) 工具栏：置于首个可折叠标题之前（页头「全文」标题 data-skip-toc 不参与）
  //    opts.noBar === true 时不逐节生成工具栏——改由页面级「一套」统一控件管理全页
  //    （见 window._installPageBar / window._foldPage）。
  if (groups && !o.noBar) {
    var first = root.querySelector(SEL);
    if (first) {
      var bar = document.createElement('div');
      bar.className = 'secfold-bar';
      var pre = o.label ? o.label + ' · ' : '';
      var mix = [];
      [2, 3, 4, 5].forEach(function (l) { if (counts[l]) mix.push('h' + l + '×' + counts[l]); });
      bar.innerHTML = '<span style="opacity:.85">' + pre + '章节折叠 · 共 ' + total
        + ' 节（' + mix.join(' · ') + '）</span>'
        + '<button type="button" class="sf-btn" data-sf="fold">全部折叠</button>'
        + '<button type="button" class="sf-btn" data-sf="open">全部展开</button>'
        + '<span style="opacity:.6">默认折叠 · 点击任一标题可单独展开</span>';
      bar.addEventListener('click', function (e) {
        var b = e.target.closest ? e.target.closest('.sf-btn') : null;
        if (!b) return;
        var fold = b.dataset.sf === 'fold';
        root.querySelectorAll(SEL).forEach(function (x) { setFolded(x, fold); });
      });
      first.parentNode.insertBefore(bar, first);
    }
  }
  return { h2: counts[2], h3: counts[3], h4: counts[4], h5: counts[5], groups: groups, total: total };
};

// ═══ 页面级统一折叠控件（整页「一套」全部折叠／全部展开）═══
// 依用户诉求：整页只设一对按钮，统一管理全页所有可折叠内容——
//   ① 章节折叠（h2/h3/h4/h5 .secfold）；② 原生 <details>（表折叠 table-fold、图折叠 figure-fold）。
// 与逐节 secfold-bar 并立无益，故各 _foldDoc 调用改传 {noBar:true} 取消逐节工具栏，由此一处控件总揽。
// 折叠/展开逻辑与原生理所相宜：章节切 is-folded；details 切 open 属性。
window._foldPage = function (folded, rootSel) {
  var root = rootSel ? (typeof rootSel === 'string' ? document.querySelector(rootSel) : rootSel) : document;
  if (!root) return;
  root.querySelectorAll('h2.secfold, h3.secfold, h4.secfold, h5.secfold').forEach(function (h) {
    h.classList.toggle('is-folded', !!folded);
    h.setAttribute('aria-expanded', folded ? 'false' : 'true');
  });
  root.querySelectorAll('details').forEach(function (d) {
    if (folded) d.removeAttribute('open'); else d.setAttribute('open', 'open');
  });
};

// 安装页面级一套控件于容器顶部（幂等；已存 .pagefold-bar 则不重植）。
// opts：{rootSel（_foldPage 作用域，默认全文）, mountSel（挂载容器，默认其内首个 .secfold-bar/标题之前）}。
window._installPageBar = function (opts) {
  var o = opts || {};
  if (document.querySelector('.pagefold-bar')) return false;
  var mount = o.mountSel ? document.querySelector(o.mountSel) : document.getElementById('article-full');
  if (!mount) return false;
  var nSec = document.querySelectorAll('#article-full h2.secfold, #article-full h3.secfold, #article-full h4.secfold, #article-full h5.secfold').length;
  var nDet = document.querySelectorAll('details').length;
  var bar = document.createElement('div');
  bar.className = 'secfold-bar pagefold-bar';
  bar.innerHTML = '<span style="opacity:.85">🗂 全页折叠 · 章节 ' + nSec + ' 节 · 图表 ' + nDet + ' 处</span>'
    + '<button type="button" class="sf-btn" data-pf="fold">全部折叠</button>'
    + '<button type="button" class="sf-btn" data-pf="open">全部展开</button>'
    + '<span style="opacity:.6">此一对统管全页（章节＋表格＋图像）· 各标题 ▾ 仍可单节收展</span>';
  bar.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('.sf-btn') : null;
    if (!b) return;
    window._foldPage(b.dataset.pf === 'fold', o.rootSel || '#article-root');
  });
  var anchor = mount.querySelector('.secfold, h2, h3') || mount.firstElementChild;
  if (anchor && anchor.parentNode) anchor.parentNode.insertBefore(bar, anchor);
  else mount.insertBefore(bar, mount.firstChild);
  return true;
};

// ═══ 交互面板默认折叠壳（panel-fold）═══
// 依用户诉求：文本分析层/会众名号剖面/叙事动画等 JS 交互面板，此前于附录十一之后
// 恒常「摊开」成独立一节；今一一纳入原生 <details class="fold panel-fold">，默认折叠、
// 点开方显——与全篇 table-fold 体例归一，且受页首「全页折叠/展开」(_foldPage 切 details.open) 统管。
// 返回 <details> 之外壳字符串，innerId 为内容渲染目标（各 render* 须注入 '#' + innerId）。
window._foldShellHtml = function (innerId, label) {
  return '<details class="fold panel-fold">'
    + '<summary>📁 ' + label + '<span style="font-weight:400;color:var(--text2)"> · 默认折叠，点开查看</span></summary>'
    + '<div class="fold-body"><div id="' + innerId + '"></div></div>'
    + '</details>';
};

