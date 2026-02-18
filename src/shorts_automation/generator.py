from __future__ import annotations

import json
import os
from dataclasses import dataclass

from .models import Scene, ShortsProject


@dataclass
class GenerationOptions:
    topic: str
    angle: str = "educational"
    duration_seconds: int = 30
    audience: str = "general"


class ShortsGenerator:
    def generate(self, options: GenerationOptions) -> ShortsProject:
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                return self._generate_with_openai(options)
            except Exception:
                # Graceful fallback when API/network/parsing fails
                return self._generate_local(options)
        return self._generate_local(options)

    def _generate_local(self, options: GenerationOptions) -> ShortsProject:
        scene_count = max(4, min(7, options.duration_seconds // 5))
        seconds_per_scene = max(3, options.duration_seconds // scene_count)

        hook = f"Stop scrolling: {options.topic.title()} in {options.duration_seconds} seconds."
        cta = "Follow for more bite-sized AI-powered shorts ideas."

        scenes: list[Scene] = []
        narration_lines: list[str] = []

        for idx in range(scene_count):
            start = idx * seconds_per_scene
            end = min(options.duration_seconds, start + seconds_per_scene)
            point = idx + 1
            narration = (
                f"Point {point}: {options.topic} insight focused on {options.angle} for {options.audience} viewers."
            )
            subtitle = f"{options.topic.title()} Tip {point}"
            visual_prompt = (
                f"Vertical cinematic b-roll illustrating {options.topic}, dynamic motion, high contrast, scene {point}."
            )
            scenes.append(
                Scene(
                    start_second=start,
                    end_second=end,
                    visual_prompt=visual_prompt,
                    narration_line=narration,
                    subtitle=subtitle,
                )
            )
            narration_lines.append(narration)

        title = f"{options.topic.title()} in {options.duration_seconds}s (AI Shorts Blueprint)"
        description = (
            f"Fast breakdown on {options.topic}. Built for {options.audience} viewers with an "
            f"{options.angle} angle. Use this script to produce your next YouTube Short."
        )
        hashtags = [
            "#shorts",
            "#youtubeshorts",
            "#ai",
            f"#{options.topic.replace(' ', '')}",
        ]
        voiceover_script = f"{hook} " + " ".join(narration_lines) + f" {cta}"

        return ShortsProject(
            topic=options.topic,
            angle=options.angle,
            hook=hook,
            cta=cta,
            title=title,
            description=description,
            hashtags=hashtags,
            voiceover_script=voiceover_script,
            scenes=scenes,
        )

    def _generate_with_openai(self, options: GenerationOptions) -> ShortsProject:
        from openai import OpenAI

        client = OpenAI()
        prompt = (
            "Generate a YouTube Shorts production plan as strict JSON with keys: "
            "title, description, hashtags (array), hook, cta, voiceover_script, scenes (array). "
            "Each scene must have start_second, end_second, visual_prompt, narration_line, subtitle. "
            f"Topic: {options.topic}. Angle: {options.angle}. Audience: {options.audience}. "
            f"Duration target: {options.duration_seconds} seconds."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert viral short-form video producer.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        content = response.choices[0].message.content or "{}"
        payload = json.loads(content)
        scenes = [Scene(**scene) for scene in payload["scenes"]]

        return ShortsProject(
            topic=options.topic,
            angle=options.angle,
            hook=payload["hook"],
            cta=payload["cta"],
            title=payload["title"],
            description=payload["description"],
            hashtags=payload["hashtags"],
            voiceover_script=payload["voiceover_script"],
            scenes=scenes,
        )
