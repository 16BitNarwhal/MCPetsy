import json
import re
from anthropic import Anthropic

client = Anthropic()

def extract_json_from_text(text):
    """Extract JSON from text that might contain other content"""
    # Look for JSON object in the text
    json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    # If no JSON found, try to parse the entire text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None

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
                            "text": """Analyze this image and provide product information for a Kijiji listing.

IMPORTANT: Respond ONLY with valid JSON in this exact format:
{
    "title": "Product title here",
    "description": "Detailed product description here",
    "price": "25.00",
    "category": "Electronics"
}

Do not include any other text, explanations, or formatting outside the JSON object."""
                        }
                    ],
                }
            ],
        )
        
        content = message.content[0].text
        print(f"Claude raw response: {content}")  # Debug line
        
        # Try to extract JSON from the response
        product_info = extract_json_from_text(content)
        
        if product_info is None:
            print("Failed to extract JSON from Claude response")
            raise ValueError("Invalid JSON response from Claude")
        
        # Validate required fields
        required_fields = ["title", "description", "price", "category"]
        for field in required_fields:
            if field not in product_info:
                print(f"Missing required field: {field}")
                raise ValueError(f"Missing required field: {field}")
        
        # Ensure price is a string with proper format
        if isinstance(product_info["price"], (int, float)):
            product_info["price"] = f"{product_info['price']:.2f}"
        
        print(f"Parsed product info: {product_info}")
        return product_info
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Raw content: {content}")
        return get_fallback_product_info()
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return get_fallback_product_info()

def get_fallback_product_info():
    """Return a fallback product info if analysis fails"""
    return {
        "title": "Sample Product",
        "description": "Product description could not be generated. Please add details manually.",
        "price": "13.00",
        "category": "General",
    }