import xml.etree.ElementTree as ET
import json
import pypandoc
import re
import sqlite3
import pycountry
from extractsounds import extractSoundSection, ExtractedSound
from extractlanguages import extractLangSection, ExtractedLang

con = sqlite3.connect('myantionary.db')

cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE words
               (id text, title text,meaning text)''')

# initialize xml root
tree = ET.parse('data.xml')
root = tree.getroot()

i = 0
for page in root:

    # if (i > 200):
    #     break
    id = page.find('id').text
    title = page.find('title').text
    # print(text)
    revision = page.find('revision/text').text
    extractedLang = extractLangSection(revision)
    if (extractedLang != None and  extractedLang.extractedSection!=None):
        revision = revision[:extractedLang.start] + extractedLang.extractedSection + revision[extractedLang.end:]
    extractedSound = extractSoundSection(revision)
    if (extractedSound!= None and  extractedSound.extractedSection!=None):
        revision = revision[:extractedSound.start] + "\n===အသံထွက်===\n" + extractedSound.extractedSection + revision[
                                                                                                            extractedSound.end:]
        # add to db
    cur.execute("INSERT INTO words (id,title,meaning) VALUES (?,?,?)", (id, title, revision))
    i += 1

# db save and close
con.commit()
con.close()
