import json
import re
import unicodedata as ud

def js_r(filename):
   with open(filename) as f_in:
       return(json.load(f_in))

def normalize_name(s: str):
    # Remove accents
    s = ''.join(c for c in ud.normalize('NFD', s.lower()) if ud.category(c) != 'Mn')
    s = re.sub(r',|\.|:|\(|\)|’|“|”|&', '', s)
    s = re.sub(r'\s+', '-', s)
    return s.replace('#', 'hash').replace('*', 'asterisk')

# def encode(s: str) -> str:
#     """
#     Turns all astral characters (code points U+10000 and bigger)
#     in string ``s`` into surrogate pairs:
#     a high surrogate (code points U+D800 to U+DBFF)
#     followed by a low surrogate (code points U+DC00 to U+DFFF).
#     """
#     if not isinstance(s, str):
#         raise TypeError('Not a string: {!r}'.format(s))

#     encoded_s = []

#     for ch in s:
#         if ord(ch) < 0x10000:
#             encoded_s.append(ch)
#         else:
#             high_surrogate = ((ord(ch) - 0x10000) // 0x400) + 0xD800
#             low_surrogate = ((ord(ch) - 0x10000) & (0x400 - 1)) + 0xDC00
#             encoded_s.append(chr(high_surrogate) + chr(low_surrogate))

#     return ''.join(encoded_s)

emoji_map = js_r('emoji.json')
   
with open('Engrams and Moonwalks.tex', 'r') as file:
  data = file.read()

# TODO process in order of most pairs to least pairs so skintone processes right.
for emoji_data in emoji_map:
    emoji_name = normalize_name(emoji_data["description"])
    emoji = emoji_data["emoji"]
    unicode=json.dumps(emoji).replace("\"", "")
    # print(json.dumps(emoji), normalize_name(emoji_name))
    splitunicode=unicode.split("\\u")
    to_replace=f"[{splitunicode[1]}?]"
    for idx,d in enumerate(splitunicode):
      if idx>1:
        to_replace += f"[{d}?]"
    
    data=data.replace(to_replace.upper(), f"\emoji{{{emoji_name}}}", )
    
    print(to_replace.upper(), f"\emoji{{{emoji_name}}}")

with open('Engrams and Moonwalks.tex','w') as file:
  file.write(data)