from pathlib import Path
import os, zipfile, xml.etree.ElementTree as ET, html

ROOT = Path(__file__).parent
D = ROOT
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with zipfile.ZipFile(next(ROOT.parent.glob('*.docx'))) as z:
    xml = ET.fromstring(z.read('word/document.xml'))
lines = [''.join(t.text or '' for t in p.findall('.//w:t', ns)) for p in xml.findall('.//w:p', ns)]


def esc(s):
    return html.escape(s)


nav = [('about', 'About'), ('services', 'Services'), ('sectors', 'Sectors'), ('approach', 'Our approach'), ('cie', 'CIE')]
ARROW = '<svg class="arrow" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'


def link(slug):
    return slug


def button(text, href, kind=''):
    return f'<a class="button {kind}" href="{href}"><span class="button-label">{text}</span>{ARROW}</a>'


def img(name, alt, cls='', eager=False):
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return f'<img class="{cls}" src="assets/img/{name}.webp" alt="{esc(alt)}" {load}>'


HEROES = {
    'index': ('hero-home', 'A Zimbabwean business leader looking out over the Harare skyline at sunset'),
    'about': ('hero-about', 'Zimbabwean business leaders walking together outside a modern office'),
    'services': ('hero-services', 'Three professionals reviewing plans and a financial model around a boardroom table'),
    'sectors': ('hero-sectors', 'A farmer and an adviser walking through a commercial farm with a processing facility behind'),
    'approach': ('hero-approach', 'A business partner and a site engineer shaking hands on a project site at sunrise'),
    'contact': ('hero-contact', 'An executive welcoming a visitor with a handshake in a bright office'),
    'cie': ('hero-cie', 'Young entrepreneurs at a workshop listening to a founder present her product idea'),
    'legal': ('hero-legal', 'A business leader standing at an office window above the city'),
}


def hero(page, eyebrow, title_html, lead='', actions='', bottom=''):
    name, alt = HEROES.get(page, HEROES['legal'])
    return f'''<section class="hero" data-hero>
<div class="hero-media" data-hero-media>{img(name, alt, 'hero-img', eager=True)}<div class="hero-shade" aria-hidden="true"></div></div>
<div class="wrap hero-inner" data-hero-content>

<h1 class="hero-title" data-hero-title>{title_html}</h1>
{f'<p class="hero-lead" data-hero-fade>{lead}</p>' if lead else ''}
{f'<div class="actions" data-hero-fade>{actions}</div>' if actions else ''}
</div>
{bottom}
</section>'''


def scroll_cue():
    return '<a class="scroll-cue" href="#main-content" aria-label="Scroll to content"><span></span></a>'


