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

})();
