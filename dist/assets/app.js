/* Chisi Capital Partners — interaction & motion
   GSAP 3.13 (ScrollTrigger + SplitText) with Lenis smooth scrolling.
   Everything degrades to a static, fully readable page when motion is reduced or scripts fail. */
(() => {
  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const header = document.querySelector('[data-header]');
  const toggle = document.querySelector('.menu-toggle');
  const menu = document.querySelector('#mobile-nav');
  let lenis = null;

  /* ---------- Header state ---------- */
  let lastY = 0;
  const onScroll = y => {
    header.classList.toggle('is-scrolled', y > 60);
    const goingDown = y > lastY && y > window.innerHeight * 0.6;
    if (!header.classList.contains('menu-open')) header.classList.toggle('is-hidden', goingDown);
    lastY = y;
  };
  addEventListener('scroll', () => onScroll(scrollY), { passive: true });
  onScroll(scrollY);

  /* ---------- Mobile menu ---------- */
  function setMenu(open) {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    header.classList.toggle('menu-open', open);
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) {
      menu.hidden = false; lenis?.stop();
      if (window.gsap && !reduce) {
        gsap.fromTo(menu, { clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0% 0)', duration: .8, ease: 'expo.out' });
        gsap.fromTo(menu.querySelectorAll('a span, .mobile-contact'), { yPercent: 110, opacity: 0 }, { yPercent: 0, opacity: 1, duration: .9, stagger: .06, ease: 'expo.out', delay: .15 });
      }
    } else {
      lenis?.start();
      if (window.gsap && !reduce) gsap.to(menu, { clipPath: 'inset(0 0 100% 0)', duration: .6, ease: 'expo.inOut', onComplete: () => { menu.hidden = true; } });
      else menu.hidden = true;
    }
  }
  toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
  addEventListener('keydown', e => { if (e.key === 'Escape' && !menu.hidden) { setMenu(false); toggle.focus(); } });
  addEventListener('resize', () => { if (innerWidth > 960 && !menu.hidden) setMenu(false); });

  /* ---------- Enquiry form (local brief only) ---------- */
  const form = document.querySelector('#enquiry-form');
  form?.addEventListener('submit', e => {
    e.preventDefault();
    const data = new FormData(form);
    const brief = 'CHISI CAPITAL PARTNERS — ENQUIRY BRIEF\n\n' + [...data].map(([k, v]) => `${k}: ${v}`).join('\n\n');
    const url = URL.createObjectURL(new Blob([brief], { type: 'text/plain;charset=utf-8' }));
    const a = Object.assign(document.createElement('a'), { href: url, download: 'chisi-project-enquiry.txt' });
    document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    document.querySelector('#form-status').textContent = 'Your brief has been prepared for download. Nothing has been sent. Call 077 358 8945 to discuss your opportunity.';
  });

  /* ---------- Motion ---------- */
  if (reduce || !window.gsap || !window.ScrollTrigger) { root.classList.remove('motion'); return; }
  root.dataset.ready = '1';
  gsap.registerPlugin(ScrollTrigger);
  const hasSplit = !!window.SplitText;
  if (hasSplit) gsap.registerPlugin(SplitText);

  // Smooth scrolling synced to GSAP's ticker
  if (window.Lenis) {
    lenis = new Lenis({ lerp: 0.085, wheelMultiplier: 1, smoothWheel: true });
    lenis.on('scroll', ({ scroll }) => { ScrollTrigger.update(); onScroll(scroll); });
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) { e.preventDefault(); lenis.scrollTo(target, { offset: -20, duration: 1.4 }); }
    }));
  }

  const splitLines = el => hasSplit
    ? SplitText.create(el, { type: 'lines', mask: 'lines', linesClass: 'split-line', autoSplit: true }).lines
    : [el];

  const start = () => {
    /* Hero: one orchestrated entrance */
    const heroEl = document.querySelector('[data-hero]');
    if (heroEl) {
      const media = heroEl.querySelector('[data-hero-media]');
      const imgEl = heroEl.querySelector('.hero-img');
      const title = heroEl.querySelector('[data-hero-title]');
      const fades = heroEl.querySelectorAll('[data-hero-fade]');
      const lines = splitLines(title);
      gsap.set(title, { visibility: 'visible' });
      const tl = gsap.timeline({ defaults: { ease: 'expo.out' } });
      tl.fromTo(media, { clipPath: 'inset(9% 9% 9% 9%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.8, ease: 'expo.inOut' })
        .fromTo(imgEl, { scale: 1.32 }, { scale: 1.06, duration: 2.6, ease: 'expo.out' }, 0)
        .from(lines, { yPercent: 115, duration: 1.3, stagger: .1 }, 0.75)
        .fromTo(fades, { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 1.1, stagger: .1 }, 1.05);

      // Scroll-out: image drifts, copy lifts and fades
      gsap.to(imgEl, { yPercent: 14, ease: 'none', scrollTrigger: { trigger: heroEl, start: 'top top', end: 'bottom top', scrub: true } });
      gsap.to(heroEl.querySelector('[data-hero-content]'), { y: -90, opacity: 0, ease: 'none', scrollTrigger: { trigger: heroEl, start: 'top top', end: '75% top', scrub: true } });
    }

    /* Section headings: masked line reveal */
    document.querySelectorAll('[data-split]').forEach(h => {
      const lines = splitLines(h);
      gsap.set(h, { visibility: 'visible' });
      gsap.from(lines, { yPercent: 115, duration: 1.2, stagger: .09, ease: 'expo.out', scrollTrigger: { trigger: h, start: 'top 86%', once: true } });
    });

    /* Copy blocks */
    ScrollTrigger.batch('.reveal', {
      start: 'top 90%', once: true,
      onEnter: els => gsap.fromTo(els, { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 1.1, stagger: .08, ease: 'expo.out' })
    });

    /* Image clip reveals */
    document.querySelectorAll('.reveal-img').forEach(fig => {
      const im = fig.querySelector('img');
      const tl = gsap.timeline({ scrollTrigger: { trigger: fig, start: 'top 85%', once: true } });
      tl.fromTo(fig, { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.4, ease: 'expo.inOut' })
        .from(im, { scale: 1.35, duration: 1.8, ease: 'expo.out' }, 0.1);
    });

    /* Parallax inside framed images */
    document.querySelectorAll('[data-parallax]').forEach(wrap => {
      const target = wrap.matches('.cta-media, .approach-media') ? wrap : wrap.querySelector('img');
      gsap.fromTo(target, { yPercent: -7 }, { yPercent: 7, ease: 'none', scrollTrigger: { trigger: wrap.closest('section') || wrap, start: 'top bottom', end: 'bottom top', scrub: true } });
    });

    /* Sectors: pinned horizontal scroll on desktop */
    const mm = gsap.matchMedia();
    mm.add('(min-width: 961px)', () => {
      const section = document.querySelector('[data-sectors]');
      const track = document.querySelector('[data-track]');
      if (!section || !track) return;
      const distance = () => Math.max(0, track.scrollWidth - innerWidth);
      const tween = gsap.to(track, {
        x: () => -distance(), ease: 'none',
        scrollTrigger: { trigger: section, start: 'top top', end: () => '+=' + distance(), pin: true, scrub: 0.8, invalidateOnRefresh: true, anticipatePin: 1 }
      });
      gsap.to('[data-track-progress]', { scaleX: 1, ease: 'none', scrollTrigger: { trigger: section, start: 'top top', end: () => '+=' + distance(), scrub: true } });
      track.querySelectorAll('.sector-card-media img').forEach(im => {
        gsap.fromTo(im, { xPercent: -6 }, { xPercent: 6, ease: 'none', scrollTrigger: { trigger: im.closest('.sector-card'), containerAnimation: tween, start: 'left right', end: 'right left', scrub: true } });
      });
    });

    /* Process: progress line drawn by scroll, steps light up */
    const processSection = document.querySelector('[data-process]');
    if (processSection) {
      const steps = processSection.querySelectorAll('[data-step]');
      gsap.to('[data-process-line]', { scaleX: 1, ease: 'none', scrollTrigger: { trigger: processSection.querySelector('.process'), start: 'top 75%', end: 'bottom 45%', scrub: true,
        onUpdate: self => steps.forEach((s, i) => s.classList.toggle('is-active', self.progress >= i / steps.length + .02)) } });
      gsap.from(steps, { opacity: 0, y: 40, duration: 1.1, stagger: .12, ease: 'expo.out', scrollTrigger: { trigger: processSection.querySelector('.process'), start: 'top 82%', once: true } });
    }

    /* CTA headline scale-in */
    document.querySelectorAll('[data-cta] .button').forEach(b => gsap.from(b, { opacity: 0, y: 30, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: b, start: 'top 92%', once: true } }));

    /* Cursor-following image preview on service rows */
    const preview = document.querySelector('.cursor-preview');
    const rows = document.querySelectorAll('[data-preview]');
    if (finePointer && preview && rows.length) {
      const pImg = preview.querySelector('img');
      const xTo = gsap.quickTo(preview, 'x', { duration: .6, ease: 'expo.out' });
      const yTo = gsap.quickTo(preview, 'y', { duration: .6, ease: 'expo.out' });
      rows.forEach(r => { const i = new Image(); i.src = r.dataset.preview; });
      addEventListener('mousemove', e => { xTo(e.clientX + 40); yTo(e.clientY); });
      rows.forEach(r => {
        r.addEventListener('mouseenter', () => { pImg.src = r.dataset.preview; gsap.to(preview, { autoAlpha: 1, scale: 1, rotate: -2, duration: .6, ease: 'expo.out' }); });
        r.addEventListener('mouseleave', () => gsap.to(preview, { autoAlpha: 0, scale: .6, rotate: 0, duration: .5, ease: 'expo.out' }));
      });
    }

    /* Magnetic buttons */
    if (finePointer) {
      document.querySelectorAll('.button, .header-cta, .scroll-cue').forEach(el => {
        const xTo = gsap.quickTo(el, 'x', { duration: .8, ease: 'elastic.out(1,0.4)' });
        const yTo = gsap.quickTo(el, 'y', { duration: .8, ease: 'elastic.out(1,0.4)' });
        el.addEventListener('mousemove', e => { const r = el.getBoundingClientRect(); xTo((e.clientX - r.left - r.width / 2) * .22); yTo((e.clientY - r.top - r.height / 2) * .32); });
        el.addEventListener('mouseleave', () => { xTo(0); yTo(0); });
      });
    }

    ScrollTrigger.refresh();
  };

  // Wait for the brand font so line splits measure correctly (capped so a slow font never blocks)
  Promise.race([document.fonts?.ready || Promise.resolve(), new Promise(r => setTimeout(r, 900))]).then(start);
  addEventListener('load', () => ScrollTrigger.refresh());
})();
