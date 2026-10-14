"""Generates the four EquaLex pages (EN/DE home + legal notice) from one template."""
import os, sys, hashlib
ROOT = sys.argv[1]
CSS_V = hashlib.sha1(open(os.path.join(ROOT, "assets/style.css"), "rb").read()).hexdigest()[:8]

MARK = ('<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
        '<rect x="3" y="9" width="26" height="4.5" rx="0.5" fill="#d9b866"/>'
        '<rect x="3" y="18.5" width="26" height="4.5" rx="0.5" fill="#d9b866"/></svg>')

def head(lang, title, desc, base, noindex=False):
    alt = ('<link rel="alternate" hreflang="en" href="https://equalex.com/">\n'
           '<link rel="alternate" hreflang="de" href="https://equalex.com/de/">\n'
           '<link rel="alternate" hreflang="x-default" href="https://equalex.com/">\n') if not noindex else '<meta name="robots" content="noindex">\n'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#13233f">
{alt}<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{base}assets/fonts/source-serif-4-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{base}assets/style.css?v={CSS_V}">
</head>
<body>
'''

def header(t, home, nav):
    items = "\n".join(f'        <li{" class=\"lang\"" if c else ""}><a href="{h}"{a}>{l}</a></li>' for l, h, c, a in nav)
    return f'''<a class="skip" href="#main">{t["skip"]}</a>
<div class="band">
<header class="site-header">
  <div class="wrap">
    <a class="wordmark" href="{home}" aria-label="EquaLex – {t["home"]}">{MARK}<span>EquaLex</span></a>
    <nav class="site-nav" aria-label="{t["navlabel"]}">
      <ul>
{items}
      </ul>
    </nav>
  </div>
</header>
'''

def footer(t, legal_href, legal_label):
    return f'''<footer class="site-footer">
  <div class="wrap">
    <p>© 2026 EquaLex GmbH</p>
    <p><a href="{legal_href}">{legal_label}</a></p>
  </div>
</footer>
</body>
</html>
'''

def home(t, base, other_lang):
    nav = [(t["nav_services"], "#" + t["id_services"], False, ""),
           (t["nav_about"], "#" + t["id_about"], False, ""),
           (t["nav_contact"], "#" + t["id_contact"], False, ""),
           other_lang]
    services = "\n".join(f'''        <li>
          <h3>{h}</h3>
          <p>{p}</p>
        </li>''' for h, p in t["services"])
    fw = "\n".join(f'        <li><span class="name">{n}</span><span class="scope">{s}</span></li>' for n, s in t["frameworks"])
    roles = "\n".join(f"            <li>{r}</li>" for r in t["roles"])
    return (head(t["lang"], t["title"], t["desc"], base) + header(t, "./", nav) + f'''<main id="main">
  <div class="wrap hero">
    <div>
      <h1>{t["h1"]}</h1>
      <p class="intro">{t["intro"]}</p>
      <a class="button" href="#{t["id_contact"]}">{t["cta"]}</a>
    </div>
    <figure>
      <img src="{base}assets/img/richard-whittle-2026.jpg" alt="{t["portrait_alt"]}" width="600" height="600">
      <figcaption><strong>Richard Whittle</strong>{t["caption"]}</figcaption>
    </figure>
  </div>
</div>

  <section id="{t["id_services"]}" aria-labelledby="services-h">
    <div class="wrap">
      <h2 id="services-h">{t["nav_services"]}</h2>
      <ul class="services">
{services}
      </ul>
    </div>
  </section>

  <section aria-labelledby="frameworks-h">
    <div class="wrap">
      <h2 id="frameworks-h">{t["fw_h"]}</h2>
      <p class="lead">{t["fw_lead"]}</p>
      <ul class="frameworks">
{fw}
      </ul>
    </div>
  </section>

  <section id="{t["id_about"]}" aria-labelledby="about-h">
    <div class="wrap">
      <h2 id="about-h">{t["nav_about"]}</h2>
      <div class="bio">
        <p>{t["bio1"]}</p>
        <p>{t["bio2"]}</p>
        <ul>
{roles}
        </ul>
        <p>{t["bio3"]}</p>
      </div>
    </div>
  </section>

  <section id="{t["id_contact"]}" class="contact" aria-labelledby="contact-h">
    <div class="wrap">
      <h2 id="contact-h">{t["nav_contact"]}</h2>
      <p class="lead">{t["contact_lead"]}</p>
      <dl>
        <dt>{t["email_label"]}</dt>
        <dd><a class="email" href="mailto:richard.whittle@equalex.com">richard.whittle@<wbr>equalex.com</a></dd>
        <dt>{t["loc_label"]}</dt>
        <dd>{t["loc"]}</dd>
      </dl>
    </div>
  </section>
