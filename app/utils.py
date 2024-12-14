import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import string
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")

# Initialize global variables
lem = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
exclude = set(string.punctuation)

def filter_keywords(doc):
    doc = str(doc).lower()
    stop_free = " ".join([i for i in doc.split() if i not in stop_words])
    punc_free = "".join(ch for ch in stop_free if ch not in exclude)
    word_tokens = word_tokenize(punc_free)
    filtered_sentence = [(lem.lemmatize(w, "v")) for w in word_tokens]
    return filtered_sentence

def prepare_data(df):
    # Clean product category tree
    df['product_category_tree'] = df['product_category_tree'].map(lambda x: x.strip('[]'))
    df['product_category_tree'] = df['product_category_tree'].map(lambda x: x.strip('"'))
    df['product_category_tree'] = df['product_category_tree'].map(lambda x: x.split('>>'))

    # Drop unwanted columns
    del_list = ['crawl_timestamp', 'product_url', "retail_price", "discounted_price",
                "is_FK_Advantage_product", "product_rating", "overall_rating", "product_specifications"]
    df = df.drop(del_list, axis=1)

    # Drop duplicates
    df.drop_duplicates(subset="product_name", keep="first", inplace=True)

    # Apply text preprocessing
    df['product'] = df['product_name'].apply(filter_keywords)
    df['description'] = df['description'].astype("str").apply(filter_keywords)
    df['brand'] = df['brand'].astype("str").apply(filter_keywords)

    # Combine all metadata
    df["all_meta"] = df['product'] + df['brand'] + df['product_category_tree'] + df['description']
    df["all_meta"] = df["all_meta"].apply(lambda x: ' '.join(x))

    return df