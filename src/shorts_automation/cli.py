from __future__ import annotations

import argparse
from pathlib import Path

from .generator import GenerationOptions, ShortsGenerator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shorts-automation",
        description="Create an AI-powered YouTube Shorts production package.",
    )
    parser.add_argument("topic", help="Shorts topic, e.g. 'AI tools for students'")
    parser.add_argument("--angle", default="educational", help="Creative angle")
    parser.add_argument("--audience", default="general", help="Target audience")
    parser.add_argument(
        "--duration",
        type=int,
        default=30,
        help="Target duration in seconds (default: 30)",
    )
    parser.add_argument(
        "--output",
        default="output",
        help="Directory where JSON and markdown plan will be saved",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    options = GenerationOptions(
        topic=args.topic,
        angle=args.angle,
        duration_seconds=args.duration,
        audience=args.audience,
    )

    project = ShortsGenerator().generate(options)
    output_dir = Path(args.output)
    project.write(output_dir)

    print("✅ Shorts automation package generated")
    print(f"Topic: {project.topic}")
    print(f"Title: {project.title}")
    print(f"Files written to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
