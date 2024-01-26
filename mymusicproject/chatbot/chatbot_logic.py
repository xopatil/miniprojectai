# chatbot/chatbot_logic.py
import requests
from textblob import TextBlob

def generate_bot_response(user_message):
    # Convert the user's message to lowercase for case-insensitive matching
    user_message_lower = user_message.lower()

    # Define some keywords and corresponding responses
    keyword_responses = {
        'hello': 'Hi there! How can I help you?',
        'music': 'I love music! What genre are you interested in?',
        'python': 'Python is a fantastic programming language!',
    }

    # Check if any keyword is present in the user's message
    for keyword, response in keyword_responses.items():
        if keyword in user_message_lower:
            return response, 'Positive'

    # If no specific keyword is found, provide a default response
    return "I'm not sure how to respond to that. Feel free to ask me about music, programming, or say hello!", 'Neutral'


def analyze_tone(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity

    # You can customize this based on your specific requirements
    if sentiment_score >= 0.5:
        return 'positive'
    elif sentiment_score <= -0.5:
        return 'negative'
    else:
        return 'neutral'

def get_recommendation(tone):
    # Replace 'YOUR_LASTFM_API_KEY' with your actual Last.fm API key
    lastfm_api_key = '24c647077bbf53e8249f9febf6433ecc'
    
    # Example Last.fm API request to get a song recommendation based on tone
    lastfm_api_url = f'http://ws.audioscrobbler.com/2.0/?method=track.getrecommendations&api_key={lastfm_api_key}&format=json&limit=1&seed_track=cher-believe'  # Use a seed track relevant to your project

    try:
        response = requests.get(lastfm_api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Extract relevant information from the Last.fm API response
        if 'track' in data and 'name' in data['track'][0]:
            song_title = data['track'][0]['name']
            artist = data['track'][0]['artist']['name']
        else:
            song_title = 'Unknown'
            artist = 'Unknown'

        return {
            'message': f'Recommended Song: {song_title} by {artist}',
            'sentiment': tone,
        }

    except requests.RequestException as e:
        # Handle the error, log it, and return a default recommendation
        print(f"Error during Last.fm API request: {e}")
        return {
            'message': 'Unable to fetch recommendation at the moment. Please try again later.',
            'sentiment': tone,
        }

# Additional helper functions or constants can be added as needed

