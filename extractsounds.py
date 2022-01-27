import re

#accept sound section and convert it to list string
def modifySoundSection(section):
  if len(section)==0:
    return ""

  
  soundLinesPattern = re.compile(r'\*\s\{{2}.+\}{2}')
  lineMatches = soundLinesPattern.finditer(section)

  finalSounds = ""
  for lineMatch in lineMatches:   
    #get the line
    line = section[lineMatch.start():lineMatch.end()]
    
    #a section
    modifiedAs = "( "
    aPattern = re.compile(r'\{{2}a\|(.+?)\}{2}')
    aMatches = aPattern.finditer(line)
    for a in aMatches:
       modifiedAs+=a.group(1)+","
    modifiedAs=modifiedAs.rstrip(',')
    modifiedAs=(modifiedAs+" ),").replace("(  ),", "").strip(',')
    #end a section
    
    #accents
    pattern = re.compile(r"\{{2}(rhymes.+|IPA.+|enPR.+?)\}{2}")
    matches = pattern.finditer(line)
    finalLine = ""
    for match in matches:
      line = match.group(1)
      line = line.replace("|", ": ")
      line = re.sub(r'(\||:\s)lang=.{2}', "", line)
      if(modifiedAs!=""):
        finalLine+=("** "+line+"\n")
      else:
        finalLine+=("* "+line)
    #end accents
    
    #final modificatioin
    if(modifiedAs!=""):
      finalSounds+="* "+modifiedAs+"\n"+finalLine+"\n"
    else:
      finalSounds+=finalLine+"\n"
  return finalSounds


#extract sound section as a string
def extractSoundSection(string):
    if string==None:
      return ExtractedSound(None,None,None)
    pattern = re.compile(r'\n===အသံထွက်===.*\n*((?:\n.*)+?)(?=\n===)')
    soundSection = pattern.search(string)
    if soundSection!=None:
      modifiedString = modifySoundSection(soundSection.group(0))
      return ExtractedSound(soundSection.start(), soundSection.end(), modifiedString)

    return ExtractedSound(None, None, None)
class ExtractedSound:
  def __init__(self,start,end,extractedSection):
    self.start = start
    self.end = end
    self.extractedSection = extractedSection