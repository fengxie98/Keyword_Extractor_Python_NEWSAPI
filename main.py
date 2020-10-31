import spacy
from newsapi.newsapi_client import NewsApiClient
import en_core_web_lg

nlp = en_core_web_lg.load()
newsapi = NewsApiClient(api_key='9136c62f61b14708acdd3a21dc7e6546')


# articles = newsapi.get_everything(q='coronavirus', language='en', from_param='2020-10-01', to='2020-10-30', sort_by='relevancy', page=5)

def getSomething(x):
    temp = newsapi.get_everything(q='coronavirus', language='en',
                                  from_param='2020-10-20', to='2020-10-30',
                                  sort_by='relevancy', page=x)
    return temp


articles = list(map(getSomething, range(1, 6)))
print(articles)

import pandas as pd

dados = []

for i, article in enumerate(articles):
    for x in article['articles']:
        title = x['title']
        description = x['description']
        content = x['content']
        dados.append({'title': title, 'desc': description, 'content': content})
df = pd.DataFrame(dados)
df = df.dropna()
df.head()

from collections import Counter
from string import punctuation

results = []


def get_keywords_eng(text):
    result = []
    pos_tag = ['PROPN', 'VERB', 'NOUN']
    doc = nlp(text.lower())
    for token in doc:
        if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            result.append(token.text)
    print(result)
    return result


for content in df.content.values:
    results.append([('#' + x[0]) for x in Counter(get_keywords_eng(content)).most_common(5)])

df['keywords'] = results

from wordcloud import WordCloud
import matplotlib.pyplot as plt

text = str(results)

wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
