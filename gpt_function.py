import os
from openai import OpenAI
import time
import pandas as pd

API_SECRET_KEY = "sk-zk2540be597471c72fa10ea895db68d386d6792170a963e7"
BASE_URL = "https://api.zhizengzeng.com/v1/"

def generate_description(theme):
    client = OpenAI(api_key=API_SECRET_KEY, base_url=BASE_URL)

    # First generate basic description
    initial_prompt = f"Describe a traditional Chinese New Year painting with the theme: {theme}\nIncorporating traditional Chinese culture and historical stories, only describe the details of figure's characteristics, such as expression, attire, posture, and objects held, without including any content related to painting techniques, artistic aspects, or background. The language should be concise."

    initial_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a painter who understands traditional Chinese culture."},
            {"role": "user", "content": initial_prompt}
        ]
    )

    description = initial_response.choices[0].message.content


    return description


def generate_link(theme):
    # 直接读取Excel
    df = pd.read_excel(r"C:\Xing\LLM proj\woodprint\data\base_image.xlsx")
    content = df.to_string()

    client = OpenAI(api_key=API_SECRET_KEY, base_url=BASE_URL)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "你是一个帮助匹配年画图片的助手。根据用户描述，返回最匹配的图片链接。"},
            {"role": "user", "content": f"年画清单:\n{content}\n描述:{theme}\n只返回最匹配的图片链接。"}
        ]
    )

    link = response.choices[0].message.content

    return link

