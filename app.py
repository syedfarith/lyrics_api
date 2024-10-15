from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from groq import Groq
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000", "http://localhost:5000","http://localhost:3000"], # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers (Authorization, Content-Type, etc.)
)
# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Pydantic model for request validation
class LyricsRequest(BaseModel):
    description: str
    language: str = "English"
    genre: str = "Pop"

# Function to generate lyrics using Groq API
def generate_lyrics_from_groq(prompt: str) -> str:
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


# POST endpoint to generate lyrics
@app.post("/generate_lyrics")
async def generate_lyrics(request: LyricsRequest):
    song_description = request.description
    language = request.language
    genre = request.genre

    # Check if description is empty
    if not song_description:
        raise HTTPException(status_code=400, detail="Please provide a song description.")

    # Create the prompt for lyrics generation
    prompt = f"Generate song lyrics in {language}, genre: {genre}, description: {song_description}"

    try:
        # Generate lyrics using the external API (Groq)
        generated_lyrics = generate_lyrics_from_groq(prompt)
        return {"lyrics": generated_lyrics}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate lyrics: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
