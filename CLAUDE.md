# CLAUDE.md — Deep Research Repository

This file describes the purpose, workflows, conventions, and AI instructions for this repository.

---

## Repository Purpose

This repository is dedicated to **AI-driven multi-angle deep research with comparative analysis**.

The core philosophy: a single research pass is never enough. By approaching a topic from multiple independent angles — including live community signals from Discord — comparing the results for commonalities and contradictions, and then structuring those findings into a coherent analytical framework, we produce insights that no single-pass research can achieve.

**High-level flow:**

```
Topic
  └─► Multi-angle Research (parallel streams)
  │     ├─ Web / academic research (per angle)
  │     └─ Discord community research (via MCP)
        └─► Cross-angle Comparison (commonalities / differences)
              └─► Synthesis & Structural Analysis (framework / diagram)
                    └─► Final Report + Notebook + Audio
```

---

## Directory Structure

```
research/
├── CLAUDE.md                        # This file
├── topics/                          # One subdirectory per research topic
│   └── <topic-slug>/
│       ├── brief.md                 # Research question and scope definition
│       ├── angles/                  # Independent research by angle
│       │   ├── technical.md
│       │   ├── historical.md
│       │   ├── economic.md
│       │   ├── social.md
│       │   ├── policy.md
│       │   ├── future_outlook.md
│       │   └── discord_community.md # Community signals gathered via Discord MCP
│       ├── comparison.md            # Cross-angle: commonalities & differences
│       ├── framework.md             # Synthesized structural analysis / framework
│       ├── report.md                # Final comprehensive report
│       ├── notebook.ipynb           # Jupyter Notebook version of the report
│       └── audio_script.md          # Narration script for audio commentary
├── templates/                       # Reusable templates
│   ├── angle_template.md
│   ├── comparison_template.md
│   ├── framework_template.md
│   ├── report_template.md
│   ├── notebook_template.ipynb
│   └── audio_script_template.md
└── scripts/                         # Automation scripts
    ├── generate_notebook.py         # Converts report.md → notebook.ipynb
    └── generate_audio.py            # Converts audio_script.md → audio file
```

---

## Research Workflow for Claude

### Step 1: Define Research Angles

Before starting, define 4–6 distinct lenses through which to examine the topic. Default angles:

| Angle | What to investigate |
|-------|---------------------|
| **Technical** | Mechanisms, how it works, current state of technology |
| **Historical** | Origins, evolution, key milestones and turning points |
| **Economic** | Market dynamics, incentives, costs, winners and losers |
| **Social** | Human impact, culture, equity, public perception |
| **Policy / Regulatory** | Laws, governance, geopolitics, standards bodies |
| **Future Outlook** | Trends, forecasts, expert predictions, open questions |

Adjust angles based on topic — not all angles are relevant for every topic.

The **Discord Community** angle is always included when a relevant server is available — it captures real practitioner sentiment, emerging debates, and tacit knowledge not found in formal sources.

### Step 2: Multi-Angle Deep Research

For **each angle independently**:
- Research deeply and thoroughly from that angle's perspective
- Do not let other angles contaminate — stay in the lane of this angle
- Cite sources with URLs
- Capture key data points, quotes, and findings
- Output each angle to `topics/<topic-slug>/angles/<angle>.md`

> **Important:** Treat each angle as if it were a standalone research task. The goal is genuine depth per angle, not a surface overview from all angles.

#### Discord Community Angle (via MCP)

When a Discord server is provided as part of the research brief, use the Discord MCP to gather community intelligence:

**What to collect:**
- Dominant topics and recurring questions in relevant channels
- Strong opinions and debates (what people fight about)
- Practitioner workarounds, tips, and undocumented knowledge
- Sentiment trends: excitement, frustration, confusion, distrust
- Influential voices and their positions
- Links, tools, or resources frequently shared by the community

**How to structure `angles/discord_community.md`:**

```markdown
# Discord Community Research: <Topic>

## Server(s) Analyzed
- Server: <name> | Invite: <url>
- Channels reviewed: #channel-a, #channel-b, ...
- Date range analyzed: YYYY-MM-DD to YYYY-MM-DD

## Key Themes
1. <Theme> — summary of what people are saying
2. ...

## Major Debates / Disagreements
- <Topic>: <Side A> vs <Side B>

## Practitioner Insights (not in official docs)
- ...

## Sentiment Summary
- Overall tone: [enthusiastic / cautious / frustrated / mixed]
- Top positive signals: ...
- Top pain points: ...

## Influential Voices
- @username — known for: ...

## Frequently Shared Resources
- [Title](URL) — why it's popular
```

