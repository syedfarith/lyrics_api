from flask import Flask, request, jsonify
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def generate_lyrics_from_groq(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a music assistant to create lyrics based on the user description, language, and genre.",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

@app.route('/generate_lyrics', methods=['POST'])
def generate_lyrics():
    data = request.json

    # Extract the fields from JSON payload
    song_description = data.get('description', '')
    language = data.get('language', 'English')
    genre = data.get('genre', 'Pop')

    # Error handling if description is missing
    if not song_description:
        return jsonify({'error': 'Please provide a song description'}), 400

    # Create the prompt for the lyrics generation
    prompt = f"Generate song lyrics in {language}, genre: {genre}, description: {song_description}"

    try:
        # Generate lyrics using the external API (Groq)
        generated_lyrics = generate_lyrics_from_groq(prompt)
        return jsonify({'lyrics': generated_lyrics})
    
    except Exception as e:
        return jsonify({'error': 'Failed to generate lyrics', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
