import importlib
import unittest


class OpenAIDependencyTest(unittest.TestCase):
    def test_openai_module_is_available(self) -> None:
        self.assertIsNotNone(importlib.util.find_spec("openai"))


if __name__ == "__main__":
    unittest.main()
