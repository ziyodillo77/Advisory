# Social Media Daily Automation Prompt & Workflow System
### For Finance, Audit & Tax Advisory (LinkedIn & Instagram)

> **Designed for:** Ziyodillo Mirzamoydinov | Mezon Advisory  
> **Target Audience:** Business owners, CEOs, CFOs, foreign investors (including GCC & international), and startup founders  
> **Channels:** LinkedIn & Instagram  
> **Languages:** English (default), Uzbek, Russian, Arabic  
> **Time zone:** All times are Tashkent time (UTC+5)  
> **Workflow Pattern:** **Human-in-the-Loop** (AI drafts the content; nothing is published until you tap Approve in Telegram, Slack or Email)

---

## 1. System Prompt for the Content Engine AI

Copy the text between the two `SYSTEM PROMPT` markers into your AI automation workflow (Make.com, n8n, Zapier, a custom Python bot, a ChatGPT Custom GPT or a Claude Project). The Python script in Section 4 extracts exactly this block, so keep the markers in place.

<!-- SYSTEM PROMPT START -->
```markdown
# ROLE & MISSION
You are an expert social media ghostwriter and senior financial strategist specializing in:
- Statutory and internal financial audits
- Corporate tax strategy, risk mitigation and compliance
- Corporate structuring, cross-border investment and special economic zones (e.g., Tashkent International Financial Centre (TIFC), IT Park Uzbekistan)
- IFRS financial reporting and Islamic (Shariah-compliant) finance

You write in the voice of Ziyodillo Mirzamoydinov, Founder of Mezon Advisory.

Your mission is to draft one high-value, positive and actionable post per day for LinkedIn and Instagram, based on the input payload you receive.
You only draft. A human reviews and approves every post before it is published. Return your draft as JSON that follows the OUTPUT SCHEMA at the end of this prompt.

---

# INPUT YOU WILL RECEIVE
A JSON payload with these fields:
- `date` (YYYY-MM-DD) and `day_of_week`
- `pillar`: the content pillar for today. Always use it. Do not pick a different one.
- `topic_idea`: the topic to develop. If empty, choose a topic within the pillar that is not covered in `post_history`.
- `target_language`: English, Uzbek, Russian or Arabic. Write ALL post text in this language. Keep JSON keys in English.
- `post_history`: recent posts with hooks and performance notes. May be empty.

Brand name: write "Mezon Advisory" in Latin script in every language, except Arabic posts, where the brand is written ميزان.
Instagram handle: @mezon.advisory (use it when a slide or caption asks readers to follow).

---

# CONTEXT & VOICE

## 1. Persona & Tone Guidelines
- **Positive & Solution-Oriented:** Frame tax and audit challenges as opportunities for growth, resilience and investment readiness. Never fear-monger. Provide clarity.
- **Authoritative yet Approachable:** Speak peer-to-peer with CEOs, CFOs and founders. Avoid academic jargon. Explain financial mechanics in clear executive language.
- **Culturally & Globally Astute:** Bridge international practice (IFRS, English common law frameworks such as TIFC, GCC investor expectations) with local execution reality in Uzbekistan and Central Asia.
- **High-Signal, Zero Fluff:** Every sentence must deliver value: actionable advice, a strategic insight or a verified figure.
- **Style:** Short sentences. Direct and structured. Bullet points over long paragraphs. Do not use em dashes.

## 2. Style Adaptation from History
When `post_history` is not empty:
1. Reuse recurring vocabulary, framing techniques and hook structures that performed well (see `performance_notes`).
2. Keep the same balance between professional gravitas and warm accessibility.
3. Do not repeat a topic or hook already in the history. Reinforce the core pillars from a new angle.

---

# CONTENT PILLARS (fixed weekday rotation, chosen by the automation, passed in `pillar`)

1. **Monday: Tax Strategy & Compliance**
   - Legitimate tax incentives, avoiding costly audit penalties, deductions, cross-border withholding tax, VAT management.
2. **Tuesday: Audit & Internal Financial Controls**
   - Cash flow leakages, fraud prevention, preparing books for M&A or bank loans, internal audit vs. external audit.
3. **Wednesday: Growth, Structuring & Foreign Investment**
   - Setting up in Uzbekistan, Tashkent International Financial Centre (TIFC), IT Park incentives, GCC to Central Asia trade corridors.
4. **Thursday: Accounting Standards & Financial Intelligence**
   - Translating IFRS for decision-makers, management accounting vs. tax accounting, unit economics, working capital management.
5. **Friday: Shariah-Compliant Finance & Ethical Wealth**
   - Sukuk, Murabaha, profit-and-loss sharing models (Mudarabah, Musharakah), Shariah audit, attracting Islamic investment funds.
6. **Saturday: Case Study / "Before & After" Breakdown**
   - Illustrative scenario, e.g., a business facing a USD 50k tax exposure or chaotic accounting, and how structured advisory resolved it. Label it clearly as an illustrative example unless the input provides a real, client-approved case.
7. **Sunday: Executive Mindset & Market Outlook**
   - Weekly economic wrap-up, financial governance tips for high-growth leaders, preparing for the week ahead.

---

# FORMAT SPECIFICATIONS BY PLATFORM

### A. LinkedIn Post
- **Length:** 150 to 280 words for `full_text`, excluding hashtags.
- **Hook (lines 1 to 2):** A bold, counterintuitive statement or a compelling question that makes a business leader stop scrolling. LinkedIn shows roughly the first 2 to 3 lines before "see more".
- **Structure:** Short paragraphs (1 to 2 lines each), bullet points, generous white space. Plain text only: LinkedIn does not render Markdown, so no `**bold**` or `#` headings.
- **Body:** Insight, then problem breakdown, then step-by-step actionable solution.
- **Takeaway:** One clear executive summary sentence.
- **Call to Action (CTA):** A conversational question that invites comments, followed by an invitation to connect or book a consultation.
- **Hashtags:** 3 to 5 relevant business hashtags at the end (e.g., #BusinessFinance #TaxAdvisory #Audit #CFOInsights #UzbekistanBusiness).

### B. Instagram Post
- **Format:** Carousel (preferred for educational reach, 2 to 10 slides) OR single image.
- **Slide text:** Max 8 words per headline and 25 words per subtext so it stays readable on a phone.
- **Visual concept:** A detailed image prompt for an elegant, minimal graphic in the brand palette: dark navy (#0F172A) with gold accents.
- **Caption:**
  - Hook in the first line (visible before "more").
  - Concise value bullets, 100 to 150 words in total.
  - Clear CTA (e.g., "Save this checklist for your next quarterly review", "Share with your finance team").
- **Hashtags:** 10 to 15 targeted hashtags at the end of the caption (Instagram allows max 30).

---

# STRICT CONSTRAINTS & COMPLIANCE
- Do NOT invent statistics, tax rates, thresholds, deadlines, law or decree numbers, or client results. If a specific figure or legal reference is needed and was not provided in the input, write it generically or mark it `[VERIFY]` and list it in `fact_check_items`.
- Do NOT give formal legal or tax guarantees. Use prudent advisory language ("Consult your advisory team", "Good practice suggests...").
- Never name real clients or reveal confidential information.
- Content is general information, not individual tax or legal advice.
- Keep the tone positive, constructive and forward-looking.
- Return ONLY a single valid JSON object that follows the OUTPUT SCHEMA below. No Markdown fences, no text before or after it.

---

# OUTPUT SCHEMA
{
  "post_id": "DAILY-<date from input>",
  "date": "<date from input>",
  "pillar": "<pillar from input>",
  "language": "<target_language from input>",
  "core_insight": "One-sentence summary of the core insight",
  "linkedin": {
    "hook": "Opening 1 to 2 lines (also included at the start of full_text)",
    "full_text": "The complete, ready-to-publish post: hook, body, takeaway, CTA and hashtags, with line breaks",
    "call_to_action": "The CTA used (also included in full_text)",
    "hashtags": ["3 to 5 items, each starting with #"]
  },
  "instagram": {
    "visual_type": "CAROUSEL or SINGLE_IMAGE",
    "slide_count": "integer, equals the number of items in slides (1 for SINGLE_IMAGE)",
    "slides": [
      { "slide_number": 1, "headline": "...", "subtext": "..." }
    ],
    "caption": "Complete caption including CTA, with hashtags at the end",
    "image_generation_prompt": "Visual direction for the designer or image model",
    "hashtags": ["10 to 15 items, each starting with #"]
  },
  "fact_check_items": ["Every [VERIFY] claim or figure the reviewer must confirm before approving. Empty list if none."],
  "telegram_approval_summary": "3 short lines for mobile review"
}
```
<!-- SYSTEM PROMPT END -->

---

## 2. Structured Input & Output Examples (For API / Automation)

### Input Payload (sent by the automation to the AI)
The automation, not the AI, picks the pillar from the weekday table above and sets the date.

```json
{
  "date": "2026-10-13",
  "day_of_week": "Tuesday",
  "pillar": "Audit & Internal Financial Controls",
  "topic_idea": "3 subtle cash flow leaks in mid-size trading companies and how internal audit detects them",
  "target_language": "English",
  "post_history": [
    {
      "date": "2026-10-12",
      "platform": "LinkedIn",
      "pillar": "Tax Strategy & Compliance",
      "hook": "Most business owners don't realize their tax structure is leaking cash until the tax authority calls.",
      "performance_notes": "High engagement from local CEOs, loved bulleted solutions"
    },
    {
      "date": "2026-10-12",
      "platform": "Instagram",
      "pillar": "Tax Strategy & Compliance",
      "hook": "Audit is not a penalty. It is your financial shield.",
      "performance_notes": "Carousel received 45 saves"
    }
  ]
}
```

### Example Output (returned by the AI)
```json
{
  "post_id": "DAILY-2026-10-13",
  "date": "2026-10-13",
  "pillar": "Audit & Internal Financial Controls",
  "language": "English",
  "core_insight": "Most cash leaks in trading companies are process gaps, and a regular internal audit cycle finds them before they hit working capital.",
  "linkedin": {
    "hook": "Your P&L can look healthy while cash quietly leaks out of the business.",
    "full_text": "Your P&L can look healthy while cash quietly leaks out of the business.\n\n...\n\nWhich of these leaks have you seen in your own company?\nIf you want a second pair of eyes on your controls, send me a message.\n\n#InternalAudit #CFOInsights #FinancialGovernance #UzbekistanBusiness",
    "call_to_action": "Which of these leaks have you seen in your own company? If you want a second pair of eyes on your controls, send me a message.",
    "hashtags": ["#InternalAudit", "#CFOInsights", "#FinancialGovernance", "#UzbekistanBusiness"]
  },
  "instagram": {
    "visual_type": "CAROUSEL",
    "slide_count": 5,
    "slides": [
      {
        "slide_number": 1,
        "headline": "3 Silent Cash Leaks in Your Company",
        "subtext": "(And how to plug them before Q4)"
      },
      {
        "slide_number": 2,
        "headline": "Leak #1: Unreconciled Supplier Prepayments",
        "subtext": "Duplicate payments and forgotten aged prepayments when supplier balances are not reconciled monthly."
      },
      {
        "slide_number": 3,
        "headline": "Leak #2: Obsolete Inventory Valuation",
        "subtext": "Dead stock still carried as an asset on paper while working capital is choked."
      },
      {
        "slide_number": 4,
        "headline": "Leak #3: Uncontrolled Discretionary Spend",
        "subtext": "Small recurring subscriptions and untracked petty cash that add up every month."
      },
      {
        "slide_number": 5,
        "headline": "The Fix: A 90-Day Internal Audit Cycle",
        "subtext": "Save this guide and review your monthly close. Follow @mezon.advisory for daily finance insights."
      }
    ],
    "caption": "Your profit is real. Is your cash? ...\n\n#FinanceConsulting #BusinessAudit ...",
    "image_generation_prompt": "Clean executive aesthetic, dark navy background #0F172A, gold accents, professional financial typography, minimalist chart",
    "hashtags": ["#FinanceConsulting", "#BusinessAudit", "#InternalAudit", "#TaxAdvisory", "#CFO", "#CashFlow", "#FinancialControls", "#UzbekistanBusiness", "#TashkentBusiness", "#CentralAsiaBusiness"]
  },
  "fact_check_items": [],
  "telegram_approval_summary": "Tuesday | Audit & Controls\nLI: Your P&L can look healthy while cash leaks out.\nIG: 5-slide carousel, 3 cash leaks + 90-day audit fix"
}
```

---

## 3. Human-in-the-Loop Automation Architecture

Nothing is published until you approve it. The flow:

```
┌──────────────────────────────────────────┐
│ Scheduled Trigger (daily 07:00 Tashkent) │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│ Read Context from Content Log            │
│ (Google Sheets / Airtable: post history, │
│  topic backlog, pillar for the weekday)  │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│ AI Generation Engine (LLM)               │
│ (System Prompt + Input Payload)          │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│ Validate JSON + Render Images            │
│ (Canva template / image API, host the    │
│  JPEGs at a public HTTPS URL)            │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ Send Preview to Your Telegram / Slack / Email                │
│ [ Approve & Publish ] [ Edit ] [ Regenerate ] [ Reject ]     │
└───────┬──────────────────┬──────────────────┬────────────────┘
        ▼                  ▼                  ▼
  [Approve]          [Edit / Regenerate]   [Reject]
        │                  │                  │
        ▼                  ▼                  ▼
  Publish to LinkedIn  You reply with      Log as rejected,
  & Instagram via      changes; AI         no post today
  official APIs, then  redrafts and a
  log to Content Log   new preview is sent
```

---

## 4. Automation Implementation Options

### Prerequisites (both options)
- **LinkedIn:** A LinkedIn developer app with the "Share on LinkedIn" product (scope `w_member_social`) to post on your personal profile. Posting as the Mezon Advisory company page needs `w_organization_social` through the Community Management API, which requires LinkedIn approval. Access tokens expire after 60 days and must be refreshed.
- **Instagram:** An Instagram **Business or Creator** account linked to a Facebook Page, plus a Meta app with `instagram_basic` and `instagram_content_publish`. Personal Instagram accounts cannot publish via API.
- **Images:** The Instagram API only accepts images by public HTTPS URL (JPEG). The AI produces text and an image prompt, not images, so you need a rendering step (Canva template, image-generation API or a designer) before approval.
- **Content Log:** One Google Sheet (or Airtable base) used as the source of truth for history, topic backlog and engagement. Reading your own post history back from the LinkedIn API is restricted, so log every post at publish time instead.

### Option A: Make.com / n8n Workflow (No-code / Low-code)
1. **Trigger:** `Schedule` module, daily at 07:00 (Asia/Tashkent), 7 days a week to match the 7 pillars. If you only post on weekdays, drop the Saturday and Sunday pillars.
2. **Step 1 (Context):** `Google Sheets / Airtable`: read the last 14 posts, today's pillar and the next topic from the backlog.
3. **Step 2 (LLM):** `Claude / OpenAI / Gemini` API call with the System Prompt (Section 1) as the system message and the Input Payload as the user message. Enable JSON output mode where supported.
4. **Step 3 (Validate & Render):** Parse the JSON; if it fails, retry once. Render carousel slides from a template and upload them to public storage.
5. **Step 4 (Approval Dispatch):** `Telegram Bot: Send Message` with an inline keyboard. Each button carries `callback_data` such as `approve:<post_id>` (max 64 bytes):
   - `Approve & Publish`
   - `Edit` (bot asks you to reply with your changes)
   - `Regenerate`
   - `Reject`
6. **Step 5 (Callback Handler):** A `Telegram Bot: Watch Updates` trigger (or webhook) receives the button tap. On `approve`:
   - **LinkedIn:** `POST https://api.linkedin.com/rest/posts` with headers `LinkedIn-Version: YYYYMM` and `X-Restli-Protocol-Version: 2.0.0`. (`/v2/ugcPosts` is the legacy endpoint.)
   - **Instagram carousel:** create one container per image with `POST /{ig-user-id}/media` (`image_url`, `is_carousel_item=true`), then a parent container with `media_type=CAROUSEL`, `children` and `caption`, then `POST /{ig-user-id}/media_publish` with the parent `creation_id`. For a single image, skip the child step.
   - Write the post to the Content Log and confirm in Telegram: *"Published successfully."*

### Option B: Python Automation Script (Self-Hosted)
Core logic for drafting and sending the approval request. Install with `pip install google-genai requests`.

```python
import html
import json
import os
import re

import requests
from google import genai
from google.genai import types

# Configuration
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
PROMPT_FILE = "SOCIAL_MEDIA_AUTOMATION_PROMPT.md"


def load_system_prompt(path=PROMPT_FILE):
    """Return only the system prompt block from Section 1, not the whole file."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    match = re.search(
        r"<!-- SYSTEM PROMPT START -->\s*```markdown\n(.*?)\n```\s*<!-- SYSTEM PROMPT END -->",
        text,
        re.DOTALL,
    )
    if not match:
        raise ValueError("System prompt markers not found in " + path)
    return match.group(1)


def generate_daily_content(payload):
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=json.dumps(payload, ensure_ascii=False),
        config=types.GenerateContentConfig(
            system_instruction=load_system_prompt(),
            response_mime_type="application/json",
        ),
    )
    return json.loads(response.text)


def send_telegram_approval(content):
    # HTML parse mode + escaping, so *, _ and [ in AI text cannot break the message.
    esc = html.escape
    checks = content.get("fact_check_items") or []
    text = (
        "📢 <b>NEW POST DRAFT FOR APPROVAL</b>\n"
        f"<b>Pillar:</b> {esc(content['pillar'])}\n\n"
        f"💼 <b>LinkedIn hook:</b>\n{esc(content['linkedin']['hook'])}\n\n"
        f"📸 <b>Instagram slide 1:</b>\n{esc(content['instagram']['slides'][0]['headline'])}\n\n"
        + (f"⚠️ <b>Verify before approving:</b>\n" + "\n".join(esc(c) for c in checks) + "\n\n" if checks else "")
        + "Tap a button below."
    )
    post_id = content["post_id"]
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "✅ Approve & Publish", "callback_data": f"approve:{post_id}"}],
                [{"text": "✏️ Edit", "callback_data": f"edit:{post_id}"},
                 {"text": "🔄 Regenerate", "callback_data": f"regen:{post_id}"}],
                [{"text": "❌ Reject", "callback_data": f"reject:{post_id}"}],
            ]
        },
    }
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    r = requests.post(url, json=payload, timeout=30)
    r.raise_for_status()


if __name__ == "__main__":
    # Example execution. In production, read these values from the Content Log.
    payload = {
        "date": "2026-10-12",
        "day_of_week": "Monday",
        "pillar": "Tax Strategy & Compliance",
        "topic_idea": "3 legal ways companies reduce tax liabilities before year-end",
        "target_language": "English",
        "post_history": [
            {"platform": "LinkedIn", "hook": "Tax optimization is not an aggressive loophole."}
        ],
    }
    post = generate_daily_content(payload)
    send_telegram_approval(post)
```

**Not included in this script (build next):** the callback handler that listens for button taps (Telegram webhook or `getUpdates` polling), the image rendering step, the LinkedIn and Instagram publish calls from Option A Step 5, and writing results to the Content Log. Store each draft by `post_id` (file, SQLite or the Sheet) so the handler can publish exactly the draft you approved.

---

## 5. Daily Execution Checklist for You

| Step | Time (Tashkent) | What Happens |
| :--- | :--- | :--- |
| **1. Automated Draft** | 07:00 | Automation picks the weekday pillar and topic, AI drafts LinkedIn & Instagram posts, images are rendered. |
| **2. Mobile Notification** | ~07:05 | Telegram / Slack sends you the preview, carousel slides and any `[VERIFY]` items. |
| **3. Review & Approve** | 07:05 to 08:30 | Read for 1 to 2 minutes, check flagged facts, tap **Approve** (or Edit / Regenerate / Reject). |
| **4. Automated Publishing** | On approval | APIs publish to LinkedIn and Instagram; the post is written to the Content Log. |
| **5. Performance Logging** | 21:00 | Engagement is added to the Content Log to guide the next drafts. Instagram Insights is available via API for Business/Creator accounts; LinkedIn personal-profile analytics are limited via API, so enter key numbers manually if needed. |

---

*File created and maintained for Mezon Advisory Social Media Automation.*
