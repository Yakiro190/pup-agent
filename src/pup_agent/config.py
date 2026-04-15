from __future__ import annotations

import os

DEFAULT_PROVIDER = os.getenv("PUP_PROVIDER", "mock").strip().lower() or "mock"
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip() or "gpt-4.1-mini"
DEFAULT_MAX_STEPS = int(os.getenv("PUP_MAX_STEPS", "6"))
