import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from shorts_automation.generator import GenerationOptions, ShortsGenerator


class ShortsGeneratorTests(unittest.TestCase):
    def test_local_generation_contains_required_sections(self) -> None:
        generator = ShortsGenerator()
        options = GenerationOptions(topic="ai productivity", duration_seconds=30)

        project = generator._generate_local(options)

        self.assertTrue(project.title)
        self.assertGreaterEqual(len(project.scenes), 4)
        self.assertIn("#shorts", project.hashtags)
        self.assertIn("Stop scrolling", project.voiceover_script)


if __name__ == "__main__":
    unittest.main()
