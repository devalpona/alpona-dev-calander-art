#!/usr/bin/env python3
"""
Create decorative empty commits spelling "ALPONA DEV"
on a GitHub contribution calendar using dates in 2026.

Use only in a dedicated repository you control.
These commits are decorative, not evidence of software work.
"""

from datetime import date, datetime, timedelta
import os
import subprocess
import sys

# 3x5 pixel font
ART = {
    "A": [".#.", "###", "#.#", "#.#", "#.#"],
    "L": ["#..", "#..", "#..", "#..", "###"],
    "P": ["##.", "#.#", "##.", "#..", "#.."],
    "O": ["###", "#.#", "#.#", "#.#", "###"],
    "N": ["#.#", "###", "###", "###", "#.#"],
    "D": ["##.", "#.#", "#.#", "#.#", "##."],
    "E": ["###", "#..", "##.", "#..", "###"],
    "V": ["#.#", "#.#", "#.#", "#.#", ".#."],
}

# Your sister's details
NAME = "ALPONA DEV"
GIT_AUTHOR_NAME = "devalpona"
GIT_AUTHOR_EMAIL = "jobadev2003@gmail.com"

# Calendar settings — 2026 only
START_SUNDAY = date(2026, 1, 4)
COMMITS_PER_SQUARE = 1


def run(args, *, env=None, check=True, capture=False):
    return subprocess.run(
        args,
        env=env,
        check=check,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def build_pixels():
    rows = ["", "", "", "", ""]

    for i, char in enumerate(NAME):
        if char == " ":
            for r in range(5):
                rows[r] += " "
            continue

        glyph = ART.get(char)

        if glyph is None:
            raise ValueError(f"No font glyph defined for {char!r}")

        for r in range(5):
            rows[r] += glyph[r]

        if i != len(NAME) - 1:
            for r in range(5):
                rows[r] += " "

    return rows


def main():
    if not os.path.isdir(".git"):
        print("ERROR: Run this script from your Git repository folder.")
        sys.exit(1)

    branch = run(
        ["git", "branch", "--show-current"],
        capture=True,
    ).stdout.strip()

    if not branch:
        print("ERROR: Could not detect the current Git branch.")
        sys.exit(1)

    status = run(
        ["git", "status", "--porcelain"],
        capture=True,
    ).stdout.strip()

    if status:
        print("ERROR: Your working tree is not clean.")
        print("Commit or stash your changes before running this script.")
        print(status)
        sys.exit(1)

    pixels = build_pixels()
    squares = []

    # Each letter row maps to Monday–Friday.
    # Each letter column advances by one week.
    for col in range(max(map(len, pixels))):
        for row, pixel_row in enumerate(pixels):
            if col < len(pixel_row) and pixel_row[col] == "#":
                day = START_SUNDAY + timedelta(
                    days=col * 7 + row + 1
                )

                if day.year == 2026:
                    squares.append((day, col, row))

    total = len(squares) * COMMITS_PER_SQUARE

    print(f'Contribution art: "{NAME}"')
    print(f"Git author: {GIT_AUTHOR_NAME}")
    print(f"Email: {GIT_AUTHOR_EMAIL}")
    print("Year: 2026")
    print(f"Branch: {branch}")
    print(f"Empty commits to create: {total}")
    print()
    print("These are decorative empty commits.")
    print("They will NOT be pushed automatically.")
    print()
    print("Make sure the email is verified on the intended GitHub account.")

    confirm = input('\nType CREATE to continue: ').strip()

    if confirm != "CREATE":
        print("Cancelled. No commits were created.")
        return

    created = 0

    for day, col, row in squares:
        for shade_index in range(COMMITS_PER_SQUARE):
            stamp = datetime(
                day.year,
                day.month,
                day.day,
                12,
                shade_index,
                0,
            ).astimezone().isoformat()

            env = os.environ.copy()

            env["GIT_AUTHOR_DATE"] = stamp
            env["GIT_COMMITTER_DATE"] = stamp

            env["GIT_AUTHOR_NAME"] = GIT_AUTHOR_NAME
            env["GIT_AUTHOR_EMAIL"] = GIT_AUTHOR_EMAIL

            env["GIT_COMMITTER_NAME"] = GIT_AUTHOR_NAME
            env["GIT_COMMITTER_EMAIL"] = GIT_AUTHOR_EMAIL

            message = (
                f"Decorative contribution art: "
                f"{NAME} ({day.isoformat()})"
            )

            run(
                ["git", "commit", "--allow-empty", "-m", message],
                env=env,
            )

            created += 1

    print(f"\nCreated {created} empty commits locally.")
    print("\nReview recent commits with:")
    print("git log --date=short --format='%h %ad %s' -n 10")

    print("\nIf you want to publish them, run:")
    print(f"git push -u origin {branch}")

    print("\nGitHub may take time to refresh the contribution graph.")
    print("Contribution counting depends on GitHub's email, repository,")
    print("visibility, and default-branch requirements.")


if __name__ == "__main__":
    main()