</main>
''' + footer(t, "impressum.html", t["legal_label"]))

def legal(t, base, other_lang):
    nav = [(t["nav_home"], "./", False, ""), other_lang]
    return (head(t["lang"], t["legal_title"], t["legal_title"], base, noindex=True) + header(t, "./", nav) + "</div>\n" + f'''<main id="main">
  <div class="wrap legal">
{t["legal_body"]}
  </div>
</main>
''' + footer(t, "./", t["back"]))

EN = dict(
    lang="en", title="EquaLex – Disability equality law consultancy",
    desc="EquaLex is a Swiss consultancy advising businesses, public bodies and NGOs on disability equality law and policy.",
    skip="Skip to content", home="home", navlabel="Main", nav_home="Home",
    nav_services="Services", nav_about="About", nav_contact="Contact",
    id_services="services", id_about="about", id_contact="contact",
    h1="Advice on disability equality law for organisations that want to get it right",
    intro="EquaLex is a consultancy based in Zurich. We help businesses, public bodies and non-governmental organisations understand their obligations under disability equality law and turn them into practical, meaningful compliance.",
    cta="Get in touch", portrait_alt="Portrait of Richard Whittle",
    caption="Managing Partner. Teaching and advising on disability law since 1995.",
    services=[
        ("Legal and compliance advice", "Reviewing policies, products and services against disability equality law, and advising on the steps needed for compliance that works for disabled people in practice."),
        ("Policy and organisational consulting", "Advising public bodies and NGOs on the design and application of disability law and policy, including project management for implementation."),
        ("Training", "Training for judges, prosecutors, legal professionals and staff on disability law, with particular attention to the requirements of international law."),
        ("The disability market", "Helping businesses understand disabled people as customers and employees, and build accessibility into how they operate."),
        ("Corporate services", "In addition to consultancy, EquaLex accepts fiduciary mandates for companies. Please contact us to discuss your requirements."),
    ],
    fw_h="Legal frameworks we work with",
    fw_lead="Our advice draws on international, European and national law, so organisations working across borders get one consistent picture.",
    frameworks=[
        ("UN Convention on the Rights of Persons with Disabilities", "International"),
        ("EU equality law, including the European Accessibility Act", "European Union"),
        ("Disability Equality Act (BehiG)", "Switzerland"),
        ("Equality Act 2010", "United Kingdom"),
    ],
    bio1="Richard Whittle founded EquaLex after a long career as a legal academic in the UK, specialising in EU equality law, comparative disability law and international human rights law and policy. He has lectured in law since 1995, most recently as Senior Lecturer at Sheffield Hallam University.",
    bio2="Throughout that time he has advised public bodies and NGOs at national and international level on the design and application of disability law, and advised businesses on meaningful compliance. His roles have included:",
    roles=[
        "Expert adviser to the British Disability Rights Commission (now the Equality and Human Rights Commission)",
        "Expert adviser to the European Disability Forum",
        "Member of the European Commission’s group of experts on combating discrimination on grounds of disability",
        "Assisting in the drafting of the first European Union law prohibiting disability discrimination",
    ],
    bio3="Richard regularly trains members of the judiciary and senior public prosecutors on disability law, and lectures on the disability programmes of the Academy of European Law (ERA).",
    contact_lead="For an initial conversation about your organisation’s needs, please email us.",
    email_label="Email", loc_label="Location", loc="Regensdorf, Zurich, Switzerland",
    legal_label="Legal notice", legal_title="Legal notice – EquaLex", back="Back to home",
    legal_body='''    <h1>Legal notice</h1>
    <h2>Company</h2>
    <address>EquaLex GmbH (EquaLex LLC)<br>Riedthofstrasse 214<br>8105 Regensdorf<br>Switzerland</address>
    <h2>Contact</h2>
    <p>Email: <a href="mailto:richard.whittle@equalex.com">richard.whittle@equalex.com</a></p>
    <h2>Registration</h2>
    <p>Registered in the commercial register of the Canton of Zurich.<br>UID: CHE-201.369.986</p>
    <h2>Responsible for content</h2>
    <p>Richard Whittle, Managing Partner</p>
    <h2>Privacy</h2>
    <p>This website does not use cookies, analytics or tracking, and loads no content from third parties. It is hosted on GitHub Pages; GitHub may log visitors’ IP addresses for security purposes. If you contact us by email, we use your details only to respond to your enquiry.</p>
    <h2>Disclaimer</h2>
    <p>The information on this website is provided for general information only and does not constitute legal advice.</p>''',
)

DE = dict(
    lang="de", title="EquaLex – Beratung im Behindertengleichstellungsrecht",
    desc="EquaLex ist ein Schweizer Beratungsunternehmen für Unternehmen, Behörden und NGOs im Bereich Gleichstellungsrecht für Menschen mit Behinderungen.",
    skip="Zum Inhalt springen", home="Startseite", navlabel="Hauptnavigation", nav_home="Startseite",
    nav_services="Leistungen", nav_about="Über uns", nav_contact="Kontakt",
    id_services="leistungen", id_about="ueber-uns", id_contact="kontakt",
    h1="Beratung im Gleichstellungsrecht für Menschen mit Behinderungen",
    intro="EquaLex ist ein Beratungsunternehmen mit Sitz im Kanton Zürich. Wir unterstützen Unternehmen, Behörden und Nichtregierungsorganisationen dabei, ihre Pflichten aus dem Behindertengleichstellungsrecht zu verstehen und wirksam umzusetzen.",
    cta="Kontakt aufnehmen", portrait_alt="Porträt von Richard Whittle",
    caption="Managing Partner. Lehre und Beratung im Behindertenrecht seit 1995.",
    services=[
        ("Rechts- und Compliance-Beratung", "Prüfung von Richtlinien, Produkten und Dienstleistungen anhand des Behindertengleichstellungsrechts sowie Beratung zu den Schritten, die eine in der Praxis wirksame Umsetzung ermöglichen."),
        ("Politik- und Organisationsberatung", "Beratung von Behörden und NGOs bei der Gestaltung und Anwendung von Recht und Politik im Behindertenbereich, einschließlich Projektmanagement bei der Umsetzung."),
        ("Weiterbildung", "Schulungen für Richterinnen und Richter, Staatsanwaltschaften, Juristinnen und Juristen sowie Mitarbeitende zum Behindertenrecht, mit besonderem Augenmerk auf die Anforderungen des Völkerrechts."),
        ("Menschen mit Behinderungen als Zielgruppe", "Unterstützung von Unternehmen dabei, Menschen mit Behinderungen als Kundschaft und Mitarbeitende zu verstehen und Barrierefreiheit in ihre Abläufe einzubauen."),
        ("Unternehmensdienstleistungen", "Neben der Beratung übernimmt EquaLex Treuhandmandate für Unternehmen. Bitte kontaktieren Sie uns, um Ihre Anforderungen zu besprechen."),
    ],
    fw_h="Rechtsgrundlagen, mit denen wir arbeiten",
    fw_lead="Unsere Beratung stützt sich auf internationales, europäisches und nationales Recht. So erhalten grenzüberschreitend tätige Organisationen ein einheitliches Bild.",
    frameworks=[
        ("UN-Behindertenrechtskonvention (UN-BRK)", "International"),
        ("EU-Gleichstellungsrecht, einschließlich des European Accessibility Act", "Europäische Union"),
        ("Behindertengleichstellungsgesetz (BehiG)", "Schweiz"),
        ("Equality Act 2010", "Vereinigtes Königreich"),
    ],
    bio1="Richard Whittle gründete EquaLex nach einer langen Laufbahn als Rechtswissenschaftler im Vereinigten Königreich, spezialisiert auf EU-Gleichstellungsrecht, rechtsvergleichendes Behindertenrecht sowie internationales Menschenrecht und Politik. Seit 1995 lehrt er Recht an Universitäten, zuletzt als Senior Lecturer an der Sheffield Hallam University.",
    bio2="In dieser Zeit beriet er Behörden und NGOs auf nationaler und internationaler Ebene bei der Gestaltung und Anwendung des Behindertenrechts sowie Unternehmen bei einer wirksamen Umsetzung. Zu seinen Funktionen gehörten:",
    roles=[
        "Fachberater der britischen Disability Rights Commission (heute Equality and Human Rights Commission)",
        "Fachberater des Europäischen Behindertenforums (European Disability Forum)",
        "Mitglied der Expertengruppe der Europäischen Kommission zur Bekämpfung von Diskriminierung aufgrund einer Behinderung",
        "Mitwirkung an der Ausarbeitung des ersten EU-Rechtsakts, der Diskriminierung aufgrund einer Behinderung verbietet",
    ],
    bio3="Er schult regelmäßig Mitglieder der Justiz und leitende Staatsanwältinnen und Staatsanwälte im Behindertenrecht und unterrichtet in den Programmen der Europäischen Rechtsakademie (ERA) zum Behindertenrecht.",
    contact_lead="Für ein erstes Gespräch über die Anliegen Ihrer Organisation schreiben Sie uns bitte eine E-Mail.",
    email_label="E-Mail", loc_label="Standort", loc="Regensdorf, Kanton Zürich, Schweiz",
    legal_label="Impressum", legal_title="Impressum – EquaLex", back="Zur Startseite",
    legal_body='''    <h1>Impressum</h1>
    <h2>Unternehmen</h2>
    <address>EquaLex GmbH<br>Riedthofstrasse 214<br>8105 Regensdorf<br>Schweiz</address>
    <h2>Kontakt</h2>
    <p>E-Mail: <a href="mailto:richard.whittle@equalex.com">richard.whittle@equalex.com</a></p>
    <h2>Handelsregister</h2>
    <p>Eingetragen im Handelsregister des Kantons Zürich.<br>UID: CHE-201.369.986</p>
    <h2>Verantwortlich für den Inhalt</h2>
    <p>Richard Whittle, Managing Partner</p>
    <h2>Datenschutz</h2>
    <p>Diese Website verwendet keine Cookies, keine Analyse- oder Trackingdienste und lädt keine Inhalte von Dritten. Sie wird über GitHub Pages bereitgestellt; GitHub kann IP-Adressen der Besucherinnen und Besucher zu Sicherheitszwecken protokollieren. Wenn Sie uns per E-Mail kontaktieren, verwenden wir Ihre Angaben ausschließlich zur Beantwortung Ihrer Anfrage.</p>
    <h2>Haftungsausschluss</h2>
    <p>Die Informationen auf dieser Website dienen ausschließlich der allgemeinen Information und stellen keine Rechtsberatung dar.</p>''',
)

to_de = ("Deutsch", "de/", True, ' hreflang="de" lang="de"')
to_en = ("English", "../", True, ' hreflang="en" lang="en"')
files = {
    "index.html": home(EN, "", to_de),
    "impressum.html": legal(EN, "", ("Deutsch", "de/impressum.html", True, ' hreflang="de" lang="de"')),
    "de/index.html": home(DE, "../", to_en),
    "de/impressum.html": legal(DE, "../", ("English", "../impressum.html", True, ' hreflang="en" lang="en"')),
}
for p, s in files.items():
    with open(os.path.join(ROOT, p), "w") as f:
        f.write(s)

with open(os.path.join(ROOT, "assets/favicon.svg"), "w") as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="4" fill="#13233f"/>'
            '<rect x="6" y="10" width="20" height="4" fill="#d9b866"/><rect x="6" y="18" width="20" height="4" fill="#d9b866"/></svg>\n')
print("built", list(files))
