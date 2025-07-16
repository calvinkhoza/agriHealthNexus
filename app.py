from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from requests_oauthlib import OAuth1
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
# Load environment variables
#load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# FatSecret API credentials
CONSUMER_KEY = os.getenv('FATSECRET_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('FATSECRET_CONSUMER_SECRET')

print("KEY:", CONSUMER_KEY)
print("SECRET:", CONSUMER_SECRET)

# OAuth1 authentication
oauth = OAuth1(
    CONSUMER_KEY,
    client_secret=CONSUMER_SECRET,
    signature_method='HMAC-SHA1',
    signature_type='query'
)

BASE_URL = 'https://platform.fatsecret.com/rest/server.api'

@app.route('/')
def index():
    return render_template('scanner.html')

@app.route('/api/search', methods=['POST'])
def search_food():
    try:
        data = request.get_json()
        food_name = data.get('food', '').strip()
        
        if not food_name:
            return jsonify({'error': 'Food name is required'}), 400
        
        # Prepare parameters
        params = {
            'method': 'foods.search',
            'search_expression': food_name,
            'format': 'json',
            'max_results': 5,
            'page_number': 0
        }

        # Make authenticated request
        response = requests.get(
            BASE_URL,
            params=params,
            auth=oauth,
            headers={'User-Agent': 'FoodNutritionScanner/1.0'}
        )
        
        # Check for API errors
        if response.status_code != 200:
            error_msg = f"FatSecret API error: {response.status_code}"
            if response.text:
                error_msg += f" - {response.text[:200]}"
            return jsonify({'error': error_msg}), 502
        
        data = response.json()
        
        # Handle FatSecret API error responses
        if 'error' in data:
            return jsonify({
                'error': f"FatSecret API error: {data['error']['message']}"
            }), 400
        
        return jsonify(data)
    
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': f"Network error: {str(e)}"
        }), 503
    except Exception as e:
        return jsonify({
            'error': f"Server error: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)