# AI Shorts Automation Software

`shorts-automation` is a lightweight Python CLI that generates a complete YouTube Shorts production package from a single topic prompt.

## What it creates

Given a topic, the tool generates:

- A **title**, **description**, and **hashtags**
- A full **voiceover script** with hook + CTA
- A timestamped **scene-by-scene shot list**
- A production **checklist** for exporting and uploading
- Output as both JSON (`shorts_project.json`) and Markdown (`shorts_project.md`)

## Install

```bash
python -m pip install -e .
```

## Usage

```bash
shorts-automation "AI tools for creators" \
  --angle "problem-solution" \
  --audience "beginner creators" \
  --duration 35 \
  --output output/creators-short
```

Or without installation:

```bash
PYTHONPATH=src python -m shorts_automation.cli "AI side hustles"
```

## Optional OpenAI mode

If `OPENAI_API_KEY` is set and the `openai` Python package is installed, the generator attempts to use OpenAI for richer scripts. If anything fails, it automatically falls back to local deterministic generation.

## Output example

After running, the output directory contains:

- `shorts_project.json`
- `shorts_project.md`

These files are ready for editors, content teams, or downstream automation workflows.
