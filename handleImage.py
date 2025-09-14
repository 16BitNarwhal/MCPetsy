import json
from anthropic import Anthropic

client = Anthropic()

def analyze_image(image_data, image_media_type):
    """Analyze base64 image using Claude Vision to extract product info and price"""
    try:
        message = client.messages.create(
            model="claude-sonnet-4-0",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image_media_type,
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": """Analyze this image and provide:
                1. Product name/title (for Kijiji ad)
                2. Product description (detailed, for Kijiji ad)
                3. Recommended price (in USD, based on condition and market value)
                4. Category (e.g., Electronics, Books, Furniture, etc.)

                Format your response as JSON:
                {
                    "title": "Product title",
                    "description": "Detailed description",
                    "price": "25.00",
                    "category": "Electronics",
                }"""
                        }
                    ],
                }
            ],
        )
        
        content = message.content[0].text
        product_info = json.loads(content)
        
        return product_info
        
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return {
            "title": "Sample Product",
            "description": "Sample description here",
            "price": "13.00",
            "category": "Books",
        }