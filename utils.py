# Standard Library Imports
import re

def remove_surrounding(text: str) -> str:
    return re.sub(r'\[[^\]]*\]|\{[^}]*\}|\([^)]*\)','',text)

def remove_new_line(text: str) -> str:
    return re.sub(r'[\n]','',text)

def remove_IBGE(text: str) -> str:
    return re.sub(r'IBGE.*','',text)

def remove_unicode(text:str) -> str:
    return text.replace("\xa0","").replace("•","");

def transform(text:str)-> str:
    return remove_IBGE(remove_unicode(remove_new_line(remove_surrounding(text.replace("Lista",""))))).lstrip()
