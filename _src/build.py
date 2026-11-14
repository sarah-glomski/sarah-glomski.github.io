"""Builds the static site from the files in _src/.

Run from anywhere:  python3 _src/build.py
Edit content in _src/ (projects.json, research.json, about.html, projects/*.html),
then rebuild. Generated pages: index.html, research.html, about.html, resume.html,
projects/*.html.
"""
import json
import os
from datetime import date
from html import escape

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(SRC)

SITE = {
    "name": "Sarah Glomski",
    "email": "glomski@stanford.edu",
    "linkedin": "https://www.linkedin.com/in/sarah-glomski/",
    "resume": "files/Sarah-Glomski-Resume.pdf",
    "description": "Sarah Glomski is a Mechanical Engineering PhD student at Stanford working on robot learning, haptics, and design.",
}
NAV = [("Projects", "index.html"), ("Research", "research.html"), ("About", "about.html"), ("Resume", "resume.html")]

ICON_LINKEDIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M4 5h16a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm-1 1 9 7 9-7"/></svg>'
ICON_DOC = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8zm0 0v5h5M9 13h6M9 17h6"/></svg>'
ICON_EXTERNAL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M14 4h6v6m0-6-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>'
ICON_ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M5 12h14m-6-6 6 6-6 6"/></svg>'


def read(path):
    with open(os.path.join(SRC, path), encoding="utf-8") as f:
        return f.read()


def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def fmt_date(iso):
    return date.fromisoformat(iso).strftime("%B %Y")


def page(title, body, root="", active="", description=SITE["description"], image="files/profile.png"):
    nav = "".join(
        f'<a href="{root}{href}"{" aria-current=\"page\"" if label == active else ""}>{label}</a>'
        for label, href in NAV
    )
    full_title = SITE["name"] if title == SITE["name"] else f"{title} · {SITE['name']}"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(full_title)}</title>
<meta name="description" content="{escape(description)}">
<meta property="og:title" content="{escape(full_title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:image" content="https://sarah-glomski.github.io/{image}">
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{root}style.css">
</head>
<body>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="wordmark" href="{root}index.html">Sarah Glomski</a>
    <nav class="site-nav" aria-label="Main">{nav}<a class="icon-link" href="{SITE['linkedin']}" target="_blank" rel="noopener" aria-label="LinkedIn">{ICON_LINKEDIN}</a></nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <div class="wrap footer-inner">
    <p class="footer-cta">Contact</p>
    <div class="footer-links">
      <a href="mailto:{SITE['email']}">{ICON_MAIL}<span>{SITE['email']}</span></a>
      <a href="{SITE['linkedin']}" target="_blank" rel="noopener">{ICON_LINKEDIN}<span>LinkedIn</span></a>
      <a href="{root}{SITE['resume']}" target="_blank">{ICON_DOC}<span>Resume (PDF)</span></a>
    </div>
    <p class="fineprint">© {date.today().year} Sarah Glomski</p>
  </div>
</footer>
</body>
</html>
"""


def tag_list(tags):
    return '<ul class="tags">' + "".join(f"<li>{escape(t)}</li>" for t in tags) + "</ul>"


def card(p, root=""):
    img = f'<img src="{root}{p["image"]}" alt="" loading="lazy">' if p["image"] else ""
    return f"""<a class="card" href="{root}projects/{p['slug']}.html" data-tags="{escape('|'.join(p['tags']))}">
  <div class="card-media">{img}</div>
  <div class="card-body">
    {tag_list(p['tags'])}
    <h3>{escape(p['title'])}</h3>
    <p>{escape(p['excerpt'])}</p>
  </div>
</a>"""


def build_home(projects):
    all_tags = []
    for p in projects:
        all_tags += [t for t in p["tags"] if t not in all_tags]
    order = ["Medical Devices", "Robotics", "Research", "Machine Learning", "Software", "CAD", "Imaging", "Simulation", "Personal"]
    all_tags.sort(key=lambda t: order.index(t) if t in order else 99)
    chips = '<button class="chip" aria-pressed="true" data-filter="">All</button>' + "".join(
        f'<button class="chip" aria-pressed="false" data-filter="{escape(t)}">{escape(t)}</button>' for t in all_tags
    )
    cards = "\n".join(card(p) for p in projects)
    body = f"""<section class="hero wrap">
  <div class="hero-text">
    <p class="eyebrow">Mechanical Engineering PhD Student at Stanford</p>
    <h1>Sarah Glomski</h1>
    <p class="lede">I’m a PhD student and EDGE Doctoral Fellow at Stanford. I build robot learning pipelines, do systems engineering with haptics, and teach design as a course assistant for ME310. Before Stanford, I studied biomedical and mechanical engineering at Duke and worked on surgical robotics, medical devices, and CT imaging.</p>
    <div class="actions">
      <a class="btn primary" href="#projects">See my projects {ICON_ARROW}</a>
      <a class="btn" href="resume.html">{ICON_DOC} Resume</a>
      <a class="btn" href="{SITE['linkedin']}" target="_blank" rel="noopener">{ICON_LINKEDIN} LinkedIn</a>
    </div>
  </div>
  <div class="hero-photo"><img src="files/profile.png" alt="Portrait of Sarah Glomski" width="720" height="900"></div>
</section>

