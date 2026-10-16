#!/usr/bin/env python3
"""Check a local content manifest's structure, never its semantic accuracy.

Python 3.9+, standard library only. All text is strict UTF-8 without a BOM;
newlines are preserved. Paths are relative to the manifest's directory and
must resolve within it. SHA-256 values describe the original source bytes.
"""

import hashlib
import json
import math
import re
import sys
from pathlib import Path, PureWindowsPath


VERSION = "0.1.1"
KINDS = frozenset(("sourced", "editorial", "synthetic", "disclosure"))
STATUSES = frozenset(("active", "withdrawn", "unresolved"))
SHA256 = re.compile(r"[0-9a-fA-F]{64}\Z")


class _DuplicateKey(ValueError):
    pass


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKey("Duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError("Non-finite JSON number")


def _finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("Non-finite JSON number")
    return number


def _report():
    return {
        "checker_version": VERSION,
        "status": "blocked",
        "semantic_review": "NOT_PERFORMED",
        "publication_ready": False,
        "drafts": [],
        "errors": [],
    }


class _Checker:
    def __init__(self):
        self.report = _report()
        self.base = None

    def error(self, code, location, message, context=None):
        item = {"code": code, "location": location, "message": message}
        if context:
            item.update(context)
        self.report["errors"].append(item)

    def string(self, obj, field, location, context=None, trim=False):
        value = obj.get(field)
        if not isinstance(value, str):
            self.error("INVALID_STRING", location + "." + field,
                       "Expected a nonempty string.", context)
            return None
        if not (value.strip() if trim else value):
            self.error("EMPTY_STRING", location + "." + field,
                       "Expected a nonempty string.", context)
            return None
        return value

    def list_field(self, obj, field, location, context=None, nonempty=True):
        value = obj.get(field)
        if not isinstance(value, list):
            self.error("INVALID_LIST", location + "." + field,
                       "Expected an array.", context)
            return None
        if nonempty and not value:
            self.error("EMPTY_LIST", location + "." + field,
                       "Expected at least one item.", context)
        return value

    def identifier(self, obj, location, seen, context=None):
        value = self.string(obj, "id", location, context, trim=True)
        if value is not None:
            if value in seen:
                self.error("DUPLICATE_ID", location + ".id",
                           "IDs must be unique within this array.", context)
            seen.add(value)
        return value

    def read_relative(self, value, location, context=None):
        if value is None:
            return None
        try:
            path = Path(value)
            windows_path = PureWindowsPath(value)
            if path.is_absolute() or windows_path.drive or windows_path.root:
                self.error("ABSOLUTE_PATH", location,
                           "Use a relative path within the package.", context)
                return None
            resolved = (self.base / path).resolve(strict=True)
            try:
                resolved.relative_to(self.base)
            except ValueError:
                self.error("PATH_OUTSIDE_PACKAGE", location,
                           "Resolved path leaves the manifest directory.", context)
                return None
            if not resolved.is_file():
                self.error("FILE_READ_ERROR", location,
                           "Path must identify a readable regular file.", context)
                return None
            raw = resolved.read_bytes()
        except (OSError, ValueError, RuntimeError, UnicodeError):
            self.error("FILE_READ_ERROR", location,
                       "Could not resolve or read this package file.", context)
            return None
        if raw.startswith(b"\xef\xbb\xbf"):
            self.error("UTF8_BOM_NOT_ALLOWED", location,
                       "Save text as UTF-8 without a BOM.", context)
            return None
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeError:
            self.error("INVALID_UNICODE", location,
                       "File must contain valid UTF-8 text.", context)
            return None
        return raw, text

    def unicode_valid(self, value, location="$", context=None):
        # JSON permits escaped lone surrogates, but the package requires UTF-8.
        if isinstance(value, str):
            try:
                value.encode("utf-8", errors="strict")
            except UnicodeError:
                self.error("INVALID_UNICODE", location,
                           "JSON strings must be representable in UTF-8.", context)
                return False
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if not self.unicode_valid(item, "{}[{}]".format(location, i)):
                    return False
        elif isinstance(value, dict):
            for key, item in value.items():
                if not self.unicode_valid(key, location):
                    return False
                child = location + "[" + json.dumps(key, ensure_ascii=True) + "]"
                if not self.unicode_valid(item, child):
                    return False
        return True

    def load_manifest(self, manifest_path):
        try:
            path = Path(manifest_path).resolve(strict=True)
            if not path.is_file():
                raise OSError("Not a file")
            raw = path.read_bytes()
            self.base = path.parent
        except (OSError, TypeError, ValueError, RuntimeError, UnicodeError):
            self.error("MANIFEST_READ_ERROR", "$", "Could not read the manifest file.")
            return None
        if raw.startswith(b"\xef\xbb\xbf"):
            self.error("UTF8_BOM_NOT_ALLOWED", "$", "Save JSON as UTF-8 without a BOM.")
            return None
        try:
            document = raw.decode("utf-8", errors="strict")
        except UnicodeError:
            self.error("INVALID_UNICODE", "$", "Manifest must contain valid UTF-8.")
            return None
        try:
            manifest = json.loads(document, object_pairs_hook=_unique_object,
                                  parse_constant=_reject_constant,
                                  parse_float=_finite_float)
        except _DuplicateKey:
            self.error("DUPLICATE_JSON_KEY", "$", "JSON objects must not repeat keys.")
            return None
        except (ValueError, RecursionError):
            self.error("INVALID_JSON", "$", "Manifest is not valid finite JSON.")
            return None
        if not isinstance(manifest, dict):
            self.error("INVALID_OBJECT", "$", "Manifest must be a JSON object.")
            return None
        try:
            if not self.unicode_valid(manifest):
                return None
        except RecursionError:
            self.error("INVALID_JSON", "$", "Manifest nesting is too deep.")
            return None
        return manifest

    def sources(self, manifest):
        rows = self.list_field(manifest, "sources", "$")
        sources = {}
        seen = set()
        for i, row in enumerate(rows or []):
            location = "$.sources[{}]".format(i)
            if not isinstance(row, dict):
                self.error("INVALID_OBJECT", location, "Source must be an object.")
                continue
            identifier = self.identifier(row, location, seen)
            path = self.string(row, "path", location, trim=True)
            sha = row.get("sha256")
            valid_sha = isinstance(sha, str) and SHA256.fullmatch(sha) is not None
            if not valid_sha:
                self.error("INVALID_SHA256", location + ".sha256",
                           "Expected exactly 64 hexadecimal characters.")
            loaded = self.read_relative(path, location + ".path")
            if loaded is not None:
                raw, text = loaded
                if valid_sha and hashlib.sha256(raw).hexdigest() != sha.lower():
                    self.error("SOURCE_HASH_MISMATCH", location + ".sha256",
                               "Source bytes differ from the recorded SHA-256.")
            else:
                text = None
            if identifier is not None and identifier not in sources:
                sources[identifier] = {"text": text}
        return sources

    def claims(self, manifest, sources):
        rows = self.list_field(manifest, "claims", "$")
        claims = {}
        seen = set()
        for i, row in enumerate(rows or []):
            location = "$.claims[{}]".format(i)
            if not isinstance(row, dict):
                self.error("INVALID_OBJECT", location, "Claim must be an object.")
                continue
            identifier = self.identifier(row, location, seen)
            source_id = self.string(row, "source_id", location, trim=True)
            quote = self.string(row, "quote", location, trim=True)
            status = row.get("status")
            if not isinstance(status, str) or status not in STATUSES:
                self.error("INVALID_CLAIM_STATUS", location + ".status",
                           "Use active, withdrawn, or unresolved.")
            if source_id is not None:
                if source_id not in sources:
                    self.error("UNKNOWN_SOURCE", location + ".source_id",
                               "Referenced source ID does not exist.")
                elif quote is not None and sources[source_id]["text"] is not None:
                    if quote not in sources[source_id]["text"]:
                        self.error("QUOTE_NOT_FOUND", location + ".quote",
                                   "Exact quote is absent from the source text.")
            if identifier is not None and identifier not in claims:
                claims[identifier] = {"status": status}
        return claims

    def drafts(self, manifest, claims):
        rows = self.list_field(manifest, "drafts", "$")
        seen = set()
        for i, row in enumerate(rows or []):
            location = "$.drafts[{}]".format(i)
            if not isinstance(row, dict):
                self.error("INVALID_OBJECT", location, "Draft must be an object.")
                continue
            identifier = self.identifier(row, location, seen)
            context = {"draft_id": identifier}
            path = self.string(row, "path", location, context, trim=True)
            loaded = self.read_relative(path, location + ".path", context)
            segments = self.list_field(row, "segments", location, context)
            dependency_ids = []
            texts = []
            all_texts_valid = segments is not None
            for j, segment in enumerate(segments or []):
                segment_location = location + ".segments[{}]".format(j)
                segment_context = {"draft_id": identifier, "segment_index": j}
                if not isinstance(segment, dict):
                    self.error("INVALID_OBJECT", segment_location,
                               "Segment must be an object.", segment_context)
                    all_texts_valid = False
                    continue
                text = self.string(segment, "text", segment_location, segment_context)
                if text is None:
                    all_texts_valid = False
                else:
                    texts.append(text)
                kind = segment.get("kind")
                if not isinstance(kind, str) or kind not in KINDS:
                    self.error("INVALID_SEGMENT_KIND", segment_location + ".kind",
                               "Use sourced, editorial, synthetic, or disclosure.",
                               segment_context)
                claim_ids = segment.get("claim_ids", [])
                if not isinstance(claim_ids, list):
                    self.error("INVALID_LIST", segment_location + ".claim_ids",
                               "Expected an array of claim IDs.", segment_context)
                    claim_ids = []
                if kind == "sourced":
                    if not claim_ids:
                        self.error("MISSING_CLAIM_IDS", segment_location + ".claim_ids",
                                   "A sourced segment needs at least one active claim.",
                                   segment_context)
                    for k, claim_id in enumerate(claim_ids):
                        claim_location = segment_location + ".claim_ids[{}]".format(k)
                        if not isinstance(claim_id, str) or not claim_id.strip():
                            self.error("INVALID_STRING", claim_location,
                                       "Expected a nonempty claim ID.", segment_context)
                            continue
                        if claim_id not in dependency_ids:
                            dependency_ids.append(claim_id)
                        if claim_id not in claims:
                            self.error("UNKNOWN_CLAIM", claim_location,
                                       "Referenced claim ID does not exist.", segment_context)
                        elif claims[claim_id]["status"] != "active":
                            self.error("INACTIVE_CLAIM", claim_location,
                                       "Referenced claim is not active.", segment_context)
                elif isinstance(kind, str) and kind in KINDS:
                    if claim_ids:
                        self.error("UNEXPECTED_CLAIM_IDS", segment_location + ".claim_ids",
                                   "Only sourced segments may declare claim IDs.",
                                   segment_context)
                    self.string(segment, "review_note", segment_location,
                                segment_context, trim=True)
            draft_text = loaded[1] if loaded is not None else None
            mapped_text = "".join(texts) if all_texts_valid else None
            if draft_text is not None and mapped_text is not None and draft_text != mapped_text:
                self.error("DRAFT_COVERAGE_MISMATCH", location + ".segments",
                           "Ordered segment text must exactly equal the entire draft file.",
                           context)
            self.report["drafts"].append({
                "id": identifier,
                "character_length": len(draft_text) if draft_text is not None else None,
                "mapped_character_length": len(mapped_text) if mapped_text is not None else None,
                "segment_count": len(segments) if segments is not None else None,
                "claim_ids": dependency_ids,
            })

    def run(self, manifest_path):
        manifest = self.load_manifest(manifest_path)
        if manifest is None:
            return self.report
        version = manifest.get("schema_version")
        if type(version) is not int or version != 1:
            self.error("INVALID_SCHEMA_VERSION", "$.schema_version",
                       "schema_version must be the integer 1.")
        sources = self.sources(manifest)
        claims = self.claims(manifest, sources)
        self.drafts(manifest, claims)
        if not self.report["errors"]:
            self.report["status"] = "structure_ready"
        return self.report


def check_package(manifest_path):
    """Return a JSON-serializable structural report; never approve publication."""
    return _Checker().run(manifest_path)


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        checker = _Checker()
        checker.error("CLI_ARGUMENTS", "$", "Usage: check_content_package.py package.json")
        report = checker.report
    else:
        report = check_package(args[0])
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 0 if report["status"] == "structure_ready" else 2


if __name__ == "__main__":
    sys.exit(main())
