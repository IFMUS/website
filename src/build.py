"""Builds the IFMUS static mockup.

Outputs:
  ../dist/<page>.html + ../dist/styles.css   multi-page static site (open dist/index.html)
  argv[1] (optional)               single-file preview with hash navigation
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "dist"
CSS = (HERE / "styles.css").read_text()

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700&display=swap">')

LOGO_SRC = (HERE / "brand" / "ifmus-logo.svg").read_text()
_logo_n = [0]


def logo():
    """Official logo (brand/ifmus-logo.svg), inlined and cropped to the artwork.
    Blue follows currentColor; the white halo around the people and the serpent follows --logo-halo."""
    _logo_n[0] += 1
    n = _logo_n[0]
    svg = LOGO_SRC[LOGO_SRC.index("<svg"):]
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r"#(?:285ba3|0a5ca8)", "currentColor", svg, flags=re.I)
    svg = re.sub(r"#(?:ffffff|f9f9f9)\b", "var(--logo-halo)", svg, flags=re.I)
    svg = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{m.group(1)}-{n}"', svg)
    svg = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{m.group(1)}-{n})", svg)
    svg = re.sub(r"<svg\b[^>]*>", '<svg class="logo" viewBox="8 31.5 143 96" aria-hidden="true">', svg, count=1)
    return re.sub(r">\s+<", "><", re.sub(r"\s+", " ", svg)).strip()


NAV = [("about", "About"), ("membership", "Membership"), ("education", "Education"),
       ("events", "Events"), ("research", "Research"), ("contact", "Contact")]

HERO_ART = '''<div class="hero-art">
<svg viewBox="0 0 400 400" role="img" aria-label="An ultrasound probe on a globe, with sound waves spreading out">
<defs><clipPath id="globe"><circle cx="200" cy="220" r="165"/></clipPath></defs>
<circle cx="200" cy="220" r="165" fill="var(--brand-soft)"/>
<g clip-path="url(#globe)" fill="none" stroke="var(--brand)" stroke-opacity="0.18" stroke-width="1.5">
<ellipse cx="200" cy="220" rx="70" ry="165"/><ellipse cx="200" cy="220" rx="130" ry="165"/>
<path d="M35 220h330M55 140h290M55 300h290"/></g>
<g transform="rotate(-38 200 220)">
<g fill="none" stroke-linecap="round" stroke-width="6">
<path class="wave" d="M166.4 105.7 A60 60 0 0 0 233.6 105.7" stroke="var(--accent)"/>
<path class="wave w2" d="M138.4 147.1 A110 110 0 0 0 261.6 147.1" stroke="var(--brand)"/>
<path class="wave w3" d="M110.5 188.5 A160 160 0 0 0 289.5 188.5" stroke="var(--brand)"/>
<path class="wave w4" d="M82.5 229.9 A210 210 0 0 0 317.5 229.9" stroke="var(--brand)"/>
</g>
<path d="M200 30 C200 14 214 6 226 6" fill="none" stroke="var(--fg)" stroke-opacity="0.35" stroke-width="3" stroke-linecap="round"/>
<rect x="170" y="28" width="60" height="32" rx="16" fill="var(--accent)"/>
</g>
</svg>
<span class="chip c1"><i>✓</i>Scan review</span>
<span class="chip c2"><i>▶</i>Free webinars</span>
<span class="chip c3"><i>♥</i>Mentoring</span>
</div>'''

PAGES = {}

PAGES["home"] = ("IFMUS", "home", f'''
<section class="band-warm hero"><div class="wrap">
  <div class="hero-copy">
    <p class="tagline">Advancing POCUS · Empowering clinicians · Improving care</p>
    <h1>Bringing point‑of‑care ultrasound into <span>family medicine</span></h1>
    <p class="lede">IFMUS is the international society for point-of-care ultrasound (POCUS) in family medicine. We bring together GPs, family physicians, educators and researchers who want ultrasound to become a routine part of primary care.</p>
    <div class="btn-row"><a class="btn btn-primary" href="@membership">Become a member</a><a class="btn btn-ghost" href="@about">About the society</a></div>
  </div>
  {HERO_ART}
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><p class="eyebrow">Our mission</p><h2>Learn. Connect. Teach. Research. Lead.</h2></div>
  <div class="verbs">
    <div class="verb"><strong>Learn</strong><p>Build your skills with a curated image library, step-by-step technique guides and regular webinars.</p></div>
    <div class="verb"><strong>Connect</strong><p>Join a network of family doctors who scan, and find a mentor when you need one.</p></div>
    <div class="verb"><strong>Teach</strong><p>Train as an accredited IFMUS instructor and pass your skills on to colleagues.</p></div>
    <div class="verb"><strong>Research</strong><p>Take part in multinational studies through our research network.</p></div>
    <div class="verb"><strong>Lead</strong><p>Set up and run an IFMUS clinical hub in your own region.</p></div>
  </div>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head"><p class="eyebrow">For members</p><h2>What you get as a member</h2><p class="lede">Membership costs €50 a year, or €25 for residents and for clinicians in low- and lower-middle-income countries.</p></div>
  <div class="grid-3">
    <a class="card card-link" href="@education"><span class="tag">Education</span><h3>Pathology image library</h3><p>Browse curated clinical cases, organised by organ system and finding.</p><span class="more">Explore education</span></a>
    <a class="card card-link" href="@education"><span class="tag">Education</span><h3>Expert scan review</h3><p>Send us anonymised clips and get feedback on both your technique and your interpretation.</p><span class="more">How scan review works</span></a>
    <a class="card card-link" href="@events"><span class="tag">Events</span><h3>Webinars and the annual conference</h3><p>Free access to every IFMUS webinar, plus 25% off our annual scientific conference.</p><span class="more">See upcoming events</span></a>
  </div>
</div></section>

<section class="band-warm section"><div class="wrap feature">
  <div class="stack"><p class="eyebrow">Clinical hubs</p><h2>Lead the way in your region</h2>
  <p class="lede">IFMUS clinical hubs are local centres for training, scan review and research. Each one is run by an IFMUS member who practises in the area.</p>
  <div class="btn-row"><a class="btn btn-primary" href="@about">How hubs work</a></div></div>
  <div class="stat-row">
    <div class="stat"><b>11</b><span>member benefits</span></div>
    <div class="stat"><b>€25</b><span>reduced annual fee</span></div>
    <div class="stat"><b>25%</b><span>off the annual conference</span></div>
  </div>
</div></section>
''')

PAGES["about"] = ("About IFMUS", "about", '''
<section class="band-warm page-hero"><div class="wrap">
  <p class="eyebrow">About</p><h1>A global home for ultrasound in primary care</h1>
  <p class="lede">IFMUS connects family doctors, educators, researchers and clinical leaders around the world who share one goal: making ultrasound part of everyday primary care.</p>
</div></section>

<section class="section"><div class="wrap grid-2">
  <div class="prose"><h2>Who we are</h2>
    <p>Point-of-care ultrasound lets a family doctor answer a focused clinical question in the consulting room. Is there free fluid? Is this pregnancy intrauterine? Is the aorta dilated? Is there a DVT? Used well, it leads to a faster, more accurate diagnosis and keeps care close to the patient.</p>
    <p>Most ultrasound societies are built around hospital specialties. IFMUS is the only international society devoted entirely to how POCUS is learned, taught, studied and practised in family medicine.</p>
  </div>
  <div class="prose"><h2>What we are working towards</h2>
    <ul class="checks">
      <li>A community that shares knowledge freely across countries and health systems.</li>
      <li>Closer collaboration between the clinicians, educators and researchers who use ultrasound in primary care.</li>
      <li>Shared standards that raise the quality of ultrasound training and patient care.</li>
    </ul>
    <p><strong>Together, we can advance POCUS and strengthen family medicine around the world.</strong></p>
  </div>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head"><p class="eyebrow">Clinical hubs</p><h2>Regional hubs, run by members</h2><p class="lede">A hub is a practice or training centre that hosts hands-on courses, coordinates scan review and supports local research. Any member can apply to lead a hub in their region.</p></div>
  <div class="grid-3">
    <div class="card"><span class="tag">Open call</span><h3>Europe</h3><p>Now accepting applications for hub directors.</p></div>
    <div class="card"><span class="tag">Open call</span><h3>Americas</h3><p>Now accepting applications for hub directors.</p></div>
    <div class="card"><span class="tag">Open call</span><h3>Africa</h3><p>Now accepting applications for hub directors.</p></div>
    <div class="card"><span class="tag">Open call</span><h3>Asia</h3><p>Now accepting applications for hub directors.</p></div>
    <div class="card"><span class="tag">Open call</span><h3>Middle East</h3><p>Now accepting applications for hub directors.</p></div>
    <div class="card"><span class="tag">Open call</span><h3>Oceania</h3><p>Now accepting applications for hub directors.</p></div>
  </div>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head"><p class="eyebrow">People</p><h2>Our officers</h2></div>
  <div class="people">
    <div class="person"><div class="avatar">EL</div><h3>Eva Leceaga-Gaztambide</h3><p>Membership Officer</p></div>
    <div class="person"><div class="avatar">?</div><h3>To be announced</h3><p>President</p></div>
    <div class="person"><div class="avatar">?</div><h3>To be announced</h3><p>Education Lead</p></div>
    <div class="person"><div class="avatar">?</div><h3>To be announced</h3><p>Research Lead</p></div>
  </div>
</div></section>
''')

BENEFITS = [
    ("Educational resources", [
        (1, "Online pathology image library", "Learn from a curated collection of real clinical cases."),
        (2, "Scanning technique guides", "Step-by-step guidance on image acquisition from experts around the world."),
        (3, "Research updates", "Regular summaries of new POCUS publications, so you stay up to date."),
        (4, "Free webinars", "Live teaching sessions with international specialists."),
        (6, "Expert scan review", "Feedback on your own scans, covering both technique and interpretation."),
    ]),
    ("Professional development", [
        (5, "Mentoring and peer support", "Guidance from experienced colleagues who understand the challenges you face."),
        (7, "Instructor accreditation", "Become an accredited IFMUS POCUS instructor and build your teaching credentials."),
        (8, "Research network", "Join the IFMUS researcher network and collaborate on international studies."),
    ]),
    ("Leadership", [
        (9, "Clinical hub director", "Lead the development of ultrasound in your region."),
        (10, "International educator", "Teach for IFMUS and share your expertise with colleagues worldwide."),
    ]),
    ("Conference", [
        (11, "25% conference discount", "A reduced fee for the IFMUS annual scientific conference."),
    ]),
]
benefit_html = "".join(
    f'<div class="benefit-group"><h3>{g}</h3><ol class="benefits">'
    + "".join(f'<li><span class="n">{n}</span><div><strong>{t}</strong><span>{d}</span></div></li>' for n, t, d in items)
    + "</ol></div>" for g, items in BENEFITS)

PAGES["membership"] = ("Membership", "membership", f'''
<section class="band-warm page-hero"><div class="wrap">
  <p class="eyebrow">Membership</p><h1>Join the International Family Medicine Ultrasound Society</h1>
  <p class="lede">Membership runs for twelve months from the date we receive your payment and renews automatically. Signing up takes about three minutes.</p>
  <div class="btn-row"><a class="btn btn-primary" href="@join">Join now</a></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><p class="eyebrow">Fees</p><h2>Annual membership fees</h2></div>
  <div class="fees">
    <div class="fee featured"><h3>Standard</h3><div class="price">€50 <small>/ year</small></div><p>For practising family doctors and other primary care clinicians.</p><a class="btn btn-primary" href="@join">Join as a standard member</a></div>
    <div class="fee"><h3>Resident</h3><div class="price">€25 <small>/ year</small></div><p>For doctors currently in family medicine or GP specialty training.</p><a class="btn btn-ghost" href="@join">Join as a resident</a></div>
    <div class="fee"><h3>Reduced rate</h3><div class="price">€25 <small>/ year</small>*</div><p>For clinicians practising in a low- or lower-middle-income country.</p><a class="btn btn-ghost" href="@join">Join at reduced rate</a></div>
  </div>
  <p class="footnote">* Eligibility is based on the World Bank’s classification of low-income and lower-middle-income economies.</p>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head"><p class="eyebrow">Benefits</p><h2>Membership benefits</h2></div>
  <div class="benefit-groups">{benefit_html}</div>
</div></section>

<section class="band-warm section"><div class="wrap grid-2">
  <div class="stack"><p class="eyebrow">After you join</p><h2>What happens next</h2><p class="lede">As soon as your payment is confirmed, you will receive:</p></div>
  <ul class="checks">
    <li>Your IFMUS membership certificate</li>
    <li>Access to the members’ portal</li>
    <li>Invitations to upcoming webinars and events</li>
    <li>A monthly digest of new research and publications</li>
    <li>An invitation to join the working groups that match your interests</li>
  </ul>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><p class="eyebrow">Questions</p><h2>Frequently asked questions</h2></div>
  <div class="faq">
    <details><summary>Who can join?</summary><p>Membership is open to family medicine and primary care professionals, trainees, researchers and educators with an interest in point-of-care ultrasound. You don’t need to be scanning already.</p></details>
    <details><summary>How do I qualify for the reduced rate?</summary><p>The €25 rate applies to doctors in family medicine training and to clinicians practising in a country the World Bank classifies as low-income or lower-middle-income.</p></details>
    <details><summary>How do I pay?</summary><p>We take payments securely through PayPal. Your membership starts on the day we receive your payment.</p></details>
    <details><summary>Can I cancel the automatic renewal?</summary><p>Yes. Just contact our Membership Officer before your renewal date and we will cancel it.</p></details>
  </div>
</div></section>
''')

PAGES["join"] = ("Join IFMUS", "membership", '''
<section class="band-warm page-hero"><div class="wrap">
  <p class="eyebrow">Membership</p><h1>Join IFMUS</h1>
  <p class="lede">It only takes three steps. Your membership runs for twelve months from the date we receive your payment.</p>
</div></section>
<section class="section"><div class="wrap stack" style="gap:2.5rem">
  <ol class="steps">
    <li><h3>Tell us about you</h3><p>Your name, country, practice setting and membership type.</p></li>
    <li><h3>Pay securely</h3><p>Pay your annual fee through PayPal.</p></li>
    <li><h3>Get your certificate</h3><p>We email your certificate and your login for the members’ portal.</p></li>
  </ol>
  <form class="form js-demo-form" style="max-width:40rem">
    <div class="grid-2">
      <div class="field"><label for="j-first">First name</label><input id="j-first" value="Ana"></div>
      <div class="field"><label for="j-last">Surname</label><input id="j-last" value="Example"></div>
    </div>
    <div class="field"><label for="j-email">Email</label><input id="j-email" type="email" value="ana@example.org"></div>
    <div class="grid-2">
      <div class="field"><label for="j-country">Country of practice</label><input id="j-country" value="Spain"></div>
      <div class="field"><label for="j-cat">Membership type</label><select id="j-cat"><option>Standard, €50 / year</option><option>Resident, €25 / year</option><option>Reduced rate, €25 / year</option></select></div>
    </div>
    <div class="field"><label for="j-setting">Practice setting</label><select id="j-setting"><option>Urban family practice</option><option>Rural family practice</option><option>Academic / teaching practice</option><option>GP / family medicine training</option></select></div>
    <div class="btn-row"><button class="btn btn-primary" type="submit">Continue to PayPal</button></div>
    <p class="form-status" role="status" aria-live="polite"></p>
  </form>
  <p class="footnote">The form is pre-filled with example details for this mockup. The PayPal link is still a placeholder.</p>
</div></section>
''')

SCANS = [("Gallbladder", "Cholelithiasis with acoustic shadow", "50%", "60%"),
         ("Lung", "B-lines in heart failure", "35%", "40%"),
         ("Aorta", "Infrarenal AAA, 4.2 cm", "50%", "50%"),
         ("Kidney", "Moderate hydronephrosis", "60%", "55%"),
         ("Leg veins", "Non-compressible common femoral vein", "45%", "45%"),
         ("Early pregnancy", "Intrauterine gestational sac", "50%", "40%"),
         ("Thyroid", "Solid nodule, TI-RADS 4", "40%", "55%"),
         ("Knee", "Baker's cyst", "55%", "60%")]
scan_html = "".join(
    f'<figure class="scan"><div class="scan-img" style="--x:{x};--y:{y}"><span class="label">{a.upper()}</span><span class="lock">Members</span></div>'
    f'<figcaption><strong>{a}</strong>{f}</figcaption></figure>' for a, f, x, y in SCANS)

PAGES["education"] = ("Education", "education", f'''
<section class="band-warm page-hero"><div class="wrap">
  <p class="eyebrow">Education</p><h1>Learn to scan, and keep improving</h1>
  <p class="lede">Members get free access to our image library, technique guides, webinars and expert scan review.</p>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><p class="eyebrow">Pathology image library</p><h2>Real cases from primary care</h2><p class="lede">Each case pairs the clinical question with the image and a short teaching point. The library is available to members only.</p></div>
  <div class="scans">{scan_html}</div>
  <p class="footnote">These images are placeholders until the library content is ready.</p>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head"><p class="eyebrow">Technique guides</p><h2>Getting the image, step by step</h2><p class="lede">Each guide covers probe selection, patient positioning, the standard views and the most common pitfalls.</p></div>
  <div class="grid-3">
    <div class="card"><span class="tag">Chest</span><h3>Lung</h3><p>A-lines, B-lines, pleural effusion, and ruling out pneumothorax using lung sliding.</p></div>
    <div class="card"><span class="tag">Cardiac</span><h3>Focused cardiac</h3><p>Parasternal, apical and subcostal views to assess LV function and pericardial effusion.</p></div>
    <div class="card"><span class="tag">Abdomen</span><h3>Aorta and biliary</h3><p>AAA screening, gallstones and the right upper quadrant.</p></div>
    <div class="card"><span class="tag">Vascular</span><h3>DVT two-point compression</h3><p>Compression of the common femoral and popliteal veins in the clinic.</p></div>
    <div class="card"><span class="tag">Women's health</span><h3>Early pregnancy</h3><p>Confirming an intrauterine pregnancy and measuring crown–rump length.</p></div>
    <div class="card"><span class="tag">MSK</span><h3>Musculoskeletal</h3><p>Shoulders, knees and the soft-tissue lumps that family doctors see every week.</p></div>
  </div>
</div></section>

<section class="band-warm section"><div class="wrap grid-2">
  <div class="stack"><p class="eyebrow">Scan review</p><h2>Expert feedback on your own scans</h2>
  <p class="lede">Upload anonymised clips through the members’ portal. An IFMUS educator will review both the image quality and your interpretation, then send you practical teaching points.</p></div>
  <ol class="steps" style="grid-template-columns:1fr">
    <li><h3>Upload</h3><p>Share an anonymised clip along with your clinical question.</p></li>
    <li><h3>Review</h3><p>An IFMUS educator assesses how the image was acquired and interpreted.</p></li>
    <li><h3>Feedback</h3><p>You receive written teaching points to apply to your next scan.</p></li>
  </ol>
</div></section>

<section class="section"><div class="wrap grid-2">
  <div class="card"><span class="tag">Teaching</span><h3>Accredited IFMUS POCUS instructor</h3><p>Members who scan regularly can apply for accreditation and teach IFMUS courses in their region. The accreditation criteria are currently being finalised.</p></div>
  <div class="card"><span class="tag">Teaching</span><h3>International IFMUS educator</h3><p>Experienced instructors can lead webinars and courses for members worldwide and help new clinical hubs get started.</p></div>
</div></section>
''')

PAGES["events"] = ("Events", "events", '''
<section class="band-warm page-hero"><div class="wrap">
  <p class="eyebrow">Events</p><h1>Webinars, courses and the annual conference</h1>
  <p class="lede">Webinars are free for members, who also receive 25% off the IFMUS annual scientific conference.</p>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><p class="eyebrow">Annual scientific conference</p><h2>IFMUS Conference 2027</h2><p class="lede">Hands-on workshops, original research and the people shaping POCUS in family medicine. Dates and venue to be announced.</p></div>
  <div class="card" style="max-width:40rem"><h3>Register your interest</h3><p>We’ll email you as soon as registration opens. Members receive 25% off the conference fee.</p><div class="btn-row"><a class="btn btn-primary" href="@contact">Register your interest</a></div></div>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head"><p class="eyebrow">Upcoming webinars</p><h2>Learn from international specialists</h2><span class="sample-note">Example listings for this mockup</span></div>
  <div class="events">
    <article class="event"><time datetime="2026-11-12"><b>12</b><span>Nov</span></time><div><h3>Lung ultrasound in the community</h3><p>B-lines, effusions and pneumothorax. Online, 19:00 CET, 60 minutes.</p></div><a class="btn btn-ghost" href="@membership">Free for members</a></article>
    <article class="event"><time datetime="2026-12-03"><b>3</b><span>Dec</span></time><div><h3>Early pregnancy scanning in general practice</h3><p>How to confirm an intrauterine pregnancy safely. Online, 19:00 CET, 60 minutes.</p></div><a class="btn btn-ghost" href="@membership">Free for members</a></article>
    <article class="event"><time datetime="2027-01-21"><b>21</b><span>Jan</span></time><div><h3>Two-point compression for DVT</h3><p>Technique, pitfalls and when to refer. Online, 19:00 CET, 45 minutes.</p></div><a class="btn btn-ghost" href="@membership">Free for members</a></article>
    <article class="event"><time datetime="2027-02-18"><b>18</b><span>Feb</span></time><div><h3>Building a POCUS curriculum for GP trainees</h3><p>For programme directors and educators. Online, 19:00 CET, 75 minutes.</p></div><a class="btn btn-ghost" href="@membership">Free for members</a></article>
  </div>
</div></section>
''')

PAGES["research"] = ("Research", "research", '''
<section class="band-warm page-hero"><div class="wrap">
  <p class="eyebrow">Research</p><h1>Building the evidence for POCUS in primary care</h1>
  <p class="lede">The IFMUS researcher network connects members who want to study how ultrasound affects diagnosis, referrals and patient outcomes in family medicine.</p>
</div></section>

<section class="section"><div class="wrap grid-2">
  <div class="prose"><h2>Researcher network</h2>
    <p>Multinational studies depend on recruiting sites. The network puts members who have a research question in touch with practices that can recruit patients, and with colleagues who have experience in study design and statistics.</p>
    <ul class="checks"><li>Find collaborators and recruiting sites in other countries</li><li>Share protocols, data collection forms and ethics templates</li><li>Present your work at the annual scientific conference</li></ul>
    <div class="btn-row"><a class="btn btn-primary" href="@membership">Become a member to take part</a></div>
  </div>
  <div class="prose"><h2>Publication updates</h2>
    <p>Every month, members receive a digest of new POCUS research relevant to family medicine, with a short summary of what each paper means for everyday practice.</p>
    <div class="card"><span class="tag">Monthly digest</span><h3>What the digest covers</h3><p>Diagnostic accuracy studies, research on education and training, implementation in primary care, and new guidelines from ultrasound and family medicine organisations.</p></div>
  </div>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head"><p class="eyebrow">Working groups</p><h2>Proposed working groups</h2><p class="lede">New members are invited to join the groups that match their interests.</p></div>
  <div class="grid-3">
    <div class="card"><h3>Education standards</h3><p>Shared curricula and competency assessment for POCUS in family medicine.</p></div>
    <div class="card"><h3>Clinical impact</h3><p>How POCUS affects diagnosis, referrals and patient outcomes in primary care.</p></div>
    <div class="card"><h3>Global access</h3><p>Ultrasound in rural and low-resource settings, including the use of handheld devices.</p></div>
  </div>
</div></section>
''')

PAGES["contact"] = ("Contact", "contact", '''
<section class="band-warm page-hero"><div class="wrap">
  <p class="eyebrow">Contact</p><h1>Get in touch</h1>
  <p class="lede">Whether your question is about membership, education, events or research, we’re happy to help.</p>
</div></section>
<section class="section"><div class="wrap grid-2">
  <dl class="contact-list">
    <div><dt>Membership</dt><dd>Eva Leceaga-Gaztambide, Membership Officer</dd></div>
    <div><dt>Email</dt><dd><span class="placeholder">[INSERT EMAIL]</span></dd></div>
    <div><dt>Website</dt><dd><span class="placeholder">[INSERT WEBSITE]</span></dd></div>
  </dl>
  <form class="form js-demo-form">
    <div class="field"><label for="c-name">Name</label><input id="c-name" autocomplete="name"></div>
    <div class="field"><label for="c-email">Email</label><input id="c-email" type="email" autocomplete="email"></div>
    <div class="field"><label for="c-topic">Topic</label><select id="c-topic"><option>Membership</option><option>Education and scan review</option><option>Events and the conference</option><option>Research collaboration</option><option>Clinical hubs</option></select></div>
    <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" rows="5"></textarea></div>
    <div class="btn-row"><button class="btn btn-primary" type="submit">Send message</button></div>
    <p class="form-status" role="status" aria-live="polite"></p>
  </form>
</div></section>
''')

ORDER = ["home", "about", "membership", "join", "education", "events", "research", "contact"]


CUR = ' aria-current="page"'


def header(active):
    links = "".join(
        f'<a href="@{k}"{CUR if k == active else ""} data-nav="{k}">{label}</a>'
        for k, label in NAV)
    return f'''<header class="site-header"><div class="wrap">
<a class="brand" href="@home">{logo()}<span class="brand-name">International<br>Family Medicine<br>Ultrasound Society</span></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
<nav class="nav" id="nav" aria-label="Main">{links}<a class="btn btn-primary" href="@join">Join IFMUS</a></nav>
</div></header>'''


FOOTER = '''<section class="cta"><div class="wrap"><h2>Join family doctors around the world who are bringing ultrasound into their practice.</h2><a class="btn btn-accent" href="@join">Become a member</a></div></section>
<footer class="site-footer"><div class="wrap">
<div><a class="brand" href="@home">''' + logo() + '''<span class="brand-name">International<br>Family Medicine<br>Ultrasound Society</span></a>
<p style="margin-top:1rem;max-width:22rem">Together, we can advance POCUS and strengthen family medicine around the world.</p>
<p class="motto">Learn. Connect. Teach. Research. Lead.</p></div>
<div><h3>Society</h3><ul><li><a href="@about">About</a></li><li><a href="@membership">Membership</a></li><li><a href="@contact">Contact</a></li></ul></div>
<div><h3>Members</h3><ul><li><a href="@education">Education</a></li><li><a href="@events">Events</a></li><li><a href="@research">Research</a></li></ul></div>
<p class="legal">© 2026 International Family Medicine Ultrasound Society · Prototype. Content subject to change.</p>
</div></footer>'''

SCRIPT = '''<script>
(function () {
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  if (btn) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open'); btn.setAttribute('aria-expanded', open);
  });
  document.addEventListener('submit', function (e) {
    var f = e.target; if (!f.classList.contains('js-demo-form')) return;
    e.preventDefault();
    f.querySelector('.form-status').textContent = 'This is a prototype, so nothing was sent.';
  });
  __ROUTER__
})();
</script>'''

ROUTER = '''var pages = document.querySelectorAll('[data-page]');
  var navOf = { join: 'membership' };
  function show() {
    var id = (location.hash || '#home').slice(1);
    if (!document.querySelector('[data-page="' + id + '"]')) id = 'home';
    pages.forEach(function (p) { p.hidden = p.dataset.page !== id; });
    var active = navOf[id] || id;
    document.querySelectorAll('[data-nav]').forEach(function (a) {
      if (a.dataset.nav === active) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    nav.classList.remove('open'); btn.setAttribute('aria-expanded', 'false');
    window.scrollTo(0, 0);
  }
  window.addEventListener('hashchange', show); show();'''


def links(html, mode):
    def sub(m):
        k = m.group(1)
        if mode == "multi":
            return 'href="' + ("index" if k == "home" else k) + '.html"'
        return f'href="#{k}"'
    return re.sub(r'href="@(\w+)"', sub, html)


def build_multi():
    OUT.mkdir(exist_ok=True)
    for key in ORDER:
        title, active, body = PAGES[key]
        full_title = "IFMUS" if key == "home" else f"{title} · IFMUS"
        html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{full_title}</title>{FONTS}<link rel="stylesheet" href="styles.css"></head>
<body>{header(active)}<main>{body}</main>{FOOTER}{SCRIPT.replace("__ROUTER__", "")}</body></html>
'''
        name = "index" if key == "home" else key
        (OUT / f"{name}.html").write_text(links(html, "multi"))
    (OUT / "styles.css").write_text(CSS)


def build_preview(path):
    mains = "".join(f'<main data-page="{k}"{" hidden" if k != "home" else ""}>{PAGES[k][2]}</main>' for k in ORDER)
    html = (f'<title>IFMUS Website</title>{FONTS}<style>{CSS}</style>'
            f'{header("none")}{mains}{FOOTER}{SCRIPT.replace("__ROUTER__", ROUTER)}')
    pathlib.Path(path).write_text(links(html, "preview"))


build_multi()
if len(sys.argv) > 1:
    build_preview(sys.argv[1])
