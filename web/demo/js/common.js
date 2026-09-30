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

  // ── 点击锚点：平滑滚动，避开顶部 sticky 页头 ──
  rail.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
    if (!a) return;
    var id = a.getAttribute('href').slice(1);
    var el = document.getElementById(id);
    if (!el) return;
    e.preventDefault();
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
