import asyncio
import re
import sys
from datetime import datetime, timezone

import colorama

from checker import check_username

colorama.init()


def color(text: str, code: str) -> str:
    return f"{code}{text}{colorama.Style.RESET_ALL}"


ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def visible_len(text: str) -> int:
    return len(ANSI_RE.sub("", text))


def status_color(status: str) -> str:
    if status == "available":
        return color(status, colorama.Fore.GREEN)
    if status == "taken":
        return color(status, colorama.Fore.RED)
    if status == "unknown":
        return color(status, colorama.Fore.YELLOW)
    return color(status, colorama.Fore.MAGENTA)


def format_row(cols, widths):
    parts = []
    for value, width in zip(cols, widths):
        text = str(value)
        pad = max(0, width - visible_len(text))
        parts.append(f"{text}{' ' * pad}")
    return "  ".join(parts)


def print_results(username: str, results: list) -> None:
    header = f"Results for {username}"
    timestamp = datetime.now(timezone.utc).isoformat()

    print("\n" + color(header, colorama.Style.BRIGHT))
    print(color(timestamp, colorama.Fore.CYAN))

    rows = []
    for item in results:
        link = item.get("url") or "-"
        status = status_color(item.get("status", "unknown"))
        rows.append([item.get("platform", "-"), status, link])

    headers = ["Platform", "Status", "Link"]
    widths = [
        max(8, max(visible_len(r[0]) for r in rows) if rows else 8),
        max(6, max(visible_len(r[1]) for r in rows) if rows else 6),
        max(4, max(visible_len(r[2]) for r in rows) if rows else 4),
    ]

    print("\n" + format_row(headers, widths))
    print(format_row(["-" * w for w in widths], widths))

    for row in rows:
        print(format_row(row, widths))


def is_valid(username: str) -> bool:
    if not (2 <= len(username) <= 30):
        return False
    for ch in username:
        if not (ch.isalnum() or ch in "_."):
            return False
    return True


async def run_once(username: str) -> None:
    results = await check_username(username)
    print_results(username, results)


def main() -> int:
    banner = r"""
888   |                          888 888                 ,d88~~\                             d8
888___|   /~~~8e  888-~88e  e88~\888 888  e88~~8e        8888     e88~~\  e88~-_  888  888 _d88__
888   |       88b 888  888 d888  888 888 d888  88b       `Y88b   d888    d888   i 888  888  888
888   |  e88~-888 888  888 8888  888 888 8888__888        `Y88b, 8888    8888   | 888  888  888
888   | C888  888 888  888 Y888  888 888 Y888    ,          8888 Y888    Y888   ' 888  888  888
888   |  "88_-888 888  888  "88_/888 888  "88___/        \__88P'  "88__/  "88_-~  "88_-888  "88_/
"""
    print(color(banner, colorama.Style.BRIGHT))
    print(color("Best-effort username checks across popular platforms.", colorama.Fore.WHITE))
    print("")

    while True:
        prompt = color("Username (or 'q' to quit): ", colorama.Style.BRIGHT + colorama.Fore.CYAN)
        username = input(prompt).strip()
        if username.lower() in {"q", "quit", "exit"}:
            print("Goodbye.")
            return 0
        if not is_valid(username):
            print(color("Use 2-30 characters: letters, numbers, underscore, or dot.", colorama.Fore.RED))
            continue
        try:
            asyncio.run(run_once(username))
        except KeyboardInterrupt:
            print("\nStopped.")
            return 0
        except Exception as exc:
            print(color(f"Error: {exc}", colorama.Fore.RED))
        print("")


if __name__ == "__main__":
    raise SystemExit(main())
