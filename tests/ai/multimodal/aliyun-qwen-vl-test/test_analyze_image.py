#!/usr/bin/env python3
"""Unit tests for Qwen VL analyze_image helper behaviors."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


def _load_module():
    root = Path(__file__).resolve().parents[4]
    module_path = root / "skills/ai/multimodal/alicloud-ai-multimodal-qwen-vl/scripts/analyze_image.py"
    spec = importlib.util.spec_from_file_location("analyze_image", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load analyze_image module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AnalyzeImageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mod = _load_module()

    def test_build_payload_with_json_mode(self) -> None:
        payload = self.mod.build_payload(
            req={"prompt": "extract", "max_tokens": 100, "temperature": 0.0},
            model="qwen3-vl-plus",
            image_url="https://example.com/img.jpg",
            detail="auto",
            json_mode=True,
            schema_obj=None,
        )
        self.assertEqual(payload["response_format"]["type"], "json_object")

    def test_build_payload_with_schema(self) -> None:
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        }
        payload = self.mod.build_payload(
            req={"prompt": "extract", "max_tokens": 100, "temperature": 0.0},
            model="qwen3-vl-plus",
            image_url="https://example.com/img.jpg",
            detail="high",
            json_mode=False,
            schema_obj=schema,
        )
        self.assertEqual(payload["response_format"]["type"], "json_schema")
        self.assertEqual(payload["response_format"]["json_schema"]["schema"], schema)

    def test_extract_text_content_from_list(self) -> None:
        text = self.mod.extract_text_content(
            [
                {"type": "text", "text": "hello"},
                {"type": "reasoning", "text": "ignore"},
            ]
        )
        self.assertEqual(text, "hello")

    def test_parse_json_text(self) -> None:
        parsed = self.mod.try_parse_json_text('{"a":1}')
        self.assertEqual(parsed, {"a": 1})
        self.assertIsNone(self.mod.try_parse_json_text("not json"))

    def test_extract_error_message(self) -> None:
        message = self.mod.extract_error_message({"error": {"message": "bad request"}})
        self.assertEqual(message, "bad request")


if __name__ == "__main__":
    unittest.main()
