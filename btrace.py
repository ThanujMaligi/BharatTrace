#!/usr/bin/env python3
"""
BharatTrace - AI Terminal Exception Explainer & One-Click Auto-Fix CLI
Powered by BharatCode API
Author: Thanuj Kumar Maligi (@ThanujMaligi)
"""

import os
import sys
import json
import click
import requests
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

BHARATCODE_API_KEY = os.getenv("BHARATCODE_API_KEY", "")
BHARATCODE_API_URL = os.getenv(
    "BHARATCODE_API_URL", "https://api.bharatcode.ai/v1/chat/completions"
)

SYSTEM_PROMPT = """You are BharatTrace, an intelligent terminal debugging agent powered by BharatCode.
The user provides a terminal error, stack trace, or compiler failure along with optional local file context.
Your goal:
1. Explain the root cause in 2 concise, clear sentences.
2. Provide the exact fix (terminal command or code replacement).
3. Be direct, practical, and prioritize zero-fluff developer solutions."""

def call_bharatcode(error_log: str, context: str = "") -> str:
    """Send traceback and code context to BharatCode API with graceful demo fallback."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BHARATCODE_API_KEY}" if BHARATCODE_API_KEY else ""
    }
    
    user_content = f"Error / Traceback:\n```\n{error_log}\n```"
    if context:
        user_content += f"\n\nSource Code Context:\n```\n{context}\n```"

    payload = {
        "model": "qwen-3.8-27b",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.2
    }

    if not BHARATCODE_API_KEY:
        # Graceful interactive demo mode for evaluation
        return (
            "### 🔍 Root Cause Analysis (Demo Mode)\n"
            "**Exception Detected:** `KeyError` or missing configuration in execution stream.\n\n"
            "### 🛠️ Proposed Solution:\n"
            "Ensure the target key or environment variable is loaded before accessing dictionary objects.\n\n"
            "```python\n"
            "# Suggested Fix:\n"
            "value = data.get('key_name', default_fallback)\n"
            "```\n\n"
            "> *Tip: Set `export BHARATCODE_API_KEY=your_key` for live BharatCode Qwen-27B inference.*"
        )

    try:
        response = requests.post(BHARATCODE_API_URL, headers=headers, json=payload, timeout=25)
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"**BharatCode API Error (Status {response.status_code}):** {response.text}"
    except Exception as e:
        return f"**Connection Error:** {str(e)}"


@click.group()
def cli():
    """BharatTrace: AI Terminal Exception Explainer & One-Click Fix CLI."""
    pass


@cli.command()
@click.argument("error_text", required=False)
@click.option("--file", "-f", help="Path to failing file for local context.")
def explain(error_text, file):
    """Explain a crash or traceback from stdin or argument."""
    if not error_text:
        if not sys.stdin.isatty():
            error_text = sys.stdin.read().strip()
        else:
            console.print("[bold red]Usage Error:[/bold red] Pipe an error or provide text: `python app.py 2>&1 | btrace explain`")
            return

    context = ""
    if file and os.path.exists(file):
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            context = f.read()

    with console.status("[bold green]Analyzing error with BharatCode AI...", spinner="dots"):
        solution = call_bharatcode(error_text, context)

    console.print("\n")
    console.print(Panel(Markdown(solution), title="[bold cyan]BharatTrace AI Diagnosis[/bold cyan]", border_style="cyan"))


@cli.command()
@click.argument("cmd", nargs=-1, required=True)
def run(cmd):
    """Run any command and automatically catch & diagnose failures."""
    cmd_str = " ".join(cmd)
    console.print(f"[dim]Running: {cmd_str}...[/dim]\n")
    
    proc = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate()

    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)

    if proc.returncode != 0:
        console.print("\n")
        console.print(Panel("[bold red]Command Failed![/bold red] Triggering BharatTrace Diagnosis...", border_style="red"))
        with console.status("[bold green]Querying BharatCode API for fix...", spinner="dots"):
            solution = call_bharatcode(stderr or stdout)
        console.print(Panel(Markdown(solution), title="[bold green]BharatTrace Recommended Fix[/bold green]", border_style="green"))


if __name__ == "__main__":
    cli()
