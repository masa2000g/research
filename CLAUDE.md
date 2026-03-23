# CLAUDE.md — Deep Research Repository

This file describes the purpose, workflows, conventions, and AI instructions for this repository.

---

## Repository Purpose

This repository is dedicated to **AI-driven deep research**. The workflow is:

1. **Research** — Claude performs comprehensive deep research on a given topic
2. **Review & Expand** — Claude reviews its own research, identifies gaps, and performs additional targeted research
3. **Report Generation** — Claude produces a high-quality, information-dense, multi-angle report
4. **Notebook Integration** — Reports are automatically structured into Jupyter Notebooks (`.ipynb`)
5. **Audio Commentary** — Reports are converted into audio narration scripts or audio files

---

## Directory Structure (Intended)

```
research/
├── CLAUDE.md                  # This file
├── topics/                    # One subdirectory per research topic
│   └── <topic-slug>/
│       ├── brief.md           # Initial research brief / prompt
│       ├── research.md        # Raw research output (first pass)
│       ├── review.md          # Self-review notes and gap analysis
│       ├── deep_research.md   # Follow-up focused research
│       ├── report.md          # Final synthesized report
│       ├── notebook.ipynb     # Jupyter Notebook version of the report
│       └── audio_script.md    # Narration script for audio commentary
├── templates/                 # Reusable templates
│   ├── report_template.md
│   ├── notebook_template.ipynb
│   └── audio_script_template.md
└── scripts/                   # Automation scripts
    ├── generate_notebook.py   # Converts report.md → notebook.ipynb
    └── generate_audio.py      # Converts audio_script.md → audio file
```

---

## Research Workflow for Claude

### Step 1: Initial Deep Research

When given a research topic:
- Search broadly across multiple angles: technical, historical, economic, social, policy, and future outlook
- Cite sources with URLs where possible
- Identify key players, key data points, and competing perspectives
- Output to `topics/<topic-slug>/research.md`

### Step 2: Self-Review and Gap Analysis

After initial research:
- Re-read the research output critically
- Ask: What is missing? What is shallow? What is contested?
- Identify 3–7 specific gaps or questions that need deeper investigation
- Output gap analysis to `topics/<topic-slug>/review.md`

### Step 3: Targeted Deep Dive

For each identified gap:
- Perform focused research to fill that specific gap
- Prioritize primary sources, recent data, and expert opinions
- Output to `topics/<topic-slug>/deep_research.md`

### Step 4: Final Report Synthesis

Synthesize all research into a final report:
- Use clear section headers
- Include an executive summary (3–5 bullet points)
- Present multiple perspectives (not just one viewpoint)
- Include data, statistics, and concrete examples
- End with conclusions and open questions
- Output to `topics/<topic-slug>/report.md`

### Step 5: Notebook Generation

Convert the report into a Jupyter Notebook:
- Each major section becomes a Markdown cell
- Data tables become structured cells
- Charts or visualizations are included where applicable
- Output to `topics/<topic-slug>/notebook.ipynb`

### Step 6: Audio Script

Create an audio narration script:
- Conversational tone (as if explaining to a smart friend)
- No markdown formatting — plain spoken language
- Estimated reading time noted at the top
- Output to `topics/<topic-slug>/audio_script.md`

---

## Report Quality Standards

A high-quality report in this repository must meet these standards:

| Criterion | Requirement |
|-----------|-------------|
| Coverage | Multiple angles covered (technical, social, economic, etc.) |
| Depth | Not just surface-level; goes into mechanisms and causes |
| Balance | Competing perspectives acknowledged |
| Evidence | Data, statistics, citations included |
| Clarity | Readable by a non-expert; jargon explained |
| Structure | Clear sections, executive summary, conclusions |
| Length | Proportional to topic complexity (typically 1,500–5,000 words) |

---

## Conventions

### File Naming
- Use lowercase with hyphens for topic slugs: `climate-finance`, `llm-safety`, `quantum-computing`
- Date-prefix versions if iterating: `report_v2.md`, `report_2026-03.md`

### Markdown Style
- Use `#` for top-level headings, `##` for sections, `###` for subsections
- Use tables for comparative information
- Use blockquotes (`>`) for direct quotes from sources
- Use footnote-style links when citing: `[Source Title](URL)`

### Git Commits
- Commit message format: `research(<topic>): <what was done>`
- Examples:
  - `research(ai-governance): add initial deep research`
  - `research(ai-governance): add self-review and gap analysis`
  - `research(ai-governance): add final report and notebook`

---

## AI Assistant Instructions

When working in this repository, Claude should:

1. **Always follow the 6-step workflow** described above for any new research topic
2. **Never skip the self-review step** — this is critical to quality
3. **Actively search the web** for recent information; do not rely solely on training data
4. **Be explicit about uncertainty** — if a claim is uncertain, say so
5. **Produce complete files** — do not leave placeholders like `[TODO]` in final outputs
6. **Check existing research** before starting — if `research.md` already exists, read it first
7. **Update this CLAUDE.md** if the project structure or workflow evolves

---

## Audio Generation Notes

For audio commentary:
- Target voice: clear, neutral, educational (like a podcast or documentary narration)
- Script structure: Hook → Context → Deep Dive → Key Takeaways → Closing
- Estimated duration: 5–15 minutes per report
- Tool integration (future): scripts in `scripts/generate_audio.py` will call a TTS API

---

## Notebook Generation Notes

For Jupyter Notebooks:
- Reports become structured notebooks with Markdown and code cells
- Where data is available, include Python code to fetch/visualize it
- Notebooks should be runnable (no broken imports or missing data)
- Tool integration: `scripts/generate_notebook.py` converts `report.md` to `.ipynb`

---

## Getting Started (for a new research topic)

```bash
# Create the topic directory
mkdir -p topics/<topic-slug>

# Add the research brief
echo "# Research Brief: <Topic Title>\n\nResearch question: ..." > topics/<topic-slug>/brief.md

# Then ask Claude to execute the full 6-step research workflow
```

---

*This CLAUDE.md was last updated: 2026-03-23*
