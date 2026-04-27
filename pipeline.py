import os
import csv
import json
import time
import html as html_lib
import feedparser
import anthropic
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from pathlib import Path

RSS_FEEDS = [
    {"name": "Adweek",      "url": "https://www.adweek.com/feed/"},
    {"name": "Digiday",     "url": "https://digiday.com/feed/"},
    {"name": "The Drum",    "url": "https://www.thedrum.com/rss.xml"},
    {"name": "AdExchanger", "url": "https://www.adexchanger.com/feed/"},
    {"name": "Ad Age",      "url": "https://adage.com/rss"},
]

DATA_DIR    = Path("data")
REPORTS_DIR = Path("reports")
ARTICLES_CSV = DATA_DIR / "articles.csv"
TRENDS_CSV   = DATA_DIR / "trends.csv"

ARTICLES_HEADERS = [
    "Date", "Publication", "Headline", "URL",
    "Categories", "Topics", "FAANG Mentions",
    "Retail Media Networks", "Attribution Topics", "Ad Formats",
    "Relevance Score", "Summary",
]

TRENDS_HEADERS = [
    "Week Start", "Topic", "Category", "Count", "Prior Week Count", "% Change",
]

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM_PROMPT = """You are a digital advertising industry analyst specializing in programmatic advertising, retail media, ad tech platforms, attribution/measurement, and ad formats.

Your job is to analyze trade press articles and extract structured intelligence about the following focus areas:

PROGRAMMATIC ADVERTISING
- DSPs (Demand Side Platforms): The Trade Desk, DV360, Amazon DSP, Xandr, Verizon Media
- SSPs (Supply Side Platforms): Magnite, PubMatic, OpenX, Xandr, Google Ad Manager
- Real-time bidding (RTB), private marketplace deals (PMPs), programmatic direct
- Header bidding, wrapper solutions
- Contextual targeting, audience targeting, data clean rooms

RETAIL MEDIA NETWORKS
- Amazon Ads / Amazon DSP / Amazon Marketing Cloud (AMC)
- Walmart Connect
- Target Roundel
- Kroger Precision Marketing
- Instacart Ads
- Albertsons Media Collective
- Other retailer-owned ad networks

FAANG & BIG TECH IN AD TECH
- Meta / Facebook: Advantage+, Meta AI ads, Reels monetization
- Amazon: DSP, Sponsored Products, AMC, retail media
- Apple: ATT (App Tracking Transparency), SKAdNetwork, Privacy manifests
- Netflix: Ad-supported tier, Netflix Ads, programmatic partnerships
- Google: Performance Max (PMax), Privacy Sandbox, DV360, Google Ads, Topics API

ATTRIBUTION & MEASUREMENT
- Incrementality testing / lift studies
- Last-click attribution
- View-through attribution (VTA)
- Multi-touch attribution (MTA)
- Marketing Mix Modeling (MMM / media mix modeling)
- Data clean rooms (LiveRamp, InfoSum, Habu, etc.)
- Cookieless measurement, ID solutions (UID2, RampID)
- Brand lift, conversion lift

AD FORMATS & CHANNELS
- CTV / OTT (Connected TV, streaming video ads)
- Audio (podcast ads, streaming audio, Spotify, Pandora)
- DOOH (Digital Out-of-Home)
- Display (banner ads, rich media)
- Native advertising
- Online Video (pre-roll, mid-roll, outstream)
- Social (Facebook, Instagram, TikTok, Snapchat, Pinterest ads)
- Search (Google Ads, Microsoft Ads, retail search)
- Retail Media Ads (sponsored products, display on retail sites)

When analyzing an article, be precise and conservative — only flag topics that are genuinely covered in the article, not tangentially related."""

