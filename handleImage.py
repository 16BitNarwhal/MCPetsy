import json
import re
from anthropic import Anthropic

client = Anthropic()

# Valid categories from the Kijiji category selection
VALID_CATEGORIES = [
    "Buy & Sell",
    "Arts & Collectibles", 
    "Audio",
    "Baby Items",
    "Bags & Luggage",
    "Bikes",
    "Books",
    "Business & Industrial",
    "Cameras & Camcorders",
    "CDs, DVDs & Blu-ray",
    "Clothing",
    "Computers",
    "Computer Accessories",
    "Electronics",
    "Free Stuff",
    "Furniture",
    "Garage Sales",
    "Health & Special Needs",
    "Hobbies & Crafts",
    "Home Appliances",
    "Home - Indoor",
    "Home - Outdoor & Garden",
    "Home Renovation Materials",
    "Jewellery & Watches",
    "Musical Instruments",
    "Phones",
    "Sporting Goods & Exercise",
    "Tools",
    "Toys & Games",
    "TVs & Video",
    "Video Games & Consoles",
    "Other"
]

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

def validate_and_fix_category(category):
    """Validate category and return a valid one, defaulting to 'Other' if not found"""
    if category in VALID_CATEGORIES:
        return category
    
    # Try to find a close match (case-insensitive)
    category_lower = category.lower()
    for valid_cat in VALID_CATEGORIES:
        if valid_cat.lower() == category_lower:
            return valid_cat
    
    # If no match found, return 'Other'
    print(f"Category '{category}' not found in valid categories, defaulting to 'Other'")
    return "Other"

def analyze_image(image_data, image_media_type):
    """Analyze base64 image using Claude Vision to extract product info and price"""
    try:
        # Create the categories list for the prompt
        categories_text = "\n".join([f"- {cat}" for cat in VALID_CATEGORIES])
        
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
                            "text": f"""Analyze this image and provide product information for a Kijiji listing.

IMPORTANT: Respond ONLY with valid JSON in this exact format:
{{
    "title": "Product title here",
    "description": "Detailed product description here",
    "price": "25",
    "category": "Electronics"
}}

The category MUST be one of these exact options:
{categories_text}

Choose the most appropriate category from the list above. Do not include any other text, explanations, or formatting outside the JSON object."""
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
        
        # Validate and fix category
        product_info["category"] = validate_and_fix_category(product_info["category"])
        
        # Ensure price is a string with proper format
        if isinstance(product_info["price"], (int, float)):
            product_info["price"] = str(int(product_info['price']))
        
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
        "price": "13",
        "category": "Other",
    }