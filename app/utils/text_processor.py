import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import string

# Download required NLTK data
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")

class TextProcessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.exclude = set(string.punctuation)

    def filter_keywords(self, doc):
        doc = str(doc).lower()
        stop_free = " ".join([i for i in doc.split() if i not in self.stop_words])
        punc_free = "".join(ch for ch in stop_free if ch not in self.exclude)
        word_tokens = word_tokenize(punc_free)
        filtered_sentence = [(self.lemmatizer.lemmatize(w, "v")) for w in word_tokens]
        return filtered_sentence