import re


# remove translation section
def getTranslationSection(string):
    if len(string) == 0:
        return ""
    pattern = re.compile(r'\n==အသံထွက်==.*\n*((?:\n.*)+?)(?=\n==)')
    soundSection = pattern.search(string)
    if soundSection == None:
        return None
    return soundSection
