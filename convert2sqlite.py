import xml.etree.ElementTree as ET
import json
import pypandoc
import re
import sqlite3
import pycountry
from extractsounds import extract_sound, ExtractedSound
from extractlanguages import extract_lang, ExtractedLang

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
    extracted_lang = extract_lang(revision)
    if extracted_lang is not None and extracted_lang.lang_string is not None:
        revision = revision[:extracted_lang.start] + extracted_lang.lang_string + revision[extracted_lang.end:]
    extracted_sound = extract_sound(revision)
    if extracted_sound is not None and extracted_sound.sound_string is not None:
        revision = revision[:extracted_sound.start] + "\n===အသံထွက်===\n" + extracted_sound.sound_string + revision[
                                                                                                          extracted_sound.end:]
    # add to db
    cur.execute("INSERT INTO words (id,title,meaning) VALUES (?,?,?)", (id, title, revision))
    i += 1

# db save and close
con.commit()
con.close()
