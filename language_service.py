import sys
sys.path.insert(0, './strings')
import json
import os
import strings_en
import strings_jp


strings = {}
strings["en"] = strings_en.dictionary
strings["jp"] = strings_jp.dictionary
        
def get_string(language, string_name):
    if language in strings:
        return strings[language][string_name]
    return strings["en"][string_name]