def shell(slug, title, desc, body):
    links = ''.join(f'<a href="{link(s)}" ' + ('aria-current="page"' if slug == s else '') + f'>{n}</a>' for s, n in nav)
    mobile_links = ''.join(f'<a href="{link(s)}"><span>{n}</span></a>' for s, n in nav + [('contact', 'Contact')])
    cie_contact = '<p class="footer-sub">CIE enquiries</p><a href="mailto:info@cie.co.zw">info@cie.co.zw</a>' if slug == 'cie' else ''
    footer_brand = ('<img class="footer-logo footer-logo-cie" src="assets/logo-cie-light.png" alt="Centre for Impactful Entrepreneurs" width="760" height="298" loading="lazy">'
                    if slug == 'cie' else
                    '<img class="footer-logo" src="assets/logo-light.png" alt="Chisi Capital Partners" width="760" height="249" loading="lazy"><p class="footer-line">Rooted in heritage.<br>Building enduring value.</p>')
    footer = f'''<footer class="footer"><div class="wrap footer-grid"><div class="footer-brand">{footer_brand}</div><div><p class="eyebrow">Explore</p>{links}</div><div><p class="eyebrow">Start a conversation</p><a href="tel:+263773588945">077 358 8945</a><a href="mailto:info@chisicapitalpartners.co.zw">info@chisicapitalpartners.co.zw</a>{cie_contact}<p>64 Cork Road, Avondale<br>Harare, Zimbabwe</p><a class="text-link light" href="contact">Discuss a project {ARROW}</a></div></div><div class="wrap footer-bottom"><span>© 2026 Chisi Capital Partners</span><div><a href="privacy-policy">Privacy</a><a href="cookie-policy">Cookies</a><a href="terms">Website terms</a><a href="photo-credits">Imagery</a></div></div></footer>'''
    out = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#052137"><link rel="canonical" href="https://chisicapitalpartners.co.zw/{"" if slug=="index" else slug}"><link rel="icon" href="assets/favicon.png" type="image/png"><link rel="apple-touch-icon" href="assets/apple-touch-icon.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&amp;display=swap" rel="stylesheet"><link rel="preload" as="image" href="assets/img/{HEROES.get(slug, HEROES['legal'])[0]}.webp"><link rel="stylesheet" href="assets/tailwind.css"><link rel="stylesheet" href="assets/lenis.css"><link rel="stylesheet" href="assets/style.css"><script>(function(l){{var p=l.pathname,c=p.replace(/(^|\/)index\.html$/,'$1').replace(/\.html$/,'');if(c!==p&&l.protocol!=='file:')history.replaceState(null,'',c+l.search+l.hash)}})(location)</script><script>(function(d){{if(!matchMedia('(prefers-reduced-motion: reduce)').matches){{d.classList.add('motion');setTimeout(function(){{if(!d.dataset.ready)d.classList.remove('motion')}},3500)}}}})(document.documentElement)</script><script defer src="assets/gsap.min.js"></script><script defer src="assets/ScrollTrigger.min.js"></script><script defer src="assets/SplitText.min.js"></script><script defer src="assets/lenis.min.js"></script><script defer src="assets/app.js"></script></head><body data-page="{slug}"><a class="skip" href="#main-content">Skip to content</a><header class="header" data-header><div class="wrap header-inner"><a href="/" class="brand" aria-label="Chisi Capital Partners home"><img class="logo-light" src="assets/logo-light.png" alt="" width="760" height="249"><img class="logo-brass" src="assets/logo-color.png" alt="" width="760" height="249"></a><nav class="desktop-nav" aria-label="Main navigation">{links}</nav><a class="header-cta" href="contact"><span>Discuss a project</span>{ARROW}</a><button class="menu-toggle" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open navigation"><span></span><span></span></button></div></header><nav id="mobile-nav" class="mobile-nav" hidden aria-label="Mobile navigation"><div class="wrap">{mobile_links}<div class="mobile-contact"><a href="tel:+263773588945">077 358 8945</a><a href="mailto:info@chisicapitalpartners.co.zw">info@chisicapitalpartners.co.zw</a><p>64 Cork Road, Avondale, Harare</p></div></div></nav><main id="main">{body}</main>{footer}<div class="cursor-preview" aria-hidden="true"><img alt=""></div></body></html>'''
    target = D / (slug + '.html'); tmp = target.with_suffix('.html.tmp')
    tmp.write_text(out, encoding='utf-8'); os.replace(tmp, target)


services = [
    ('Project origination & development', 'Identifying and shaping commercially viable opportunities in productive sectors.', 'boardroom-plans'),
    ('Project preparation & investment structuring', 'Developing feasibility inputs, financial models and investable transaction structures.', 'analyst'),
    ('Capital mobilisation & transaction advisory', 'Supporting funding strategies and engagement with potential financiers and strategic investors.', 'hero-approach'),
    ('Fund development & investment strategy', 'Developing investment approaches and fund concepts, subject to relevant requirements.', 'hero-services'),
    ('Strategic partnerships', 'Connecting technical, commercial and funding relationships to advance implementation.', 'hero-about'),
]
sectors = [
    ('Manufacturing & industry', 'Projects that create or expand local productive capacity, including inputs and manufacturing value chains.', 'sector-manufacturing', 'An engineer inspecting machinery on a factory floor'),
    ('Agro-processing', 'Opportunities that transform agricultural output into higher-value products for domestic and regional markets.', 'sector-agro', 'Women sorting fresh produce in an agro-processing facility'),
    ('Mineral beneficiation', 'Commercially grounded ventures that add value to mineral resources through processing and manufacturing.', 'sector-minerals', 'A metallurgist examining refined ore samples at a processing plant'),
    ('Import substitution', 'Enterprises with credible demand for competitively produced goods that may replace imports.', 'sector-import', 'Workers packing locally made goods on a production line'),
    ('Energy & infrastructure', 'Energy and enabling infrastructure that support viable enterprises and industrial activity.', 'sector-energy', 'An engineer with a tablet walking between rows of solar panels'),
    ('Export value chains', 'Businesses positioned to serve regional customers and participate in cross-border supply chains.', 'sector-export', 'Workers loading export citrus cartons beside a shipping container'),
]
steps = [('Discover', 'Understand the opportunity and its commercial context.'), ('Assess', 'Test market demand and commercial fundamentals.'), ('Structure', 'Prepare the project and its investment proposition.'), ('Engage', 'Support dialogue with potential capital and technical partners.')]


