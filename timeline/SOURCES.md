# Scripture Atlas — sources and editorial boundaries

Snapshot assembled 2026-11-06. The live, reader-friendly explanation is [sources.html](sources.html).

## Coverage and requested collection

This project is a curated interactive Creation-to-new-creation timeline, with its original Genesis–Kings material retained unchanged. Jake requested the wider 88-book Ethiopian collection as its reference scope, with Enoch and its stories included in the main experience. The exact 88-book edition remains unidentified, so this release does not claim edition-level completeness.

The existing BibleBucket book index is a broad reading list, not evidence for the contents of a particular Ethiopian edition. The Ethiopian Orthodox Tewahedo Church's own English canon explanation describes 81 books with its grouping conventions: <https://www.ethiopianorthodox.org/english/canonical/books.html>. Modern English “88-book” compilations differ. Meqabyan must never be substituted with the Greek Maccabees books.

Integrated primary sources include 1 Enoch (108 chapters), Jubilees (50 chapters), the shared Genesis–Kings narratives, Chronicles, prophetic books, and the separately transmitted Prayer of Manasseh. The continuation adds exile and return, Second Temple context, Jesus’ arrival, ministry, cross and resurrection, Acts and the letters, and Revelation. All 27 New Testament books are cited in curated entries. Greek 1 Maccabees supplies an explicitly identified historical bridge; it is not Meqabyan. The reading room also makes the remaining supplied WEB Classic texts available, without labeling their collection as the Ethiopian canon. There are 83 reading-text files, not a claim of an 83-book or 88-book canon.

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
- Projection: the original simple equirectangular view covers 24°–49° E and 25°–40° N; the added Mediterranean frame covers 10°–50° E and 22°–46° N. Both use the identical Natural Earth input hash. Small islands may be omitted at this coarse map scale. No modern country borders. This is an orientation map, not a reconstruction of ancient geography.
- Place coordinates are editorial approximate markers. Disputed/regional markers are flagged in `data.json`. Eden, celestial journeys, and an exact Exodus crossing remain unmapped.
- Dashed lines connect locations associated with a selected entry. They do not assert the sequence or path of an ancient journey.
- `assets/story-world.svg` is an original, editable illustration created for BibleBucket. It depicts a conceptual garden-to-city journey, not an archaeological reconstruction.

## Content maintenance

`tools/build_data.py` and its additive `tools/new_testament.py` module are the curated sources for entities, relationships, genealogies, map markers, and guided trails. `data.json` is its published output. Every entry has at least one primary reference. Source badges identify Enoch and Jubilees; they do not grade their value relative to other texts.

Relationship graphs distinguish parent/child, marriage, and distant ancestry. Family trees are selected subsets. Athaliah's conflicting kinship wording is explained instead of silently resolved. Named duplicates such as the two Jehorams, two Ahaziahs, and two Joashes remain separate IDs.

On revisions: run the data builder, validate all references against local text files, check all four views and reading-room interaction, then review the focused Git diff. Keep content corrections and source provenance in this repository, not in an unrelated agent skill.

## Jesus, the calendar, and the Gospel accounts

BC/AD numbering was devised centuries after Jesus to count from His birth. BCE/CE uses the same numbering; this historical convention has no year zero. Jesus’ birth is commonly placed around 6–4 BCE. The infancy accounts name rulers and circumstances with well-known chronological difficulties; this atlas does not invent a solution to the Herod/Quirinius problem. Public ministry is placed broadly in the late 20s / early 30s CE, and 30 or 33 CE are common crucifixion proposals. These are orientation notes, not claims of exact dates from the passages alone.

Chronology references: [Britannica, Jesus](https://www.britannica.com/biography/Jesus), [When Was Jesus Born?](https://www.britannica.com/topic/When-Was-Jesus-Born), and [Christian chronology](https://www.britannica.com/topic/chronology/Christian). For the Persian-period bridge, [Temple of Jerusalem](https://www.britannica.com/topic/Temple-of-Jerusalem) supplies the conventional 538/515 BCE context. Birth and crucifixion dates remain labeled approximate.

The Gospels retain their distinct voices: infancy details, temptation order, temple-action placement, meal chronology, resurrection witnesses, and appearances are not flattened into an invented exact harmonization. Matthew’s genealogy is displayed as a selected line with omitted generations labeled; Mary’s parenthood and Joseph’s household/guardian role have different edge types. Luke 3 is linked for comparison, not silently replaced with Matthew’s line. Mary Magdalene is not identified as Luke 7’s unnamed woman. Different people called Herod, John, James, and Joseph remain distinguished.

## Revelation: a source-led exploration, not a prediction engine

Revelation is arranged by its reading sequence. Its visions receive no BCE/CE positions. The introductory panel distinguishes common first-century, recurring-pattern, church-history, and future-focused readings without declaring one the established meaning. The millennium entry separately notes premillennial, amillennial, and postmillennial disagreement.

The 27 `echoes` panels across the expansion label each connection: explicit quotation, textual identification, comparison, or shared imagery. E.g. Revelation 1:20 identifies lampstands; Revelation 12:9 identifies the dragon. The woman, witnesses, beasts, 144,000, and millennium have disputed interpretations that are not treated as textual identifications. Image similarities do not establish a precise prophetic timetable or a named modern target.

Supplemental reading: [Bible Odyssey, The Seven Cities of Revelation](https://www.bibleodyssey.org/articles/the-seven-cities-of-revelation/), [The Sign of the Beast](https://www.bibleodyssey.org/articles/the-sign-of-the-beast/), and [Gematria](https://www.bibleodyssey.org/articles/gematria-2/). These present scholarly historical approaches, not a consensus statement binding every tradition. Nero Caesar is identified as a prominent proposal for 666; the 616 manuscript variant is noted separately from the WEB reading text, which prints 666. No new translation or manuscript variant is silently inserted into Scripture.

The Ethiopian official in Acts 8 is connected with the ancient Kandake’s African court, commonly identified with Kush rather than mapped directly onto modern Ethiopia ([BiblicalTraining, Ethiopian Eunuch](https://www.biblicaltraining.org/library/ethiopian-eunuch)). Acts’ narrative, later church tradition, and modern borders are not conflated. Jude 14–15 and 1 Enoch 1 have an explicit connection; that citation does not settle every tradition’s canon boundaries.

## Preservation and verification

`tools/check_expansion.mjs` hashes the original first-release arrays and verifies the unchanged 188 entries, seven eras, 34 places, five families, six trails, and 17 prophet windows. The original SVG, heartlands asset, reading texts, and other BibleBucket sections are retained. `tools/check_data.mjs` checks all passage references, including explicitly labeled edition-note-only verses, and every echo panel’s citations. Original saved IDs remain valid.
