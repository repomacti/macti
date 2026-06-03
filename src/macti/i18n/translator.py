
# macti/i18n.py

import json
from pathlib import Path


class Translator:

    def __init__(self, language="es"):
        self.language = language

        file = (
            Path(__file__).parent
            / "locales"
            / f"{language}.json"
        )

        with open(file, encoding="utf-8") as f:
            self.messages = json.load(f)

    def tr(self, key, **kwargs):

        text = self.messages.get(key, key)

        return text.format(**kwargs)

