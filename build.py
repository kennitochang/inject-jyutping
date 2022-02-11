import json
import os

# Library
os.system('wget -nc -O lib/browser-polyfill.js https://unpkg.com/webextension-polyfill@0.8.0/dist/browser-polyfill.js')

# Preprocess
os.system('wget -nc https://raw.githubusercontent.com/CanCLID/ToJyutping/74f8e9c/preprocess.py')
os.system("sed -i '' 's/src\/ToJyutping\/jyut6ping3.simple.dict.yaml/jyut6ping3.simple.dict.yaml/' preprocess.py")
os.system('python3 preprocess.py')

l = []

MARKS = {
"a": [None, "\\u0101", "\\u00E1", "a", "\\u00E0", "\\u01CE", "\\u1EA1"],
"e": [None, "\\u0113", "\\u00E9", "e", "\\u00E8", "\\u011B", "\\u1EB9"],
"i": [None, "\\u012B", "\\u00ED", "i", "\\u00EC", "\\u01D0", "\\u1ECB"],
"o": [None, "\\u014D", "\\u00F3", "o", "\\u00F2", "\\u01D2", "\\u1ECD"],
"u": [None, "\\u016B", "\\u00FA", "u", "\\u00F9", "\\u01D4", "\\u1EE5"],
"n": [None, "n\\u0304","\\u0144", "n", "\\u01F9", "\\u0148", "\\u1E47"],
"m": [None, "m\\u0304","\\u1E3F", "m", "m\\u0300","m\\u030C","\\u1E43"]}

def convert_to_tonemarks(s):
  if s == "":
    return ""
  y = []
  for x in s.split(" "):
    if x[:-1] in ["m", "ng"]:
      y += [MARKS[x[0]][int(x[-1])] + x[1:-1]]
      continue 
    
    for i in range(len(x)):
      if x[i] in "aeiou":
        y += [x[:i] + MARKS[x[i]][int(x[-1])] + x[i+1:-1]]
        break
  return " ".join(y)

with open('jyut6ping3.simple.dict.yaml') as f:
    for line in f:
        k, v = line.rstrip('\n').split('\t')
        v = convert_to_tonemarks(v)
        print(v)
        l.append((k, v))

# *.json.txt: See mozilla/addons-linter#1700
with open('background_scripts/dictionary.json.txt', 'w') as f:
    f.write(json.dumps(l, ensure_ascii=False).replace('], [', '],\n['))
    f.write('\n')  # Add line break at the end of file
