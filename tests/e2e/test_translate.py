import os
from unittest import TestCase, main

from util import REPO_ROOT, cd, run


class TestParser(TestCase):
    def setUp(self) -> None:
        with cd(REPO_ROOT):
            run("pip install .")
        return super().setUp()

    def tearDown(self) -> None:
        run("pip uninstall -y gptw")
        return super().tearDown()

    def test_parse(self):
        api_key = os.getenv("OPENAI_APIKEY")

        with cd(REPO_ROOT):
            run(f"ww --key {api_key}")
            self.assertIn("model", str(run('ww a "who are you?"')))
            self.assertIn("ww", str(run("ww -v")))


if __name__ == "__main__":
    main()
