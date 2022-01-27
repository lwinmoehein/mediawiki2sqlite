import re


# accept sound section and convert it to list string
def modify_sound(section):
    if len(section) == 0:
        return ""

    sound_string_pattern = re.compile(r'\*\s\{{2}.+\}{2}')
    sound_matches = sound_string_pattern.finditer(section)

    modified_sounds = ""
    for lineMatch in sound_matches:
        # get the line
        line = section[lineMatch.start():lineMatch.end()]

        # a section
        modified_a_string = "( "
        a_pattern = re.compile(r'\{{2}a\|(.+?)\}{2}')
        a_matches = a_pattern.finditer(line)
        for a in a_matches:
            modified_a_string += a.group(1) + ","
        modified_a_string = modified_a_string.rstrip(',')
        modified_a_string = (modified_a_string + " ),").replace("(  ),", "").strip(',')
        # end a section

        # accents
        pattern = re.compile(r"\{{2}(rhymes.+|IPA.+|enPR.+?)\}{2}")
        matches = pattern.finditer(line)
        child_sound_string = ""
        for match in matches:
            line = match.group(1)
            line = line.replace("|", ": ")
            line = re.sub(r'(\||:\s)lang=.{2}', "", line)
            if modified_a_string != "":
                child_sound_string += ("** " + line + "\n")
            else:
                child_sound_string += ("* " + line)
        # end accents

        # final modification
        if modified_a_string != "":
            modified_sounds += "* " + modified_a_string + "\n" + child_sound_string + "\n"
        else:
            modified_sounds += child_sound_string + "\n"
    return modified_sounds


# extract sound section as a string
def extract_sound(string):
    if string is None:
        return ExtractedSound(None, None, None)
    pattern = re.compile(r'\n===အသံထွက်===.*\n*((?:\n.*)+?)(?=\n===)')
    sound_pattern = pattern.search(string)
    if sound_pattern is not None:
        modified_sound_string = modify_sound(sound_pattern.group(0))
        return ExtractedSound(sound_pattern.start(), sound_pattern.end(), modified_sound_string)

    return ExtractedSound(None, None, None)


class ExtractedSound:
    def __init__(self, start, end, sound_string):
        self.start = start
        self.end = end
        self.sound_string = sound_string
