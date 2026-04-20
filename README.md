# Weekly Ad Tech Market Research Pipeline

Automatically pulls from digital advertising trade publications each week, analyzes articles with Claude AI, and commits an HTML report + CSV data directly to this GitHub repo — ready every Monday morning.

## What It Does

- **Fetches** articles from Adweek, Digiday, The Drum, AdExchanger, and Ad Age (last 8 days)
- **Analyzes** each article with Claude to extract categories, topics, FAANG mentions, retail media networks, attribution topics, ad formats, and a relevance score
- **Tracks trends** week-over-week with % change per topic/category
- **Writes** all articles to `data/articles.csv` with rolling history
- **Generates** a styled HTML report in `reports/YYYY-MM-DD.html` with the narrative digest, trend breakdown, and a filterable article table
- **Commits** all output files back to the repo automatically

**Focus areas:** Programmatic advertising · Retail media networks (Amazon, Walmart, Target, Kroger, Instacart) · FAANG in ad tech (Meta, Amazon, Apple, Netflix, Google) · Attribution/measurement (incrementality, MMM, clean rooms, cookieless) · Ad formats (CTV/OTT, Audio, DOOH, Display, Native, Video, Social, Search)

---

## Setup

### 1. Create a GitHub Repository

Push this project to a new GitHub repo (public or private).

### 2. Get an Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Create an API key under **API Keys**

### 3. Add the Secret to GitHub

1. Go to your GitHub repo → **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Name: `ANTHROPIC_API_KEY`, Value: your key

That's it — no Google Cloud, no service accounts, no other credentials needed.

---

## Running the Pipeline

### Automatic (Every Monday Morning)

The GitHub Actions workflow runs automatically at **3am UTC every Monday** (Sunday ~10pm EST).

### Manual Run

1. Go to your GitHub repo → **Actions**
2. Click **Weekly Ad Tech Market Research** in the left sidebar
3. Click **Run workflow** → **Run workflow**

### Local Run

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key"
python pipeline.py
```

---

## Viewing Reports

After each run, the pipeline commits:

```
data/
  articles.csv      ← rolling history of every article analyzed
  trends.csv        ← weekly trend counts with % change
reports/
  index.html        ← list of all weekly reports
  2025-01-06.html   ← each week's full report
  2025-01-13.html
  ...
```

**Option A — Browse directly on GitHub:** Navigate to `reports/` in your repo and click any `.html` file → click the **Raw** button → your browser renders it.

**Option B — GitHub Pages (recommended):** Turn the reports into a real website:
1. Go to repo **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: `main`, folder: `/ (root)`
4. Save — your reports will be live at `https://YOUR-USERNAME.github.io/YOUR-REPO/reports/`

**Option C — Download the CSV:** Go to `data/articles.csv` → **Raw** → save and open in Excel or Google Sheets for your own analysis.

---

## Output

### HTML Report (`reports/YYYY-MM-DD.html`)

Each weekly report contains:
- **Narrative digest** — 2-3 paragraph summary of the week's themes and trends
- **Trending topics** — frequency counts by category (Programmatic, FAANG, Retail Media, Attribution, Ad Formats)
- **Article table** — filterable list of every article with headline link, categories, FAANG mentions, ad formats, and relevance score

### `data/articles.csv`

| Column | Description |
|--------|-------------|
| Date | Article publication date |
| Publication | Source (Adweek, Digiday, etc.) |
| Headline | Article title |
| URL | Link to the article |
| Categories | Broad categories (Programmatic, Retail Media, FAANG, etc.) |
| Topics | Specific topics covered |
| FAANG Mentions | Which major tech companies are substantively covered |
| Retail Media Networks | Which retail media networks are mentioned |
| Attribution Topics | Attribution/measurement topics covered |
| Ad Formats | Ad formats covered (CTV, Audio, DOOH, etc.) |
| Relevance Score | 1–10 relevance for ad tech professionals |
| Summary | One-sentence article summary |

### `data/trends.csv`

Weekly frequency counts per topic/category with week-over-week % change — open in Excel/Sheets to chart longer-term trends.

---

## Adding More RSS Feeds

Edit the `RSS_FEEDS` list in [pipeline.py](pipeline.py):

```python
RSS_FEEDS = [
    {"name": "Adweek",      "url": "https://www.adweek.com/feed/"},
    # Add more here:
    # {"name": "Marketing Land", "url": "https://..."},
]
```

---

## Costs

Each weekly run analyzes roughly 50–200 articles.

- **Claude API:** ~$0.50–$2.00/week (prompt caching on the system prompt reduces per-article costs significantly)
- **GitHub Actions:** Free within the 2,000 minutes/month free tier
