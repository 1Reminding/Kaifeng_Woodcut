import requests

def generate_image(link,description):
    url = "https://api.zhishuyun.com/midjourney/imagine/relax?token=250d56818cac49cabcb67497e53d9bf2"

    headers = {
        "content-type": "application/json"
    }
    initial_prompt = f"{link}\nDescription: {description}\nStyle: Papercut style, Peking Opera character style, flat color blocks, simple lines\nFeatures: Larger head, highly exaggerated head-to-body ratio, rustic figure design, expressions without coquettishness\nMedium: Traditional Chinese woodblock New Year painting, simple line drawing\nBackground: White background\nComposition: Compact, full, symmetrical, full-body figures\nColors: Vintage tones, woodblock red, copper green, and mallow purple\n--no text,seal --style raw --iw 2.0"
    payload = {
        "prompt": initial_prompt
    }
    response = requests.post(url, json=payload, headers=headers)

    return response.text