ARTICLE_PROMPT = """Analyze this digital advertising trade press article and extract structured data.

Publication: {publication}
Date: {date}
Headline: {title}
Summary/Excerpt: {summary}

Return a JSON object with exactly these fields:
{{
  "categories": ["list of broad categories from: Programmatic, Retail Media, FAANG, Attribution/Measurement, Ad Formats, Industry/Business, Privacy/Regulation, Technology"],
  "topics": ["specific topics covered, e.g. 'header bidding', 'incrementality testing', 'CTV advertising'"],
  "faang_mentions": ["which FAANG companies are mentioned: Meta, Amazon, Apple, Netflix, Google — only include if substantively covered"],
  "retail_media_networks": ["which retail media networks: Amazon Ads, Walmart Connect, Target Roundel, Kroger, Instacart, Albertsons, Other — only if substantively covered"],
  "attribution_topics": ["which attribution/measurement topics: Incrementality, Last-Click, View-Through, MMM, MTA, Clean Rooms, Cookieless, ID Solutions — only if substantively covered"],
  "ad_formats": ["which ad formats: CTV/OTT, Audio, DOOH, Display, Native, Video, Social, Search, Retail Media Ads — only if substantively covered"],
  "relevance_score": <integer 1-10 where 10 = extremely relevant to digital ad tech professionals>,
  "one_sentence_summary": "one concise sentence describing what this article is about"
}}

Return only valid JSON, no other text."""


def ensure_dirs():
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    if not ARTICLES_CSV.exists():
        with open(ARTICLES_CSV, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(ARTICLES_HEADERS)
    if not TRENDS_CSV.exists():
        with open(TRENDS_CSV, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(TRENDS_HEADERS)


def fetch_articles(lookback_days=8):
    cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days)
    articles = []
    for feed_config in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_config["url"])
        except Exception as e:
            print(f"[WARN] Failed to fetch {feed_config['name']}: {e}")
            continue
        for entry in feed.entries:
            pub_date = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                pub_date = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)

            if pub_date and pub_date < cutoff:
                continue

            summary = ""
            if hasattr(entry, "summary"):
                summary = entry.summary[:500]
            elif hasattr(entry, "description"):
                summary = entry.description[:500]

            articles.append({
                "publication": feed_config["name"],
                "title":       getattr(entry, "title", ""),
                "url":         getattr(entry, "link", ""),
                "date":        pub_date.strftime("%Y-%m-%d") if pub_date else "",
                "summary":     summary,
            })

    print(f"[INFO] Fetched {len(articles)} articles from {len(RSS_FEEDS)} feeds")
    return articles


def get_existing_urls():
    if not ARTICLES_CSV.exists():
        return set()
    with open(ARTICLES_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["URL"] for row in reader}


