import re

cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

def clean_html(raw_html):
  return re.sub(cleaner, '', raw_html)