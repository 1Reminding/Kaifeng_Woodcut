import pandas as pd
from openai import OpenAI
import numpy as np


class ThemeMatcher:
    def __init__(self, api_key: str, base_url: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def get_embedding(self, text: str) -> list:
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

    def load_xls(self, xls_path: str) -> list:
        df = pd.read_excel(xls_path)
        entries = []
        for _, row in df.iterrows():
            entries.append({
                'id': row[0],
                'theme': row[1],
                'description': row[2],
                'link': row[3]
            })
        return entries

    def create_index(self, entries: list) -> dict:
        index = {}
        for entry in entries:
            text = f"{entry['theme']} {entry['description']}"
            embedding = self.get_embedding(text)
            index[entry['id']] = {
                'embedding': embedding,
                'data': entry
            }
        return index

    def find_best_match(self, query: str, index: dict, top_k: int = 1):
        query_embedding = self.get_embedding(query)

        scores = {}
        for id, data in index.items():
            similarity = np.dot(query_embedding, data['embedding'])
            scores[id] = {
                'score': similarity,
                'data': data['data']
            }

        sorted_matches = sorted(scores.items(),
                                key=lambda x: x[1]['score'],
                                reverse=True)[:top_k]

        return [match[1]['data'] for match in sorted_matches]


def main():
    API_SECRET_KEY = "sk-zk2540be597471c72fa10ea895db68d386d6792170a963e7"
    BASE_URL = "https://api.zhizengzeng.com/v1/"

    matcher = ThemeMatcher(API_SECRET_KEY, BASE_URL)

    entries = matcher.load_xls(r"F:\Desktop\base_image.xlsx")
    index = matcher.create_index(entries)

    query = "五子登科"
    matches = matcher.find_best_match(query, index)

    if matches:
        match = matches[0]
        print(f"\n找到最相关的主题:")
        print(f"主题: {match['theme']}")
        print(f"描述: {match['description']}")
        print(f"链接: {match['link']}")
    else:
        print("未找到相关主题")