**Discord MCP setup** (see [MCP Setup](#discord-mcp-setup) section below).

### Step 3: Cross-Angle Comparison

After all angles are complete, perform a structured comparison:

**Identify Commonalities:**
- What conclusions appear across multiple angles independently?
- Where do different disciplines converge on the same insight?
- What facts or data points are corroborated by multiple angles?

**Identify Differences and Tensions:**
- Where do angles contradict each other?
- What does one angle see as a benefit that another sees as a risk?
- What assumptions differ between angles?
- What would each angle prioritize differently?

**Identify Blind Spots:**
- What does each angle miss or underweight?
- Which angle's framing is most commonly adopted in public discourse, and what does that hide?

Output the full comparison to `topics/<topic-slug>/comparison.md`.

### Step 4: Structural Analysis and Framework

Using the comparison as input, build a **synthesized analytical framework**:

- Construct a mental model or diagram that captures the core dynamics
- Name and define the key forces, tensions, and feedback loops
- Show how the different angles relate to each other
- Propose a 2x2 matrix, a causal map, a timeline overlay, or a systems diagram — whichever best fits the topic
- Articulate the "core insight" that only emerges from combining all angles

Output to `topics/<topic-slug>/framework.md`.

The framework section should include:
1. **Framework title** — a short name for the model
2. **Core insight** — 1–3 sentences summarizing the key finding
3. **Diagram or structured description** — ASCII or Mermaid diagram if applicable
4. **Key tensions** — the 2–4 central trade-offs or contradictions
5. **Implications** — what this framework suggests for decision-makers, researchers, or practitioners

### Step 5: Final Report Synthesis

Synthesize all previous steps into a final report:
- Executive summary (5–7 bullet points capturing the most important findings)
- One section per angle (summarized, not repeated verbatim)
- Cross-angle comparison section
- Framework section (with diagram)
- Conclusions and open questions
- Full citations list

Output to `topics/<topic-slug>/report.md`.

### Step 6: Notebook Generation

Convert the report into a Jupyter Notebook:
- Each major section becomes a Markdown cell
- Data tables become structured cells
- Include Python code cells for any data visualizations where data is available
- Framework diagrams rendered as images or Mermaid code cells
- Output to `topics/<topic-slug>/notebook.ipynb`

### Step 7: Audio Script

Create an audio narration script:
- Conversational tone (explaining to a smart, curious friend)
- No markdown — plain spoken language
- Structure: Hook → Context → Angle-by-angle tour → Comparison highlights → Framework reveal → Key takeaways → Closing question
- Estimated reading time at the top (assume 150 words/minute)
- Output to `topics/<topic-slug>/audio_script.md`

---

## Comparison Template

When writing `comparison.md`, use this structure:

```markdown
# Cross-Angle Comparison: <Topic>

## Commonalities (What all/most angles agree on)
- ...
- ...

## Key Differences and Tensions
| Dimension | Angle A says... | Angle B says... | Tension |
|-----------|-----------------|-----------------|---------|
| ...       | ...             | ...             | ...     |

## Surprising Contradictions
- ...

## Blind Spots by Angle
| Angle | What it misses |
|-------|----------------|
| ...   | ...            |

## Emerging Synthesis Questions
(Questions that only arise when you compare angles)
- ...
```

---

## Framework Template

When writing `framework.md`, use this structure:

```markdown
# Analytical Framework: <Framework Title>

## Core Insight
<1–3 sentence summary of the insight that only emerges from multi-angle analysis>

## Diagram
<ASCII, Mermaid, or structured description>

## Key Forces / Components
1. **<Force A>** — description
2. **<Force B>** — description
...

## Central Tensions
- <Tension 1>: <Angle X> pulls toward X, while <Angle Y> pulls toward Y
- ...

## Implications
- For practitioners: ...
- For policy: ...
- For future research: ...
```

---

## Discord MCP Setup

To enable Claude to read Discord channels directly, configure a Discord MCP server.

### Option A: v-3/discordmcp (recommended — simple setup)

**GitHub:** [https://github.com/v-3/discordmcp](https://github.com/v-3/discordmcp)

```bash
# Install
npm install -g discordmcp

# Add to Claude Code MCP config (~/.claude/settings.json or .claude/settings.json)
```

```json
{
  "mcpServers": {
    "discord": {
      "command": "discordmcp",
      "env": {
        "DISCORD_TOKEN": "<your-discord-bot-token>",
        "DISCORD_GUILD_ID": "<optional-default-server-id>"
      }
    }
  }
}
```

### Option B: SaseQ/discord-mcp (Docker-based, more features)

**GitHub:** [https://github.com/SaseQ/discord-mcp](https://github.com/SaseQ/discord-mcp)

```bash
docker pull saseq/discord-mcp
```

```json
{
  "mcpServers": {
    "discord": {
      "command": "docker",
      "args": ["run", "--rm", "-e", "DISCORD_TOKEN", "saseq/discord-mcp"],
      "env": {
        "DISCORD_TOKEN": "<your-discord-bot-token>"
      }
    }
  }
}
```

### Creating a Discord Bot Token

1. Go to [https://discord.com/developers/applications](https://discord.com/developers/applications)
2. Create a new application → Bot → Reset Token → copy the token
3. Enable **Message Content Intent** under Privileged Gateway Intents
4. Invite the bot to your server with at minimum `Read Messages` and `Read Message History` permissions
5. Set `DISCORD_TOKEN` in your MCP config (never commit this to the repo — use env vars or a secrets manager)

### Key MCP Tools Available

Once configured, Claude can use these tools:

| Tool | What it does |
|------|-------------|
| `discord_read_messages` | Read recent messages from a channel |
| `discord_list_channels` | List all channels in a server |
| `discord_get_server_info` | Get server metadata |
| `discord_search_messages` | Search messages by keyword |
| `discord_get_thread` | Read a specific thread |

### Security Notes

- **Never commit `DISCORD_TOKEN` to git** — add it to `.env` and `.gitignore`
- Bot only accesses servers it has been explicitly invited to
- Use read-only permissions unless write access is needed
- Treat gathered Discord data as potentially sensitive; do not publish raw message logs

---

## Report Quality Standards

| Criterion | Requirement |
|-----------|-------------|
| Multi-angle coverage | At least 4 distinct angles researched independently (Discord angle included when server available) |
| Comparison depth | Explicit commonalities AND differences documented |
| Framework quality | A synthesized model that goes beyond summarizing each angle |
| Evidence | Data, statistics, citations per angle |
| Balance | No single angle's framing dominates the final report |
| Clarity | Readable by a non-expert; jargon explained |
| Length | Proportional to complexity (typically 3,000–8,000 words for full report) |

---

## Conventions

### File Naming
- Use lowercase with hyphens for topic slugs: `climate-finance`, `llm-safety`, `quantum-computing`
- Angle files: `technical.md`, `economic.md`, `social.md`, etc.

### Markdown Style
- Use `#` for top-level headings, `##` for sections, `###` for subsections
- Use tables for comparative information
- Use blockquotes (`>`) for direct quotes from sources
- Use footnote-style links when citing: `[Source Title](URL)`
- Use Mermaid fenced code blocks for diagrams: ` ```mermaid `

### Git Commits
- Commit message format: `research(<topic>): <what was done>`
- Examples:
  - `research(ai-governance): add technical and historical angle research`
  - `research(ai-governance): add cross-angle comparison`
  - `research(ai-governance): add analytical framework`
  - `research(ai-governance): add final report and notebook`

---

## AI Assistant Instructions

When working in this repository, Claude should:

1. **Always research each angle independently** — do not blend angles during the research phase
2. **Never skip the comparison step** — the comparison is where the real insight lives
3. **Build a genuine framework** — not just a summary, but a structural model that reveals something new
4. **Actively search the web** for recent information; do not rely solely on training data
5. **Be explicit about uncertainty** — if a claim is uncertain or contested, say so and note which angle makes the claim
6. **Produce complete files** — do not leave placeholders like `[TODO]` in final outputs
7. **Check existing work** before starting — if angle files already exist, read them first
8. **Use Discord MCP** when a server is provided — community signals are a first-class research source, not an afterthought
9. **Never share raw Discord message logs** in reports — synthesize and anonymize
10. **Update this CLAUDE.md** if the project structure or workflow evolves

---

## Audio Generation Notes

- Target voice: clear, neutral, educational (like a podcast or documentary narration)
- Script structure: Hook → Context → Angle Tour → Comparison Highlights → Framework Reveal → Key Takeaways → Closing
- Estimated duration: 8–20 minutes per report
- Tool integration (future): `scripts/generate_audio.py` calls a TTS API

---

## Notebook Generation Notes

- Reports become structured notebooks with Markdown and code cells
- Where data is available, include Python code to fetch/visualize it
- Framework diagrams rendered as Mermaid code or matplotlib figures
- Notebooks should be runnable (no broken imports or missing data)
- Tool integration: `scripts/generate_notebook.py` converts `report.md` to `.ipynb`

---

## Getting Started (for a new research topic)

```bash
# Create the topic directory structure
mkdir -p topics/<topic-slug>/angles

# Add the research brief
cat > topics/<topic-slug>/brief.md << 'EOF'
# Research Brief: <Topic Title>

## Core Question
<What do we want to understand?>

## Scope
<What is in / out of scope?>

## Angles to Research
- [ ] Technical
- [ ] Historical
- [ ] Economic
- [ ] Social
- [ ] Policy / Regulatory
- [ ] Future Outlook

## Key Deliverables
- [ ] angles/*.md (one per angle)
- [ ] comparison.md
- [ ] framework.md
- [ ] report.md
- [ ] notebook.ipynb
- [ ] audio_script.md
EOF

# Then instruct Claude to execute the full 7-step workflow
```

---

*This CLAUDE.md was last updated: 2026-03-23 (added Discord MCP integration)*
