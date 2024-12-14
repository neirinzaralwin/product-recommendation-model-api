import os
import nltk

def download_nltk_data():
    nltk_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'nltk_data')

    os.makedirs(nltk_data_path, exist_ok=True)

    nltk.data.path.append(nltk_data_path)

    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
        print("NLTK Data already exists")
    except LookupError:
        print("Downloading NLTK Data...")
        nltk.download('punkt', download_dir=nltk_data_path)
        nltk.download('stopwords', download_dir=nltk_data_path)
        print("NLTK Data download completed")