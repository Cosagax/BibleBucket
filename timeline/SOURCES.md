# Scripture Atlas — sources and editorial boundaries

Snapshot assembled 2026-11-06. The live, reader-friendly explanation is [sources.html](sources.html).

## Coverage and requested collection

This project is a curated interactive Genesis–Kings timeline. Jake requested the wider 88-book Ethiopian collection as its reference scope, with Enoch and its stories included in the main experience. The exact 88-book edition remains unidentified, so this release does not claim edition-level completeness.

The existing BibleBucket book index is a broad reading list, not evidence for the contents of a particular Ethiopian edition. The Ethiopian Orthodox Tewahedo Church's own English canon explanation describes 81 books with its grouping conventions: <https://www.ethiopianorthodox.org/english/canonical/books.html>. Modern English “88-book” compilations differ. Meqabyan must never be substituted with the Greek Maccabees books.

Integrated primary sources include 1 Enoch (108 chapters), Jubilees (50 chapters), the shared Genesis–Kings narratives, Chronicles, prophetic books, and the separately transmitted Prayer of Manasseh. The reading room also makes the remaining supplied WEB Classic texts available, without labeling their collection as the Ethiopian canon. There are 83 reading-text files, not a claim of an 83-book or 88-book canon.

Outstanding source work: identify the requested edition's actual table of contents; obtain verified, suitably licensed English texts for Meqabyan and any other Ethiopian-specific works to be represented; place material according to its actual narrative setting rather than forcing later books into the early timeline. These gaps are visible on the source page.

## Public-domain reading texts

| Text | Exact source | Rights and processing |
| --- | --- | --- |
| World English Bible Classic, full ecumenical book set | <https://ebible.org/Scriptures/eng-web_html.zip> (existing library snapshot); publisher <https://ebible.org/eng-web/> | Public domain; `World English Bible` is a trademark of eBible.org. Verse wording is preserved; website furniture, section headings, ordinary footnotes, and HTML markup are omitted. Notes explaining footnote-only verse numbers are preserved as explicitly labeled edition notes, not merged into Scripture. This remains an excerpted reading presentation of the named edition, not a new translation. |
| 1 Enoch, R. H. Charles, 1917 | <https://www.gutenberg.org/ebooks/77935>; original local library text retained as `texts/enoch-original.txt` | Source work public domain in the United States. Original Gutenberg notices/license retained in the full source file. Reader extracts the 108 chapter texts, omitting editorial headings, endnotes, introductory essay, and transcription notes. Critical symbols and verse numbering are preserved. The edition places some chapter 91 material with chapter 93; that material is collected under chapter 91 in the reader. |
| Jubilees, R. H. Charles, 1913 | <https://wesley.nnu.edu/sermons-essays-books/noncanonical-literature/noncanonical-literature-ot-pseudepigrapha/the-book-of-jubilees/> | Public-domain translation from *The Apocrypha and Pseudepigrapha of the Old Testament*, Oxford: Clarendon Press, 1913. Transcription credited on the source to Joshua Williams, Northwest Nazarene College. Only translation chapters are bundled; neither the site's presentation nor Charles's introduction is reproduced. Inline editorial chronological annotations remain identified as edition material. |

Input SHA-256 hashes are recorded in `source-checksums.json`. The original research downloads are not required for the published runtime. Rebuilding requires the four inputs named by `tools/build_sources.py`; no private paths are embedded in the site.

## Dates

Primary passages support the narrative claims; they do not by themselves prove modern BCE assignments. Early Genesis, patriarchal, Exodus, and settlement entries use narrative order. The kings view follows the Thiele column of the comparison tables at <https://en.wikipedia.org/wiki/Kings_of_Israel_and_Judah>, consulted 2026-11-06, as an explicitly approximate display convention. Thiele's listed sole-rule intervals are used consistently rather than mixing them with another table's co-regency start dates. The display extends Jehoiachin to 597 BCE to represent the conventional capture date. It does not claim a resolution of every synchronization or regnal total.

Saul (c. 1050–1010), David (c. 1010–970), and Solomon (c. 970–931) are broad conventional estimates. Rival and short reigns are labeled in their entries. Minimum-width graphical markers do not imply a year-long reign. Prophet windows are deliberately broad editorial context bands based on named kings and narrative contexts in the cited passages; exact ministry dates are not asserted.

## Maps and original art

- Natural Earth 1:110m land: <https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson>.
- Public-domain rights: <https://www.naturalearthdata.com/about/terms-of-use/>.
- Projection: simple equirectangular view over 24°–49° E and 25°–40° N. No modern country borders. This is an orientation map, not a reconstruction of ancient geography.
- Place coordinates are editorial approximate markers. Disputed/regional markers are flagged in `data.json`. Eden, celestial journeys, and an exact Exodus crossing remain unmapped.
- Dashed lines connect locations associated with a selected entry. They do not assert the sequence or path of an ancient journey.
- `assets/story-world.svg` is an original, editable illustration created for BibleBucket. It depicts a conceptual garden-to-city journey, not an archaeological reconstruction.

## Content maintenance

`tools/build_data.py` is the curated source for entities, relationships, genealogies, map markers, and guided trails. `data.json` is its published output. Every entry has at least one primary reference. Source badges identify Enoch and Jubilees; they do not grade their value relative to other texts.

Relationship graphs distinguish parent/child, marriage, and distant ancestry. Family trees are selected subsets. Athaliah's conflicting kinship wording is explained instead of silently resolved. Named duplicates such as the two Jehorams, two Ahaziahs, and two Joashes remain separate IDs.

On revisions: run the data builder, validate all references against local text files, check all four views and reading-room interaction, then review the focused Git diff. Keep content corrections and source provenance in this repository, not in an unrelated agent skill.
