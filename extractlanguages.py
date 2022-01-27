from iso639 import Lang
import re


# extract sound languages as a string
def extract_lang(expected_lang_string):
    if expected_lang_string is None:
        return ExtractedLang(None, None, None)
    pattern = re.compile(r'\n====ဆင့်ပွားအသုံးများ====(.|\n)+\}{2}')
    lang_section = pattern.search(expected_lang_string)
    if lang_section is not None:
        modified_string = modify_lang(lang_section.group(0))
        return ExtractedLang(lang_section.start(), lang_section.end(), modified_string)

    return ExtractedLang(None, None, None)


# modify and return lang changed section
def modify_lang(lang_string):
    # lang header
    modified_lang_string = "\n====ဆင့်ပွားအသုံးများ====\n"
    removed_lang_string = re.sub(r'(desctree\|*)|(desc\|*)|(\|*bor=1\|*)|(\{{2}l\|.+\}{2})', "", lang_string)
    rename_lang_pattern = re.compile(r'\{{2}([a-z]{2,3})\|(.+)\}{2}')
    langs = rename_lang_pattern.finditer(removed_lang_string)
    for lan in langs:
        try:
            if lan.group(1) == 'ux':
                continue
            modified_lang_string += "* ''" + Lang(lan.group(1)).name + "'' : " + lan.group(2) + "\n"
        except:
            print("Lang Exception:" + lan.group(1) + ":" + lan.group(0))
    return modified_lang_string


class ExtractedLang:
    def __init__(self, start, end, lang_string):
        self.start = start
        self.end = end
        self.lang_string = lang_string