<section class="projects wrap" id="projects">
  <div class="section-head">
    <h2>Projects</h2>
    <p>Academic, professional, and personal work.</p>
  </div>
  <div class="chips" role="group" aria-label="Filter projects">{chips}</div>
  <div class="grid">
{cards}
  </div>
</section>
<script>
document.querySelectorAll('.chip').forEach(function (chip) {{
  chip.addEventListener('click', function () {{
    var f = chip.dataset.filter;
    document.querySelectorAll('.chip').forEach(function (c) {{ c.setAttribute('aria-pressed', c === chip); }});
    document.querySelectorAll('.card').forEach(function (c) {{
      c.hidden = f && c.dataset.tags.split('|').indexOf(f) < 0;
    }});
  }});
}});
</script>"""
    write("index.html", page(SITE["name"], body, active="Projects"))


def build_projects(projects):
    for i, p in enumerate(projects):
        content = read(f"projects/{p['slug']}.html").replace("@root/", "../")
        newer = projects[i - 1] if i > 0 else None
        older = projects[i + 1] if i + 1 < len(projects) else None
        pager = '<nav class="pager" aria-label="More projects">'
        pager += f'<a class="prev" href="{newer["slug"]}.html"><span>Newer</span>{escape(newer["title"])}</a>' if newer else "<span></span>"
        pager += f'<a class="next" href="{older["slug"]}.html"><span>Older</span>{escape(older["title"])}</a>' if older else "<span></span>"
        pager += "</nav>"
        body = f"""<article class="post">
  <header class="post-head wrap narrow">
    <a class="back" href="../index.html#projects">← All projects</a>
    {tag_list(p['tags'])}
    <h1>{escape(p['title'])}</h1>
    <p class="meta">{fmt_date(p['date'])}</p>
  </header>
  <div class="prose wrap narrow">
{content}
  </div>
  <div class="wrap narrow">{pager}</div>
</article>"""
        write(f"projects/{p['slug']}.html", page(p["title"], body, root="../", active="Projects",
                                                description=p["excerpt"], image=p["image"] or "files/profile.png"))


def build_research():
    items = json.loads(read("research.json"))
    entries = []
    for e in items:
        bullets = "".join(f"<li>{escape(b)}</li>" for b in e["bullets"])
        media = "".join(
            f'<li><a href="{escape(m["href"])}"{" target=\"_blank\"" if m["href"].endswith(".pdf") else ""}>'
            f'{ICON_DOC if m["href"].endswith(".pdf") else ICON_ARROW}<span><strong>{escape(m["title"])}</strong>'
            f'<small>{escape(m["note"])}</small></span></a></li>'
            for m in e["media"]
        )
        entries.append(f"""<li class="tl-item">
  <p class="tl-date">{escape(e['dates'])}</p>
  <div class="tl-body">
    <h3>{escape(e['org'])}{f' <a class="ext-link" href="{escape(e["link"])}" target="_blank" rel="noopener" aria-label="Open lab website in a new tab" title="Open lab website">{ICON_EXTERNAL}</a>' if e.get('link') else ''}</h3>
    {f'<p class="tl-role">{escape(e["role"])}</p>' if e['role'] else ''}
    {f'<ul class="tl-bullets">{bullets}</ul>' if bullets else ''}
    {f'<ul class="media-list">{media}</ul>' if media else ''}
  </div>
</li>""")
    body = f"""<section class="wrap page-head">
  <p class="eyebrow">Research</p>
  <h1>Research portfolio</h1>
  <p class="lede">My key research projects, with takeaways and the posters, presentations, and papers that came out of each. For more detail, see the <a href="index.html#projects">project write-ups</a> or <a href="mailto:{SITE['email']}">email me</a>.</p>
</section>
<section class="wrap">
  <ol class="timeline">
{''.join(entries)}
  </ol>
</section>"""
    write("research.html", page("Research", body, active="Research"))


def build_about():
    body = f"""<section class="wrap about">
  <div class="about-photo"><img src="files/profile.png" alt="Portrait of Sarah Glomski" width="720" height="900"></div>
  <div class="about-text">
    <p class="eyebrow">About me</p>
    <h1>Design is the common thread.</h1>
    <div class="prose">
{read('about.html')}
    </div>
  </div>
</section>"""
    write("about.html", page("About", body, active="About"))


def build_resume():
    body = f"""<section class="wrap page-head">
  <p class="eyebrow">Resume</p>
  <h1>Resume</h1>
  <div class="actions">
    <a class="btn primary" href="{SITE['resume']}" download>{ICON_DOC} Download PDF</a>
    <a class="btn" href="{SITE['resume']}" target="_blank">Open in new tab {ICON_ARROW}</a>
  </div>
</section>
<section class="wrap">
  <object class="resume-embed" data="{SITE['resume']}" type="application/pdf">
    <a href="{SITE['resume']}"><img src="files/resume-preview.png" alt="Resume preview" class="resume-fallback"></a>
  </object>
</section>"""
    write("resume.html", page("Resume", body, active="Resume"))


if __name__ == "__main__":
    projects = json.loads(read("projects.json"))
    projects.sort(key=lambda p: p["date"], reverse=True)
    build_home(projects)
    build_projects(projects)
    build_research()
    build_about()
    build_resume()
    print(f"Built {len(projects)} projects + 4 pages into {OUT}")
