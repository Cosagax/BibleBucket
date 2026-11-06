#!/usr/bin/env python3
"""Rebuild local, public-domain reading texts; no runtime Python is required.

Usage: python3 tools/build_sources.py --web-html ARCHIVE --enoch TEXT
    --jubilees-html HTML --land-geojson GEOJSON
Install beautifulsoup4 in your development environment if it is not available.
Sources, editions, and rights are documented in ../SOURCES.md.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
from zipfile import ZipFile
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[1]


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, separators=(',', ':')) + '\n')


def roman(value):
    table = dict(I=1, V=5, X=10, L=50, C=100, D=500, M=1000)
    total, last = 0, 0
    for c in reversed(value):
        n = table[c]
        total += -n if n < last else n
        last = max(last, n)
    return total


def build(args):
    manifest = {}
    books = {}
    with ZipFile(args.web_html) as archive:
        for name in sorted(archive.namelist()):
            match = re.fullmatch(r'([A-Z0-9]{3})(\d+)\.htm', name)
            if not match or match[1] in ('FRT', 'GLO'):
                continue
            code, chapter = match[1], str(int(match[2]))
            soup = BeautifulSoup(archive.read(name), 'html.parser')
            main = soup.select_one('.main')
            if not main:
                continue
            verse_notes = {}
            for marker in main.select('a.notemark'):
                verse = marker.find_previous('span', class_='verse')
                popup = marker.select_one('.popup')
                if verse and popup:
                    number = verse.get('id', '').removeprefix('V')
                    verse_notes.setdefault(number, []).append(popup.get_text(' ', strip=True))
            for unwanted in main.select('.tnav,.footnote,.copyright,.notemark,.chapterlabel,.s,.s1,.s2,.r,.sr,.mr'):
                unwanted.decompose()
            verses, current, parts = {}, None, []
            for node in main.descendants:
                if isinstance(node, Tag) and 'verse' in node.get('class', []):
                    if current:
                        verses[current] = re.sub(r'\s+', ' ', ''.join(parts)).strip()
                    current, parts = node.get('id', '').removeprefix('V'), []
                elif isinstance(node, NavigableString) and current:
                    if not any('verse' in p.get('class', []) for p in node.parents if isinstance(p, Tag)):
                        parts.append(str(node))
            if current:
                verses[current] = re.sub(r'\s+', ' ', ''.join(parts)).strip()
            if not verses:
                continue
            title = re.sub(r'\s+\d+$', '', soup.title.get_text().replace('World English Bible Classic ', ''))
            book = books.setdefault(code, {'title': title, 'edition': 'World English Bible Classic', 'format': 'verses', 'chapters': {}})
            omitted = {n: ' '.join(verse_notes.get(n, [])) for n, value in verses.items() if not value.strip()}
            for number, note in omitted.items():
                assert note, f'{code} {chapter}:{number}: empty verse with no source note'
                del verses[number]
            if omitted:
                book.setdefault('textualNotes', {})[chapter] = omitted
            book['chapters'][chapter] = verses
    assert len(books['GEN']['chapters']) == 50
    assert len(books['PSA']['chapters']) == 150
    assert len(books['REV']['chapters']) == 22
    assert books['GEN']['chapters']['1']['1'] == 'In the beginning, God created the heavens and the earth.'
    for code, book in books.items():
        save(ROOT / 'texts' / (code + '.json'), book)
        manifest[code] = {k: book[k] for k in ('title', 'edition', 'format')}
        manifest[code]['chapters'] = sorted(map(int, book['chapters']))

    enoch_original = Path(args.enoch).read_text()
    enoch = enoch_original.split('*** END OF THE PROJECT GUTENBERG')[0]
    enoch = enoch[enoch.index('I. 1. The words of the blessing'):]
    # Chapter 38's numeral occurs only in its editorial heading in this edition.
    enoch = enoch.replace('XXXVIII. _The Coming Judgement of the Wicked._', 'XXXVIII. ')
    enoch = enoch.replace('XCI. 12-17. _The Last Three Weeks._', 'XCI. ')
    enoch = re.sub(r'CVIII\.\s+AN APPENDIX TO THE BOOK OF ENOCH\.', 'CVIII. ', enoch)
    enoch = enoch.split('PRINTED IN GREAT BRITAIN BY')[0]
    paragraphs = []
    for paragraph in re.split(r'\n\s*\n', enoch):
        stripped = paragraph.strip()
        if not stripped:
            continue
        # Drop standalone editorial headings, preserving actual chapter text.
        if stripped.startswith(('_', '=')) or stripped == 'AN APPENDIX TO THE BOOK OF ENOCH.':
            continue
        if re.match(r'^[IVXLCDM][IVXLCDM,.\d\s–-]*[_=]', stripped):
            continue
        paragraphs.append(paragraph)
    enoch = '\n\n'.join(paragraphs)
    matches = list(re.finditer(r'^[ \t]*\[?([IVXLCDM]+)\.[ \t]+(?![ \t]*[_=])', enoch, re.M))
    chapters = {}
    for index, match in enumerate(matches):
        chapter = roman(match[1])
        end = matches[index + 1].start() if index + 1 < len(matches) else len(enoch)
        text = enoch[match.end():end].strip()
        # Separate scholarly endnotes and inter-chapter headings from the translation.
        text = re.split(r'\n\s*\[\d+\]', text)[0]
        text = re.sub(r'\n\s+[IVXLCDM]+[^\n]*_.*?(?=\n\n|$)', '', text, flags=re.S)
        text = re.sub(r'\[\d+\]', '', text)
        text = re.sub(r'\n[ \t]+', '\n', text).strip()
        chapters[str(chapter)] = (chapters.get(str(chapter), '') + '\n\n' + text).strip()
    assert set(map(int, chapters)) == set(range(1, 109)), 'Check Enoch chapter boundaries before publishing'
    book = {'title': '1 Enoch', 'edition': 'R. H. Charles, 1917', 'format': 'prose', 'chapters': chapters}
    save(ROOT / 'texts/ENO.json', book)
    # Keep the source and its license byte-for-byte, including original CRLFs.
    (ROOT / 'texts/enoch-original.txt').write_bytes(Path(args.enoch).read_bytes())
    manifest['ENO'] = {'title': '1 Enoch', 'edition': book['edition'], 'format': 'prose', 'chapters': list(range(1, 109))}

    soup = BeautifulSoup(Path(args.jubilees_html).read_text(), 'html.parser')
    text = soup.get_text('\n', strip=True)
    matches = list(re.finditer(r'\[Chapter (\d+)\]', text))
    chapters = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        chapter_text = text[match.end():end].strip()
        if index == len(matches) - 1:
            # The translation ends at the doxology, before the host site's footer.
            ending = re.search(r'Herewith is completed the account of the division of the days\.', chapter_text)
            if not ending:
                ending = re.search(r'ever and ever\.\s*Amen\.', chapter_text, re.I)
            if ending:
                chapter_text = chapter_text[:ending.end()]
        chapters[match[1]] = chapter_text
    assert set(map(int, chapters)) == set(range(1, 51)), 'Check Jubilees chapter boundaries before publishing'
    book = {'title': 'Jubilees', 'edition': 'R. H. Charles, 1913', 'format': 'prose', 'chapters': chapters}
    save(ROOT / 'texts/JUB.json', book)
    manifest['JUB'] = {'title': 'Jubilees', 'edition': book['edition'], 'format': 'prose', 'chapters': list(range(1, 51))}
    save(ROOT / 'texts/index.json', manifest)

    # Equirectangular base map. Clip to the eastern Mediterranean / Near East.
    # Coordinates remain geographic; no modern political boundaries are drawn.
    geo = json.loads(Path(args.land_geojson).read_text())
    paths = []
    for feature in geo['features']:
        geom = feature['geometry']
        polygons = [geom['coordinates']] if geom['type'] == 'Polygon' else geom['coordinates']
        for polygon in polygons:
            ring = polygon[0]
            xs, ys = zip(*ring)
            if max(xs) < 24 or min(xs) > 49 or max(ys) < 25 or min(ys) > 40:
                continue
            paths.append('M' + 'L'.join(f'{(x-24)*40:.2f},{(40-y)*40:.2f}' for x,y in ring) + 'Z')
    save(ROOT / 'assets/land.json', paths)
    inputs = {key: hashlib.sha256(Path(getattr(args, key)).read_bytes()).hexdigest() for key in ('web_html', 'enoch', 'jubilees_html', 'land_geojson')}
    save(ROOT / 'source-checksums.json', inputs)
    print(f'Built {len(manifest)} reading texts, {sum(len(x["chapters"]) for x in manifest.values())} chapters, and {len(paths)} land shapes.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for option in ('web-html', 'enoch', 'jubilees-html', 'land-geojson'):
        parser.add_argument('--' + option, required=True)
    build(parser.parse_args())
