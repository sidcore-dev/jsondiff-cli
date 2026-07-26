import unittest

from jsondiff_cli.core import diff


class TestDiff(unittest.TestCase):
    def test_identical(self):
        self.assertEqual(diff({"a": 1}, {"a": 1}), [])

    def test_added_key(self):
        entries = diff({"a": 1}, {"a": 1, "b": 2})
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].kind, "added")
        self.assertEqual(entries[0].path, "root.b")

    def test_removed_key(self):
        entries = diff({"a": 1, "b": 2}, {"a": 1})
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].kind, "removed")

    def test_changed_scalar(self):
        entries = diff({"a": 1}, {"a": 2})
        self.assertEqual(entries[0].kind, "changed")
        self.assertEqual(entries[0].old, 1)
        self.assertEqual(entries[0].new, 2)

    def test_nested_path(self):
        entries = diff({"a": {"b": {"c": 1}}}, {"a": {"b": {"c": 2}}})
        self.assertEqual(entries[0].path, "root.a.b.c")

    def test_list_changed_index(self):
        entries = diff({"a": [1, 2, 3]}, {"a": [1, 9, 3]})
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].path, "root.a[1]")

    def test_list_added_item(self):
        entries = diff({"a": [1]}, {"a": [1, 2]})
        self.assertEqual(entries[0].kind, "added")
        self.assertEqual(entries[0].path, "root.a[1]")

    def test_list_removed_item(self):
        entries = diff({"a": [1, 2]}, {"a": [1]})
        self.assertEqual(entries[0].kind, "removed")

    def test_type_changed(self):
        entries = diff({"a": 1}, {"a": "1"})
        self.assertEqual(entries[0].kind, "type_changed")

    def test_numeric_pair_not_type_changed(self):
        entries = diff({"a": 1}, {"a": 1.0})
        self.assertEqual(entries, [])

    def test_bool_vs_int_is_type_changed(self):
        entries = diff({"a": 1}, {"a": True})
        self.assertEqual(entries[0].kind, "type_changed")


if __name__ == "__main__":
    unittest.main()
