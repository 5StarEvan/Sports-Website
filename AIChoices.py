from openai import OpenAI
import os

OPENAI_API_KEY = 'sk-h_3ErXctXRlZxP3meOQ6j3S3RrnaGfB9Sf5TWl238kT3BlbkFJ2OEOHHEpmXtjOCeqSG7Wm3SyyR0Tt42ZyNRwozfuMA'
client = OpenAI(api_key=OPENAI_API_KEY)


def getAIPicks():

    prompt = f"""Generate players who you think will do good in the NBA for the next NBA game(5 players). 
    List them out line by line with just their name in order"""

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Extract the name, fen, and description from the response
    lines = response.choices[0].message.content.splitlines()

    return lines;

