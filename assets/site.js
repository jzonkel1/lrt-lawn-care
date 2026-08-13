(function(){
  "use strict";
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  /* ---- pre-fill the quote form's service from ?service= (plan buttons link here) ---- */
  var svcPre = new URLSearchParams(location.search).get('service');
  if (svcPre){
    document.querySelectorAll('form[name="lrt-quote"] select[name="service"]').forEach(function(sel){
      sel.value = svcPre;
      if (sel.value !== svcPre) sel.selectedIndex = 0;   // unknown value — leave the placeholder
    });
  }

  /* ---- nav + sticky call bar ---- */
  var nav = document.getElementById('nav'), bar = document.getElementById('callbar');
  function onScroll(){
    var y = window.scrollY;
    if (nav) nav.classList.toggle('solid', y > 40);
    if (bar) bar.classList.toggle('up', y > window.innerHeight * .7);
  }
  addEventListener('scroll', onScroll, {passive:true}); onScroll();

  /* ---- services dropdown (hover opens it; click/keys for touch + a11y) ---- */
  var drop = document.getElementById('navDrop');
  if (drop){
    var trigger = drop.querySelector('button');
    trigger.addEventListener('click', function(e){
      e.stopPropagation();
      var open = drop.classList.toggle('open');
      trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function(e){
      if (!drop.contains(e.target)){ drop.classList.remove('open'); trigger.setAttribute('aria-expanded','false'); }
    });
    drop.addEventListener('keydown', function(e){
      if (e.key === 'Escape'){ drop.classList.remove('open'); trigger.setAttribute('aria-expanded','false'); trigger.focus(); }
    });
  }

  /* ---- reveal on scroll ---- */
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e, i){
        if (e.isIntersecting){
          e.target.style.transitionDelay = Math.min(i * 70, 280) + 'ms';
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, {rootMargin:'0px 0px -12% 0px', threshold:.08});
    rv.forEach(function(el){ io.observe(el); });
  } else { rv.forEach(function(el){ el.classList.add('in'); }); }

  /* ---- hero quote wizard (POSTs to Netlify Forms) ---- */
  (function(){
    var form = document.getElementById('qwiz'); if (!form) return;
    var steps = form.querySelectorAll('.qwiz-step'),
        qbar = document.getElementById('qwBar'),
        head = document.getElementById('qwHead'),
        done = document.getElementById('qwDone'),
        urgent = document.getElementById('qwUrgent'),
        err = document.getElementById('qwErr'),
        TOTAL = steps.length, cur = 1;

    function show(n){
      cur = Math.max(1, Math.min(TOTAL, n));
      steps.forEach(function(s){ s.classList.toggle('active', +s.dataset.step === cur); });
      qbar.style.width = (cur / TOTAL * 100) + '%';
      if (cur === TOTAL){
        urgent.classList.toggle('on', /gotten away/i.test(document.getElementById('qw-timing').value));
        setTimeout(function(){
          var f = form.querySelector('.qwiz-step.active input');
          if (f) f.focus({preventScroll:true});
        }, 300);
      }
    }

    form.addEventListener('click', function(e){
      var opt = e.target.closest('.qwiz-opt');
      if (opt){
        opt.parentElement.querySelectorAll('.qwiz-opt').forEach(function(o){ o.classList.remove('sel'); });
        opt.classList.add('sel');
        var hidden = document.getElementById('qw-' + opt.dataset.field);
        if (hidden) hidden.value = opt.dataset.value;
        setTimeout(function(){ show(cur + 1); }, 230);   // let the highlight register
        return;
      }
      if (e.target.closest('[data-back]')) show(cur - 1);
    });

    form.addEventListener('keydown', function(e){
      if (e.key === 'Enter' && e.target.tagName === 'INPUT'){ e.preventDefault(); form.requestSubmit(); }
    });

    form.addEventListener('submit', function(e){
      e.preventDefault();
      var name = document.getElementById('qw-name').value.trim(),
          phone = document.getElementById('qw-phone').value.replace(/\D/g, '');
      if (!name || phone.length < 7){
        err.textContent = 'Add a name and a number we can text.';
        err.classList.add('on'); return;
      }
      err.classList.remove('on');
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      fetch('/', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: new URLSearchParams(new FormData(form)).toString()
      }).then(function(r){
        if (!r.ok) throw new Error(r.status);
        steps.forEach(function(s){ s.classList.remove('active'); });
        head.style.display = 'none';
        done.classList.add('on');
      }).catch(function(){
        btn.disabled = false;
        err.textContent = "That didn't go through — call or text (361) 765-5258 instead.";
        err.classList.add('on');
      });
    });

    show(1);
  })();

  /* ---- before / after sliders (default 80% BEFORE) ---- */
  document.querySelectorAll('[data-ba]').forEach(function(ba){
    var top = ba.querySelector('.ba-top'),
        handle = ba.querySelector('.ba-handle'),
        pct = 80, dragging = false;

    function paint(p){
      pct = Math.max(0, Math.min(100, p));
      top.style.width = pct + '%';
      handle.style.left = pct + '%';
      ba.setAttribute('aria-valuenow', Math.round(pct));
    }
    function fromEvent(e){
      var r = ba.getBoundingClientRect();
      var x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
      paint(x / r.width * 100);
    }
    function sizeTop(){
      top.querySelector('img').style.width = ba.getBoundingClientRect().width + 'px';
    }

    ba.addEventListener('pointerdown', function(e){
      dragging = true; ba.setPointerCapture(e.pointerId); fromEvent(e); e.preventDefault();
    });
    ba.addEventListener('pointermove', function(e){ if (dragging) fromEvent(e); });
    ['pointerup','pointercancel'].forEach(function(t){
      ba.addEventListener(t, function(){ dragging = false; });
    });
    ba.addEventListener('keydown', function(e){
      if (e.key === 'ArrowLeft'){ paint(pct - 4); e.preventDefault(); }
      if (e.key === 'ArrowRight'){ paint(pct + 4); e.preventDefault(); }
      if (e.key === 'Home'){ paint(0); e.preventDefault(); }
      if (e.key === 'End'){ paint(100); e.preventDefault(); }
    });

    addEventListener('resize', sizeTop);
    var base = ba.querySelector('.ba-base');
    if (base.complete) { sizeTop(); } else { base.addEventListener('load', sizeTop); }
    sizeTop(); paint(80);
  });

  /* ---- lightbox: photos and clips ---- */
  var lb = document.getElementById('lb'),
      lbImg = document.getElementById('lbImg'),
      lbVid = document.getElementById('lbVid');

  function openLb(){ lb.classList.add('on'); document.body.style.overflow = 'hidden'; }
  function closeLb(){
    lb.classList.remove('on'); document.body.style.overflow = '';
    lbImg.hidden = true; lbImg.removeAttribute('src');
    lbVid.hidden = true; lbVid.pause(); lbVid.removeAttribute('src'); lbVid.load();
  }
  function showImg(img){
    lbVid.hidden = true; lbVid.pause(); lbVid.removeAttribute('src');
    lbImg.src = img.currentSrc || img.src; lbImg.alt = img.alt; lbImg.hidden = false;
    openLb();
  }
  function showVid(v){
    lbImg.hidden = true; lbImg.removeAttribute('src');
    lbVid.src = v.currentSrc || v.src; lbVid.poster = v.poster;
    lbVid.hidden = false; lbVid.muted = false; lbVid.currentTime = 0;
    openLb();
    lbVid.play().catch(function(){ lbVid.muted = true; lbVid.play().catch(function(){}); });
  }

  if (lb){
    document.querySelectorAll('.gal').forEach(function(gal){
      gal.addEventListener('click', function(e){
        var img = e.target.closest('img'); if (img) showImg(img);
      });
    });
    document.getElementById('lbX').addEventListener('click', closeLb);
    lb.addEventListener('click', function(e){ if (e.target === lb) closeLb(); });
    addEventListener('keydown', function(e){ if (e.key === 'Escape' && lb.classList.contains('on')) closeLb(); });
  }

  /* ---- home job-site reel carousel (native scroll-snap track) ---- */
  var hrTrack = document.getElementById('hrTrack');
  if (hrTrack){
    var hrPrev = document.getElementById('hrPrev'),
        hrNext = document.getElementById('hrNext'),
        hrDots = document.getElementById('hrDots');

    function hrPages(){
      var w = hrTrack.clientWidth;
      if (!w) return 1;
      // ceil, with slack so 5 slides at 4-per-view still counts as 2 pages
      return Math.max(1, Math.ceil((hrTrack.scrollWidth - 4) / w));
    }
    function hrPage(){
      var max = hrTrack.scrollWidth - hrTrack.clientWidth;
      if (max <= 0) return 0;
      // the last page is shorter than a full viewport, so snap the count at the end
      if (hrTrack.scrollLeft >= max - 4) return hrPages() - 1;
      return Math.round(hrTrack.scrollLeft / hrTrack.clientWidth);
    }
    function hrSync(){
      var pages = hrPages(), page = hrPage();
      hrPrev.disabled = page <= 0;
      hrNext.disabled = page >= pages - 1;
      if (hrDots.children.length !== pages){
        hrDots.innerHTML = '';
        for (var i = 0; i < pages; i++){
          var b = document.createElement('button');
          b.type = 'button';
          b.setAttribute('aria-label', 'Go to clips ' + (i + 1) + ' of ' + pages);
          (function(n){ b.addEventListener('click', function(){ hrGo(n); }); })(i);
          hrDots.appendChild(b);
        }
      }
      for (var j = 0; j < hrDots.children.length; j++){
        hrDots.children[j].classList.toggle('on', j === page);
      }
    }
    function hrGo(n){
      var max = hrTrack.scrollWidth - hrTrack.clientWidth;
      hrTrack.scrollTo({left: Math.min(n * hrTrack.clientWidth, max), behavior: 'smooth'});
    }
    hrPrev.addEventListener('click', function(){ hrGo(hrPage() - 1); });
    hrNext.addEventListener('click', function(){ hrGo(hrPage() + 1); });
    hrTrack.addEventListener('scroll', hrSync, {passive: true});
    addEventListener('resize', hrSync);
    hrSync();

    // Lazy-attach each clip's src on first intersection, then play/pause with
    // visibility. A <video src> downloads on mount no matter what preload says,
    // so off-screen slides cost zero bytes until they scroll into view.
    if ('IntersectionObserver' in window){
      var hio = new IntersectionObserver(function(es){
        es.forEach(function(e){
          var v = e.target;
          if (e.isIntersecting){
            if (!v.src) v.src = v.dataset.src;
            v.play().catch(function(){});
          } else { v.pause(); }
        });
      }, {threshold:.25});
      hrTrack.querySelectorAll('video').forEach(function(v){ hio.observe(v); });
    } else {
      hrTrack.querySelectorAll('video').forEach(function(v){ v.src = v.dataset.src; });
    }
  }

  /* ---- reel: carousel under 980px, static 2-up grid above ---- */
  var track = document.getElementById('reelTrack');
  if (track){
    var items = track.children, idx = 0;
    var prev = document.getElementById('reelPrev'), next = document.getElementById('reelNext');
    var carousel = window.matchMedia('(max-width: 979px)');

    function step(){
      if (!carousel.matches){ track.style.transform = ''; return; }
      var w = items[0].getBoundingClientRect().width + 16;
      var perView = Math.max(1, Math.floor((track.parentElement.clientWidth + 16) / w));
      var max = Math.max(0, items.length - perView);
      idx = Math.min(idx, max);
      track.style.transform = 'translate3d(' + (-idx * w) + 'px,0,0)';
      prev.disabled = idx <= 0; next.disabled = idx >= max;
    }
    prev.addEventListener('click', function(){ idx--; step(); });
    next.addEventListener('click', function(){ idx++; step(); });
    addEventListener('resize', step);
    carousel.addEventListener('change', function(){ idx = 0; step(); });
    step();

    // tap / click / Enter on a clip opens it big, with sound and native fullscreen
    track.addEventListener('click', function(e){
      var fig = e.target.closest('.reel-item'); if (fig) showVid(fig.querySelector('video'));
    });
    track.addEventListener('keydown', function(e){
      if (e.key !== 'Enter' && e.key !== ' ') return;
      var fig = e.target.closest('.reel-item'); if (!fig) return;
      e.preventDefault(); showVid(fig.querySelector('video'));
    });

    // the inline previews only autoplay while they're actually on screen
    if ('IntersectionObserver' in window){
      var vio = new IntersectionObserver(function(es){
        es.forEach(function(e){
          if (e.isIntersecting){ e.target.play().catch(function(){}); } else { e.target.pause(); }
        });
      }, {threshold:.4});
      track.querySelectorAll('video').forEach(function(v){ vio.observe(v); });
    }
  }
})();
