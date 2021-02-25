"""
Requires:
 - nltk, pandas, numpy, gensim
 - raw.txt, which is gotten from step1
 Outputs:
 - PCA-checkpoint.tsv, Metadata-change-file-extension-to-tsv.csv
"""

class bcolors:
    OKBLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    OKCYAN = '\033[96m'


print(bcolors.OKBLUE + "Starting program" + bcolors.ENDC)

import pandas as pd
import numpy as np

from gensim.models import Word2Vec
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')



#Read in text as list of lists, each line is considered a document
df = pd.read_csv('data/poetry/raw.txt')
df = df.values.tolist()
print('Snippet of df: ', df[0:2])

# =========== DATA PRE-PROCESSING ============ #

#make corpus a list like ['line1', 'line2', ... 'line_n']
corpus = [','.join((x)) for x in df]
print('This is a snippet of our corpus\n',corpus[0:5])

#make stop words
english_stops = set(stopwords.words('english')).union(set(['to', 'those', 'or', 'all', 'che', 'mi', 'thy', 'thee', 'yet', 'thou', 'thus', 'one', 'many', 'whose', 'every', 'shall', 'e', 'oh', 'could', 'shall', 'would', 'i']))

#take ['line1'] and make it [ ['word1_line1', 'word2line1', ... ], ['word1_line2', 'word2_line2, ...] ]
#only keep words (just to remove '--' punctuation)
tokenizer = RegexpTokenizer("[\w']+")
tokenized = [tokenizer.tokenize(x) for x in corpus]

#apply stop words to each word, this is to remove the fluff of "thou" or other stuff which is not helpful

for line in range(len(tokenized)):
  tokenized[line] = [word for word in tokenized[line] if word not in english_stops]

print('This is a snippet of our tokenized corpus\n',tokenized[0:5])

model = Word2Vec(tokenized)

words=list(model.wv.vocab)
print('Here is a snippet of our words, which we can call our vocabulary in terms of word2vec',words[0:5])

#store all the word vectors in the data frame with 100 dimensions and use this data frame for PCA
X=model[model.wv.vocab]
df=pd.DataFrame(X, index=model.wv.vocab)
df.shape
df.head()

# ============ PCA CHECKPOINT ============== #

#Computing the correlation matrix
X_corr=df.corr()

#Computing eigen values and eigen vectors
values,vectors=np.linalg.eig(X_corr)

#Sorting the eigen vectors coresponding to eigen values in descending order
args = (-values).argsort()
values = vectors[args]
vectors = vectors[:, args]

#Taking first 3 components which explain maximum variance for projecting
new_vectors=vectors[:,:3]

#Projecting it onto new dimesion with 3 axis
neww_X=np.dot(X,new_vectors)

#Save PCA

np.savetxt("data/poetry/PCA-checkpoint.tsv", neww_X, delimiter='\t')
print(bcolors.OKBLUE + 'Saved PCA-checkpoint.tsv' + bcolors.ENDC)

# ============ METADATA ============== #
#create a list of each word
y = []
for x in range(len(tokenized)):
  for word in tokenized[x]:
    y.append(word)
print('There are',len(y),'words in our corpus.')

#calculate a frequency distribution
frequency_dict = nltk.FreqDist(y)
frequency_dict = dict(frequency_dict)

#Sanity check: we should see that our word count of y is decreased in frequency_dict.
def total_keys(test_dict):
    return (0 if not isinstance(test_dict, dict)
    else len(test_dict) + sum(total_keys(val) for val in test_dict.values()))

print('There are',total_keys(frequency_dict),'unique words in our frequency dictionary')

#Store our word / count in an array.
end_arr = []
for key, value in frequency_dict.items():
  end_arr.append([key, frequency_dict[key]])

#Put that array into a dictionary
print('\n\nHere is that word/count array as a DataFrame:')
end_arr = pd.DataFrame(end_arr, columns=['word', 'count'])
print(end_arr.head())

print(bcolors.OKBLUE + 'Saved Metadata-change-file-extension-to-tsv.csv' + bcolors.ENDC)
print(bcolors.BOLD + bcolors.UNDERLINE + bcolors.OKBLUE + 'Please dont forget to change Metadata-change-file-extension-to-tsv.csv to Metadata-change-file-extension-to-tsv.tsv' + bcolors.ENDC)
x = "\t"
end_arr.to_csv('data/poetry/Metadata-change-file-extension-to-tsv.csv', sep='\t', index=False)
