from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
import string
from langid.langid import LanguageIdentifier, model
stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()

language_identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
def clean(doc):
    classification = language_identifier.classify(doc)
    if classification[0] == 'en':
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        three_char = " ".join(word for word in normalized.split() if len(word) > 3)
        url_less = " ".join(non_url for non_url in three_char.split() if non_url[:4] != "http")
        tagged_sentence = nltk.pos_tag(url_less.split())
        edited_sentence = " ".join(word for word, tag in tagged_sentence if tag[:2] == 'NN' or tag[:2] == 'JJ')
        return edited_sentence
    else:
        return ""

doc_clean1 = [clean(doc).split() for doc in tweets_list2]
doc_clean = [l for l in doc_clean1 if l != []]
# Importing Gensim
import gensim
from gensim import corpora

# Creating the term dictionary of our courpus, where every unique term is assigned an index. 
dictionary = corpora.Dictionary(doc_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Training LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=4, id2word = dictionary, passes=250)

print(ldamodel.print_topics(num_topics=10, num_words=10))

"""
refer to documentation for parameter tuning:
    https://radimrehurek.com/gensim/models/ldamodel.html
"""

ts = []
for d in doc_clean:
    bow = dictionary.doc2bow(d)
    t = ldamodel.get_document_topics(bow, minimum_probability = 0.6)
    ts.append(t)