#!/usr/bin/env python3
"""Validate declared evidence, asset and delivery metadata; no visual certification."""
import argparse
import hashlib
import json
from pathlib import Path


def validate(data, base, delivery=False):
    errors, warnings = [], []
    def check(condition, message):
        if not condition:
            errors.append(message)
    def index(key):
        rows = data.get(key, [])
        ids = [r.get('id') for r in rows]
        check(all(ids) and len(set(ids)) == len(ids) if rows else True,
              f'{key}: missing or duplicate IDs')
        return {r.get('id'): r for r in rows}
    sources, claims, slides, assets = [index(k) for k in ('sources', 'claims', 'slides', 'assets')]
    check(bool(data.get('revision')), 'Missing revision')
    if not sources:
        warnings.append('No designated sources registered; confirm source requirements with brief')
    for sid, s in sources.items():
        check(s.get('kind') in ('video', 'official', 'transcript'), f'{sid}: invalid source kind')
        check(bool(s.get('url')) and s.get('designated_by_user') is True, f'{sid}: source missing or not user-designated')
    for cid, c in claims.items():
        check(c.get('type') in ('fact', 'demo', 'plan', 'inference'), f'{cid}: invalid claim type')
        check(bool(c.get('text')) and bool(c.get('evidence')), f'{cid}: missing claim/evidence')
        for e in c.get('evidence', []):
            check(e.get('source_id') in sources and bool(e.get('locator')), f'{cid}: unresolved evidence')
    def box(b):
        return (isinstance(b, list) and len(b) == 4 and
                all(isinstance(v, (int, float)) and not isinstance(v, bool) and 0 <= v <= 1 for v in b)
                and b[0] < b[2] and b[1] < b[3])
    for aid, a in assets.items():
        check(a.get('source_id') in sources and bool(a.get('locator')), f'{aid}: missing source/locator')
        check(a.get('supports_claim') in claims, f'{aid}: missing supported claim')
        check(bool(a.get('slide_ids')) and all(s in slides for s in a.get('slide_ids', [])), f'{aid}: invalid target slides')
        check(a.get('status') in ('planned', 'saved'), f'{aid}: invalid asset status')
        if a.get('status') == 'saved':
            check(bool(a.get('path')) and (base / a['path']).is_file(), f'{aid}: saved asset file missing')
            crop, subject = a.get('crop'), a.get('subject_box')
            check(box(crop) and box(subject), f'{aid}: invalid crop/subject box')
            if box(crop) and box(subject):
                check(crop[0] <= subject[0] and crop[1] <= subject[1] and crop[2] >= subject[2] and crop[3] >= subject[3], f'{aid}: crop cuts protected subject')
        if delivery:
            check(a.get('status') == 'saved', f'{aid}: planned asset remains')
    for sid, s in slides.items():
        check(bool(s.get('title')), f'{sid}: missing title')
        check(all(c in claims for c in s.get('claim_ids', [])), f'{sid}: unknown claim')
        for aid in s.get('asset_ids', []):
            check(aid in assets and sid in assets[aid].get('slide_ids', []), f'{sid}: asset binding missing {aid}')
        for group in s.get('parallel_groups', []):
            check(len(group) >= 2 and all(a in s.get('asset_ids', []) for a in group), f'{sid}: incomplete parallel image group')
    for aid, a in assets.items():
        for sid in a.get('slide_ids', []):
            check(sid in slides and aid in slides[sid].get('asset_ids', []), f'{aid}: reverse slide binding missing {sid}')
    for g in data.get('glossary', []):
        check(bool(g.get('official_name')) and bool(g.get('description')) and g.get('first_slide_id') in slides, 'Incomplete glossary entry')
    if delivery:
        check(bool(sources) and bool(slides), 'Delivery requires sources and slides')
        check(bool(data.get('manifest')) and (base / data['manifest']).is_file(), 'Canonical manifest missing')
        requested = data.get('requested_formats', [])
        check(all(f in ('html', 'pdf', 'pptx', 'zip') for f in requested), 'Unsupported requested format')
        artifacts = data.get('artifacts', [])
        check(bool(requested) or bool(data.get('site')), 'No delivery requested')
        expected = [{'id': s['id'], 'title': s['title']} for s in data.get('slides', [])]
        for fmt in requested:
            matches = [a for a in artifacts if a.get('format') == fmt]
            check(len(matches) == 1, f'{fmt}: expected one current artifact')
        for a in artifacts:
            label = a.get('format', 'artifact')
            p = base / a.get('path', '')
            check(p.is_file(), f'{label}: file missing')
            if p.is_file():
                check(hashlib.sha256(p.read_bytes()).hexdigest() == a.get('sha256'), f'{label}: changed file hash')
            check(a.get('revision') == data['revision'], f'{label}: stale revision')
            check(a.get('slides') == expected, f'{label}: slide count/order/title mismatch')
            check(a.get('visual_review') == 'passed', f'{label}: visual inspection incomplete')
        site = data.get('site')
        if site:
            check(bool(site.get('url')) and site.get('revision') == data['revision'] and site.get('verified') is True, 'Site unverified or stale')
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('register', type=Path)
    parser.add_argument('--delivery', action='store_true')
    args = parser.parse_args()
    try:
        errors, warnings = validate(json.loads(args.register.read_text()), args.register.resolve().parent, args.delivery)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(json.dumps({'input_error': str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({'errors': errors, 'warnings': warnings, 'scope': 'metadata/files only; actual visual inspection required'}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
