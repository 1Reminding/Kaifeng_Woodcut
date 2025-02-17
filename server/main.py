from flask import Flask, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask_cors import CORS
from gpt_function import generate_link,generate_description
from midjourney import generate_image

app = Flask(__name__)
CORS(app)


@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        theme = data.get('theme')

        # 添加调试日志
        print(f"Received theme: {theme}")

        if not theme:
            return jsonify({
                'success': False,
                'error': 'Theme is required'
            }), 400

        # 逐步调试每个生成函数
        try:
            description = generate_description(theme)
            print(f"Generated description: {description}")
        except Exception as e:
            print(f"Description generation error: {str(e)}")
            raise

        try:
            base_link = generate_link(theme)
            print(f"Generated base link: {base_link}")
        except Exception as e:
            print(f"Link generation error: {str(e)}")
            raise

        try:
            image_url = generate_image(base_link, description)
            print(f"Generated image URL: {image_url}")
        except Exception as e:
            print(f"Image generation error: {str(e)}")
            raise

        return jsonify({
            'success': True,
            'data': {
                'description': description,
                'baseLink': base_link,
                'imageUrl': image_url
            }
        })

    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # 添加错误日志
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)