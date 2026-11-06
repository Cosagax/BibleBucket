#!/usr/bin/env python3
"""Build the second map from the SAME Natural Earth source as the original.

Usage: python3 timeline/tools/build_mediterranean.py /path/to/land.geojson
The original heartlands asset and reading texts are never modified.
"""
import hashlib
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
source = Path(sys.argv[1])
expected = json.loads((root / 'source-checksums.json').read_text())['land_geojson']
assert hashlib.sha256(source.read_bytes()).hexdigest() == expected, 'Unexpected Natural Earth source; review provenance before replacing it.'
paths = []
for feature in json.loads(source.read_text())['features']:
    geometry = feature['geometry']
    polygons = [geometry['coordinates']] if geometry['type'] == 'Polygon' else geometry['coordinates']
    for polygon in polygons:
        ring = polygon[0]
        xs, ys = zip(*ring)
        if max(xs) < 10 or min(xs) > 50 or max(ys) < 22 or min(ys) > 46:
            continue
        paths.append('M' + 'L'.join(f'{(x-10)*25:.2f},{(46-y)*25:.2f}' for x, y in ring) + 'Z')
(root / 'assets/mediterranean-land.json').write_text(json.dumps(paths, separators=(',', ':')) + '\n')
print(f'Built {len(paths)} Mediterranean land shapes; original map retained.')
