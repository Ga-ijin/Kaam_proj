# -*- coding: utf-8 -*-
"""
Created on Thu May 13 16:22:49 2021

@author: Ga
"""
# In[0]: libraries
import pandas as pd
from sqlalchemy import create_engine
import yaml
import os

# In[1]: textmining libraries
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from PIL import Image
import numpy as np

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from collections import Counter
import seaborn as sns

import string
import re

# In[2] : db
dir = r'C:\Users\Ga\Documents\GitHub\Kaam_proj'
os.chdir(dir)

login = yaml.safe_load(open('logins.yml', 'r'))
user = login['postgres']
password = user['password']
db = user['db']
host="localhost"
port="5432"

# engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
engine = create_engine('postgresql://postgres:8774755@localhost:5432/kaam_db2')
dbConnection = engine.connect()

sql = """select script from episode;"""
df = pd.read_sql_query(sql, engine)

# In[3]: Traitement du texte brut
text = ""
for script in df.script : 
    text+=script
    text+=" "

def onlyUpper(word):
    for c in word:
        if not c.isupper():
            return False
    return True

s = text
listReplace = ["’", '—', '–', '«', '»']
for replace in listReplace:
    s = s.replace(replace, " ")
# s = s.replace("’", " ")
for char in string.punctuation:
    s = s.replace(char, ' ')

words = s.split()
good_words = []

for w in words:
    if not onlyUpper(w):
        good_words.append(w)

text2 = ""
for w in good_words:
    text2 = text2 + w + " "

text3 = re.sub(r'[0-9]', '', text2)
text3 = text3.lower()

# In[4]: Stopwords

stop_words = set(stopwords.words('french'))
with open("rawData/stopwords.txt", 'r', encoding = 'utf-8') as stopwordstxt:
    word = stopwordstxt.read().replace('\n', ' ').split(" ")
    stop_words.update(word)
addingStopWordsList = ["faire", "faut", "oui", "dit","puis", "sais"]
for mot in addingStopWordsList:
    stop_words.add(mot)

# Liste qui sépare chacun des mots de la string text et exclue les stopwords

text_tokenized = word_tokenize(text3, language='french')

tokens = []
for mot in text_tokenized:
    if mot not in stop_words:
        tokens.append(mot)
        
# In[5] : WordCloud
# Création du nuage de mots suivant une image
    
def plot_word_cloud(txt, masque, background_color = "white") :
    # Définir un masque
    # mask_coloring = np.array(Image.open(str(masque)))
    # from wordcloud import ImageColorGenerator
    mask = np.array(Image.open(masque))
    # img_color = ImageColorGenerator(mask)
    
    # Définir le calque du nuage des mots
    wc = WordCloud(mask = mask,random_state=50, collocations=False,
              width=400, height=200, margin=2,
              ranks_only=None, prefer_horizontal=0.9,
              scale=1, color_func=None,
              max_words=1000, 
              min_font_size=4, stopwords=stop_words,
              background_color='white', contour_width=1, contour_color='grey',
              max_font_size=90, font_step=1, mode='RGB',
              relative_scaling=0.5, regexp=None, colormap=None, normalize_plurals=True)
    
    plt.figure(figsize= (15,10)) # Initialisation d'une figure
    wc.generate(txt)           # "Calcul" du wordcloud
    plt.imshow(wc, interpolation = 'bilinear') # Affichage
    plt.axis('off')
    plt.show()
test = plot_word_cloud(text3, 'rawData/knight_mask.png')

# In[6]: Bar graphs des 15 mots les plus utilisés
dico = Counter(tokens)
dico.most_common(15)

mots = [m[0] for m in dico.most_common(15)]
freq = [m[1] for m in dico.most_common(15)]

plt.figure(figsize= (15,10))
sns.barplot(x=mots, y=freq)
plt.title('15 mots les plus fréquemment employés')
plt.show()