import json
from .text_processor import TextProcessor

class DataPreprocessor:
    def __init__(self):
        self.text_processor = TextProcessor()

    def prepare_data(self, df):
        # Clean and preprocess 'product_category_tree'
        if 'product_category_tree' in df.columns:
            df['product_category_tree'] = df['product_category_tree'].fillna('[]')  # Handle NaN values
            df['product_category_tree'] = df['product_category_tree'].apply(
                lambda x: ' >> '.join(json.loads(x)) if isinstance(x, str) and x.startswith('[') else str(x)
            )

        # Drop unwanted columns (if they exist)
        del_list = ['crawl_timestamp', 'product_url', 'retail_price', 'discounted_price',
                    'is_FK_Advantage_product', 'product_rating', 'overall_rating', 
                    'product_specifications']
        for col in del_list:
            if col in df.columns:
                df.drop(col, axis=1, inplace=True)

        # Drop duplicates based on 'product_name'
        if 'product_name' in df.columns:
            df.drop_duplicates(subset='product_name', keep='first', inplace=True)

        # Apply text preprocessing
        if 'product_name' in df.columns:
            df['product'] = df['product_name'].astype(str).apply(self.text_processor.filter_keywords)
        else:
            df['product'] = ''

        if 'description' in df.columns:
            df['description'] = df['description'].astype(str).apply(self.text_processor.filter_keywords)
        else:
            df['description'] = ''

        if 'brand' in df.columns:
            df['brand'] = df['brand'].astype(str).apply(self.text_processor.filter_keywords)
        else:
            df['brand'] = ''

        if 'product_category_tree' in df.columns:
            df['product_category_tree'] = df['product_category_tree'].apply(lambda x: x if isinstance(x, list) else [x])
        else:
            df['product_category_tree'] = ''

        # Combine all metadata into a single field
        df['all_meta'] = df['product'] + df['brand'] + df['product_category_tree'] + df['description']
        df['all_meta'] = df['all_meta'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x)  # Normalize spaces

        return df
