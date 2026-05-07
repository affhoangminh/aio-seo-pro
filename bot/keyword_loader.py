import pandas as pd
import random


class KeywordLoader:

    def __init__(self, file_path):

        self.keywords = []

        try:

            df = pd.read_excel(file_path)

            # lấy cột đầu tiên
            self.keywords = df.iloc[:,0].dropna().tolist()

        except Exception as e:

            print("Keyword load error:", e)

    def random_keyword(self):

        if not self.keywords:
            return None

        return random.choice(self.keywords)