from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
import json


@dataclass
class Scene:
    start_second: int
    end_second: int
    visual_prompt: str
    narration_line: str
    subtitle: str


@dataclass
class ShortsProject:
    topic: str
    angle: str
    hook: str
    cta: str
    title: str
    description: str
    hashtags: list[str]
    voiceover_script: str
    scenes: list[Scene]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["scenes"] = [asdict(scene) for scene in self.scenes]
        return payload

    def write(self, output_dir: Path) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path = output_dir / "shorts_project.json"
        markdown_path = output_dir / "shorts_project.md"

        json_path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

        markdown_lines = [
            f"# AI Shorts Plan: {self.topic}",
            "",
            f"## Title\n{self.title}",
            "",
            "## Description",
            self.description,
            "",
            f"## Hashtags\n{' '.join(self.hashtags)}",
            "",
            "## Hook",
            self.hook,
            "",
            "## Voiceover Script",
            self.voiceover_script,
            "",
            "## Shot List",
        ]

        for scene in self.scenes:
            markdown_lines.extend(
                [
                    f"### {scene.start_second}s - {scene.end_second}s",
                    f"- Visual prompt: {scene.visual_prompt}",
                    f"- Narration: {scene.narration_line}",
                    f"- Subtitle: {scene.subtitle}",
                    "",
                ]
            )

        markdown_lines.extend(
            [
                "## CTA",
                self.cta,
                "",
                "## Production Checklist",
                "- [ ] Generate voiceover audio",
                "- [ ] Gather or generate vertical clips (9:16)",
                "- [ ] Add subtitles and hook text",
                "- [ ] Sync cuts to narration pacing",
                "- [ ] Export MP4 (1080x1920)",
                "- [ ] Upload and schedule",
            ]
        )

        markdown_path.write_text("\n".join(markdown_lines), encoding="utf-8")