def analyze_article(title, publication, date, summary):
    prompt = ARTICLE_PROMPT.format(
        publication=publication, date=date, title=title, summary=summary,
    )
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=600,
        system=[{
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)


def build_article_row(article, analysis):
    def fmt(lst):
        return ", ".join(lst) if lst else ""
    return [
        article["date"],
        article["publication"],
        article["title"],
        article["url"],
        fmt(analysis.get("categories", [])),
        fmt(analysis.get("topics", [])),
        fmt(analysis.get("faang_mentions", [])),
        fmt(analysis.get("retail_media_networks", [])),
        fmt(analysis.get("attribution_topics", [])),
        fmt(analysis.get("ad_formats", [])),
        str(analysis.get("relevance_score", "")),
        analysis.get("one_sentence_summary", ""),
    ]


def aggregate_trends(new_rows, week_start):
    counts = defaultdict(lambda: defaultdict(int))
    col = {h: i for i, h in enumerate(ARTICLES_HEADERS)}

    for row in new_rows:
        for item in (row[col["Topics"]] or "").split(", "):
            if item.strip():
                counts["Topics"][item.strip()] += 1
        for item in (row[col["FAANG Mentions"]] or "").split(", "):
            if item.strip():
                counts["FAANG"][item.strip()] += 1
        for item in (row[col["Retail Media Networks"]] or "").split(", "):
            if item.strip():
                counts["Retail Media Networks"][item.strip()] += 1
        for item in (row[col["Attribution Topics"]] or "").split(", "):
            if item.strip():
                counts["Attribution"][item.strip()] += 1
        for item in (row[col["Ad Formats"]] or "").split(", "):
            if item.strip():
                counts["Ad Formats"][item.strip()] += 1

    prior_week_start = (
        datetime.strptime(week_start, "%Y-%m-%d") - timedelta(days=7)
    ).strftime("%Y-%m-%d")

    prior_counts = defaultdict(lambda: defaultdict(int))
    if TRENDS_CSV.exists():
        with open(TRENDS_CSV, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("Week Start") == prior_week_start:
                    prior_counts[row["Category"]][row["Topic"]] = int(row.get("Count") or 0)

    trend_rows = []
    for category, topics in counts.items():
        for topic, count in sorted(topics.items(), key=lambda x: -x[1]):
            prior = prior_counts[category].get(topic, 0)
            if prior > 0:
                pct_change = f"{((count - prior) / prior * 100):+.0f}%"
            elif count > 0:
                pct_change = "NEW"
            else:
                pct_change = ""
            trend_rows.append([week_start, topic, category, str(count), str(prior), pct_change])

    with open(TRENDS_CSV, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(trend_rows)

    print(f"[INFO] Appended {len(trend_rows)} trend rows")
    return counts


def generate_digest(week_start, new_articles, counts):
    top_topics = {
        cat: sorted(topics.items(), key=lambda x: -x[1])[:5]
        for cat, topics in counts.items()
    }
    articles_list = "\n".join(
        f"- [{a['publication']}] {a['title']} | URL: {a['url']}"
        for a in new_articles[:30]
    )
    prompt = f"""Write a weekly market research digest for a product marketing team covering the digital advertising industry.

Week of: {week_start}
Total new articles analyzed: {len(new_articles)}

TOP TRENDING TOPICS BY CATEGORY:
{json.dumps(top_topics, indent=2)}

ARTICLES THIS WEEK (with URLs):
{articles_list}

Write a 3-4 paragraph narrative digest that:
1. Opens with the most significant overarching theme or story of the week
2. Covers what's trending across programmatic advertising, retail media networks, FAANG activity, attribution/measurement, and ad formats — with specific mention of topic frequency (e.g., "CTV was mentioned in 12 articles") and any notable week-over-week changes
3. Closes with a brief "what to watch" forward-looking observation
4. Write a final paragraph under the subheading <h3>Yelp Impact Analysis</h3> that specifically covers:
   - News affecting restaurant, services, and local business verticals (Yelp's core business)
   - Ad tech developments relevant to high-intent audience platforms (Yelp is a high-intent platform where consumers are actively searching for businesses and ready to convert)
   - Competitive moves from Google Local Services Ads, Meta local business ads, Nextdoor, Apple Business Connect, and other local advertising products
   - Implications for programmatic or managed-service ad products targeting multi-location businesses (restaurants, home services, auto, etc.)
   If nothing this week is directly relevant to these areas, briefly note that and highlight the closest adjacent trend that could impact Yelp's competitive position.

FORMATTING RULES — follow these exactly:
- Write in HTML, not markdown
- When you reference a specific article or finding, hyperlink the relevant phrase using <a href="URL" target="_blank">linked text</a> — use the article URLs provided above
- Use <strong>bold</strong> for company names, key topics, and important figures
- Wrap each paragraph in <p> tags
- Use <h3> tags for section subheadings within the digest
- Do not use ** for bold, do not use markdown, only HTML
- Do not use bullet points; use flowing paragraphs only"""

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1500,
        thinking={"type": "adaptive"},
        messages=[{"role": "user", "content": prompt}],
    )
    for block in response.content:
        if block.type == "text":
            return block.text.strip()
    return ""


def _score_class(score_str):
    try:
        s = int(score_str)
        if s >= 8:
            return "high"
        if s >= 5:
            return "med"
    except (ValueError, TypeError):
        pass
    return ""


def _change_class(change_str):
    if not change_str:
        return ""
    if change_str == "NEW":
        return "new"
    try:
        return "up" if float(change_str.replace("%", "").replace("+", "")) > 0 else "down"
    except ValueError:
        return ""


def build_trends_html(counts):
    if not counts:
        return "<p>No trend data available.</p>"

    parts = []
    for category, topics in sorted(counts.items()):
        items_html = ""
        for topic, count in sorted(topics.items(), key=lambda x: -x[1])[:10]:
            items_html += f'<div class="trend-item"><span>{html_lib.escape(topic)}</span><span class="trend-count">{count}</span></div>\n'
        parts.append(
            f'<div class="trend-category">'
            f'<h3>{html_lib.escape(category)}</h3>'
            f'{items_html}'
            f'</div>'
        )
    return "\n".join(parts)


def load_all_trends():
    """Read all historical trend data for the interactive chart."""
    if not TRENDS_CSV.exists():
        return {}
    data = defaultdict(lambda: defaultdict(list))
    with open(TRENDS_CSV, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            data[row["Category"]][row["Topic"]].append({
                "week": row["Week Start"],
                "count": int(row.get("Count") or 0),
            })
    # Keep only top 15 topics per category by max count
    result = {}
    for category, topics in data.items():
        sorted_topics = sorted(
            topics.items(),
            key=lambda x: max(p["count"] for p in x[1]),
            reverse=True,
        )[:15]
        result[category] = {
            topic: sorted(points, key=lambda x: x["week"])
            for topic, points in sorted_topics
        }
    return result


def build_rows_html(new_rows):
    col = {h: i for i, h in enumerate(ARTICLES_HEADERS)}
    rows = []
    for row in new_rows:
        score     = row[col["Relevance Score"]]
        sc        = _score_class(score)
        cats      = html_lib.escape(row[col["Categories"]])
        faang     = row[col["FAANG Mentions"]]
        formats   = row[col["Ad Formats"]]
        headline  = html_lib.escape(row[col["Headline"]])
        url       = html_lib.escape(row[col["URL"]])
        pub       = html_lib.escape(row[col["Publication"]])
        date      = html_lib.escape(row[col["Date"]])
        summary   = html_lib.escape(row[col["Summary"]])

        def tags(s):
            return " ".join(f'<span class="tag">{html_lib.escape(t.strip())}</span>' for t in s.split(",") if t.strip())

        rows.append(
            f"<tr>"
            f'<td>{date}</td>'
            f'<td>{pub}</td>'
            f'<td><a href="{url}" target="_blank" rel="noopener">{headline}</a>'
            f'<div style="color:#888;font-size:0.75rem;margin-top:0.2rem">{summary}</div></td>'
            f'<td>{tags(cats)}</td>'
            f'<td>{tags(faang)}</td>'
            f'<td>{tags(formats)}</td>'
            f'<td><span class="score {sc}">{score}</span></td>'
            f"</tr>"
        )
    return "\n".join(rows)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ad Tech Digest &mdash; {week_start}</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f5f7fa;color:#222}}
    header{{background:#0f172a;color:#fff;padding:2rem 2.5rem}}
    header h1{{font-size:1.4rem;font-weight:700;letter-spacing:-0.01em}}
    header p{{color:#94a3b8;margin-top:0.3rem;font-size:0.9rem}}
    .container{{max-width:1280px;margin:0 auto;padding:2rem 2.5rem}}
    .card{{background:#fff;border-radius:10px;padding:1.75rem;margin-bottom:1.5rem;box-shadow:0 1px 4px rgba(0,0,0,.08)}}
    h2{{font-size:1rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:#64748b;margin-bottom:1.2rem}}
    .digest{{line-height:1.8;font-size:0.95rem;color:#334155}}
    .digest p{{margin-bottom:1rem}}
    .digest a{{color:#4f46e5;text-decoration:underline}}
    .digest h3{{font-size:0.88rem;font-weight:700;color:#0f172a;margin:1.4rem 0 0.5rem;padding-top:0.8rem;border-top:1px solid #e2e8f0}}
    .score-legend{{font-size:.72rem;color:#94a3b8;margin-top:.5rem}}
    .chart-controls{{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:1rem}}
    .cat-btn{{padding:.35rem .75rem;border:1px solid #e2e8f0;border-radius:6px;background:#fff;font-size:.78rem;cursor:pointer;color:#475569;transition:all .15s}}
    .cat-btn:hover{{border-color:#6366f1;color:#4f46e5}}
    .cat-btn.active{{background:#4f46e5;color:#fff;border-color:#4f46e5}}
    .chart-container{{position:relative;height:400px;width:100%}}
    .chart-note{{font-size:.72rem;color:#94a3b8;margin-top:.75rem}}
    .trends-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1.25rem}}
    .trend-category h3{{font-size:0.72rem;text-transform:uppercase;letter-spacing:.07em;color:#94a3b8;margin-bottom:.6rem;font-weight:600}}
    .trend-item{{display:flex;justify-content:space-between;align-items:center;padding:.3rem 0;border-bottom:1px solid #f1f5f9;font-size:.82rem}}
    .trend-count{{font-weight:700;color:#0f172a;background:#f1f5f9;padding:.1rem .45rem;border-radius:999px;font-size:.75rem}}
    input#filter{{width:100%;padding:.55rem .8rem;border:1px solid #e2e8f0;border-radius:6px;font-size:.875rem;margin-bottom:1rem;outline:none}}
    input#filter:focus{{border-color:#6366f1;box-shadow:0 0 0 3px rgba(99,102,241,.1)}}
    table{{width:100%;border-collapse:collapse;font-size:.8rem}}
    th{{background:#f8fafc;text-align:left;padding:.55rem .75rem;font-size:.7rem;text-transform:uppercase;letter-spacing:.05em;color:#94a3b8;border-bottom:2px solid #e2e8f0;white-space:nowrap}}
    td{{padding:.55rem .75rem;border-bottom:1px solid #f1f5f9;vertical-align:top}}
    tr:hover td{{background:#fafbff}}
    a{{color:#4f46e5;text-decoration:none}}
    a:hover{{text-decoration:underline}}
    .score{{display:inline-block;padding:.15rem .45rem;border-radius:999px;font-size:.72rem;font-weight:700;background:#dbeafe;color:#1e40af}}
    .score.high{{background:#dcfce7;color:#166534}}
    .score.med{{background:#fef9c3;color:#854d0e}}
    .tag{{display:inline-block;background:#f1f5f9;border-radius:4px;padding:.1rem .35rem;font-size:.68rem;margin:.1rem;color:#475569}}
    .back{{font-size:.85rem;margin-bottom:1.25rem;display:inline-block;color:#64748b}}
    .back:hover{{color:#0f172a}}
  </style>
</head>
<body>
  <header>
    <h1>Ad Tech Weekly Digest</h1>
    <p>Week of {week_start} &bull; {article_count} articles analyzed</p>
  </header>
  <div class="container">
    <a href="index.html" class="back">&larr; All reports</a>
    <div class="card">
      <h2>Weekly Narrative</h2>
      <div class="digest">{digest}</div>
    </div>
    <div class="card">
      <h2>Topic Trends Over Time</h2>
      <div class="chart-controls">
        <button class="cat-btn active" data-category="all">All</button>
      </div>
      <div class="chart-container">
        <canvas id="trendsChart"></canvas>
      </div>
      <p class="chart-note">Click category buttons to filter. Click legend items to toggle individual topics.</p>
    </div>
    <div class="card">
      <h2>Trending Topics This Week</h2>
      <div class="trends-grid">{trends_html}</div>
    </div>
    <div class="card">
      <h2>Articles ({article_count})</h2>
      <input type="text" id="filter" placeholder="Filter by headline, topic, publication&hellip;">
      <table id="tbl">
        <thead>
          <tr>
            <th>Date</th><th>Publication</th><th>Headline</th>
            <th>Categories</th><th>FAANG</th><th>Ad Formats</th>
            <th>Score <span class="score-legend" title="1-10 relevance to ad tech professionals. 8-10 = highly relevant, 5-7 = moderately relevant, 1-4 = low relevance">(?)</span></th>
          </tr>
        </thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
  </div>
  <script>
    document.getElementById('filter').addEventListener('input', function() {{
      const q = this.value.toLowerCase();
      document.querySelectorAll('#tbl tbody tr').forEach(r => {{
        r.style.display = r.textContent.toLowerCase().includes(q) ? '' : 'none';
      }});
    }});
  </script>
  <script>
  (function() {{
    var trendData = {trends_json};
    var categoryColors = {{
      'Ad Formats':            {{base:'#4f46e5',variants:['#4f46e5','#6366f1','#818cf8','#a5b4fc','#c7d2fe','#3730a3','#312e81','#4338ca','#5b21b6','#7c3aed']}},
      'Attribution':           {{base:'#0891b2',variants:['#0891b2','#06b6d4','#22d3ee','#67e8f9','#0e7490','#155e75','#164e63','#0284c7','#0369a1','#075985']}},
      'FAANG':                 {{base:'#dc2626',variants:['#dc2626','#ef4444','#f87171','#fca5a5','#b91c1c','#991b1b','#7f1d1d','#e11d48','#be123c','#9f1239']}},
      'Retail Media Networks': {{base:'#16a34a',variants:['#16a34a','#22c55e','#4ade80','#86efac','#15803d','#166534','#14532d','#059669','#047857','#065f46']}},
      'Topics':                {{base:'#d97706',variants:['#d97706','#f59e0b','#fbbf24','#fcd34d','#b45309','#92400e','#78350f','#a16207','#ca8a04','#eab308']}}
    }};
    var allWeeks = [];
    var weekSet = {{}};
    for (var cat in trendData) {{
      for (var topic in trendData[cat]) {{
        trendData[cat][topic].forEach(function(p) {{
          if (!weekSet[p.week]) {{
            weekSet[p.week] = true;
            allWeeks.push(p.week);
          }}
        }});
      }}
    }}
    allWeeks.sort();
    var datasets = [];
    for (var cat in trendData) {{
      var colors = categoryColors[cat] || {{base:'#64748b',variants:['#64748b']}};
      var colorIdx = 0;
      var topicEntries = [];
      for (var topic in trendData[cat]) {{
        var maxCount = 0;
        trendData[cat][topic].forEach(function(p) {{
          if (p.count > maxCount) maxCount = p.count;
        }});
        topicEntries.push({{topic: topic, points: trendData[cat][topic], maxCount: maxCount}});
      }}
      topicEntries.sort(function(a, b) {{ return b.maxCount - a.maxCount; }});
      topicEntries.slice(0, 10).forEach(function(entry) {{
        var weekMap = {{}};
        entry.points.forEach(function(p) {{ weekMap[p.week] = p.count; }});
        var color = colors.variants[colorIdx % colors.variants.length];
        colorIdx++;
        datasets.push({{
          label: entry.topic,
          data: allWeeks.map(function(w) {{ return weekMap[w] || 0; }}),
          borderColor: color,
          backgroundColor: color + '33',
          tension: 0.3,
          pointRadius: 3,
          borderWidth: 2,
          _category: cat,
          hidden: false
        }});
      }});
    }}
    if (allWeeks.length < 2) {{
      var note = document.querySelector('.chart-note');
      if (note) note.textContent = 'Only one week of data so far. The trend lines will appear as more weekly reports are generated.';
    }}
    var ctx = document.getElementById('trendsChart').getContext('2d');
    var chart = new Chart(ctx, {{
      type: 'line',
      data: {{ labels: allWeeks, datasets: datasets }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        interaction: {{ mode: 'index', intersect: false }},
        plugins: {{
          legend: {{
            position: 'bottom',
            labels: {{ font: {{ size: 11 }}, boxWidth: 12, padding: 8 }}
          }},
          tooltip: {{
            callbacks: {{
              title: function(items) {{ return 'Week of ' + items[0].label; }}
            }}
          }}
        }},
        scales: {{
          x: {{
            title: {{ display: true, text: 'Week', font: {{ size: 12 }} }},
            grid: {{ display: false }}
          }},
          y: {{
            title: {{ display: true, text: 'Mentions', font: {{ size: 12 }} }},
            beginAtZero: true,
            ticks: {{ stepSize: 1 }}
          }}
        }}
      }}
    }});
    var controlsDiv = document.querySelector('.chart-controls');
    var categories = Object.keys(trendData).sort();
    categories.forEach(function(cat) {{
      var btn = document.createElement('button');
      btn.className = 'cat-btn';
      btn.setAttribute('data-category', cat);
      btn.textContent = cat;
      controlsDiv.appendChild(btn);
    }});
    controlsDiv.addEventListener('click', function(e) {{
      var btn = e.target.closest('.cat-btn');
      if (!btn) return;
      controlsDiv.querySelectorAll('.cat-btn').forEach(function(b) {{ b.classList.remove('active'); }});
      btn.classList.add('active');
      var selectedCat = btn.getAttribute('data-category');
      chart.data.datasets.forEach(function(ds, i) {{
        if (selectedCat === 'all') {{
          chart.setDatasetVisibility(i, true);
        }} else {{
          chart.setDatasetVisibility(i, ds._category === selectedCat);
        }}
      }});
      chart.update();
    }});
  }})();
  </script>
</body>
</html>"""


def generate_report(week_start, digest, counts, new_rows):
    all_trends = load_all_trends()
    trends_json = json.dumps(all_trends)
    report_path = REPORTS_DIR / f"{week_start}.html"
    content = HTML_TEMPLATE.format(
        week_start=week_start,
        article_count=len(new_rows),
        digest=digest,
        trends_html=build_trends_html(counts),
        rows_html=build_rows_html(new_rows),
        trends_json=trends_json,
    )
    report_path.write_text(content, encoding="utf-8")
    print(f"[INFO] Wrote report to {report_path}")
    return report_path


def update_index():
    reports = sorted(
        [p for p in REPORTS_DIR.glob("*.html") if p.name != "index.html"],
        reverse=True,
    )
    rows = "".join(
        f'<li><a href="{p.name}">{p.stem}</a></li>\n'
        for p in reports
    )
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Ad Tech Weekly Digests</title>
  <style>
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:600px;margin:4rem auto;color:#222;padding:0 1rem}}
    h1{{font-size:1.3rem;font-weight:700;margin-bottom:.5rem}}
    p{{color:#64748b;font-size:.9rem;margin-bottom:1.5rem}}
    ul{{list-style:none;padding:0}}
    li{{margin:.5rem 0}}
    a{{color:#4f46e5;text-decoration:none;font-size:.95rem}}
    a:hover{{text-decoration:underline}}
  </style>
</head>
<body>
  <h1>Ad Tech Weekly Digests</h1>
  <p>Auto-generated every Monday from Adweek, Digiday, The Drum, AdExchanger &amp; Ad Age.</p>
  <ul>{rows}</ul>
</body>
</html>"""
    (REPORTS_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print(f"[INFO] Updated reports/index.html ({len(reports)} reports)")


def main():
    week_start = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"[INFO] Starting pipeline for week of {week_start}")

    ensure_dirs()

    articles = fetch_articles(lookback_days=8)
    if not articles:
        print("[WARN] No articles fetched. Exiting.")
        return

    existing_urls = get_existing_urls()
    new_articles  = [a for a in articles if a["url"] not in existing_urls]
    print(f"[INFO] {len(new_articles)} new articles to process ({len(articles) - len(new_articles)} already seen)")

    if not new_articles:
        print("[INFO] Nothing new this week. Exiting.")
        return

    new_rows = []
    for i, article in enumerate(new_articles):
        print(f"[INFO] Analyzing {i+1}/{len(new_articles)}: {article['title'][:60]}")
        try:
            analysis = analyze_article(
                title=article["title"],
                publication=article["publication"],
                date=article["date"],
                summary=article["summary"],
            )
            row = build_article_row(article, analysis)
        except Exception as e:
            print(f"[WARN] Failed to analyze '{article['title'][:40]}': {e}")
            row = build_article_row(article, {})
        new_rows.append(row)

        if (i + 1) % 10 == 0:
            time.sleep(2)

    with open(ARTICLES_CSV, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(new_rows)
    print(f"[INFO] Appended {len(new_rows)} rows to {ARTICLES_CSV}")

    counts = aggregate_trends(new_rows, week_start)

    print("[INFO] Generating weekly digest...")
    digest = generate_digest(week_start, new_articles, counts)

    generate_report(week_start, digest, counts, new_rows)
    update_index()

    print(f"[INFO] Pipeline complete. Processed {len(new_articles)} articles.")


if __name__ == "__main__":
    main()
