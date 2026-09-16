import ast
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
BOT_PATH = ROOT / "bot.py"


class GoldBotContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = BOT_PATH.read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source)

    def test_source_compiles(self):
        compile(self.source, str(BOT_PATH), "exec")

    def test_three_core_menu_callbacks(self):
        required = {
            'callback_data="menu:gold"',
            'callback_data="menu:markets"',
            'callback_data="menu:glossary"',
        }
        for marker in required:
            self.assertIn(marker, self.source)

    def test_only_supported_user_commands_are_exposed(self):
        self.assertIn('("start", "Open the Gold Academy")', self.source)
        self.assertIn('("help", "Show how to use the bot")', self.source)
        self.assertNotIn('Command("about")', self.source)
        self.assertNotIn('Command("privacy")', self.source)

    def test_callback_handlers_cover_menu_and_content_prefixes(self):
        for prefix in ("gold:", "market:", "glossary:"):
            self.assertIn(f'F.data.startswith("{prefix}")', self.source)

    def test_main_menu_has_no_reply_keyboard(self):
        self.assertNotIn("ReplyKeyboardBuilder", self.source)

    def test_no_hardcoded_token(self):
        self.assertIn('os.getenv("BOT_TOKEN")', self.source)


if __name__ == "__main__":
    unittest.main()