def cta(image='hero-legal', alt='A business leader standing at an office window above the city'):
    return f'''<section class="cta" data-cta><div class="cta-media" data-parallax>{img(image, alt, 'cta-img')}</div><div class="wrap cta-inner"><p class="eyebrow light">The next step starts with a conversation</p><h2 class="split" data-split>Have a project<br><em>worth developing?</em></h2>{button('Let’s discuss the opportunity', 'contact', 'light')}</div></section>'''


rows = ''.join(
    f'<a class="service-row" href="services#service-{i}" data-preview="assets/img/{im}.webp"><span class="number">0{i}</span><h3>{t}</h3><p>{d}</p><span class="row-arrow" aria-hidden="true">{ARROW}</span></a>'
    for i, (t, d, im) in enumerate(services, 1))
cards = ''.join(
    f'<a class="sector-card" href="sectors#sector-{i}"><div class="sector-card-media">{img(im, alt)}</div><div class="sector-card-body"><span class="number">0{i}</span><h3>{t}</h3><p>{d}</p></div></a>'
    for i, (t, d, im, alt) in enumerate(sectors, 1))
process = ''.join(f'<div class="step" data-step><span class="step-dot" aria-hidden="true"></span><span class="number">0{i}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(steps, 1))
strip = '<div class="hero-strip wrap" data-hero-fade><span>Project development</span><span>Investment structuring</span><span>Capital mobilisation</span>' + scroll_cue() + '</div>'
plain_strip = '<div class="wrap hero-strip" data-hero-fade>' + scroll_cue() + '</div>'

home = hero('index', 'Zimbabwe rooted. Africa focused.', 'From opportunity to <em>investment-ready</em> enterprise.',
            'We develop promising business opportunities into structured, commercially grounded projects. Built on discipline. Shaped for lasting value.',
            button('Discuss a project', 'contact', 'light') + button('Explore our services', 'services', 'ghost'), strip)
home += f'''<div id="main-content"></div>
<section class="section wrap purpose">
<figure class="purpose-media reveal-img" data-parallax>{img('portrait-leader', 'A Zimbabwean professional holding project documents in a Harare office')}</figure>
<div class="purpose-copy"><p class="eyebrow">Our purpose</p><h2 class="split" data-split>Good opportunities deserve <em>strong foundations.</em></h2><p class="large reveal">Strong ideas need more than ambition. They need robust commercial assessment, practical development pathways and structures that investors and partners can evaluate.</p><p class="reveal">We connect project preparation, investment thinking and engagement with potential capital partners across Zimbabwe and the wider African region.</p><a class="text-link reveal" href="about">Get to know Chisi {ARROW}</a></div>
</section>
<section class="services section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">What we do</p><h2 class="split" data-split>Clarity at every stage.<br><em>Purpose in every structure.</em></h2></div><a class="text-link" href="services">All services {ARROW}</a></div><div class="service-list">{rows}</div></div></section>
<section class="sectors-home" data-sectors><div class="sectors-pin"><div class="wrap sectors-head"><div><p class="eyebrow">Where we focus</p><h2 class="split" data-split>Real enterprise.<br><em>Tangible value.</em></h2></div><div class="sectors-intro"><p>Our attention is on productive sectors: enterprises that strengthen industrial capabilities, add value and create lasting economic contribution.</p>{button('Explore our sectors', 'sectors', 'outline')}</div></div><div class="sector-track" data-track>{cards}</div><div class="wrap sector-progress" aria-hidden="true"><span data-track-progress></span></div></div></section>
<section class="approach-band" data-process><div class="approach-media" data-parallax>{img('analyst', 'An analyst reviewing a financial model across two monitors')}</div><div class="wrap approach-inner"><div class="section-heading"><div><p class="eyebrow light">The way forward</p><h2 class="split" data-split>Ambition, meet <em>discipline.</em></h2></div><a class="text-link light" href="approach">Our full approach {ARROW}</a></div><div class="process"><div class="process-line" aria-hidden="true"><span data-process-line></span></div>{process}</div><p class="qualification">Every opportunity is assessed on its own merits, subject to due diligence and applicable approvals.</p></div></section>
<section class="section wrap collaboration"><div class="collab-copy"><p class="eyebrow">Connected expertise</p><h2 class="split" data-split>Entrepreneurial ideas.<br><em>Commercial possibilities.</em></h2><p class="large reveal">We collaborate with the Centre for Impactful Entrepreneurs (CIE), connecting entrepreneurial development and incubation with commercial assessment, project preparation and investment structuring.</p><a class="text-link reveal" href="cie">Meet CIE {ARROW}</a></div><figure class="collab-media reveal-img" data-parallax>{img('entrepreneur', 'A young entrepreneur presenting a business plan to a mentor at an incubation hub')}</figure></section>'''
shell('index', 'Chisi Capital Partners | Project Development & Investment Structuring', 'Project development, investment structuring and capital mobilisation across Zimbabwe and Africa.', home + cta())

inner_ctas = {'about': ('Discuss an opportunity', 'contact'), 'services': ('Discuss a project', 'contact'), 'sectors': ('Submit a sector opportunity', 'contact'), 'approach': ('Start a conversation', 'contact')}
sections = [('about', 'ABOUT CHISI', 'SERVICES'), ('services', 'SERVICES', 'SECTOR FOCUS'), ('sectors', 'SECTOR FOCUS', 'OUR APPROACH'), ('approach', 'OUR APPROACH', 'CONTACT')]
inline_figures = {
    'about': {2: ('boardroom-plans', 'Professionals reviewing plans together around a boardroom table')},
    'approach': {3: ('entrepreneur', 'A young entrepreneur presenting a business plan to a mentor')},
}
for slug, start, end in sections:
    a = lines.index(start); b = lines.index(end, a + 1); content = lines[a:b]
    title = next(t.removeprefix('SEO TITLE  ') for t in content if t.startswith('SEO TITLE'))
    desc = next(t.removeprefix('META DESCRIPTION  ') for t in content if t.startswith('META DESCRIPTION'))
    hidx = next(i for i, t in enumerate(content) if t.startswith('H1  ')); heading = content[hidx][4:]; lead = content[hidx + 1]
    label, href = inner_ctas[slug]
    body = hero(slug, f'Chisi Capital Partners / {dict(nav)[slug]}', esc(heading), esc(lead), button(label, href, 'light'), plain_strip)
    body += '<div id="main-content"></div><section class="wrap editorial section">'
    opened = False; count = 0
    for t in content[hidx + 2:]:
        if not t or t.startswith(('PRIMARY CTA', 'SECONDARY CTA', 'CTA', 'SECTION CTA')):
            continue
        label, sep, rest = t.partition('  ')
        is_value = bool(sep) and label.isupper() and label != 'TYPICAL SUPPORT'
        if is_value:
            if not opened:
                body += '<article class="editorial-row"><div></div><div class="article-copy">'; opened = True
            body += f'<div class="value reveal"><h3>{esc(label.capitalize())}</h3><p>{esc(rest)}</p></div>'
            continue
        if t.startswith('TYPICAL SUPPORT'):
            body += f'<div class="support reveal"><span class="support-label">Typical support</span><p>{esc(t.removeprefix("TYPICAL SUPPORT").strip())}</p></div>'
            continue
        isheading = len(t) < 105 and not t.rstrip().endswith(('.', '?', '.”'))
        if isheading:
            if opened:
                body += '</div></article>'
            count += 1
            if slug in inline_figures and count in inline_figures[slug]:
                n, alt = inline_figures[slug][count]
                body += f'<figure class="wide-figure reveal-img" data-parallax>{img(n, alt)}</figure>'
            ident = ('service-' if slug == 'services' else 'sector-' if slug == 'sectors' else 'section-') + str(count)
            if 'Centre for' in t:
                ident = 'collaboration'
            clean = t.split(' — ', 1)[-1]
            if clean[:2].rstrip('.').isdigit() and clean[1:3] == '. ':
                clean = clean[3:]
            figure = ''
            if slug == 'sectors' and count <= len(sectors):
                _, _, im, alt = sectors[count - 1]
                figure = f'<figure class="row-figure reveal-img">{img(im, alt)}</figure>'
            body += f'<article class="editorial-row{" has-figure" if figure else ""}" id="{ident}"><div class="row-head"><span class="number">{count:02d}</span><h2 class="split" data-split>{esc(clean)}</h2></div><div class="article-copy">{figure}'
            opened = True
        else:
            if not opened:
                body += '<article class="editorial-row"><div></div><div class="article-copy">'; opened = True
            body += f'<p class="reveal">{esc(t.replace("TYPICAL SUPPORT  ", "Typical support: "))}</p>'
    if opened:
        body += '</div></article>'
    body += '</section>'
    shell(slug, title, desc, body + cta())

fields = '''<div class="grid sm:grid-cols-2 gap-6"><label>Full name <span>*</span><input name="Full name" autocomplete="name" required></label><label>Organisation<input name="Organisation" autocomplete="organization"></label><label>Work email <span>*</span><input type="email" name="Work email" autocomplete="email" required></label><label>Telephone<input type="tel" name="Telephone" autocomplete="tel"></label></div>'''
for name, options in [('I am enquiring about', ['Project development', 'Investment structuring', 'Capital mobilisation', 'Partnership', 'Other']), ('Sector', ['Manufacturing', 'Agro-processing', 'Mineral beneficiation', 'Import substitution', 'Energy and infrastructure', 'Export-oriented production', 'Other']), ('Current stage', ['Concept', 'Early assessment', 'Feasibility', 'Operating business', 'Expansion', 'Other'])]:
    fields += f'<label>{name}<select name="{name}"><option value="">Select an option</option>' + ''.join(f'<option>{s}</option>' for s in options) + '</select></label>'
fields += f'''<label>Brief description <span>*</span><textarea name="Description" rows="5" required placeholder="Tell us about the opportunity and the support you are seeking."></textarea></label><label class="consent"><input type="checkbox" required> <span>I have read the <a href="privacy-policy">privacy notice</a> and understand this form prepares a local file; it does not send my information.</span></label><button type="submit" class="button"><span class="button-label">Download enquiry brief</span>{ARROW}</button><p role="status" id="form-status"></p>'''
contact_body = hero('contact', 'Start a conversation', 'Let’s discuss <em>the opportunity.</em>', 'Tell us what you are working on, where you are in the journey and how we may be able to help.', button('Call 077 358 8945', 'tel:+263773588945', 'light'), plain_strip)
contact_body += f'''<div id="main-content"></div><section class="wrap contact-grid section"><aside class="reveal"><p class="eyebrow">Speak with us</p><a class="contact-phone" href="tel:+263773588945">077 358 8945</a><a class="contact-email" href="mailto:info@chisicapitalpartners.co.zw">info@chisicapitalpartners.co.zw</a><h2>Visit our office</h2><p>64 Cork Road, Avondale<br>Harare, Zimbabwe</p><a class="text-link" target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&query=64+Cork+Road+Avondale+Harare">Get directions {ARROW}</a><div class="contact-note"><h3>A considered first step.</h3><p>An initial discussion does not constitute acceptance of a mandate or a commitment to provide financing.</p></div></aside><div class="reveal"><h2>Prepare your project enquiry</h2><p class="form-intro">Use this form to download a brief for your records. To discuss it with our team, call the number alongside. Online submission is not yet available.</p><form id="enquiry-form">{fields}</form></div></section>'''
shell('contact', 'Contact Chisi Capital Partners | Discuss a Project', 'Discuss project development, investment structuring or a strategic partnership with Chisi Capital Partners.', contact_body)


# ---------- CIE page ----------
cie_programmes = [
    ('Enterprise development', 'Identifying promising ideas and supporting early commercial concept development.'),
    ('Training & incubation', 'Building entrepreneurship capabilities through training, mentorship and incubation initiatives.'),
    ('Industrial project origination', 'Finding productive-sector opportunities that address market gaps and strengthen local production.'),
    ('Industry engagement', 'Connecting entrepreneurs, businesses and stakeholders in practical dialogue about enterprise growth.'),
    ('Partnerships & access', 'Building relationships that improve access to expertise, markets and potential sources of finance.'),
    ('Forums & roadshows', 'Bringing ideas, businesses and industry together through workshops, forums and project showcases.'),
]
cie_steps = [
    ('Share your idea', 'Tell CIE what you want to build and the challenge or opportunity it addresses.'),
    ('Initial review', 'Suitable submissions are assessed against market demand, feasibility, impact and readiness.'),
    ('Identify the right support', 'Next steps may include training, mentorship, incubation, further preparation or a partner referral.'),
    ('Develop the opportunity', 'Promising concepts may progress towards stronger business plans and investment preparation, subject to further assessment.'),
]
cie_focus = ['Manufacturing', 'Agro-processing', 'Mineral beneficiation', 'Packaging & industrial inputs', 'Import substitution', 'Export-oriented enterprises']
programme_html = ''.join(f'<div class="pillar reveal"><h3>{t}</h3><p>{d}</p></div>' for t, d in cie_programmes)
cie_process = ''.join(f'<div class="step" data-step><span class="step-dot" aria-hidden="true"></span><span class="number">0{i}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(cie_steps, 1))
focus_html = ''.join(f'<li class="reveal">{f}</li>' for f in cie_focus)
cie_body = hero('cie', '', 'Turning promising ideas into <em>productive enterprises.</em>',
                'The Centre for Impactful Entrepreneurs (CIE) mobilises entrepreneurial ideas, supports enterprise development and connects people with the knowledge, partnerships and opportunities needed to build commercially viable businesses in Zimbabwe.',
                button('How CIE and Chisi work together', '#together', 'light') + button('Email CIE', 'mailto:info@cie.co.zw', 'ghost'), plain_strip)
cie_body += f"""<div id="main-content"></div>
<section class="section wrap cie-intro">
<div class="cie-logo-panel reveal"><img src="assets/logo-cie.png" alt="Centre for Impactful Entrepreneurs: opportunities, enterprises, people" width="760" height="298" loading="lazy"></div>
<div><p class="eyebrow">Who CIE is</p><h2 class="split" data-split>A platform for <em>enterprise development.</em></h2><p class="large reveal">CIE is an enterprise development and industrialisation initiative in Zimbabwe. It brings together entrepreneurs, industry, financial institutions, investors, development finance institutions, technical specialists and strategic partners to support enterprise growth, local manufacturing, value addition and sustainable economic development.</p>
<div class="mv"><div class="reveal"><h3>Mission</h3><p>To mobilise, nurture and empower entrepreneurs by creating pathways through which business ideas can be developed into viable enterprises, industrial projects and sustainable economic opportunities.</p></div><div class="reveal"><h3>Vision</h3><p>To become a recognised platform for entrepreneurship, enterprise development and industrial project origination, contributing to a more productive, innovative and industrialised Zimbabwe.</p></div></div></div>
</section>
<section class="services section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">What CIE does</p><h2 class="split" data-split>Practical support for <em>enterprise development.</em></h2></div></div><div class="pillars">{programme_html}</div></div></section>
<section class="approach-band" data-process><div class="approach-media" data-parallax>{img('cie-workshop', 'An entrepreneur presenting product samples to a group taking notes')}</div><div class="wrap approach-inner"><div class="section-heading"><div><p class="eyebrow light">How ideas progress</p><h2 class="split" data-split>From an idea to a <em>stronger business opportunity.</em></h2></div></div><div class="process"><div class="process-line" aria-hidden="true"><span data-process-line></span></div>{cie_process}</div><p class="qualification">A registered company or completed business plan is not required for an initial submission. Submitting an idea does not guarantee programme admission, funding or investment.</p></div></section>
<section class="section wrap cie-focus"><div><p class="eyebrow">Focus areas</p><h2 class="split" data-split>Supporting Zimbabwe’s <em>productive economy.</em></h2><p class="reveal">CIE prioritises commercially promising opportunities that contribute to domestic value addition, industrialisation, import substitution and regional trade. Sector relevance alone does not determine acceptance: projects need market demand, credible operating models and feasibility.</p></div><ul class="focus-list">{focus_html}</ul></section>
<section class="section together" id="together"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">CIE and Chisi</p><h2 class="split" data-split>Complementary roles. <em>Distinct mandates.</em></h2></div></div>
<div class="roles"><div class="role role-cie reveal"><img class="role-logo" src="assets/logo-cie.png" alt="CIE" width="760" height="298" loading="lazy"><h3>Centre for Impactful Entrepreneurs</h3><ul><li>Outreach and idea mobilisation</li><li>Entrepreneurship development and training</li><li>Mentorship and incubation</li><li>Identifying promising projects</li></ul></div>
<div class="role-link reveal" aria-hidden="true"><span></span>{ARROW}<span></span></div>
<div class="role role-chisi reveal"><img class="role-logo" src="assets/logo-color.png" alt="Chisi Capital Partners" width="760" height="249" loading="lazy"><h3>Chisi Capital Partners</h3><ul><li>Commercial assessment</li><li>Project preparation</li><li>Investment structuring</li><li>Engagement with potential capital providers, where appropriate</li></ul></div></div>
<p class="cie-contact reveal">Contact CIE directly at <a href="mailto:info@cie.co.zw">info@cie.co.zw</a>.</p><p class="note reveal">The two organisations have distinct mandates. Any referral from CIE to Chisi Capital Partners, or any next step, remains subject to assessment and applicable requirements.</p></div></section>"""
cie_cta = '<section class="cta" data-cta><div class="cta-media" data-parallax>' + img('cie-cta', 'A founder presenting her product idea to fellow entrepreneurs', 'cta-img') + '</div><div class="wrap cta-inner"><p class="eyebrow light">Whether you are at idea stage or already operating</p><h2 class="split" data-split>Have a business idea<br><em>worth exploring?</em></h2>' + button('Email info@cie.co.zw', 'mailto:info@cie.co.zw', 'light') + '</div></section>'
shell('cie', 'Centre for Impactful Entrepreneurs (CIE) | Chisi Capital Partners', 'The Centre for Impactful Entrepreneurs (CIE) mobilises entrepreneurial ideas and supports enterprise development and incubation in Zimbabwe.', cie_body + cie_cta)

legal = {
    'privacy-policy': ('Privacy notice', 'This static website does not send form entries to Chisi Capital Partners. The enquiry form creates a text file locally in your browser only when you choose to download it. Entries are not saved by this website.', 'If you telephone us, share only the information needed to discuss your enquiry. For questions about information you share directly, contact Chisi Capital Partners on 077 358 8945. Hosting providers may process technical request data to deliver the website. Fonts are loaded from Google Fonts; your browser connects to Google to request the font stylesheet and font files. A fuller privacy policy must be established before online enquiry collection is enabled.'),
    'cookie-policy': ('Cookies and local storage', 'This website does not intentionally set cookies, use analytics or advertising trackers, or store form data in browser storage.', 'The hosting platform may use technologies required to deliver and protect the website. External map links open Google Maps, which operates under its own policies.'),
    'terms': ('Website terms', 'This website provides general information about Chisi Capital Partners and its services. It is not an investment offer, a recommendation to invest, or a commitment to provide or arrange financing.', 'All engagements are subject to agreed mandates, commercial assessment, due diligence, applicable requirements and independent decisions by relevant partners. Collaboration with the Centre for Impactful Entrepreneurs does not guarantee acceptance or funding.'),
}
for slug, (title, p1, p2) in legal.items():
    shell(slug, title + ' | Chisi Capital Partners', title, hero('legal', 'Website information', title, '', '', plain_strip) + f'<div id="main-content"></div><section class="wrap legal section"><p>{p1}</p><p>{p2}</p><p>Last updated: 29 October 2026.</p></section>')

credits = hero('legal', 'Imagery', 'Imagery on this website', 'How the photographs on this website were made.', '', plain_strip) + '''<div id="main-content"></div><section class="wrap credits section"><p class="large">The photographs on this website are illustrative images created with Magnific AI and optimised as WebP files for fast loading.</p><p>They represent the people, places and sectors Chisi Capital Partners works with. The people shown are not Chisi Capital Partners staff, clients or partners, and the scenes do not depict specific Chisi projects.</p><p>Last updated: 29 October 2026.</p></section>'''
shell('photo-credits', 'Imagery | Chisi Capital Partners', 'Information about the illustrative imagery used on this website.', credits)
print('Generated eleven static pages.')
