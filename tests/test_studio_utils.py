import unittest

from studio_utils import (
    ASPECT_RATIOS,
    PROMPT_PRESETS,
    STYLE_PRESETS,
    apply_prompt_preset,
    build_effective_prompt,
    parse_generation_inputs,
)


class GenerationInputTests(unittest.TestCase):
    def valid(self, **overrides):
        values = {
            "prompt": "a quiet mountain lake at sunrise",
            "negative_prompt": "blurry",
            "aspect_ratio": "Square · 1:1",
            "steps": 25,
            "guidance": 7.5,
            "seed": 42,
            "batch_count": 1,
            "style": "None",
        }
        values.update(overrides)
        return parse_generation_inputs(**values)

    def test_normalizes_valid_inputs(self):
        values = self.valid(steps="30", batch_count=2, prompt="  a cat  ")
        self.assertEqual(values["prompt"], "a cat")
        self.assertEqual(values["steps"], 30)
        self.assertEqual(values["batch_count"], 2)

    def test_rejects_empty_or_oversized_prompt(self):
        with self.assertRaisesRegex(ValueError, "prompt"):
            self.valid(prompt="  ")
        with self.assertRaises(ValueError):
            self.valid(prompt="x" * 2001)

    def test_rejects_out_of_range_values(self):
        for fields in ({"steps": 100}, {"batch_count": 5}, {"guidance": float("nan")}, {"seed": -2}):
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                self.valid(**fields)

    def test_random_seed_becomes_concrete(self):
        self.assertGreaterEqual(self.valid(seed=-1)["seed"], 0)

    def test_presets_are_available(self):
        self.assertIn("Cinematic", STYLE_PRESETS)
        self.assertIn("Portrait", PROMPT_PRESETS)
        self.assertEqual(ASPECT_RATIOS["Wide · 16:9"], (768, 432))
        self.assertIn("cinematic composition", build_effective_prompt("a city", "Cinematic"))
        self.assertIn("professional portrait", apply_prompt_preset("a person", "Portrait"))


if __name__ == "__main__":
    unittest.main()
