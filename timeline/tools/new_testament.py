"""Additive, passage-led continuation of the original Genesis–Kings atlas.

The first-release records are deliberately left unchanged. Dates describe a
setting, not a harmonization of every Gospel or a timetable for Revelation.
"""


def extend(eras, entries, places, families, trails, refs):
    era_rows = [
        ('return', '08', 'Hope beyond exile', 'Daniel, Esther & a people returning home', 'Daniel · Esther · Ezra · Nehemiah', 'Exile and Persian-period settings · some stories overlap era 07'),
        ('threshold', '09', 'The world awaiting Jesus', 'Empires change. The promise remains.', '1 Maccabees · the prophets · Gospel context', 'Second Temple background · not four centuries of an empty story'),
        ('arrival', '10', 'Jesus enters the story', 'The Word becomes flesh and dwells among us', 'Matthew 1–3 · Luke 1–3 · John 1', 'Birth often placed c. 6–4 BCE · exact chronology debated'),
        ('ministry', '11', 'The kingdom draws near', 'Walk with Jesus: teaching, mercy & signs', 'Matthew · Mark · Luke · John', 'Public ministry · commonly placed in the late 20s / early 30s CE'),
        ('passion', '12', 'The cross & the empty tomb', 'Jesus gives His life. Death does not keep Him.', 'The four Gospels · Acts 1', 'Passion and resurrection · commonly dated around 30 or 33 CE'),
        ('church', '13', 'To the ends of the earth', 'The risen Jesus, the Spirit & a growing church', 'Acts · the New Testament letters', 'First-century settings · letters are grouped by theme, not asserted writing date'),
        ('revelation', '14', 'Behold, all things new', 'The revelation of Jesus Christ', 'Revelation · echoes across Scripture', 'Vision sequence, not a dated schedule of future events'),
    ]
    eras.extend(dict(zip(('id', 'number', 'title', 'subtitle', 'books', 'dating'), row)) for row in era_rows)

    def add(id, title, era, summary, reference, loc='', links='', kind='story', note='', date='', primary=True):
        entries.append(dict(id=id, title=title, era=era, kind=kind, summary=summary,
                            refs=refs(reference), places=loc.split(), related=links.split(),
                            collection='shared', date=date or next(e['dating'] for e in eras if e['id'] == era),
                            bce=None, primary=primary, note=note))

    # Exile is not the end of the promise. These settings can overlap the last
    # original era; retaining that distinction is better than forcing a date.
    add('daniel-exile', 'Faithfulness in a foreign court', 'return',
        'Daniel and his companions are given new names and a place in Babylon’s royal training. They cannot choose the empire around them, but they can choose faithfulness within it. The exile becomes the setting of a story about wisdom, courage, and a kingdom no human ruler can finally own.',
        'DAN 1;DAN 2', 'babylon', 'first-exile furnace daniel-son-man', note='Daniel’s narrative setting and the book’s composition are separate historical questions.')
    add('furnace', 'A fourth figure in the fire', 'return',
        'Shadrach, Meshach, and Abednego refuse to bow before the king’s golden image. Their answer does not bargain for a rescue: God can deliver them, but even if He does not, they will not worship the image. In the furnace, the king sees a fourth figure; the story turns imperial spectacle into testimony.',
        'DAN 3', 'babylon', 'daniel-exile lions-den rev-beasts', note='The king describes the fourth figure in 3:25; 3:28 calls the deliverer an angel. Identifying that figure specifically as the preincarnate Christ is a Christian interpretation, not an explicit identification in the passage.')
    add('writing-wall', 'The writing on the wall', 'return',
        'At Belshazzar’s feast, vessels taken from Jerusalem’s temple become drinking cups. A hand writes a judgment that the court cannot read. Daniel interprets the message: power has been weighed, found wanting, and is passing away. The city of exile itself stands under judgment.',
        'DAN 5', 'babylon', 'daniel-exile cyrus-return rev-babylon')
    add('lions-den', 'Prayer when the windows stay open', 'return',
        'A royal decree makes Daniel’s ordinary prayer a dangerous act. He continues to pray toward Jerusalem and is thrown into the lions’ den. The king cannot simply undo his own law; deliverance comes from the God Daniel serves. Faithfulness is shown in a daily habit before it becomes a dramatic rescue.',
        'DAN 6', 'babylon', 'daniel-exile furnace', note='The identity of “Darius the Mede” is debated. This entry follows the story without assigning him an uncontested identification or calendar year.')
    add('daniel-son-man', 'One like a son of man', 'return',
        'Beastly empires rise from the sea, but Daniel’s vision does not end with the beasts. Before the Ancient of Days, one like a son of man receives an everlasting dominion, and the holy ones receive the kingdom. Jesus’ use of “Son of Man” and Revelation’s throne-room imagery invite readers back into this vision.',
        'DAN 7;MRK 14:61-62;REV 1:12-18', links='heavenly-court jesus trial-jesus rev-beasts rev-throne', kind='vision', note='The vision explains the beasts as kingdoms and connects dominion with the holy ones. Its reception in the Gospels and Revelation is part of the connection, not a claim that every interpretive question has one answer.')
    add('dry-bones', 'Can these bones live?', 'return',
        'Ezekiel stands before a valley of dry bones and hears a question only God can answer. Bone joins bone; breath enters the slain. The passage itself names the bones as the whole house of Israel, speaking hope to a people who say their hope is lost. Resurrection imagery grows from a concrete promise of restoration.',
        'EZK 37:1-14', links='ezekiel jerusalem-falls cyrus-return resurrection-hope rev-new-creation', kind='vision')
    add('cyrus-return', 'The road home opens', 'return',
        'The opening of Ezra announces a change no prisoner could manufacture: Cyrus permits the rebuilding of the house of God in Jerusalem. Families prepare to return, neighbors contribute, and temple vessels come out of imperial storage. The promise surviving at the end of Kings now has a road to travel.',
        'EZR 1;ISA 44:24-28;ISA 45:1-6', 'babylon jerusalem', 'jehoiachin-release dry-bones second-temple zerubbabel', date='Cyrus’s decree conventionally placed c. 538 BCE')
    add('second-temple', 'A foundation laid with tears and joy', 'return',
        'Returned exiles rebuild the altar and lay the temple’s foundation. Some shout for joy; those who remember the former house weep. Opposition and discouragement delay the work, but Haggai and Zechariah call the community forward. The rebuilt temple becomes part of the world Jesus will enter.',
        'EZR 3;EZR 5:1-2;EZR 6:14-22;HAG 1', 'jerusalem', 'cyrus-return temple zerubbabel zechariah-branch temple-rededication', date='Rebuilding after the return · completion conventionally c. 515 BCE')
    add('zerubbabel', 'Zerubbabel: a royal line after exile', 'return',
        'Zerubbabel leads returned exiles and takes part in rebuilding the temple. Haggai addresses him as governor of Judah, not as a restored king. Matthew later includes him in the genealogy that leads through Joseph’s household to Jesus: exile interrupts the monarchy, but not the Gospel’s tracing of the promise.',
        'EZR 3:2-8;HAG 2:20-23;MAT 1:12-16', 'jerusalem', 'jehoiachin cyrus-return second-temple joseph-nazareth jesus', kind='person', primary=False)
    add('zechariah-branch', 'The Branch, the lampstand & the coming king', 'return',
        'Zechariah speaks to a rebuilding community with visions of cleansing, lampstands, and olive trees, and with promises of a figure called the Branch. Elsewhere a humble king arrives on a donkey. These images will reappear in the Gospel accounts of Jesus’ entrance and in Revelation’s witnesses.',
        'ZEC 3;ZEC 4;ZEC 6:9-15;ZEC 9:9-10', 'jerusalem', 'second-temple palm-entry rev-witnesses', kind='vision')
    add('esther-courage', 'For such a time as this', 'return',
        'In the Persian court at Susa, Esther must decide whether to speak when silence might seem safer. Mordecai’s challenge, a fast, carefully timed banquets, and the exposure of Haman’s plot turn a threat of destruction into deliverance. The story remembers vulnerable people living far from Jerusalem, not only those who returned.',
        'EST 4;EST 7;EST 9:20-32', 'susa', 'cyrus-return nehemiah-walls', note='This entry follows the Hebrew-form Esther supplied in the reader. The separately supplied Greek additions are not silently blended into it.')
    add('nehemiah-walls', 'A broken city becomes a shared task', 'return',
        'News of Jerusalem’s broken walls draws prayer from Nehemiah before it draws a plan. With royal permission he returns, inspects the damage, and gathers people for the work. Families rebuild amid threats and fatigue. Restoration means more than stones: Nehemiah also confronts exploitation within the community.',
        'NEH 1;NEH 2;NEH 5;NEH 6', 'susa jerusalem', 'esther-courage second-temple ezra-word', date='Persian-period restoration · fifth century BCE')
    add('ezra-word', 'The people hear the book again', 'return',
        'Ezra reads the law before a gathered people while others help them understand it. Tears give way to a call to share food and rejoice; the story of the people is heard again in their own rebuilt city. Scripture is not merely recovered as an object—it is read, explained, and lived together.',
        'EZR 7:1-10;NEH 8', 'jerusalem', 'lost-scroll nehemiah-walls nazareth-scroll', date='Persian-period restoration · fifth century BCE')
    add('malachi-messenger', 'A messenger before the Lord', 'return',
        'Malachi challenges weary worship, injustice, and broken faithfulness. The book looks toward a messenger who prepares the way and toward Elijah’s coming. When the Gospels introduce John the Baptist, they deliberately bring these words back into view: the next chapter is connected to the old promises.',
        'MAL 3:1-5;MAL 4;MRK 1:1-4;LUK 1:13-17', links='elijah john-baptist waiting-messiah')

    # A historical bridge without treating Greek Maccabees as Meqabyan.
    add('empires-between', 'Between Persia and Rome', 'threshold',
        'The opening of 1 Maccabees looks back to Alexander and the kingdoms divided among his successors. Greek-speaking political and cultural worlds form part of the background to later Jewish life. The road to the Gospels passes through living communities, contested loyalties, and changing empires—not an empty gap.',
        '1MA 1:1-15', 'jerusalem', 'cyrus-return temple-rededication rome-herod', note='This is the Greek 1 Maccabees in the WEB ecumenical collection, not Ethiopian Meqabyan. It is identified here as a historical bridge; the two works must not be substituted for one another.')
    add('temple-rededication', 'The dedication Jesus remembers', 'threshold',
        'After the temple’s desecration, Judas Maccabeus and his companions cleanse the sanctuary, rebuild the altar, and celebrate its dedication. John later places Jesus in Jerusalem during the Feast of Dedication, in winter. A named Gospel setting opens a doorway into the history between the Testaments.',
        '1MA 4:36-59;JHN 10:22-30', 'jerusalem', 'second-temple empires-between good-shepherd', date='Rededication conventionally c. 164 BCE · John’s scene is centuries later', note='The first reference is Greek 1 Maccabees, not Ethiopian Meqabyan. The later Gospel scene is linked, not assigned the rededication’s date.')
    add('rome-herod', 'An empire, a client king & a coming child', 'threshold',
        'The Gospels name rulers as well as villages: Matthew places Jesus’ birth under Herod, Luke names Augustus, and Luke’s account of John’s ministry names Tiberius and Pontius Pilate. These are stories told in a world of empire, taxation, local rulers, and ordinary families—not a kingdom waiting on an empty stage.',
        'MAT 2:1-6;LUK 2:1-7;LUK 3:1-3', 'jerusalem rome bethlehem', 'herod-great nativity john-baptist pontius-pilate', note='Matthew’s Herod setting and Luke’s reference to Quirinius raise a well-known chronological difficulty. The atlas preserves both accounts and does not claim to have resolved it.')
    add('waiting-messiah', 'Waiting for consolation', 'threshold',
        'Isaiah speaks of light, a child, and a shoot from Jesse; Luke introduces Simeon and Anna as people waiting for consolation and redemption. The Gospels tell Jesus’ story within Israel’s hopes. Those hopes were not one uniform political program, and Jesus’ way of fulfilling them repeatedly surprises those around Him.',
        'ISA 9:1-7;ISA 11:1-10;LUK 2:25-38', 'jerusalem', 'isaiah covenant-david jesus presentation')
    add('jewish-world', 'The Jewish world Jesus calls home', 'threshold',
        'Jesus’ family keeps Passover, He teaches in synagogues, and His conversations engage the Scriptures of Israel. Pharisees, Sadducees, priests, teachers, and ordinary worshippers do not all hold the same views. The Gospels’ debates belong within this varied Jewish world; they are not a portrait of an entire people as Jesus’ enemies.',
        'LUK 2:41-52;LUK 4:16-21;MRK 12:18-34;ACT 23:6-8', 'jerusalem nazareth', 'temple-child nazareth-scroll greatest-command')

    # Jesus is the center, not an appendix. His story has three distinct eras.
    add('jesus', 'Jesus · the Word made flesh', 'arrival',
        'The promises converge on a person. Matthew introduces Jesus as Messiah, son of David and son of Abraham. Luke brings us to a child laid in a manger. John reaches back to “the beginning” and announces that the Word became flesh and dwelt among us. The center of this journey is Jesus: His life, His self-giving death, His resurrection, and His invitation to follow.',
        'MAT 1:1-17;LUK 2:1-20;JHN 1:1-18;COL 1:15-20', 'bethlehem nazareth jerusalem', 'abraham-call covenant-david john-prologue nativity baptism-jesus cross-jesus empty-tomb rev-lamb', kind='person', date='Jesus’ life, death, resurrection & continuing reign', note='The Gospel genealogies and infancy accounts are presented in their own voices. Joseph’s place in Matthew’s genealogy is not a claim that he is Jesus’ biological father.')
    add('john-prologue', 'In the beginning was the Word', 'arrival',
        'John starts before Bethlehem. The Word is with God, the Word is God, and all things come into being through Him. Light shines in darkness; the Word becomes flesh and dwells among us. Read beside Genesis and the tabernacle story, this is an announcement about creation and God’s presence, not merely a new name on a family tree.',
        'JHN 1:1-18;GEN 1:1-5;EXO 40:34-38', links='creation tabernacle jesus rev-new-creation', date='John’s theological opening · the Word before creation and made flesh')
    add('annunciation', 'Let it be to me according to your word', 'arrival',
        'Gabriel comes to Mary in Nazareth with news of a son, a throne, and a kingdom without end. Mary asks how this can be; the answer points to the Holy Spirit and the power of the Most High. The promise to David is now spoken into the life of a young woman far from a royal palace.',
        'LUK 1:26-38;2SA 7:12-16', 'nazareth', 'mary-jesus covenant-david mary-elizabeth nativity')
    add('joseph-dream', 'Joseph receives a difficult promise', 'arrival',
        'Joseph’s intention to separate quietly from Mary changes after a dream. He is told not to fear taking her as his wife and to name the child Jesus, because He will save His people from their sins. Matthew links the birth with Immanuel—God with us—and shows Joseph responding with action.',
        'MAT 1:18-25;ISA 7:14', 'nazareth', 'joseph-nazareth annunciation nativity', note='Matthew explicitly applies Isaiah’s Immanuel passage to Jesus. Isaiah 7 also has its own original setting in the crisis facing King Ahaz; the connection does not erase that setting.')
    add('mary-elizabeth', 'Two mothers, one song of reversal', 'arrival',
        'Mary visits Elizabeth, and the meeting becomes blessing and song. Mary praises the God who lifts the lowly, fills the hungry, and remembers His promise to Abraham. Her song belongs beside Hannah’s: the arrival of Jesus is announced as mercy that overturns ordinary measurements of greatness.',
        'LUK 1:39-56;1SA 2:1-10', links='mary-jesus elizabeth john-birth hannah abraham-call')
    add('john-birth', 'A name, a voice & a prepared road', 'arrival',
        'Elizabeth’s child is named John, and Zechariah’s silence breaks into praise. His song looks toward salvation in David’s house and a child who will prepare the Lord’s ways. John’s story matters because it points beyond itself: the dawn he announces is about to arrive.',
        'LUK 1:5-25;LUK 1:57-80', links='elizabeth zechariah-priest john-baptist malachi-messenger')
    add('nativity', 'Good news in a manger', 'arrival',
        'Jesus is born in Bethlehem, David’s city, and laid in a manger. Luke places the announcement among ordinary travelers and shepherds, not among the empire’s celebrated victories. The child is proclaimed Savior, Christ, and Lord. The story’s center arrives with vulnerability before it is recognized in glory.',
        'LUK 2:1-20;MAT 1:18-25;MIC 5:2', 'bethlehem', 'jesus shepherds magi presentation ruth david', date='Often placed c. 6–4 BCE · exact birth date is unknown')
    add('shepherds', 'The first invitation is to shepherds', 'arrival',
        'In the fields outside Bethlehem, fear gives way to good news of great joy. The sign is a baby wrapped and lying in a manger. The shepherds go, see, tell, and return praising God; Mary keeps these things and ponders them. Wonder moves from the sky into a visit, then into a story shared.',
        'LUK 2:8-20', 'bethlehem', 'nativity mary-jesus good-shepherd')
    add('presentation', 'Simeon and Anna recognize the child', 'arrival',
        'In Jerusalem’s temple, Simeon takes Jesus in his arms and speaks of light for the nations and glory for Israel. Anna gives thanks and speaks about the child to those waiting for redemption. Celebration carries a shadow too: Simeon tells Mary of opposition and a sword that will pierce her own soul.',
        'LUK 2:21-38', 'jerusalem', 'nativity waiting-messiah mary-jesus cross-jesus')
    add('magi', 'A star, a search & another road home', 'arrival',
        'Visitors from the east come looking for the king of the Jews. In Jerusalem their question troubles Herod; in Bethlehem they offer gifts and worship the child. A dream sends them home another way. Matthew contrasts a ruler guarding his power with travelers ready to kneel before someone greater.',
        'MAT 2:1-12;MIC 5:2', 'bethlehem jerusalem', 'nativity herod-great flight-egypt', note='Matthew does not state the visitors’ number or call them kings. Their arrival is not forced onto the same night as Luke’s shepherds.')
    add('flight-egypt', 'The child becomes a refugee', 'arrival',
        'Warned in a dream, Joseph takes the child and His mother to Egypt while Herod orders violence in Bethlehem. After Herod’s death the family returns and settles in Nazareth. Matthew hears echoes of Israel’s earlier story: a threatened child, grief, Egypt, and a son called out of it.',
        'MAT 2:13-23;HOS 11:1;JER 31:15', 'bethlehem egypt nazareth', 'magi joseph-nazareth moses egypt-family', note='The Egypt marker is regional; Matthew does not supply an itinerary. Hosea’s original passage recalls Israel’s Exodus, which Matthew reuses in telling Jesus’ story.')
    add('temple-child', 'In My Father’s house', 'arrival',
        'At twelve, Jesus stays behind in Jerusalem after Passover. Mary and Joseph find Him among the teachers, listening and asking questions. His answer about His Father’s house opens a question they do not yet fully understand. Luke then returns Him to Nazareth, growing in wisdom and stature.',
        'LUK 2:41-52', 'jerusalem nazareth', 'jesus mary-jesus joseph-nazareth jewish-world', date='Jesus at twelve · Luke 2 does not specify a calendar year')
    add('john-baptist', 'A voice in the wilderness', 'arrival',
        'John calls people to repentance and baptizes in the Jordan region. The Gospels introduce him through Isaiah’s prepared road and Malachi’s messenger, while his clothing recalls Elijah. Yet John insists that the one coming after him is greater: his ministry is a doorway into Jesus’ story, not its destination.',
        'MRK 1:1-8;LUK 3:1-18;JHN 1:19-34;ISA 40:3-5', 'jordan', 'malachi-messenger elijah john-birth baptism-jesus', kind='prophet', date='John’s public ministry · Luke names Tiberius’s fifteenth year', note='The river pin indicates a region, not a securely located baptism site.')

    add('baptism-jesus', 'The beloved Son at the Jordan', 'ministry',
        'Jesus comes to John for baptism. The heavens open, the Spirit descends, and a voice names Him the beloved Son. Before the crowds, miracles, and confrontations, the Gospels place this declaration at the threshold of His public ministry. John’s witness points to Jesus as the Lamb of God.',
        'MAT 3:13-17;MRK 1:9-11;LUK 3:21-22;JHN 1:29-34', 'jordan', 'jesus john-baptist temptation-jesus transfiguration rev-lamb')
    add('temptation-jesus', 'Forty days in the wilderness', 'ministry',
        'In hunger and temptation, Jesus refuses to turn sonship into self-serving power. His answers draw from Deuteronomy: bread is not enough, God is not to be tested, and worship belongs to God alone. Israel’s wilderness story sounds again, now around the faithful Son preparing to announce the kingdom.',
        'MAT 4:1-11;LUK 4:1-13;DEU 6:13-16;DEU 8:2-3', links='baptism-jesus exodus-manna nazareth-scroll', note='Matthew and Luke arrange the temptations differently. This entry connects their shared themes without forcing an identical sequence.')
    add('exodus-manna', 'Bread in the wilderness, bread for the world', 'ministry',
        'When the crowd recalls manna, Jesus takes the conversation beyond a remembered meal. Moses did not give the final bread from heaven; the Father gives the true bread, and Jesus identifies Himself as the bread of life. This is a Gospel connection back to Exodus, not a new date assigned to the wilderness story.',
        'JHN 6:30-51;EXO 16', links='passover feeding-crowd bread-life temptation-jesus', note='This bridge entry is placed with John 6. The Exodus event itself belongs to the earlier wilderness period.')
    add('disciples-called', 'Leave the nets. Come and see.', 'ministry',
        'Jesus calls people into companionship before they understand where it will lead. Fishermen leave nets; Andrew brings Simon; Philip invites Nathanael to come and see. The Gospel accounts give distinct windows into these beginnings. The disciples will learn by walking, listening, failing, and being called again.',
        'MRK 1:16-20;LUK 5:1-11;JHN 1:35-51', 'galilee capernaum', 'peter andrew john-apostle james-zebedee peter-restored')
    add('cana', 'The first sign at a wedding', 'ministry',
        'At a wedding in Cana, the wine runs out. Mary brings the need to Jesus and tells the servants to do whatever He says. Water becomes wine, and John calls this the beginning of Jesus’ signs, revealing His glory. A household celebration becomes the setting for the disciples’ growing faith.',
        'JHN 2:1-12', 'cana', 'mary-jesus jesus disciples-called rev-wedding')
    add('nazareth-scroll', 'Today this Scripture is fulfilled', 'ministry',
        'In Nazareth’s synagogue, Jesus reads Isaiah’s announcement of good news to the poor, release, sight, and freedom. Then He says the Scripture is fulfilled in their hearing. Admiration turns toward anger when He recalls God’s mercy reaching a widow in Sidon and Naaman the Syrian. The kingdom will not be confined to hometown expectations.',
        'LUK 4:16-30;ISA 61:1-2;1KI 17:8-16;2KI 5:1-14', 'nazareth', 'isaiah elijah naaman jewish-world ezra-word')
    add('nicodemus', 'A conversation after dark', 'ministry',
        'Nicodemus comes to Jesus at night and hears about birth from above, the Spirit, and God’s love for the world. Jesus reaches back to Moses lifting the serpent in the wilderness to speak of the Son of Man being lifted up. A quiet conversation opens onto the meaning of the cross.',
        'JHN 3:1-21;NUM 21:4-9', 'jerusalem', 'jesus cross-jesus burial-jesus')
    add('samaritan-woman', 'Living water at the well', 'ministry',
        'Jesus asks a Samaritan woman for a drink and offers living water. Their conversation crosses inherited hostility and moves through thirst, truth, and worship. She leaves her water jar to invite others to meet Him. A person outside the expected circle becomes the voice that brings a town to listen.',
        'JHN 4:1-42', 'sychar', 'jacob jewish-world rev-river')
    add('beatitudes', 'Blessed are the unlikely', 'ministry',
        'Jesus calls the poor in spirit, the mourners, the meek, the merciful, and the peacemakers blessed. In the Sermon on the Mount, the kingdom’s life reaches into anger, reconciliation, desire, truthfulness, and love for enemies. The law and prophets are not discarded; the listener is invited into a searching, lived righteousness.',
        'MAT 5;MAT 7:12-29;LUK 6:20-36', 'galilee', 'jesus lord-prayer greatest-command faith-works', note='Matthew’s sermon on the mountain and Luke’s sermon on a level place are allowed their own settings and emphases. Galilee is a regional marker, not an identified hillside.')
    add('lord-prayer', 'Teach us to pray', 'ministry',
        'Jesus teaches His followers to address the Father with reverence and trust: His name, His kingdom, His will, daily bread, forgiveness, and deliverance. Prayer is neither a performance nor a way to overwhelm God with words. The prayer’s “us” keeps ordinary need and reconciliation inside a shared life.',
        'MAT 6:5-15;LUK 11:1-13', links='beatitudes gethsemane shared-life')
    add('forgiven-roof', 'A roof opens. A man rises.', 'ministry',
        'Friends carry a paralyzed man to Jesus and lower him through a roof when the crowd blocks the door. Jesus first announces forgiveness, then tells him to rise and walk. The scene brings friendship, mercy, and the question of His authority into one crowded room.',
        'MRK 2:1-12;LUK 5:17-26', 'capernaum', 'jesus sabbath-mercy')
    add('sabbath-mercy', 'Is it lawful to do good?', 'ministry',
        'In debates about grain and a healing on the Sabbath, Jesus places human need and mercy at the center of the encounter. A man’s hand is restored while opponents watch. These disputes reveal sharply different judgments about faithfulness; they are not permission to caricature Judaism as a religion without compassion.',
        'MRK 2:23-28;MRK 3:1-6;MAT 12:1-14', links='forgiven-roof jewish-world greatest-command')
    add('centurion-faith', 'Only say the word', 'ministry',
        'A centurion seeks help for a desperately ill servant. His understanding of authority becomes a picture of trust: Jesus need only speak. Jesus marvels at the faith He encounters. The kingdom’s invitation is already pressing beyond the boundaries that the disciples might have expected.',
        'MAT 8:5-13;LUK 7:1-10', 'capernaum', 'jesus syrophoenician cornelius', note='Matthew presents the appeal directly; Luke describes intermediaries. Both accounts remain available without rewriting one into the other.')
    add('widow-nain', 'Do not weep', 'ministry',
        'At Nain, Jesus meets a funeral procession for a widow’s only son. Moved with compassion, He tells her not to weep and calls the young man to rise. Luke’s wording recalls Elijah giving a restored son back to his mother: an older story of mercy sounds again as the crowd praises God.',
        'LUK 7:11-17;1KI 17:17-24', 'nain', 'elijah jairus-woman lazarus-raised')
    add('parables-seed', 'A kingdom told in seeds', 'ministry',
        'A sower scatters seed across different soils. A mustard seed grows beyond its small beginning. Through parables Jesus invites listeners to hear, reconsider, and respond: the kingdom is not measured only by what looks impressive at the start. The explanation of the soils turns the question toward the hearer’s own reception.',
        'MRK 4:1-34;MAT 13:1-35', 'galilee', 'jesus prodigal-son good-samaritan')
    add('storm-stilled', 'Who then is this?', 'ministry',
        'A storm fills the boat while Jesus sleeps. The disciples wake Him in fear; He speaks, and the wind and sea become calm. Their question shifts from whether they will survive to who is with them. Scripture’s language about God stilling the sea gives their astonishment a deeper background.',
        'MRK 4:35-41;PSA 107:23-32', 'galilee', 'jesus walking-water')
    add('jairus-woman', 'Two daughters, one interrupted journey', 'ministry',
        'Jesus goes with Jairus toward a dying child, but a woman suffering years of bleeding reaches for His garment. He stops to address her as daughter. News arrives that the child has died; Jesus continues, takes her hand, and tells her to rise. A delay becomes part of a story in which neither person is overlooked.',
        'MRK 5:21-43;LUK 8:40-56', 'galilee', 'jesus widow-nain lazarus-raised')
    add('feeding-crowd', 'Enough for the multitude', 'ministry',
        'With a hungry crowd before Him, Jesus receives a few loaves and fish, gives thanks, and distributes food through His disciples. Everyone eats, and baskets remain. All four Gospels tell this feeding; John draws the reader onward into a difficult conversation about the bread of life.',
        'MAT 14:13-21;MRK 6:30-44;LUK 9:10-17;JHN 6:1-15', 'galilee', 'exodus-manna bread-life walking-water', note='The regional lake marker does not identify a certain feeding site. This is the feeding of the five thousand, distinct from the four thousand in Matthew and Mark.')
    add('walking-water', 'It is I. Do not be afraid.', 'ministry',
        'The disciples struggle across the water and see Jesus coming toward them. Fear meets His reassurance. Matthew also tells of Peter stepping out, sinking, and being caught. The story is not about a disciple mastering the sea; it turns attention toward the one who reaches him in his fear.',
        'MAT 14:22-33;MRK 6:45-52;JHN 6:16-21', 'galilee', 'peter storm-stilled feeding-crowd')
    add('bread-life', 'Will you also go away?', 'ministry',
        'After the feeding, Jesus refuses to remain only the supplier of another meal. He speaks of Himself as the bread of life, given for the life of the world. Some listeners turn away at the difficulty of His words. Peter’s answer holds the question open in trust: to whom would they go, when Jesus has the words of eternal life?',
        'JHN 6:22-71', 'capernaum', 'feeding-crowd exodus-manna peter last-supper')
    add('syrophoenician', 'Mercy beyond the expected boundary', 'ministry',
        'A Gentile mother asks Jesus to free her daughter. The conversation is difficult, and her reply about crumbs under the table is persistent and bold. Jesus grants her request. Mark and Matthew preserve an encounter that refuses to let the reader overlook a mother’s faith across an inherited boundary.',
        'MRK 7:24-30;MAT 15:21-28', 'tyre sidon', 'centurion-faith cornelius', note='Mark calls her a Greek, Syrophoenician by birth; Matthew calls her Canaanite. The summaries retain that distinction rather than flattening the accounts.')
    add('peter-confession', 'You are the Christ', 'ministry',
        'Near Caesarea Philippi, Jesus asks who the disciples say He is. Peter names Him as the Christ. Yet recognition does not immediately become understanding: when Jesus speaks of suffering and death, Peter resists. Jesus connects discipleship with taking up a cross, not with securing the kind of victory Peter imagined.',
        'MAT 16:13-28;MRK 8:27-38', 'caesarea-philippi', 'peter daniel-son-man transfiguration cross-jesus')
    add('transfiguration', 'Listen to Him', 'ministry',
        'On a mountain, Jesus is transfigured before Peter, James, and John. Moses and Elijah appear, and the voice from the cloud calls the disciples to listen to the beloved Son. Luke says the conversation concerns the departure Jesus will accomplish in Jerusalem. Glory points toward the coming cross rather than away from it.',
        'MAT 17:1-8;MRK 9:2-8;LUK 9:28-36', links='moses elijah baptism-jesus peter-confession cross-jesus', note='The Gospels do not name this mountain. The atlas does not place an invented pin for it.')
    add('good-samaritan', 'Who became a neighbor?', 'ministry',
        'Asked who counts as a neighbor, Jesus tells of a wounded traveler, people who pass by, and a Samaritan who stops. Mercy is costly, practical, and offered across hostility. Jesus turns the question from drawing the right boundary around “my neighbor” toward becoming a neighbor to the person in need.',
        'LUK 10:25-37', links='samaritan-woman greatest-command faith-works', note='This is a parable, not a separately dated event. Its Jerusalem–Jericho setting is part of the story, not a reconstructed journey.')
    add('mary-martha', 'At His feet, in the middle of hospitality', 'ministry',
        'Martha welcomes Jesus while Mary sits listening at His feet. Distracted by much serving, Martha asks Him to intervene. Jesus answers her anxiety with an invitation to the one needed thing. The scene honors the act of hearing Him without turning hospitality or work into enemies of faith.',
        'LUK 10:38-42', links='jesus lazarus-raised bethany-anointing', note='Luke does not name the village in this scene. Its placement at Bethany is not asserted from Luke alone.')
    add('prodigal-son', 'The father runs', 'ministry',
        'A younger son wastes his inheritance and returns rehearsing a speech. His father runs to welcome him before he can bargain for a servant’s place. Outside the celebration, an older brother has his own struggle with grace. Jesus leaves the invitation sounding toward both sons—and toward those listening.',
        'LUK 15', links='jesus zacchaeus letters-love', note='The lost sheep, coin, and sons are parables told in response to criticism of Jesus welcoming sinners, not episodes on a historical calendar.')
    add('born-blind', 'One thing I know: now I see', 'ministry',
        'Jesus refuses the assumption that a man’s blindness can be explained by assigning blame to him or his parents. After Jesus gives him sight, the man faces repeated questioning and exclusion. Jesus finds him again. The chapter gradually asks who truly sees, and who is unwilling to recognize what stands before them.',
        'JHN 9', 'jerusalem', 'jesus good-shepherd sabbath-mercy')
    add('good-shepherd', 'The shepherd lays down His life', 'ministry',
        'Jesus describes a shepherd who knows His sheep, calls them by name, and does not abandon them to danger. He lays down His life willingly and speaks of other sheep and one flock. Read beside Psalm 23 and Ezekiel’s critique of failed shepherds, this image becomes a claim about the care and leadership God’s people need.',
        'JHN 10:1-30;PSA 23;EZK 34:1-16', 'jerusalem', 'shepherds born-blind temple-rededication cross-jesus rev-lamb')
    add('lazarus-raised', 'I am the resurrection and the life', 'ministry',
        'At Bethany, Martha meets Jesus with grief and trust while Mary weeps at His feet. Jesus Himself weeps. Before Lazarus is called from the tomb, Jesus identifies resurrection and life with Himself. The sign brings joy to a household and intensifies the decision of opponents to put Jesus to death.',
        'JHN 11', 'bethany', 'mary-martha bethany-anointing cross-jesus empty-tomb resurrection-hope')
    add('children-welcomed', 'Let the children come', 'ministry',
        'When the disciples try to turn children away, Jesus is indignant. He welcomes them, takes them in His arms, and speaks of receiving the kingdom like a child. The people a hurried group might treat as interruptions are placed at the center of His lesson about belonging.',
        'MRK 10:13-16;MAT 19:13-15', links='jesus beatitudes')
    add('zacchaeus', 'Today salvation has come to this house', 'ministry',
        'Zacchaeus climbs a tree to see Jesus and discovers that Jesus has come looking for him. An invitation to his house unsettles the crowd. His response involves generosity and restitution, not merely a private feeling. Jesus describes His mission as seeking and saving the lost.',
        'LUK 19:1-10', 'jericho', 'prodigal-son palm-entry faith-works')

    add('palm-entry', 'Your king comes to you, humble', 'passion',
        'Jesus enters Jerusalem on a donkey as people spread garments and branches along the way. The Gospels connect the scene with Zechariah’s humble king and the language of Psalm 118. The city receives a royal sign, but the kind of kingship Jesus will reveal is about to overturn expectations.',
        'MAT 21:1-11;MRK 11:1-11;LUK 19:28-44;JHN 12:12-19;ZEC 9:9', 'bethany jerusalem', 'zechariah-branch jesus temple-confrontation cross-jesus')
    add('temple-confrontation', 'A house of prayer for all nations', 'passion',
        'Jesus confronts buying and selling in the temple and invokes Isaiah’s house of prayer and Jeremiah’s warning about a den of robbers. His action challenges what the sanctuary has become. The conflict sharpens as leaders question His authority and the crowds continue to listen.',
        'MRK 11:15-18;ISA 56:6-7;JER 7:1-11;JHN 2:13-22', 'jerusalem', 'temple second-temple palm-entry trial-jesus', note='The Synoptic Gospels place this action in Jesus’ final Jerusalem ministry; John places a temple action near the beginning. Both passages are available without asserting that their chronology is identical.')
    add('greatest-command', 'Love God. Love your neighbor.', 'passion',
        'In a series of questions about authority, resurrection, and faithfulness, Jesus names love of God and love of neighbor as the heart of the commandments. He joins Deuteronomy and Leviticus, not a newly invented ethic detached from Israel’s Scriptures. Mark’s account ends with a teacher whom Jesus calls not far from the kingdom.',
        'MAT 22:34-40;MRK 12:28-34;DEU 6:4-5;LEV 19:18', 'jerusalem', 'jewish-world beatitudes good-samaritan letters-love')
    add('olivet-discourse', 'Watch, endure & do not be led astray', 'passion',
        'Looking toward the temple, Jesus speaks of its destruction, distress, deceptive claims, and the coming of the Son of Man. His followers are told to endure and stay awake, not to possess the day and hour. The discourse prepares readers for costly faithfulness and connects with Daniel’s language of crisis and vindication.',
        'MRK 13;MAT 24;MAT 25;LUK 21:5-36', 'mount-olives jerusalem', 'daniel-son-man rev-patmos rev-rider', note='Readers differ over how these sayings relate to Jerusalem’s destruction and the final coming of Christ. The atlas distinguishes the questions rather than turning the discourse into a modern prediction calendar.')
    add('bethany-anointing', 'A costly gift before the burial', 'passion',
        'At Bethany, costly perfume is poured out on Jesus. Objections focus on waste; Jesus speaks of burial and a deed that will be remembered with the good news. John names Mary and places the scene with Martha and Lazarus. The gift recognizes something about the coming death that others struggle to face.',
        'MRK 14:3-9;MAT 26:6-13;JHN 12:1-8', 'bethany', 'lazarus-raised mary-martha burial-jesus', note='John and the Synoptic accounts have distinct details and placement. Luke 7’s anointing is not silently merged into this Bethany scene.')
    add('last-supper', 'A table, a covenant & a coming kingdom', 'passion',
        'Jesus shares bread and a cup with His disciples and speaks of His body and blood given for them. Passover memory becomes the setting for a new-covenant promise. Betrayal is near, but the table is also pointed toward the kingdom. Paul later passes on this meal as a proclamation of the Lord’s death until He comes.',
        'LUK 22:7-23;MRK 14:12-25;1CO 11:23-26;JER 31:31-34', 'jerusalem', 'passover bread-life foot-washing cross-jesus rev-wedding', note='The Gospels’ presentation of the meal and Passover chronology is not forced into a single uncontested calendar reconstruction.')
    add('foot-washing', 'The Lord takes the servant’s place', 'passion',
        'Knowing where He has come from and where He is going, Jesus rises from supper, takes a towel, and washes His disciples’ feet. Peter struggles to receive it. Jesus turns the act into an example and gives a command to love one another as He has loved them. His greatness is expressed in service.',
        'JHN 13:1-35', 'jerusalem', 'last-supper peter vine-abiding letters-love')
    add('vine-abiding', 'Abide in Me', 'passion',
        'Jesus speaks of the vine and branches: life and fruitfulness come through remaining in Him. He calls His disciples friends, commands love, and promises the Spirit’s witness amid opposition. His prayer reaches beyond the room toward those who will believe through their word, asking that they may be one.',
        'JHN 14;JHN 15;JHN 16;JHN 17', 'jerusalem', 'foot-washing pentecost shared-life letters-love')
    add('gethsemane', 'Not My will, but Yours', 'passion',
        'In the garden, Jesus prays in deep distress while His companions struggle to stay awake. He does not disguise the cost before Him. His prayer entrusts His will to the Father, and betrayal arrives with an armed crowd. The one who could speak peace to a storm now enters suffering without abandoning His mission.',
        'MRK 14:32-52;LUK 22:39-53;JHN 18:1-11', 'mount-olives', 'lord-prayer trial-jesus peter-denial cross-jesus')
    add('peter-denial', 'Before the rooster crows', 'passion',
        'Peter has promised loyalty, but in the courtyard he repeatedly denies knowing Jesus. The rooster’s call brings Jesus’ warning back to him, and he weeps. This is not Peter’s final scene: the resurrection accounts will bring him from failure toward a renewed call to care for Jesus’ sheep.',
        'LUK 22:31-34;LUK 22:54-62;MRK 14:66-72', 'jerusalem', 'peter gethsemane peter-restored')
    add('trial-jesus', 'The Son of Man before His judges', 'passion',
        'Jesus faces questioning, conflicting testimony, mockery, and violence. In Mark, His answer about the Son of Man invokes Daniel and the language of sitting at God’s right hand. The scene places the promised king under judgment while the narrative invites readers to ask who truly holds authority.',
        'MRK 14:53-65;LUK 22:66-71;DAN 7:13-14;PSA 110:1', 'jerusalem', 'daniel-son-man gethsemane pilate-jesus', note='The accounts identify particular authorities and participants. They do not justify blaming Jewish people collectively for Jesus’ death; Jesus and His first followers are themselves Jewish.')
    add('pilate-jesus', 'My kingdom is not from this world', 'passion',
        'Before the Roman governor, Jesus is questioned about kingship. John records His answer that His kingdom is not from this world and His mission bears witness to truth. A crowd, a prisoner named Barabbas, mock royal clothing, and political pressure surround the decision. Pilate hands Jesus over to be crucified.',
        'JHN 18:28-40;JHN 19:1-16;MRK 15:1-20', 'jerusalem', 'pontius-pilate trial-jesus cross-jesus')
    add('cross-jesus', 'The King gives His life', 'passion',
        'Jesus is crucified outside Jerusalem under a royal charge. The Gospels let us hear abandonment, forgiveness, care for His mother, and trust in the Father through their distinct accounts. The curtain tears; a centurion responds. At the center of Christian faith stands this self-giving death—not a detour from Jesus’ mission, but its costly fulfillment.',
        'MRK 15:21-39;LUK 23:33-49;JHN 19:16-37;ISA 53;PSA 22', 'jerusalem', 'jesus passover last-supper burial-jesus empty-tomb rev-lamb', date='Crucifixion under Pontius Pilate · 30 and 33 CE are common proposals', note='The entries keep the Gospel accounts distinct rather than presenting a reconstructed sequence of every saying. The hill’s precise location is not asserted by a separate map pin.')
    add('burial-jesus', 'A borrowed tomb, a watched ending', 'passion',
        'Joseph of Arimathea asks for Jesus’ body and places it in a tomb. John names Nicodemus as another participant; the Synoptic accounts remember women seeing where He is laid. The story pauses with grief and a real burial, not with the disciples already expecting how the next morning will unfold.',
        'MRK 15:42-47;LUK 23:50-56;JHN 19:38-42', 'jerusalem', 'cross-jesus nicodemus mary-magdalene empty-tomb')
    add('empty-tomb', 'He is not here. He has risen.', 'passion',
        'Women come to the tomb and find that death has not kept Jesus. The Gospel accounts describe the discovery and its witnesses in different ways, but the announcement changes the direction of the whole story. The crucified Jesus is risen. Fear, joy, doubt, and recognition now lead His followers into a new beginning.',
        'MAT 28:1-10;MRK 16:1-8;LUK 24:1-12;JHN 20:1-18;1CO 15:3-8', 'jerusalem', 'jesus cross-jesus mary-risen emmaus thomas-risen resurrection-hope rev-new-creation', note='Witnesses, messengers, and the order of appearances differ across accounts. This entry does not manufacture one exhaustive itinerary. Mark 16:1–8 is used here without depending on the disputed longer ending.')
    add('mary-risen', 'He calls her by name', 'passion',
        'Mary Magdalene stands weeping near the tomb. She sees Jesus but does not recognize Him until He says her name. Grief becomes recognition and then a commission: she goes to the disciples with the announcement that she has seen the Lord. The resurrection’s good news is entrusted to her voice.',
        'JHN 20:11-18', 'jerusalem', 'mary-magdalene empty-tomb good-shepherd great-commission')
    add('emmaus', 'Their hearts burned on the road', 'passion',
        'Two disciples leave Jerusalem carrying disappointed hopes. A stranger walks with them and opens the Scriptures, beginning with Moses and the prophets. At the table, in the breaking of bread, they recognize Jesus. They hurry back: the older story has not been abandoned, but has become newly legible around the risen Christ.',
        'LUK 24:13-35', 'jerusalem', 'empty-tomb moses isaiah last-supper', note='Several sites have been proposed for Emmaus. The atlas does not choose one as certain or draw an invented route.')
    add('thomas-risen', 'My Lord and my God', 'passion',
        'Thomas is absent when Jesus first appears to the gathered disciples and resists their report. Jesus meets him with the wounds he demanded to see. Thomas answers with a confession, and Jesus speaks of those who will believe without having seen. John then explains why the signs in his Gospel were written.',
        'JHN 20:19-31', 'jerusalem', 'thomas-apostle empty-tomb jesus')
    add('peter-restored', 'Do you love Me? Feed My sheep.', 'passion',
        'Beside the lake, the risen Jesus prepares a meal after the disciples’ night of fishing. He asks Peter about love and entrusts him with caring for His sheep. Peter’s denial is not the last word over his life. The call “Follow Me” returns, now with an understanding that love will carry a cost.',
        'JHN 21', 'galilee', 'peter peter-denial good-shepherd disciples-called pentecost')
    add('great-commission', 'I am with you always', 'passion',
        'The risen Jesus meets His disciples in Galilee, where worship and doubt are both named. He sends them to make disciples of all nations, baptizing and teaching, and promises His presence to the end of the age. Matthew’s story that began with “God with us” ends with Jesus’ assurance that He remains with His people.',
        'MAT 28:16-20;MAT 1:23;LUK 24:44-49', 'galilee', 'jesus mary-risen ascension pentecost rev-new-creation')
    add('ascension', 'Witnesses, not owners of the timetable', 'passion',
        'Before Jesus is taken up, the disciples ask about the kingdom’s restoration. He redirects them from times reserved to the Father toward the Spirit’s power and their calling as witnesses: Jerusalem, Judea, Samaria, and the ends of the earth. His departure is not the end of His story; Acts follows what happens next.',
        'ACT 1:1-11;LUK 24:50-53', 'mount-olives jerusalem', 'great-commission pentecost daniel-son-man rev-rider')

    add('pentecost', 'The Spirit comes. The story goes outward.', 'church',
        'At Pentecost, the gathered followers of Jesus hear wind and see tongues like fire. People from many places hear God’s mighty works in their own languages. Peter connects the moment to Joel’s promise and proclaims the crucified and risen Jesus. A community begins to grow around repentance, baptism, teaching, meals, and prayer.',
        'ACT 2;JOL 2:28-32', 'jerusalem', 'ascension babel peter shared-life ethiopian-official')
    add('shared-life', 'Breaking bread, sharing life', 'church',
        'Acts describes believers devoting themselves to the apostles’ teaching, fellowship, the breaking of bread, and prayers. Possessions become resources for meeting need. The picture is neither an account of instant perfection nor a private spirituality: the risen Jesus is confessed through a shared, practical life.',
        'ACT 2:42-47;ACT 4:32-37;ACT 6:1-7', 'jerusalem', 'pentecost foot-washing barnabas stephen letters-love')
    add('stephen', 'A witness sees the Son of Man', 'church',
        'Chosen in the community’s response to overlooked widows, Stephen becomes a public witness. His speech retells Israel’s story, and his vision names the Son of Man at God’s right hand. As he is killed, he prays for his attackers. Saul stands nearby, a figure whose own story is about to turn.',
        'ACT 6;ACT 7', 'jerusalem', 'shared-life daniel-son-man saul-damascus', note='Stephen’s speech is a dispute narrated within the first-century biblical story, not grounds for hostility toward Jewish communities.')
    add('philip-samaria', 'Good news crosses into Samaria', 'church',
        'Persecution scatters believers, and Philip announces the Messiah in Samaria. The story that Jesus outlined before His ascension begins to unfold beyond Jerusalem. Joy, healing, baptism, and an encounter with Simon also raise a sharp question: God’s gift cannot be purchased as spiritual power.',
        'ACT 8:1-25', 'samaria', 'stephen samaritan-woman ethiopian-official ascension')
    add('ethiopian-official', 'From Isaiah’s scroll to Jesus', 'church',
        'On the road toward Gaza, Philip meets an Ethiopian court official reading Isaiah. “Who is the prophet talking about?” becomes the opening for Philip to proclaim Jesus. The official asks for baptism and goes on his way rejoicing. A reader from the African world is not on the edge of this story—he is one of its memorable witnesses to the widening good news.',
        'ACT 8:26-40;ISA 53:7-8', 'gaza', 'philip-samaria isaiah cross-jesus great-commission', note='Acts identifies the official with the Kandake’s court; this ancient “Ethiopia” is commonly connected with Kush, south of Egypt, not simply mapped onto the borders of modern Ethiopia. Later church traditions are distinct from what Acts explicitly narrates. Verse 37 appears as a labeled textual note in this reading edition.')
    add('saul-damascus', 'Saul, Saul, why do you persecute Me?', 'church',
        'Traveling to Damascus to arrest followers of the Way, Saul is confronted by the risen Jesus. Blind and dependent, he receives help from Ananias, who must face his own fear in approaching him. The persecutor becomes a witness. Acts retells the encounter later as Paul explains the calling that redirected his life.',
        'ACT 9:1-31;ACT 22:3-21;ACT 26:9-23', 'damascus', 'stephen paul barnabas first-mission')
    add('cornelius', 'God shows no partiality', 'church',
        'Cornelius receives a message to send for Peter; Peter receives a vision that challenges his boundaries. In the encounter that follows, Peter announces Jesus’ life, death, and resurrection. The Spirit comes upon Gentile hearers, and baptism follows. The church must recognize what God has already done.',
        'ACT 10;ACT 11:1-18', 'joppa caesarea', 'peter centurion-faith syrophoenician jerusalem-council')
    add('antioch-church', 'A church learns to send', 'church',
        'In Antioch, the message reaches a widening circle. Barnabas sees grace at work and brings Saul to help teach. Acts says the disciples are first called Christians here. Later, while the community worships and fasts, Barnabas and Saul are set apart and sent; a local church becomes a doorway to wider journeys.',
        'ACT 11:19-30;ACT 13:1-3', 'antioch', 'barnabas paul first-mission jerusalem-council')
    add('first-mission', 'Across Cyprus and into new towns', 'church',
        'Sent from Antioch, Barnabas and Saul travel through Cyprus and into communities of southern Asia Minor. They speak in synagogues, meet interest and resistance, and turn toward Gentile hearers. In Lystra, a healing is misunderstood as a visit from gods. On the return, they strengthen disciples and appoint elders.',
        'ACT 13;ACT 14', 'antioch salamis paphos pisidian-antioch iconium lystra derbe', 'antioch-church paul barnabas jerusalem-council', note='The map links named stops for orientation, not reconstructed sea lanes or roads. Acts 13–14 supplies the itinerary; the conventional numbered “missionary journeys” are editorial labels.')
    add('jerusalem-council', 'A table wide enough for the nations', 'church',
        'As Gentiles join the movement, a dispute arises over circumcision and the law of Moses. Peter recalls God’s action among Gentiles; Barnabas and Paul report their work; James turns to the prophets. The decision in Acts 15 seeks a way for this growing community to live together without denying what grace has done.',
        'ACT 15:1-35;AMO 9:11-12', 'jerusalem antioch', 'cornelius first-mission james-jerusalem letters-love', note='Acts and Paul’s letters offer distinct perspectives on early disputes. This entry does not assume that every related episode can be dated or aligned without debate.')
    add('lydia-philippi', 'The Lord opens Lydia’s heart', 'church',
        'A vision redirects Paul toward Macedonia. At a place of prayer outside Philippi, Lydia listens, receives the message, and opens her home. Acts introduces the new work through a woman’s response and hospitality before it describes the city’s prison. The movement grows around households as well as public speeches.',
        'ACT 16:6-15;ACT 16:40', 'troas philippi', 'paul philippi-prison letters-joy')
    add('philippi-prison', 'Songs in the prison', 'church',
        'Paul and Silas are beaten and imprisoned after a confrontation over an enslaved girl’s exploitation. At midnight they pray and sing. An earthquake opens the doors, but they stay; the jailer’s crisis becomes a question about salvation, then a shared meal and care for their wounds.',
        'ACT 16:16-40', 'philippi', 'lydia-philippi paul letters-joy')
    add('athens', 'The unknown God and the risen one', 'church',
        'In Athens, Paul reasons in the synagogue and marketplace, then addresses hearers at the Areopagus. He begins with their religious world and speaks of the Creator, repentance, judgment, and the man God raised from the dead. Some mock, some want to hear more, and some believe. Resurrection remains the point of decision.',
        'ACT 17:16-34', 'athens', 'paul empty-tomb corinth-household')
    add('corinth-household', 'Tentmakers, teachers & a growing church', 'church',
        'At Corinth, Paul works with Aquila and Priscilla while teaching about Jesus. Later, this couple helps Apollos understand the way more accurately. Their household connects travel, craft, hospitality, and teaching. Paul’s letters will address the difficult work of becoming one body amid rivalry and difference.',
        'ACT 18;ROM 16:3-5;1CO 12', 'corinth ephesus', 'paul priscilla-aquila letters-love')
    add('ephesus-word', 'The word grows in a city of competing loyalties', 'church',
        'Paul’s extended work in Ephesus brings teaching, changed loyalties, and public conflict. Some abandon magical practices; artisans fear the effect of the movement on the trade around Artemis. Acts shows the good news entering a city’s religious and economic life, not merely winning a private argument.',
        'ACT 19;ACT 20:17-38', 'ephesus', 'paul corinth-household rev-ephesus')
    add('paul-arrest', 'A witness in custody', 'church',
        'Paul’s return to Jerusalem leads to arrest, disputed accusations, and hearings before Roman officials. He speaks of his hope in resurrection and recounts his encounter with Jesus. His appeal to Caesar will carry the witness toward Rome, but as a prisoner rather than a triumphant imperial visitor.',
        'ACT 21:17-40;ACT 23;ACT 25;ACT 26', 'jerusalem caesarea', 'paul saul-damascus paul-shipwreck rome-witness')
    add('paul-shipwreck', 'Hope through the storm', 'church',
        'A journey to Rome becomes a long struggle against wind and sea. Paul encourages those aboard, food is shared, and the ship is lost while the people reach land. On Malta, strangers show extraordinary kindness. The mission continues through vulnerability and hospitality rather than control of the journey.',
        'ACT 27;ACT 28:1-10', 'crete malta', 'paul-arrest rome-witness storm-stilled', note='Acts names ports and episodes, but exact sailing tracks are reconstructed differently. The map’s connecting line is not a claim to trace the storm.')
    add('rome-witness', 'The story ends with an open door', 'church',
        'Paul reaches Rome in custody, yet receives visitors and teaches about the Lord Jesus Christ with boldness. Acts ends with the message unhindered, not with a completed biography of every apostle. The story that began in Jerusalem has reached the imperial capital—and its final scene still faces outward.',
        'ACT 28:11-31;ROM 1:1-17', 'rome', 'paul-shipwreck paul great-commission letters-love', note='Later traditions about Paul’s death are not presented as events narrated in Acts.')
    add('letters-love', 'One body. A more excellent way.', 'church',
        'The letters guide communities learning to follow Jesus together. Paul describes many gifts within one body, then names love as indispensable. Romans calls believers to overcome evil with good; Galatians speaks of the Spirit’s fruit; John insists that love of God and love of others cannot be separated.',
        '1CO 12;1CO 13;ROM 12;GAL 5:13-26;1JN 4:7-21', links='foot-washing greatest-command shared-life faith-works')
    add('faith-works', 'A living faith has hands', 'church',
        'Ephesians speaks of salvation by grace through faith and of being created for good works. James confronts a claim to faith that leaves a hungry neighbor unfed. Read in their own arguments, these passages turn the reader away from boasting and toward a life in which trust becomes visible as mercy.',
        'EPH 2:1-10;JAS 2:14-26', links='good-samaritan zacchaeus letters-love', note='Christian traditions explain the relation of faith, justification, and works differently. The atlas invites comparison of the passages rather than declaring those debates closed.')
    add('letters-joy', 'Joy shaped like self-giving', 'church',
        'Philippians calls a divided or anxious community toward the mind of Christ: humility, service, and hope. Its portrait of Jesus’ self-emptying and exaltation anchors an invitation to rejoice. Second Corinthians likewise connects treasure with fragile vessels and reconciliation with Christ, not with an appearance of invulnerability.',
        'PHP 2:1-18;PHP 4:4-9;2CO 4:7-18;2CO 5:14-21', links='cross-jesus philippi-prison letters-love')
    add('philemon-brother', 'Receive him as a beloved brother', 'church',
        'Paul appeals to Philemon concerning Onesimus, asking that he be received no longer merely as a slave but as a beloved brother. The short letter makes reconciliation concrete and personal, while leaving questions that later readers continue to wrestle with. Christian belonging presses against an existing social hierarchy.',
        'PHM 1;GAL 3:26-29', links='paul letters-love faith-works', note='The letter does not explicitly tell us every circumstance of Onesimus’s separation from Philemon or the eventual outcome. Those details are not filled in as facts.')
    add('care-communities', 'Guard the good entrusted to you', 'church',
        'Letters to Timothy and Titus speak of teaching, character, care, and leadership. Second and Third John show smaller communities wrestling with truth and hospitality; First Peter calls believers to bear witness through their conduct. These voices help the atlas follow Jesus beyond the journeys into the daily life of His people.',
        '1TI 3;2TI 1:3-14;TIT 2;2JN 1;3JN 1;1PE 2:9-12', links='timothy shared-life letters-love', note='The authorship and dates of several New Testament letters are debated. This thematic stop is not an assertion that all were written at the same moment.')
    add('jesus-high-priest', 'A priest who understands weakness', 'church',
        'Hebrews invites readers to approach God with confidence because Jesus is a high priest who knows human weakness. Its argument reaches back to Melchizedek, priesthood, covenant, and sanctuary. These older threads are not discarded: the letter rereads them around Jesus’ once-for-all self-offering and continuing intercession.',
        'HEB 4:14-16;HEB 7;HEB 9;HEB 10:1-25', links='melchizedek tabernacle last-supper cross-jesus')
    add('jude-enoch', 'Jude remembers Enoch', 'church',
        'Jude explicitly names Enoch, the seventh from Adam, and cites his announcement of the Lord coming with holy ones for judgment. Read the words beside 1 Enoch 1: the Ethiopian-preserved text is part of the conversation within the New Testament itself. Jude’s warning ends in an invitation to mercy and a doxology of hope.',
        'JUD 1:14-25;ENO 1;2PE 2:4-9', links='enoch judgment-watchers rev-judgment', note='This is an explicit textual connection. Jude’s use of Enoch does not by itself settle the canonical status of every part of 1 Enoch for all Christian traditions.')
    add('resurrection-hope', 'Because Christ has been raised', 'church',
        'Paul makes the resurrection of Jesus the foundation of hope for those who belong to Him. First Corinthians 15 speaks of Christ as firstfruits and of death’s defeat; First Thessalonians offers comfort for those grieving. Hope is not a reason to abandon ordinary faithfulness, but a reason that labor in the Lord is not in vain.',
        '1CO 15;1TH 4:13-18', links='empty-tomb dry-bones rev-judgment rev-new-creation')
    add('patient-hope', 'Hope without a counterfeit countdown', 'church',
        'Second Thessalonians warns against being quickly shaken by claims about the day of the Lord. Second Peter joins hope for new heavens and a new earth with a call to holy and patient living. The letters give urgency and endurance without handing readers a reliable date calculator.',
        '2TH 2:1-12;2PE 3', links='olivet-discourse resurrection-hope rev-millennium rev-new-creation', note='Interpretations of these passages vary. Their place in the atlas is thematic, not a claim that their images produce a settled modern timeline.')

    # Revelation starts with Jesus and ends with His invitation. Vision order
    # is deliberately not encoded as BCE/CE dates or modern identifications.
    add('rev-patmos', 'The revelation of Jesus Christ', 'revelation',
        'John, on Patmos, hears a voice and turns to see one like a son of man among seven lampstands. The figure identifies Himself as the living one who was dead and is alive forever. Revelation opens with Jesus, not a code to be solved apart from Him: the churches are addressed by the risen Lord who knows them.',
        'REV 1;DAN 7:9-14', 'patmos', 'jesus empty-tomb daniel-son-man rev-churches', kind='vision', note='The author calls himself John. Whether he is the same John associated with the Fourth Gospel is disputed; the atlas does not silently treat that identification as settled.')
    add('rev-churches', 'Seven churches, seven searching messages', 'revelation',
        'The risen Jesus addresses communities in seven cities of Roman Asia. He knows their work, suffering, compromise, love, and need for repentance. Each message asks hearers to listen to what the Spirit says. The book’s extraordinary visions begin with the practical question of how real communities remain faithful.',
        'REV 2;REV 3;REV 1:20', 'ephesus smyrna pergamum thyatira sardis philadelphia laodicea', 'rev-patmos rev-ephesus rev-smyrna rev-pergamum rev-thyatira rev-sardis rev-philadelphia rev-laodicea', kind='vision')
    church_rows = [
        ('ephesus', 'Ephesus · return to your first love', 'REV 2:1-7', 'The church’s work and endurance are recognized, but its abandoned first love cannot be excused by its other strengths. Jesus calls it to remember, repent, and do its first works. The promise to the conqueror reaches all the way back to the tree of life.', 'ephesus-word rev-river'),
        ('smyrna', 'Smyrna · faithful through suffering', 'REV 2:8-11', 'The one who died and lives again addresses a poor and afflicted community as rich. The message does not promise that suffering will disappear; it calls for faithfulness and promises the crown of life. The second death will not have the final word.', 'empty-tomb rev-judgment'),
        ('pergamum', 'Pergamum · witness amid compromise', 'REV 2:12-17', 'The community is praised for holding fast even when Antipas was killed, but challenged over teaching compared with Balaam’s stumbling block. Jesus promises hidden manna and a white stone with a new name. The precise social symbolism of the stone is debated; the invitation is to hear and remain faithful.', 'balaam exodus-manna'),
        ('thyatira', 'Thyatira · love, endurance & discernment', 'REV 2:18-29', 'Love, service, faith, and growing works are recognized, while a teacher called Jezebel is condemned for leading others astray. The name recalls an earlier biblical story rather than proving this is the ancient queen herself. The message joins discernment with a call to hold fast.', 'jezebel rev-rider'),
        ('sardis', 'Sardis · wake up', 'REV 3:1-6', 'A reputation for life conceals a community described as dead. The call is to wake up, strengthen what remains, remember what was received, and keep it. White garments and the book of life frame the promise: public reputation is not the measure of faithfulness.', 'rev-judgment'),
        ('philadelphia', 'Philadelphia · an open door', 'REV 3:7-13', 'The one holding the key of David speaks to a community with little power that has kept His word. An open door and a new name become images of belonging. The promise looks toward the city of God, the new Jerusalem coming down from heaven.', 'covenant-david rev-new-creation'),
        ('laodicea', 'Laodicea · the door and the shared meal', 'REV 3:14-22', 'A community confident in its wealth is confronted with its actual need. The vivid charge of lukewarmness leads to an invitation to repentance and fellowship. Jesus stands at the door and knocks; the promised meal is addressed here to a church being called back into communion.', 'last-supper rev-wedding'),
    ]
    for city, title, reference, summary, links in church_rows:
        add('rev-' + city, title, 'revelation', summary, reference, city,
            'rev-churches ' + links, kind='vision')
    add('rev-throne', 'A door opens into the throne room', 'revelation',
        'John sees a throne, a rainbow, elders, lamps, and living creatures whose worship never ceases. Echoes of Isaiah and Ezekiel place the scene within Scripture’s older visions of divine holiness. Before the book shows the powers that frighten the earth, it shows the reader the throne that is not empty.',
        'REV 4;ISA 6:1-8;EZK 1', links='isaiah ezekiel heavenly-court rev-lamb', kind='vision')
    add('rev-lamb', 'The Lion is a Lamb who was slain', 'revelation',
        'John hears of the Lion of Judah and the Root of David, but when he looks he sees a Lamb standing as though slain. The Lamb is worthy to open the scroll because He has redeemed people from every tribe, language, people, and nation. Revelation’s center of victory carries the marks of Jesus’ self-giving death.',
        'REV 5;GEN 49:9-10;ISA 11:1-10;JHN 1:29', links='jesus judah covenant-david cross-jesus rev-seals', kind='vision', note='The contrast between what John hears and what he sees is part of the text itself. The Lamb is not a separate rival to the Lion.')
    add('rev-seals', 'The seals and the four horsemen', 'revelation',
        'As the Lamb opens the seals, horses and riders bring images of conquest, war, scarcity, and death. The vision then hears the cry of the slain and shows a cosmic upheaval before the day of wrath. Zechariah’s horses provide an earlier visual vocabulary, though Revelation gives the imagery its own role.',
        'REV 6;ZEC 1:7-17;ZEC 6:1-8', links='rev-lamb zechariah-branch rev-multitude', kind='vision', note='Interpretations of the first rider and the sequence differ. No rider is assigned to a named modern country or event as a settled identification.')
    add('rev-multitude', 'A numbered people, an unnumbered multitude', 'revelation',
        'John hears the number of the sealed from Israel’s tribes, then sees a multitude no one can count from every nation. They stand before the throne and the Lamb, who shepherds them to springs of living water. Numbers, tribal names, and worldwide worship invite close reading rather than a quick census calculation.',
        'REV 7;EZK 9:1-6', links='twelve-tribes good-shepherd rev-lamb rev-river', kind='vision', note='Readers differ on how the 144,000 and the great multitude relate and whether the number is literal or symbolic. The text’s twelve-by-twelve-by-a-thousand pattern can be noticed without settling that debate.')
    add('rev-trumpets', 'Trumpets, plagues & a wounded creation', 'revelation',
        'Trumpet blasts bring images of fire, blood, darkened lights, locusts, and disaster. The Exodus plagues are part of the imagery’s scriptural background, while the fractions and repeated sequences give Revelation its own pattern. The visions confront idolatry and hardened refusal to turn, not just curiosity about catastrophes.',
        'REV 8;REV 9;EXO 7:14-25;EXO 10', links='passover rev-seals rev-scroll rev-bowls', kind='vision', note='The relationship among seals, trumpets, and bowls is debated: some read a sequence, others see overlapping or recapitulated perspectives. The atlas follows the book’s reading order only.')
    add('rev-scroll', 'Sweet in the mouth, bitter in the stomach', 'revelation',
        'A mighty angel holds a little open scroll. John is told to eat it; its sweetness becomes bitterness within him, and he must prophesy again. Ezekiel’s earlier call also involved eating a scroll. Receiving a prophetic word means taking it into one’s life, including its difficult burden.',
        'REV 10;EZK 2:8-10;EZK 3:1-11', links='ezekiel rev-trumpets rev-witnesses', kind='vision')
    add('rev-witnesses', 'Two witnesses, two olive trees', 'revelation',
        'Revelation describes two witnesses as olive trees and lampstands before the Lord. Their testimony, suffering, apparent defeat, and vindication use imagery recalling Zechariah, Moses, and Elijah. Their story asks what faithful witness looks like when violent power appears to have the last word.',
        'REV 11:1-14;ZEC 4;EXO 7:14-25;1KI 17:1', links='zechariah-branch moses elijah stephen rev-churches', kind='vision', note='Some readers identify two individual future witnesses; others understand a corporate or symbolic testimony. The text’s named images are distinguished from those competing identifications.')
    add('rev-woman-dragon', 'The woman, the child & the dragon', 'revelation',
        'A woman clothed with the sun, with the moon under her feet and twelve stars on her head, gives birth while a dragon waits to devour. The child is caught up to God and His throne. Revelation identifies the dragon as the ancient serpent, the devil and Satan; the accuser is overcome through the Lamb’s blood and faithful testimony.',
        'REV 12;GEN 3:14-15;GEN 37:9-11;PSA 2:7-9', links='eden jesus cross-jesus rev-lamb rev-beasts', kind='vision', note='The woman is read in relation to Israel, Mary, and the church in different traditions, sometimes in layered ways. Those readings are not flattened into a single uncontested identification.')
    add('rev-beasts', 'When power demands worship', 'revelation',
        'A beast rises from the sea with features recalling Daniel’s beasts. Another beast promotes its authority and directs worship toward it. The vision binds coercive power, deception, violence, and worship together. Its challenge is not merely to recognize a monster, but to discern what asks for the allegiance owed to God.',
        'REV 13;DAN 7', links='daniel-son-man furnace rev-woman-dragon rev-number rev-babylon', kind='vision', note='Roman imperial power is a major historical context in scholarship; Christian readings also differ over continuing and future fulfillment. No modern person or technology is identified as the beast by this atlas.')
    add('rev-number', 'The mark, the name & 666', 'revelation',
        'Revelation connects the beast’s mark with its name or number and with the pressure to participate in buying and selling. The reader is invited to calculate a number: 666 in this edition. Compare the scene with the Lamb’s followers bearing His name in the next chapter—the contest concerns worship, identity, and allegiance.',
        'REV 13:11-18;REV 14:1-5;REV 7:1-4', links='rev-beasts rev-lamb-zion rev-multitude', kind='vision', note='Ancient name-number calculation is a serious avenue of interpretation; Nero Caesar is one prominent historical proposal, not a settled identification imposed here. Some manuscripts read 616. The reading room displays its named edition, 666; current people, payment systems, and devices are not labeled as fulfillments.')
    add('rev-lamb-zion', 'A name, a song & an enduring people', 'revelation',
        'Against the beasts’ claims stands the Lamb on Mount Zion, with a people bearing His and His Father’s names. A new song, angelic announcements, and harvest imagery follow. The chapter calls for the endurance of the saints and contrasts faithfulness to the Lamb with worship of the beast.',
        'REV 14', links='rev-number rev-multitude rev-lamb rev-babylon', kind='vision', note='Zion appears within the vision; it is not turned into a mapped military assembly or an assigned future date.')
    add('rev-bowls', 'The song of Moses and the Lamb', 'revelation',
        'Those who overcome sing the song of Moses and the Lamb before the bowls are poured out. Plague imagery returns: sores, blood, darkness, and upheaval. The Exodus memory is explicit in the song, but Revelation places deliverance and judgment around the Lamb and the nations’ worship.',
        'REV 15;REV 16;EXO 15:1-18', links='sea-crossing rev-lamb rev-trumpets rev-armageddon', kind='vision')
    add('rev-armageddon', 'Armageddon: a name inside a vision', 'revelation',
        'Within the sixth bowl, deceptive spirits gather kings for battle, and the place is named in Hebrew as Armageddon. An interruption calls the reader to stay awake. The vision moves on to the seventh bowl and the downfall of Babylon; its purpose is not to provide a modern battlefield itinerary.',
        'REV 16:12-21;2KI 23:29-30;ZEC 12:10-11', links='megiddo-battle rev-bowls rev-babylon rev-rider', kind='vision', note='The name is often associated with Har-Megiddo, but its derivation and symbolic geography are debated. The historical Megiddo entry is a comparison, not proof that Revelation’s battle has a securely mapped location.')
    add('rev-babylon', 'Babylon falls: power, luxury & lament', 'revelation',
        'A richly adorned woman called Babylon is shown in relation to the beast, and a great city’s fall draws grief from kings, merchants, and seafarers. Revelation exposes a world of seduction, exploitation, and violence against witnesses. Jeremiah’s earlier judgment on Babylon supplies language for a vision reaching beyond the ancient city alone.',
        'REV 17;REV 18;JER 51', links='babel writing-wall rev-beasts rev-wedding', kind='vision', note='Many historical readings associate this Babylon with Rome, drawing on the book’s imperial imagery. Other traditions extend or locate its fulfillment differently. No pin equates the visionary city with a single settled modern target.')
    add('rev-wedding', 'The marriage supper of the Lamb', 'revelation',
        'After the lament over Babylon comes praise and an invitation to the marriage supper of the Lamb. Fine linen is explained as the righteous acts of the saints. An angel refuses John’s worship and directs him to God. The vision moves from the false city’s splendor toward a relationship of faithfulness and joy.',
        'REV 19:1-10;ISA 62:1-5', links='cana last-supper rev-babylon rev-new-creation', kind='vision')
    add('rev-rider', 'Faithful and True', 'revelation',
        'Heaven opens, and a rider on a white horse is called Faithful and True, the Word of God, King of kings and Lord of lords. The sword comes from His mouth. This is Revelation’s vision of judgment and victory through the one the book has already shown as the slain Lamb, not an invitation for readers to wage private holy war.',
        'REV 19:11-21;ISA 11:1-5;PSA 2', links='jesus john-prologue rev-lamb rev-armageddon rev-millennium', kind='vision')
    add('rev-millennium', 'A thousand years: read the vision carefully', 'revelation',
        'Revelation describes Satan bound, a thousand-year reign, a release, and the final defeat of evil. The passage has produced major Christian disagreements over how its sequence relates to Christ’s return and the present age. The shared horizon is that evil does not reign forever and the witness of those who belong to Jesus is not forgotten.',
        'REV 20:1-10', links='rev-rider patient-hope rev-judgment', kind='vision', note='Premillennial, amillennial, and postmillennial readings differ. This entry presents the chapter and names the disagreement; it does not assign the millennium a calendar start or declare one scheme proven.')
    add('rev-judgment', 'The books are opened', 'revelation',
        'Before the great white throne, the dead stand and books are opened, including the book of life. Death and Hades themselves are thrown into the lake of fire. Daniel’s opened books return in a vision of final accountability. The story is moving toward a world where death is no longer at home.',
        'REV 20:11-15;DAN 7:9-10;DAN 12:1-3', links='daniel-son-man jude-enoch resurrection-hope rev-new-creation', kind='vision')
    add('rev-new-creation', 'Behold, I make all things new', 'revelation',
        'A new heaven and a new earth appear, and the holy city comes down from God. The dwelling of God is with humanity; tears, death, mourning, crying, and pain pass away. The city has no temple because God and the Lamb are its temple, and the Lamb is its lamp. Scripture’s story of presence reaches a breathtaking homecoming.',
        'REV 21;ISA 65:17-25;EZK 37:26-28', links='creation eden tabernacle temple jesus rev-wedding rev-river', kind='vision')
    add('rev-river', 'The tree of life, for the healing of nations', 'revelation',
        'A river of the water of life flows from the throne of God and the Lamb. The tree of life bears fruit, and its leaves are for the healing of the nations. Genesis’s garden and Ezekiel’s river meet in a city without curse or night. The end does not forget the beginning: God’s servants see His face.',
        'REV 22:1-5;GEN 2:8-10;GEN 3:22-24;EZK 47:1-12', links='eden samaritan-woman rev-multitude rev-new-creation rev-come', kind='vision')
    add('rev-come', 'The Spirit and the bride say, “Come.”', 'revelation',
        'Jesus names Himself the Root and the Offspring of David, the bright morning star. The Spirit and the bride invite the thirsty to come and receive the water of life freely. The final response is not a solved timetable but a prayer: “Amen! Yes, come, Lord Jesus.” The book closes with His grace.',
        'REV 22:6-21', links='jesus covenant-david rev-river great-commission', kind='vision')

    people = [
        ('mary-jesus', 'Mary · Jesus’ mother', 'arrival', 'Mary receives Gabriel’s announcement, sings of God’s mercy, and keeps the unfolding story in her heart. The Gospels place her at Cana and at the cross; Acts names her among those praying with the disciples. Her story reaches from the birth of Jesus into the waiting church.', 'LUK 1:26-56;JHN 2:1-12;JHN 19:25-27;ACT 1:14', 'nazareth', 'annunciation mary-elizabeth jesus cana cross-jesus'),
        ('joseph-nazareth', 'Joseph · Mary’s husband', 'arrival', 'Matthew portrays Joseph receiving Mary, naming Jesus, protecting the family, and responding to guidance in dreams. Luke names him in the family’s early journeys. He is distinct from the Joseph of Genesis and from Joseph of Arimathea; Matthew’s genealogy identifies him as Mary’s husband.', 'MAT 1:16-25;MAT 2:13-23;LUK 2:41-52', 'nazareth', 'joseph-dream flight-egypt mary-jesus jesus zerubbabel'),
        ('elizabeth', 'Elizabeth', 'arrival', 'Elizabeth, wife of Zechariah and mother of John, receives a long-awaited child and welcomes Mary with blessing. Luke places her joy within the wider promise unfolding around Jesus. Her named relationship to Mary is kinship, not a precisely specified family tree.', 'LUK 1:5-25;LUK 1:39-45;LUK 1:57-66', '', 'john-birth mary-elizabeth zechariah-priest'),
        ('zechariah-priest', 'Zechariah · John’s father', 'arrival', 'A priest serving in the temple, Zechariah receives the announcement of John’s birth and responds with a question. His period of silence ends when he confirms the child’s name. His restored voice praises God’s redemption and names John’s work as preparing the Lord’s ways.', 'LUK 1:5-25;LUK 1:57-80', 'jerusalem', 'elizabeth john-birth john-baptist'),
        ('herod-great', 'Herod the Great', 'arrival', 'Matthew places the arrival of the magi and the threat against the child Jesus in the reign of Herod. The king’s fear of a rival contrasts with the visitors’ worship. This Herod is distinct from Herod Antipas, the later ruler connected with John the Baptist’s death and Jesus’ trial in Luke.', 'MAT 2', 'jerusalem', 'rome-herod magi flight-egypt herod-antipas'),
        ('herod-antipas', 'Herod Antipas', 'ministry', 'The Herod associated with John’s imprisonment and death is the tetrarch Antipas, not the Herod of Matthew’s infancy story. Mark describes the banquet at which John is killed; Luke places Jesus before this ruler during the final proceedings in Jerusalem.', 'MRK 6:14-29;LUK 3:1;LUK 23:6-12', '', 'herod-great john-baptist trial-jesus'),
        ('pontius-pilate', 'Pontius Pilate', 'passion', 'The Roman governor conducts proceedings against Jesus and authorizes His crucifixion. The Gospels describe questioning, political pressure, and a royal charge. Pilate’s official role belongs to the historical setting of Jesus’ death, distinct from the authority Jesus claims for His own kingdom.', 'LUK 3:1;JHN 18:28-40;JHN 19:1-22', 'jerusalem caesarea', 'rome-herod pilate-jesus cross-jesus'),
        ('peter', 'Simon Peter', 'ministry', 'Called from fishing into discipleship, Peter confesses Jesus as the Christ, misunderstands the way of the cross, denies Him, and receives a renewed commission. Acts follows his witness at Pentecost and his encounter with Cornelius. His courage and failure remain in the same story.', 'MRK 1:16-18;MAT 16:13-23;JHN 21:15-19;ACT 2', 'capernaum', 'disciples-called peter-confession peter-denial peter-restored cornelius'),
        ('andrew', 'Andrew', 'ministry', 'Andrew follows Jesus and brings his brother Simon to meet Him. John later shows him noticing the boy with loaves and fish and helping bring an approach from Greek visitors. His appearances often involve introducing someone else to Jesus.', 'JHN 1:35-42;JHN 6:8-9;JHN 12:20-22', 'galilee', 'peter disciples-called feeding-crowd'),
        ('john-apostle', 'John · son of Zebedee', 'ministry', 'John is called with his brother James and appears with Peter and James at moments such as the transfiguration. Acts places Peter and John together in witness. Later traditions about the Fourth Gospel and Revelation should be distinguished from what these passages themselves name.', 'MRK 1:19-20;MRK 9:2-8;ACT 3;ACT 4:13-22', 'galilee', 'james-zebedee disciples-called transfiguration peter'),
        ('james-zebedee', 'James · son of Zebedee', 'ministry', 'James is called with John from their father’s boat and is present at the transfiguration. Acts reports his execution under Herod Agrippa. He is not the James associated with leadership in the Jerusalem council; recurring names need distinct identities.', 'MRK 1:19-20;MRK 9:2-8;ACT 12:1-2', 'galilee jerusalem', 'john-apostle disciples-called transfiguration james-jerusalem'),
        ('thomas-apostle', 'Thomas', 'ministry', 'John preserves Thomas’s readiness to accompany Jesus toward danger, his question about the way, and his difficulty believing the resurrection report. His encounter with the risen Jesus leads to the confession “My Lord and my God.” Doubt is part of his story, not its final definition.', 'JHN 11:16;JHN 14:5-7;JHN 20:24-29', '', 'jesus thomas-risen'),
        ('mary-magdalene', 'Mary Magdalene', 'ministry', 'Luke names Mary among women who supported Jesus’ ministry; the Gospels remember her at the crucifixion, burial, and resurrection discovery. John gives her the announcement “I have seen the Lord.” The texts do not identify her as the unnamed sinful woman of Luke 7.', 'LUK 8:1-3;MRK 15:40-47;JHN 20:1-18', 'galilee jerusalem', 'jesus burial-jesus empty-tomb mary-risen'),
        ('paul', 'Paul · also called Saul', 'church', 'The persecutor who encounters Jesus becomes a witness among the nations. Acts narrates journeys, churches, disputes, imprisonment, and arrival in Rome; his letters speak into the lives of particular communities. Acts 13:9 says Saul was also called Paul, rather than describing a name change at his conversion.', 'ACT 9;ACT 13:9;GAL 1:11-24;ROM 1:1-7', 'tarsus', 'saul-damascus first-mission rome-witness letters-love'),
        ('barnabas', 'Barnabas · son of encouragement', 'church', 'Barnabas shares resources, vouches for Saul, recognizes grace at Antioch, and travels in mission. Acts also records a sharp disagreement between him and Paul over John Mark. Encouragement and real disagreement both belong to the story of the early church.', 'ACT 4:36-37;ACT 9:26-28;ACT 11:22-26;ACT 15:36-41', 'antioch salamis', 'paul shared-life antioch-church first-mission'),
        ('james-jerusalem', 'James · a leader in Jerusalem', 'church', 'James speaks in the Jerusalem council after Peter, Barnabas, and Paul. Galatians identifies James the Lord’s brother among the leaders Paul met. He is distinguished here from James son of Zebedee, whose death is reported earlier in Acts.', 'ACT 15:13-21;ACT 21:17-26;GAL 1:18-19', 'jerusalem', 'jerusalem-council james-zebedee paul'),
        ('priscilla-aquila', 'Priscilla & Aquila', 'church', 'This couple works with Paul, travels, opens a household to a church, and helps Apollos understand the way of God more accurately. Their story shows teaching and hospitality woven into ordinary work. Paul calls them fellow workers in Christ Jesus.', 'ACT 18;ROM 16:3-5', 'corinth ephesus rome', 'paul corinth-household shared-life'),
        ('timothy', 'Timothy', 'church', 'Acts introduces Timothy as a disciple with a Jewish believing mother and a Greek father. He joins Paul’s work; Paul speaks of him warmly in Philippians. Letters addressed to Timothy turn toward the care of teaching and communities, extending the story beyond travel into patient leadership.', 'ACT 16:1-5;PHP 2:19-24;2TI 1:3-7', 'lystra', 'paul care-communities letters-joy'),
    ]
    for id, title, era, summary, reference, loc, links in people:
        add(id, title, era, summary, reference, loc, links,
            kind='king' if id.startswith('herod-') or id == 'pontius-pilate' else 'person', primary=False)

    new_places = [
        ('susa', 'Susa', 48.25, 32.19, 'Persian royal city associated with Esther and with Nehemiah’s service at court.', False),
        ('nazareth', 'Nazareth', 35.30, 32.70, 'Galilean home of Jesus’ upbringing and setting of Luke’s synagogue scene.', False),
        ('galilee', 'Sea of Galilee', 35.59, 32.83, 'Regional lake marker for fishing, crossings, and Jesus’ Galilean ministry; not a precise location for every shoreline event.', True),
        ('capernaum', 'Capernaum', 35.58, 32.88, 'Village on the northern shore of the lake, repeatedly associated with Jesus’ teaching and healing.', False),
        ('cana', 'Cana (regional)', 35.30, 32.82, 'A regional Galilean marker. Several sites have been proposed for the Cana of John’s Gospel.', True),
        ('nain', 'Nain (traditional)', 35.35, 32.63, 'Traditionally identified with Nein in lower Galilee; the setting of the widow’s son in Luke 7.', True),
        ('sychar', 'Sychar / Jacob’s well region', 35.28, 32.21, 'Regional guide near Shechem for John 4. Identification of Sychar and the precise relationship among sites is debated.', True),
        ('caesarea-philippi', 'Caesarea Philippi', 35.69, 33.25, 'The northern district named in the accounts of Peter’s confession; distinct from the coastal Caesarea of Acts.', False),
        ('bethany', 'Bethany', 35.26, 31.77, 'Village east of Jerusalem associated with Martha, Mary, and Lazarus; distinct from the Bethany beyond the Jordan in John 1.', False),
        ('mount-olives', 'Mount of Olives', 35.25, 31.78, 'Ridge east of Jerusalem. Marker gives orientation, not a claim to locate every garden, teaching, or ascension scene precisely.', True),
        ('tyre', 'Tyre', 35.20, 33.27, 'Phoenician coastal city; the surrounding region appears in the encounter with the Syrophoenician woman.', False),
        ('joppa', 'Joppa', 34.75, 32.05, 'Coastal town where Acts places Peter’s stay with Simon the tanner and his vision.', False),
        ('caesarea', 'Caesarea Maritima', 34.90, 32.50, 'Roman coastal city associated with Cornelius and Paul’s custody. Not Caesarea Philippi.', False),
        ('antioch', 'Antioch in Syria', 36.16, 36.20, 'The sending church of Acts 13; distinct from Pisidian Antioch.', False),
        ('tarsus', 'Tarsus', 34.89, 36.92, 'Paul’s city of origin in Cilicia, identified in Acts 21:39 and 22:3.', False),
        ('salamis', 'Salamis, Cyprus', 33.90, 35.18, 'First Cypriot preaching stop named in Acts 13.', False),
        ('paphos', 'Paphos', 32.41, 34.76, 'Cypriot city associated with the encounter involving Sergius Paulus in Acts 13.', False),
        ('pisidian-antioch', 'Pisidian Antioch', 31.18, 38.31, 'City of southern Asia Minor where Acts 13 records Paul’s synagogue address. Not Syrian Antioch.', False),
        ('iconium', 'Iconium', 32.49, 37.87, 'A city on the Acts 13–14 mission sequence, near modern Konya.', False),
        ('lystra', 'Lystra', 32.37, 37.60, 'Associated with the healing in Acts 14 and Timothy’s background in Acts 16; approximate ancient-site marker.', True),
        ('derbe', 'Derbe (approximate)', 33.36, 37.35, 'A southern Asia Minor stop named in Acts 14 and 16; marker reflects an approximate site identification.', True),
        ('troas', 'Alexandria Troas', 26.16, 39.75, 'Aegean port associated with the Macedonian vision and later travel in Acts.', False),
        ('philippi', 'Philippi', 24.29, 41.01, 'Macedonian city associated with Lydia, the jailer, and the church addressed in Philippians.', False),
        ('athens', 'Athens', 23.73, 37.98, 'Greek city where Acts 17 places Paul’s marketplace conversations and Areopagus address.', False),
        ('corinth', 'Corinth', 22.88, 37.91, 'Greek city associated with Paul, Priscilla and Aquila, and the Corinthian correspondence.', False),
        ('ephesus', 'Ephesus', 27.34, 37.94, 'Roman Asian city prominent in Acts 19 and the first of Revelation’s seven messages.', False),
        ('smyrna', 'Smyrna', 27.14, 38.42, 'Coastal city, now İzmir, addressed in Revelation 2:8–11.', False),
        ('pergamum', 'Pergamum', 27.18, 39.13, 'City in western Asia Minor addressed in Revelation 2:12–17.', False),
        ('thyatira', 'Thyatira', 27.84, 38.92, 'Lydia’s city of origin in Acts 16 and one of Revelation’s seven named cities.', False),
        ('sardis', 'Sardis', 28.04, 38.49, 'Ancient Lydian center addressed in Revelation 3:1–6.', False),
        ('philadelphia', 'Philadelphia in Asia', 28.52, 38.35, 'The ancient Asian city addressed in Revelation 3:7–13, not a modern American city.', False),
        ('laodicea', 'Laodicea on the Lycus', 29.11, 37.84, 'City in the Lycus valley addressed in Revelation 3:14–22.', False),
        ('patmos', 'Patmos', 26.55, 37.31, 'Aegean island named by John as the setting of Revelation 1:9. Its visions are not geographic locations to plot.', False),
        ('crete', 'Crete', 25.0, 35.15, 'Regional island marker for the voyage in Acts 27; not an asserted reconstruction of the ship’s track.', True),
        ('malta', 'Malta', 14.45, 35.90, 'Island named in Acts 28 after the shipwreck. No specific landing cove is asserted here.', True),
        ('rome', 'Rome', 12.49, 41.89, 'Imperial capital and the final setting of Acts. This geographical pin is not a claim that every use of “Babylon” means this location.', False),
    ]
    places.extend(dict(zip(('id', 'name', 'lon', 'lat', 'description', 'uncertain'), row)) for row in new_places)

    families.append(dict(
        id='jesus-household', title='The promise leads to Jesus',
        description='A selected path through Matthew 1, not a complete genealogy. Long dashes omit generations. Mary is Jesus’ mother; Joseph’s distinct household/guardian line does not claim biological fatherhood. Luke 3 gives a different genealogy and is available for comparison.',
        nodes=[dict(id=id, x=x, y=y) for id, x, y in [('abraham', 360, 60), ('david', 360, 170), ('jehoiachin', 360, 280), ('zerubbabel', 360, 390), ('joseph-nazareth', 360, 500), ('mary-jesus', 650, 500), ('jesus', 650, 650)]],
        edges=[dict(source=a, target=b, kind=k) for a, b, k in [('abraham', 'david', 'descendant'), ('david', 'jehoiachin', 'descendant'), ('jehoiachin', 'zerubbabel', 'descendant'), ('zerubbabel', 'joseph-nazareth', 'descendant'), ('joseph-nazareth', 'mary-jesus', 'spouse'), ('mary-jesus', 'jesus', 'parent'), ('joseph-nazareth', 'jesus', 'guardian')]],
        refs=refs('MAT 1:1-25;LUK 3:23-38')))

    new_trails = [
        ('jesus-story', 'Walk with Jesus', 'From the Word made flesh to the risen Lord', 'star', 'jesus annunciation nativity baptism-jesus disciples-called nazareth-scroll samaritan-woman beatitudes feeding-crowd transfiguration lazarus-raised palm-entry last-supper cross-jesus empty-tomb emmaus peter-restored great-commission'),
        ('last-week', 'Love to the very end', 'The table, the garden, the cross & the empty tomb', 'temple', 'palm-entry bethany-anointing last-supper foot-washing gethsemane peter-denial trial-jesus pilate-jesus cross-jesus burial-jesus empty-tomb mary-risen peter-restored'),
        ('homecoming', 'The road home is not the end', 'Exile, return, expectation & the arrival of Jesus', 'city', 'jehoiachin-release daniel-exile dry-bones cyrus-return second-temple esther-courage nehemiah-walls ezra-word malachi-messenger waiting-messiah jesus'),
        ('lamb-thread', 'Follow the Lamb', 'From Passover to the center of Revelation', 'star', 'passover offering-isaac baptism-jesus last-supper cross-jesus empty-tomb rev-lamb rev-wedding rev-river'),
        ('ends-earth', 'Good news refuses to stay put', 'Jerusalem, an African reader & the road to Rome', 'branch', 'great-commission ascension pentecost philip-samaria ethiopian-official saul-damascus cornelius antioch-church first-mission jerusalem-council lydia-philippi athens paul-shipwreck rome-witness'),
        ('revelation-echoes', 'Revelation remembers', 'Trace the images back through Scripture', 'star', 'rev-patmos daniel-son-man rev-throne rev-lamb rev-seals rev-witnesses rev-woman-dragon rev-beasts rev-number rev-babylon rev-new-creation rev-river'),
        ('seven-churches', 'Seven letters from the risen Jesus', 'Open the messages. Find their cities.', 'city', 'rev-patmos rev-churches rev-ephesus rev-smyrna rev-pergamum rev-thyatira rev-sardis rev-philadelphia rev-laodicea'),
        ('creation-new', 'From a garden to a city of light', 'The whole story, with Jesus at the center', 'temple', 'creation eden abraham-call passover tabernacle covenant-david temple jerusalem-falls cyrus-return jesus cross-jesus empty-tomb pentecost rev-new-creation rev-river rev-come'),
        ('women-witness', 'The women who carry the good news', 'Courage, welcome, witness & an open door', 'branch', 'esther-courage mary-elizabeth annunciation samaritan-woman syrophoenician mary-magdalene mary-risen lydia-philippi priscilla-aquila'),
    ]
    trails.extend(dict(id=id, title=title, subtitle=subtitle, icon=icon, steps=steps.split()) for id, title, subtitle, icon, steps in new_trails)

    # These are labeled textual connections, not claims that every allusion
    # has the same status as a quotation or an identification in the text.
    def echo(id, label, relationship, explanation, reference):
        entry = next(e for e in entries if e['id'] == id)
        entry.setdefault('echoes', []).append(dict(label=label, relationship=relationship, explanation=explanation, refs=refs(reference)))

    echo('jesus', 'The promise to Abraham and David', 'Explicit genealogy', 'Matthew’s opening identifies Jesus through both names. Follow the earlier promises, then read how Matthew frames their continuation.', 'GEN 12:1-3;2SA 7:12-16;MAT 1:1')
    echo('john-prologue', 'Creation and dwelling', 'Shared language and imagery', '“In the beginning” recalls Genesis. God dwelling among His people also invites comparison with the tabernacle’s glory.', 'GEN 1:1-5;EXO 40:34-38;JHN 1:1-18')
    echo('annunciation', 'A throne and a kingdom without end', 'Promise recalled', 'Gabriel’s words about David’s throne connect Mary’s child with the promise spoken to David.', '2SA 7:12-16;LUK 1:30-33')
    echo('mary-elizabeth', 'Hannah and Mary sing', 'Thematic parallel', 'Compare the raising of the lowly and the reversal of ordinary power in these two songs. The parallel does not make their settings identical.', '1SA 2:1-10;LUK 1:46-55')
    echo('temptation-jesus', 'The wilderness answers', 'Explicit quotations', 'Jesus’ replies draw from Deuteronomy’s account of Israel learning faithfulness in the wilderness.', 'DEU 6:13-16;DEU 8:2-3;MAT 4:1-11')
    echo('nazareth-scroll', 'Good news to the poor', 'Explicit Scripture reading', 'Luke names Isaiah’s scroll. Read the original promise and Jesus’ announcement of its fulfillment together.', 'ISA 61:1-2;LUK 4:16-21')
    echo('nicodemus', 'The lifted serpent and the lifted Son', 'Explicit comparison by Jesus', 'John places Jesus’ comparison with Numbers inside the conversation about life and God’s love.', 'NUM 21:4-9;JHN 3:14-17')
    echo('transfiguration', 'Moses, Elijah, and the beloved Son', 'Named figures in the account', 'The figures are explicitly identified. Luke connects their conversation with Jesus’ coming departure at Jerusalem.', 'LUK 9:28-36;EXO 24:12-18;1KI 19:8-13')
    echo('cross-jesus', 'The psalm and the suffering servant', 'Quotation and thematic connection', 'The Gospel cry draws directly on Psalm 22. Isaiah 53 provides language that New Testament writers use when speaking of Jesus’ suffering.', 'PSA 22;ISA 53;MRK 15:24-39;ACT 8:30-35')
    echo('emmaus', 'The older story opened around Jesus', 'Explicit narrative claim', 'Luke describes Jesus interpreting Moses and the prophets but does not list every passage in the conversation. The atlas does not invent that list.', 'LUK 24:25-27;LUK 24:44-49')
    echo('pentecost', 'Many languages, one announcement', 'Thematic comparison', 'Babel and Pentecost both foreground language and scattered peoples. Acts explicitly quotes Joel; a “reversal of Babel” is a common theological comparison, not a phrase Acts itself uses.', 'GEN 11:1-9;JOL 2:28-32;ACT 2:1-21')
    echo('jude-enoch', 'Enoch named inside the New Testament', 'Explicit attribution', 'Jude names Enoch and cites the coming of the Lord with holy ones. Open the passages side by side in thought, preserving each edition’s wording.', 'JUD 1:14-15;ENO 1')
    echo('rev-patmos', 'The lampstands are explained', 'Identification in the text', 'Revelation 1:20 identifies the lampstands as churches and the stars as their angels. Start with what the book itself explains before adding a proposed decoding.', 'REV 1:12-20')
    echo('rev-throne', 'Holy, holy, holy—and living creatures', 'Shared vision imagery', 'Isaiah’s worship and Ezekiel’s living creatures are close scriptural neighbors of Revelation’s throne scene.', 'ISA 6:1-8;EZK 1:4-28;REV 4')
    echo('rev-lamb', 'Hear a Lion. See a Lamb.', 'Contrast within the vision', 'John hears the royal names, then sees the slain-yet-standing Lamb. Compare Judah’s lion and Jesse’s root without losing the startling turn in Revelation 5.', 'GEN 49:9-10;ISA 11:1-10;REV 5:5-10')
    echo('rev-seals', 'Horses before the horsemen', 'Shared prophetic imagery', 'Zechariah sees colored horses and chariots sent through the earth. Revelation reworks horse imagery in the opening of the seals; each vision still has its own meaning.', 'ZEC 1:7-17;ZEC 6:1-8;REV 6:1-8')
    echo('rev-multitude', 'A seal before judgment', 'Shared prophetic imagery', 'Compare Ezekiel’s marking of mourners with the sealing in Revelation. The Lamb’s care for the multitude is as central as the number John hears.', 'EZK 9:1-6;REV 7')
    echo('rev-trumpets', 'An Exodus vocabulary', 'Shared plague imagery', 'Water becoming blood, darkness, and locusts recall Egypt’s plagues. Similar imagery does not by itself fix a modern date for the vision.', 'EXO 7:14-25;EXO 10;REV 8;REV 9')
    echo('rev-scroll', 'The prophet eats a scroll', 'Shared commissioning image', 'Both Ezekiel and John receive the word through an enacted image of eating. Notice the sweetness and the differing emphasis on bitterness.', 'EZK 2:8-10;EZK 3:1-11;REV 10:8-11')
    echo('rev-witnesses', 'Olive trees and lampstands', 'Explicit image comparison', 'Revelation calls its witnesses olive trees and lampstands. Zechariah supplies an earlier scene of lamps, oil, and two anointed ones.', 'ZEC 4;REV 11:3-6')
    echo('rev-woman-dragon', 'Sun, moon, stars—and an ancient serpent', 'Shared images; one explicit identification', 'Joseph’s dream has sun, moon, and stars. Genesis has the serpent. Revelation itself identifies its dragon as the ancient serpent, devil, and Satan; the woman’s interpretation remains debated.', 'GEN 37:9-11;GEN 3:14-15;REV 12:1-9')
    echo('rev-beasts', 'Daniel’s beasts return in a composite', 'Shared symbolic vocabulary', 'Compare the leopard, bear, lion, horns, and blasphemous power. Daniel and Revelation do not use every detail in exactly the same way.', 'DAN 7:1-14;REV 13:1-10')
    echo('rev-number', 'Two kinds of belonging', 'Contrast within Revelation', 'The beast’s mark and number are followed by the Lamb’s people bearing His name and His Father’s name. Read the chapter boundary as a connection, not an interruption.', 'REV 13:16-18;REV 14:1-5;REV 22:3-4')
    echo('rev-bowls', 'Moses and the Lamb, together', 'Explicitly named song', 'Revelation names the song of Moses and the Lamb. Exodus’s deliverance song provides a revealing comparison before the bowls.', 'EXO 15:1-18;REV 15:1-4;REV 16')
    echo('rev-babylon', 'Come out of her, My people', 'Prophetic language reused', 'Jeremiah calls people out of historical Babylon. Revelation uses that language for its visionary city, keeping the question of allegiance in view.', 'JER 51:6-9;JER 51:45;REV 18:1-8')
    echo('rev-new-creation', 'God’s dwelling with humanity', 'Promise and shared language', 'Compare the covenant dwelling in Ezekiel, Isaiah’s new creation, and the voice from Revelation’s throne. The Lamb—not a building—is the city’s temple and light.', 'EZK 37:26-28;ISA 65:17-25;REV 21')
    echo('rev-river', 'The garden and the river return', 'Shared creation imagery', 'Genesis gives a garden, river, and tree of life; Ezekiel gives healing water and fruitful trees. Revelation brings the river and tree into the city of God and the Lamb.', 'GEN 2:8-10;GEN 3:22-24;EZK 47:1-12;REV 22:1-5')
