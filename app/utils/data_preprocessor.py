from .text_processor import TextProcessor
class DataPreprocessor:
    def __init__(self):
        self.text_processor = TextProcessor()

    def prepare_data(self, df):
        # Clean product category tree
        df['product_category_tree'] = df['product_category_tree'].map(lambda x: x.strip('[]'))
        df['product_category_tree'] = df['product_category_tree'].map(lambda x: x.strip('"'))
        df['product_category_tree'] = df['product_category_tree'].map(lambda x: x.split('>>'))

        # Drop unwanted columns
        del_list = ['crawl_timestamp', 'product_url', "retail_price", "discounted_price",
                    "is_FK_Advantage_product", "product_rating", "overall_rating", 
                    "product_specifications"]
        df = df.drop(del_list, axis=1)

        # Drop duplicates
        df.drop_duplicates(subset="product_name", keep="first", inplace=True)

        # Apply text preprocessing
        df['product'] = df['product_name'].apply(self.text_processor.filter_keywords)
        df['description'] = df['description'].astype("str").apply(self.text_processor.filter_keywords)
        df['brand'] = df['brand'].astype("str").apply(self.text_processor.filter_keywords)

        # Combine all metadata
        df["all_meta"] = (df['product'] + df['brand'] + 
                         df['product_category_tree'] + df['description'])
        df["all_meta"] = df["all_meta"].apply(lambda x: ' '.join(x))

        return df