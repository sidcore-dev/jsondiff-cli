import json
import os
import tempfile
import unittest

from jsondiff_cli.cli import main


class TestCli(unittest.TestCase):
    def _write(self, obj):
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as fh:
            json.dump(obj, fh)
        return path

    def test_exit_code_no_diff(self):
        a = self._write({"x": 1})
        b = self._write({"x": 1})
        try:
            self.assertEqual(main([a, b, "--quiet"]), 0)
        finally:
            os.remove(a)
            os.remove(b)

    def test_exit_code_with_diff(self):
        a = self._write({"x": 1})
        b = self._write({"x": 2})
        try:
            self.assertEqual(main([a, b, "--quiet"]), 1)
        finally:
            os.remove(a)
            os.remove(b)

    def test_missing_file_returns_2(self):
        b = self._write({"x": 1})
        try:
            self.assertEqual(main(["/nonexistent/file.json", b, "--quiet"]), 2)
        finally:
            os.remove(b)


if __name__ == "__main__":
    unittest.main()
