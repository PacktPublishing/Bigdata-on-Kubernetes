from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/api")
async def root():
    return {"message": "You are doing great with FastAPI..."}

@app.get("/api/{name}")
async def return_name(name): 
    return {
        "name": name, 
        "message": f"Hello, {name}!" 
    }

@app.get("/joke") 
async def return_joke(): 
    jokes = [ 
        "What do you call a fish wearing a bowtie? Sofishticated.",
        "What did the ocean say to the beach? Nothing. It just waved",
        "Have you heard about the chocolate record player? It sounds pretty sweet."
    ]

    return { 
        "joke": random.choice(jokes) 
    }
