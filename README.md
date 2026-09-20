# WebScraper

An app that extracts email addresses from any website by pasting its URL.

## Features

- Paste a URL and scrape every email address on the page in one click
- Duplicate emails are ignored automatically
- Browse collected emails and export them as a CSV file
- Domain statistics dashboard

## Requirements

- Python 3.10+
- Django 5.0

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/scrape/, paste a URL and hit Scrape.

## Configuration

Copy `env.example` to `.env` to override the Django secret key, debug mode and
allowed hosts.

## Tests

```bash
python manage.py test
```

## How the auto-agent works

This repository is continuously improved by an autonomous agent
(`webscraper_agent.py`). It watches for internet connectivity, and whenever the
machine is online it applies the next pending item in `PROGRESS.md`, commits it
and pushes it to GitHub. The backlog and history of applied changes live in
`PROGRESS.md`.
