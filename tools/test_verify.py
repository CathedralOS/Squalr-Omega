"""Harness controls only; these tests do not validate the Omega port."""
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

import verify


class HarnessTests(unittest.TestCase):
    def test_layout_has_all_declared_package_builds(self):
        self.assertEqual(verify.check_layout(verify.ROOT), (17, 37))

    def test_missing_build_rejects(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "upstream.json").write_text('{"packages": []}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing root"):
                verify.check_layout(root)

    def test_native_uses_real_run_not_interpretation(self):
        command = verify.compiler_command("native", "omega", Path("application"), "macos_arm64", Path("report"))
        self.assertEqual(command[:3], ["omega", "run", "--keep"])
        self.assertNotIn("--accept-admissions", command)

    def execute(self, program, mode="check", timeout=5):
        with tempfile.TemporaryDirectory() as directory:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                return verify.run_compiler([sys.executable, "-c", program], Path(directory),
                                           mode, timeout, "squalr-tests")

    def test_compiler_failure_is_not_success(self):
        self.assertEqual(self.execute("raise SystemExit(7)"), 7)

    def test_native_requires_marker(self):
        self.assertEqual(self.execute("pass", "native"), 1)
        self.assertEqual(self.execute("print('Squalr geometry: PASS')", "native"), 0)

    def test_timeout_is_not_source_rejection(self):
        self.assertEqual(self.execute("import time; time.sleep(5)", timeout=1), 124)


if __name__ == "__main__":
    unittest.main()
