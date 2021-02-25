"""
Generates raw.txt, which is all 10983  lines of Petrarch's canzionare.
Code modified from CloudML poetry, https://cloud.google.com/blog/products/gcp/cloud-poetry-training-and-hyperparameter-tuning-custom-text-models-on-cloud-ml-engine

Book used:
'The Sonnets, Triumphs, and Other Poems of Petrarch by Francesco Petrarca'
- gutenberg book link: https://www.gutenberg.org/files/17650/17650-h/17650-h.htm

Requires:
- gutenberg (installation instructions: https://pypi.org/project/Gutenberg/)

"""
#gutenberg is used to fetch book txt files, so long as we give it the book ID
#we will, in addition to that, feed in the # of lines we want to skip (think of it like skipping the first 10 pages),
#and give it a personal name

from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
import re

books = [
#   BookID, skip N lines
#   (26715, 1000, 'Victorian songs'),
#   (30235, 580, 'Baldwin collection'),
#   (35402, 710, 'Swinburne collection'),
#   (574, 15, 'Blake'),
#   (1304, 172, 'Bulchevys collection'),
#   (19221, 223, 'Palgrave-Pearse collection'),
#   (15553, 522, 'Knowles collection') ,
    (17650, 6605, 'The Sonnets, Triumphs, and Other Poems of Petrarch by Francesco Petrarca')
#                                    Link: https://www.gutenberg.org/ebooks/17650
#                                    6605 is the # of lines that we skip to get
#                                    to the poems.
]


#Save as raw.txt file

#with open('data/poetry/raw.txt', 'w') as ofp:
with open('your-file-path/raw.txt', 'w') as ofp:
  lineno = 0
  for (id_nr, toskip, title) in books:
    startline = lineno
    text = strip_headers(load_etext(id_nr, mirror='http://mirrors.xmission.com/gutenberg/')).strip()
    lines = text.split('\n')[toskip:]
    for line in lines:
      if (len(line) > 0
          and line.upper() != line
          and not re.match('.*[0-9]+.*', line)
          and len(line) < 50
         ): #skip Titles
        cleaned = re.sub('[^a-z\'\-]+', ' ', line.strip().lower()) #all lowercase, only letters
        ofp.write(cleaned)
        ofp.write('\n')
        lineno = lineno + 1 #next line
      else:
        ofp.write('\n')
    print('Wrote lines {} to {} from {}'.format(startline, lineno, title))
