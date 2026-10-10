"""Independent temporary fixtures for the offline package checker."""

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import urllib.request


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_content_package.py"
SPEC = importlib.util.spec_from_file_location("check_content_package", SCRIPT)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class ContentPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name) / "package"
        self.base.mkdir()
        (self.base / "sources").mkdir()
        (self.base / "drafts").mkdir()
        self.manifest_path = self.base / "package.json"
        raw = "Evidence: visible source record.\n中文原文。\n".encode("utf-8")
        (self.base / "sources" / "one.txt").write_bytes(raw)
        second = b"Small cohort: 12 signups.\n"
        (self.base / "sources" / "two.txt").write_bytes(second)
        first_segments = [
            {"text": "Draft introduction.\n", "kind": "editorial",
             "review_note": "Introduces the draft; makes no sourced factual claim."},
            {"text": "Visible source record.\n", "kind": "sourced", "claim_ids": ["C1"]},
            {"text": "Review pending.\n", "kind": "disclosure", "claim_ids": [],
             "review_note": "States that semantic review is pending."},
        ]
        second_segments = [
            {"text": "Fictional example.\n", "kind": "synthetic",
             "review_note": "Labels an invented teaching setup."},
            {"text": "The visible record supports this draft.\n", "kind": "sourced",
             "claim_ids": ["C1"]},
            {"text": "The source says 12 signups.\n", "kind": "sourced", "claim_ids": ["C2"]},
        ]
        self.manifest = {
            "schema_version": 1,
            "sources": [
                {"id": "S1", "path": "sources/one.txt", "sha256": hashlib.sha256(raw).hexdigest()},
                {"id": "S2", "path": "sources/two.txt", "sha256": hashlib.sha256(second).hexdigest()},
            ],
            "claims": [
                {"id": "C1", "source_id": "S1", "quote": "visible source record.", "status": "active"},
                {"id": "C2", "source_id": "S2", "quote": "12 signups.", "status": "active"},
            ],
            "drafts": [
                {"id": "first", "path": "drafts/one.md", "segments": first_segments},
                {"id": "second", "path": "drafts/two.md", "segments": second_segments},
            ],
        }
        for row in self.manifest["drafts"]:
            (self.base / row["path"]).write_bytes("".join(s["text"] for s in row["segments"]).encode("utf-8"))
        self.save()

    def save(self, manifest=None):
        doc = self.manifest if manifest is None else manifest
        self.manifest_path.write_bytes(json.dumps(doc, ensure_ascii=True).encode("utf-8"))

    def check(self):
        self.save()
        return CHECKER.check_package(self.manifest_path)

    def assert_blocked(self, report, code):
        self.assertEqual(report["status"], "blocked", report)
        self.assertIn(code, [e["code"] for e in report["errors"]], report)
        self.assertEqual(report["semantic_review"], "NOT_PERFORMED")
        self.assertIs(report["publication_ready"], False)

    def test_valid_two_drafts_report_and_no_input_writes(self):
        before = {str(p): p.read_bytes() for p in self.base.rglob("*") if p.is_file()}
        report = CHECKER.check_package(self.manifest_path)
        self.assertEqual(report["checker_version"], "0.1.0")
        self.assertEqual(report["status"], "structure_ready")
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["drafts"][0]["claim_ids"], ["C1"])
        self.assertEqual(report["drafts"][1]["claim_ids"], ["C1", "C2"])
        self.assertEqual(report["drafts"][0]["segment_count"], 3)
        self.assertEqual(report["drafts"][0]["character_length"], 59)
        self.assertEqual(report["semantic_review"], "NOT_PERFORMED")
        self.assertIs(report["publication_ready"], False)
        after = {str(p): p.read_bytes() for p in self.base.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_missing_initial_segment_blocks(self):
        self.manifest["drafts"][0]["segments"].pop(0)
        report = self.check()
        self.assert_blocked(report, "DRAFT_COVERAGE_MISMATCH")
        error = next(e for e in report["errors"] if e["code"] == "DRAFT_COVERAGE_MISMATCH")
        self.assertEqual(error["draft_id"], "first")
        self.assertEqual(error["location"], "$.drafts[0].segments")

    def test_missing_final_segment_blocks(self):
        self.manifest["drafts"][0]["segments"].pop()
        self.assert_blocked(self.check(), "DRAFT_COVERAGE_MISMATCH")

    def test_segment_order_is_checked(self):
        self.manifest["drafts"][0]["segments"].reverse()
        self.assert_blocked(self.check(), "DRAFT_COVERAGE_MISMATCH")

    def test_source_mutation_blocks_even_when_quote_survives(self):
        source = self.base / "sources" / "one.txt"
        source.write_bytes(source.read_bytes() + b"New evidence.\n")
        self.assert_blocked(self.check(), "SOURCE_HASH_MISMATCH")

    def test_unicode_quote_and_draft_are_exact(self):
        self.manifest["claims"][0]["quote"] = "中文原文。"
        segment = self.manifest["drafts"][0]["segments"][1]
        segment["text"] = "中文草稿 😀\n"
        draft = self.manifest["drafts"][0]
        (self.base / draft["path"]).write_bytes("".join(s["text"] for s in draft["segments"]).encode("utf-8"))
        self.assertEqual(self.check()["status"], "structure_ready")

    def test_uppercase_hash_is_accepted(self):
        self.manifest["sources"][0]["sha256"] = self.manifest["sources"][0]["sha256"].upper()
        self.assertEqual(self.check()["status"], "structure_ready")

    def test_invalid_hashes_are_rejected(self):
        for value in (None, 1, "", "a" * 63, "g" * 64, "a" * 64 + "\n"):
            with self.subTest(value=value):
                self.manifest["sources"][0]["sha256"] = value
                self.assert_blocked(self.check(), "INVALID_SHA256")

    def test_withdrawn_claim_impacts_both_drafts(self):
        self.manifest["claims"][0]["status"] = "withdrawn"
        report = self.check()
        self.assert_blocked(report, "INACTIVE_CLAIM")
        errors = [e for e in report["errors"] if e["code"] == "INACTIVE_CLAIM"]
        self.assertEqual({e["draft_id"] for e in errors}, {"first", "second"})
        self.assertTrue(all(e["segment_index"] == 1 for e in errors))

    def test_unresolved_claim_blocks(self):
        self.manifest["claims"][0]["status"] = "unresolved"
        self.assert_blocked(self.check(), "INACTIVE_CLAIM")

    def test_unknown_claim_blocks_with_location(self):
        self.manifest["drafts"][0]["segments"][1]["claim_ids"] = ["missing"]
        report = self.check()
        self.assert_blocked(report, "UNKNOWN_CLAIM")
        error = next(e for e in report["errors"] if e["code"] == "UNKNOWN_CLAIM")
        self.assertEqual(error["location"], "$.drafts[0].segments[1].claim_ids[0]")
        self.assertEqual(error["draft_id"], "first")

    def test_quote_not_found_and_no_quote_in_error_output(self):
        secret_quote = "not-in-the-source-private-placeholder"
        self.manifest["claims"][0]["quote"] = secret_quote
        report = self.check()
        self.assert_blocked(report, "QUOTE_NOT_FOUND")
        self.assertNotIn(secret_quote, json.dumps(report))
        self.assertNotIn("中文原文", json.dumps(report, ensure_ascii=False))

    def test_unknown_source_blocks(self):
        self.manifest["claims"][0]["source_id"] = "missing"
        self.assert_blocked(self.check(), "UNKNOWN_SOURCE")

    def test_duplicate_ids_in_each_collection_block(self):
        for key in ("sources", "claims", "drafts"):
            with self.subTest(collection=key):
                doc = copy.deepcopy(self.manifest)
                doc[key].append(copy.deepcopy(doc[key][0]))
                self.save(doc)
                self.assert_blocked(CHECKER.check_package(self.manifest_path), "DUPLICATE_ID")

    def test_bad_schema_versions(self):
        for value in (True, False, 1.0, "1", 2, None, [], {}):
            with self.subTest(value=value):
                self.manifest["schema_version"] = value
                self.assert_blocked(self.check(), "INVALID_SCHEMA_VERSION")

    def test_empty_collections_and_segments(self):
        for key in ("sources", "claims", "drafts"):
            with self.subTest(collection=key):
                doc = copy.deepcopy(self.manifest)
                doc[key] = []
                self.save(doc)
                self.assert_blocked(CHECKER.check_package(self.manifest_path), "EMPTY_LIST")
        self.manifest["drafts"][0]["segments"] = []
        self.assert_blocked(self.check(), "EMPTY_LIST")

    def test_wrong_array_types_and_entries(self):
        for key in ("sources", "claims", "drafts"):
            for value in (None, 3, "wrong", {}, [3], [None], ["wrong"]):
                with self.subTest(collection=key, value=value):
                    doc = copy.deepcopy(self.manifest)
                    doc[key] = value
                    self.save(doc)
                    expected = "INVALID_OBJECT" if isinstance(value, list) else "INVALID_LIST"
                    self.assert_blocked(CHECKER.check_package(self.manifest_path), expected)

    def test_wrong_scalar_fields(self):
        cases = (("sources", "id"), ("sources", "path"), ("claims", "id"),
                 ("claims", "source_id"), ("claims", "quote"), ("drafts", "id"), ("drafts", "path"))
        for collection, field in cases:
            for value in (None, 42, [], {}):
                with self.subTest(collection=collection, field=field, value=value):
                    doc = copy.deepcopy(self.manifest)
                    doc[collection][0][field] = value
                    self.save(doc)
                    self.assert_blocked(CHECKER.check_package(self.manifest_path), "INVALID_STRING")

    def test_bad_segment_fields(self):
        cases = (("text", 42, "INVALID_STRING"), ("text", "", "EMPTY_STRING"),
                 ("kind", "unknown", "INVALID_SEGMENT_KIND"), ("kind", {}, "INVALID_SEGMENT_KIND"),
                 ("claim_ids", None, "INVALID_LIST"), ("claim_ids", [42], "INVALID_STRING"),
                 ("claim_ids", [], "MISSING_CLAIM_IDS"))
        for field, value, code in cases:
            with self.subTest(field=field, value=value):
                doc = copy.deepcopy(self.manifest)
                doc["drafts"][0]["segments"][1][field] = value
                self.save(doc)
                self.assert_blocked(CHECKER.check_package(self.manifest_path), code)

    def test_missing_kind_is_not_skipped(self):
        del self.manifest["drafts"][0]["segments"][0]["kind"]
        self.assert_blocked(self.check(), "INVALID_SEGMENT_KIND")

    def test_editorial_requires_review_note_and_no_claims(self):
        segment = self.manifest["drafts"][0]["segments"][0]
        segment["claim_ids"] = ["C1"]
        segment["review_note"] = "   "
        report = self.check()
        self.assert_blocked(report, "UNEXPECTED_CLAIM_IDS")
        self.assertIn("EMPTY_STRING", [e["code"] for e in report["errors"]])

    def test_invalid_claim_status(self):
        for status in ("new", None, [], {}):
            with self.subTest(status=status):
                self.manifest["claims"][0]["status"] = status
                self.assert_blocked(self.check(), "INVALID_CLAIM_STATUS")

    def test_duplicate_json_keys_are_errors_at_any_depth(self):
        for content in ('{"schema_version":1,"schema_version":1}',
                        '{"nested":{"name":1,"name":2}}'):
            with self.subTest(content=content):
                self.manifest_path.write_text(content, encoding="utf-8")
                self.assert_blocked(CHECKER.check_package(self.manifest_path), "DUPLICATE_JSON_KEY")

    def test_invalid_or_truncated_json(self):
        for content in ("", "{", '{"sources":[', "{bad}", '{"v":NaN}', '{"v":Infinity}'):
            with self.subTest(content=content):
                self.manifest_path.write_text(content, encoding="utf-8")
                self.assert_blocked(CHECKER.check_package(self.manifest_path), "INVALID_JSON")

    def test_unknown_metadata_accepts_finite_floats(self):
        self.manifest["metadata"] = {"ratio": 1.25, "large": -3.2e100, "zero": 0.0}
        self.assertEqual(self.check()["status"], "structure_ready")

    def test_overflowing_float_exponents_are_blocked(self):
        document = json.dumps(self.manifest)
        for number in ("1e309", "-1e309", "1.5e9999", "-1.5e9999"):
            with self.subTest(number=number):
                content = document[:-1] + ', "metadata": ' + number + '}'
                self.manifest_path.write_bytes(content.encode("utf-8"))
                self.assert_blocked(CHECKER.check_package(self.manifest_path), "INVALID_JSON")

    def test_root_must_be_object(self):
        for value in (None, [], "string", 1):
            with self.subTest(value=value):
                self.save(value)
                # save(None) uses the default fixture, so write JSON null explicitly.
                if value is None:
                    self.manifest_path.write_bytes(b"null")
                self.assert_blocked(CHECKER.check_package(self.manifest_path), "INVALID_OBJECT")

    def test_invalid_utf8_and_escaped_surrogate_manifest(self):
        self.manifest_path.write_bytes(b'{"value":"\xff"}')
        self.assert_blocked(CHECKER.check_package(self.manifest_path), "INVALID_UNICODE")
        self.manifest["claims"][0]["quote"] = "\ud800"
        self.assert_blocked(self.check(), "INVALID_UNICODE")

    def test_utf8_bom_is_explicitly_rejected(self):
        raw = self.manifest_path.read_bytes()
        self.manifest_path.write_bytes(b"\xef\xbb\xbf" + raw)
        self.assert_blocked(CHECKER.check_package(self.manifest_path), "UTF8_BOM_NOT_ALLOWED")
        self.save()
        source = self.base / "sources" / "one.txt"
        source.write_bytes(b"\xef\xbb\xbf" + source.read_bytes())
        self.assert_blocked(self.check(), "UTF8_BOM_NOT_ALLOWED")

    def test_invalid_utf8_source_and_draft(self):
        for collection in ("sources", "drafts"):
            with self.subTest(collection=collection):
                path = self.base / self.manifest[collection][0]["path"]
                original = path.read_bytes()
                path.write_bytes(b"\xff")
                self.assert_blocked(self.check(), "INVALID_UNICODE")
                path.write_bytes(original)

    def test_unreadable_manifest_and_invalid_argument(self):
        self.assert_blocked(CHECKER.check_package(self.base / "missing.json"), "MANIFEST_READ_ERROR")
        self.assert_blocked(CHECKER.check_package(self.base), "MANIFEST_READ_ERROR")
        self.assert_blocked(CHECKER.check_package(None), "MANIFEST_READ_ERROR")

    def test_missing_directory_and_read_error_paths(self):
        for value in ("sources/missing.txt", "sources", "bad\x00name"):
            with self.subTest(path=value):
                self.manifest["sources"][0]["path"] = value
                self.assert_blocked(self.check(), "FILE_READ_ERROR")
        self.manifest["sources"][0]["path"] = "sources/one.txt"
        self.save()
        original = Path.read_bytes
        def deny_source(path):
            if path.name == "one.txt":
                raise PermissionError("test denial")
            return original(path)
        with mock.patch.object(Path, "read_bytes", deny_source):
            self.assert_blocked(CHECKER.check_package(self.manifest_path), "FILE_READ_ERROR")

    def test_absolute_and_windows_absolute_paths_are_rejected(self):
        for path in (str(self.base / "sources" / "one.txt"), "C:\\temp\\one.txt",
                     "C:one.txt", "\\\\host\\share\\one.txt", "\\one.txt"):
            with self.subTest(path=path):
                self.manifest["sources"][0]["path"] = path
                self.assert_blocked(self.check(), "ABSOLUTE_PATH")

    def test_parent_directory_escape_is_rejected(self):
        outside = Path(self.temp.name) / "outside.txt"
        outside.write_text("visible source record.", encoding="utf-8")
        self.manifest["sources"][0]["path"] = "../outside.txt"
        self.assert_blocked(self.check(), "PATH_OUTSIDE_PACKAGE")

    def test_symlink_escape_in_source_and_draft_is_rejected(self):
        outside = Path(self.temp.name) / "outside.txt"
        outside.write_text("visible source record.", encoding="utf-8")
        link = self.base / "escape.txt"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("Host cannot create symbolic links")
        for collection in ("sources", "drafts"):
            with self.subTest(collection=collection):
                doc = copy.deepcopy(self.manifest)
                doc[collection][0]["path"] = "escape.txt"
                self.save(doc)
                self.assert_blocked(CHECKER.check_package(self.manifest_path), "PATH_OUTSIDE_PACKAGE")

    def test_crlf_is_preserved_for_hash_quote_and_coverage(self):
        source = self.base / "sources" / "one.txt"
        raw = b"Evidence: visible\r\nsource record.\r\n"
        source.write_bytes(raw)
        self.manifest["sources"][0]["sha256"] = hashlib.sha256(raw).hexdigest()
        self.manifest["claims"][0]["quote"] = "visible\r\nsource record."
        draft = self.manifest["drafts"][0]
        for segment in draft["segments"]:
            segment["text"] = segment["text"].replace("\n", "\r\n")
        (self.base / draft["path"]).write_bytes("".join(s["text"] for s in draft["segments"]).encode("utf-8"))
        self.assertEqual(self.check()["status"], "structure_ready")
        draft["segments"][0]["text"] = draft["segments"][0]["text"].replace("\r\n", "\n")
        self.assert_blocked(self.check(), "DRAFT_COVERAGE_MISMATCH")

    def test_runs_with_network_entrypoints_disabled(self):
        with mock.patch.object(socket, "socket", side_effect=AssertionError("Network forbidden")), \
                mock.patch.object(urllib.request, "urlopen", side_effect=AssertionError("Network forbidden")):
            self.assertEqual(CHECKER.check_package(self.manifest_path)["status"], "structure_ready")

    def test_cli_json_exit_codes_and_no_traceback(self):
        environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        def run(args):
            return subprocess.run([sys.executable, "-B", str(SCRIPT)] + args,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  text=True, check=False, env=environment)
        result = run([str(self.manifest_path)])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "structure_ready")
        self.assertEqual(result.stderr, "")
        self.manifest["claims"][0]["status"] = "withdrawn"
        self.save()
        for args in ([str(self.manifest_path)], [str(self.base / "missing.json")], [], ["a", "b"]):
            with self.subTest(args=args):
                result = run(args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stdout)["status"], "blocked")
                self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
