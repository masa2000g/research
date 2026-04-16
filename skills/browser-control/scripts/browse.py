#!/usr/bin/env python3
"""
汎用ブラウザ操作スクリプト for OpenClaw browser-control skill.

Usage:
  python3 browse.py open <url> [--screenshot <path>] [--profile <name>] [--headless]
  python3 browse.py read <url> [--profile <name>] [--selector <css>]
  python3 browse.py click <url> --selector <css> [--profile <name>]
  python3 browse.py type <url> --selector <css> --text <text> [--profile <name>]
  python3 browse.py search <query> [--max-results <n>]
"""

import argparse
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

PROFILES_DIR = Path.home() / ".playwright-profiles"


def get_profile_dir(name: str) -> Path:
    d = PROFILES_DIR / name
    d.mkdir(parents=True, exist_ok=True)
    return d


def cmd_open(args):
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(get_profile_dir(args.profile)),
            headless=args.headless,
        )
        page = ctx.new_page()
        page.goto(args.url, wait_until="domcontentloaded", timeout=30000)
        print(f"Opened: {page.title()}")
        if args.screenshot:
            page.screenshot(path=args.screenshot, full_page=True)
            print(f"Screenshot saved: {args.screenshot}")
        if args.headless:
            ctx.close()
        else:
            print("Browser open. Close manually or Ctrl+C to exit.")
            try:
                page.wait_for_timeout(3600000)
            except KeyboardInterrupt:
                pass
            ctx.close()


def cmd_read(args):
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(get_profile_dir(args.profile)),
            headless=True,
        )
        page = ctx.new_page()
        page.goto(args.url, wait_until="domcontentloaded", timeout=30000)

        if args.selector:
            el = page.query_selector(args.selector)
            text = el.inner_text() if el else "(selector not found)"
        else:
            # メインコンテンツを取得（articleタグ優先、なければbody）
            article = page.query_selector("article, main, [role='main']")
            if article:
                text = article.inner_text()
            else:
                text = page.query_selector("body").inner_text()

        result = {
            "title": page.title(),
            "url": page.url,
            "content": text[:8000],  # トークン節約のため上限
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        ctx.close()


def cmd_click(args):
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(get_profile_dir(args.profile)),
            headless=args.headless,
        )
        page = ctx.new_page()
        page.goto(args.url, wait_until="domcontentloaded", timeout=30000)
        page.click(args.selector)
        print(f"Clicked: {args.selector}")
        page.wait_for_timeout(2000)
        print(f"Current URL: {page.url}")
        ctx.close()


def cmd_type(args):
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(get_profile_dir(args.profile)),
            headless=args.headless,
        )
        page = ctx.new_page()
        page.goto(args.url, wait_until="domcontentloaded", timeout=30000)
        el = page.query_selector(args.selector)
        if not el:
            print(f"Selector not found: {args.selector}", file=sys.stderr)
            ctx.close()
            sys.exit(1)
        el.click()
        el.fill(args.text)
        print(f"Typed into {args.selector}: {args.text}")
        ctx.close()


def cmd_search(args):
    query = args.query
    max_results = args.max_results
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(get_profile_dir("default")),
            headless=True,
        )
        page = ctx.new_page()
        page.goto(
            f"https://www.google.com/search?q={query}&hl=ja",
            wait_until="domcontentloaded",
            timeout=30000,
        )

        results = []
        items = page.query_selector_all("div.g")[:max_results]
        for item in items:
            title_el = item.query_selector("h3")
            link_el = item.query_selector("a")
            snippet_el = item.query_selector("div[data-sncf], div.VwiC3b, span.aCOpRe")
            results.append({
                "title": title_el.inner_text() if title_el else "",
                "url": link_el.get_attribute("href") if link_el else "",
                "snippet": snippet_el.inner_text() if snippet_el else "",
            })

        print(json.dumps(results, ensure_ascii=False, indent=2))
        ctx.close()


def main():
    parser = argparse.ArgumentParser(description="Browser control for OpenClaw")
    sub = parser.add_subparsers(dest="command", required=True)

    # open
    p_open = sub.add_parser("open", help="Open a URL")
    p_open.add_argument("url")
    p_open.add_argument("--screenshot", "-s", help="Save screenshot to path")
    p_open.add_argument("--profile", default="default")
    p_open.add_argument("--headless", action="store_true", default=False)

    # read
    p_read = sub.add_parser("read", help="Read page content as text")
    p_read.add_argument("url")
    p_read.add_argument("--selector", help="CSS selector to extract")
    p_read.add_argument("--profile", default="default")

    # click
    p_click = sub.add_parser("click", help="Click an element")
    p_click.add_argument("url")
    p_click.add_argument("--selector", required=True)
    p_click.add_argument("--profile", default="default")
    p_click.add_argument("--headless", action="store_true", default=False)

    # type
    p_type = sub.add_parser("type", help="Type into an input")
    p_type.add_argument("url")
    p_type.add_argument("--selector", required=True)
    p_type.add_argument("--text", required=True)
    p_type.add_argument("--profile", default="default")
    p_type.add_argument("--headless", action="store_true", default=False)

    # search
    p_search = sub.add_parser("search", help="Google search and return results")
    p_search.add_argument("query")
    p_search.add_argument("--max-results", type=int, default=5)

    args = parser.parse_args()
    cmds = {
        "open": cmd_open,
        "read": cmd_read,
        "click": cmd_click,
        "type": cmd_type,
        "search": cmd_search,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
