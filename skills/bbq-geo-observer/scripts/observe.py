#!/usr/bin/env python3
"""Offline normalization of manually exported observations. No model/network calls."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

UNKNOWN = 'unknown'

def tri(value):
    if value is True or str(value).strip().lower() in {'true', 'yes', '1'}:
        return True
    if value is False or str(value).strip().lower() in {'false', 'no', '0'}:
        return False
    return UNKNOWN

def normalize(row, index):
    if not isinstance(row, dict):
        raise ValueError(f'row {index}: expected object')
    raw = dict(row)
    answer = row.get('answer_text')
    if answer is None:
        answer = row.get('answer')
    if not isinstance(answer, str) or not answer.strip():
        answer = None
    status = row.get('answer_status') or ('answered' if answer else 'not_run')
    warnings = []
    if status in {'not_run', 'blocked', 'error'} and answer:
        warnings.append('answer_present_with_non_answer_status')
    answered = bool(answer) and status not in {'not_run', 'blocked', 'error'}
    if not answer and row.get('answer_record'):
        warnings.append('external_answer_record_not_loaded; supply answer_text explicitly')
    if not answer and status == 'answered':
        warnings.append('answered_status_without_answer_text')
    target = str(row.get('target_entity') or '')
    aliases = row.get('target_aliases') or []
    if not isinstance(aliases, list):
        aliases = []
    names = [x for x in [target] + aliases if isinstance(x, str) and x.strip()]
    # Literal matching is a candidate signal, never identity or implicit-mention adjudication.
    match = any(n.casefold() in answer.casefold() for n in names) if answered and names else UNKNOWN
    reported = tri(row.get('mentioned')) if answered else UNKNOWN
    if reported != UNKNOWN and match != UNKNOWN and reported != match:
        warnings.append('reported_mention_disagrees_with_literal_match; review context')
    identity = row.get('identity_verdict') or UNKNOWN
    if identity not in {'accurate', 'inaccurate', 'mixed', 'contradictory', 'not_applicable', UNKNOWN}:
        warnings.append('unrecognized_identity_verdict_preserved_in_raw')
        identity = UNKNOWN
    if not answered:
        identity = UNKNOWN
    urls = row.get('cited_urls') or []
    if isinstance(urls, str):
        try:
            decoded = json.loads(urls)
            urls = decoded if isinstance(decoded, list) else [urls]
        except json.JSONDecodeError:
            urls = [u.strip() for u in urls.split(';') if u.strip()]
    if not isinstance(urls, list):
        urls = []
        warnings.append('invalid_cited_urls_type')
    support = row.get('claim_source_support')
    if support in (None, ''):
        support = UNKNOWN
    if not answered:
        support = UNKNOWN
    return {
        'run_id': row.get('run_id') or f'row-{index}',
        'observed_at': row.get('observed_at') or UNKNOWN,
        'product_entry': row.get('product_entry') or UNKNOWN,
        'visible_version': row.get('visible_version') or UNKNOWN,
        'search_mode': row.get('search_mode') or UNKNOWN,
        'search_triggered': tri(row.get('search_triggered')) if answered else UNKNOWN,
        'target_entity_correctly_identified': tri(row.get('target_entity_correctly_identified')) if answered else UNKNOWN,
        'language': row.get('language') or UNKNOWN,
        'region': row.get('region') or UNKNOWN,
        'session_conditions': row.get('session_conditions') or UNKNOWN,
        'question_group': row.get('question_group') or UNKNOWN,
        'question': row.get('question') or UNKNOWN,
        'target_entity': target or UNKNOWN,
        'answer_status': status,
        'answer_text': answer,
        'answer_sha256': hashlib.sha256(answer.encode()).hexdigest() if answer else None,
        'mentioned': reported,
        'literal_mention_candidate': match,
        'identity_verdict': identity,
        'identity_basis': 'supplied review; not independently verified' if identity != UNKNOWN else UNKNOWN,
        'cited_urls': urls,
        'claim_source_support': support,
        'citation_basis': 'supplied review; no source fetch performed',
        'warnings': warnings,
        'raw': raw,
    }

def load(path):
    if path.suffix.lower() == '.csv':
        with path.open(encoding='utf-8-sig', newline='') as f:
            return list(csv.DictReader(f))
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    if isinstance(data, dict):
        data = data.get('observations')
    if not isinstance(data, list):
        raise ValueError('Input must be a JSON array, {observations: [...]}, or CSV')
    return data

def build(rows, dataset_kind):
    observations = [normalize(row, i + 1) for i, row in enumerate(rows)]
    counts = Counter(str(r['mentioned']).lower() for r in observations)
    return {
        'schema_version': 1, 'dataset_kind': dataset_kind,
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'mode': 'offline_manual_export',
        'summary': {'total_rows': len(observations), 'mention_review_counts': dict(counts),
                    'rates': UNKNOWN, 'reason': 'No comparable sampling denominator validated'},
        'observations': observations,
        'limits': ['No model calls or source verification', 'Literal matches may be ambiguous; absence is not a reviewed non-mention',
                   'Raw answers may contain personal or confidential information; local processing is not public-release permission',
                   'Identity and citation support are supplied reviews, never inferred from a URL or name'],
    }

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', type=Path)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--dataset-kind', required=True, choices=['fixture', 'real_manual_export'])
    args = ap.parse_args()
    try:
        result = build(load(args.input), args.dataset_kind)
    except (ValueError, OSError) as e:
        ap.exit(2, f'Input error: {e}\n')
    if args.output.resolve() == args.input.resolve():
        ap.exit(2, 'Output must not overwrite source input\n')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result['summary'], ensure_ascii=False))

if __name__ == '__main__':
    main()
