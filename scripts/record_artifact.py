#!/usr/bin/env python3
"""Record a local output and independently observed slide inventory; reset visual review."""
import argparse
import hashlib
import json
import os
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('register', type=Path)
    p.add_argument('format', choices=['html', 'pdf', 'pptx', 'zip'])
    p.add_argument('path', type=Path)
    p.add_argument('--slides', type=Path, required=True)
    a = p.parse_args()
    data = json.loads(a.register.read_text())
    slides = json.loads(a.slides.read_text())
    if not isinstance(slides, list) or not slides or any(not isinstance(s, dict) or not s.get('id') or not s.get('title') for s in slides):
        p.error('--slides requires nonempty ordered objects with id and title')
    item = {'format': a.format, 'path': os.path.relpath(a.path.resolve(), a.register.resolve().parent),
            'sha256': hashlib.sha256(a.path.read_bytes()).hexdigest(), 'revision': data['revision'],
            'slides': [{'id': s['id'], 'title': s['title']} for s in slides], 'visual_review': 'pending'}
    data['artifacts'] = [v for v in data.get('artifacts', []) if v.get('format') != a.format] + [item]
    a.register.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(f'Recorded {a.format}; visual review reset to pending')


if __name__ == '__main__':
    main()
