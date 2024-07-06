from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import pickle
from typing import List
from geopy.geocoders import Nominatim
from sklearn.exceptions import NotFittedError
from fastapi.responses import JSONResponse
from sklearn.metrics.pairwise import cosine_similarity
import joblib

#uvicorn main:app --reload

# Charger le pipeline de transformation
with open('pipeline.pkl', 'rb') as f:
    pipeline = pickle.load(f)


    
# Charger les données transformées
with open('data_transformed.pkl', 'rb') as f:
    loaded_data = pickle.load(f)

# Chager les données
data  = pd.read_csv("filmtv_movies.csv")


def recommend_film_cosine(client_preferences,pipeline=pipeline, X_transformed=loaded_data, df=data):
    type_film = client_preferences["genre"]
    # Transformez les préférences du client avec le même préprocesseur
    
    client_input = pipeline.transform(pd.DataFrame(client_preferences, index=[0]))
    
    cosine_sim = cosine_similarity(client_input, X_transformed).flatten()
    
    # Trier les films par score de similarité 
    film_id = cosine_sim.argsort()[::-1]
   
    # Renvoyer les détails des 5 films recommandés
    top_5 = df.iloc[film_id][df.iloc[film_id]['genre'] == type_film].head(5)
    
    return top_5[["year", "genre", "duration","country", "humor", "tension"]]


# Création d'une nouvelle instance FastAPI
app = FastAPI()


# Configurer CORS
origins = ["*"]  # Vous pouvez remplacer "*" par les origines autorisées

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Définir un objet (une classe) pour réaliser des requêtes
class RequestBody(BaseModel):
    year: int
    genre: str
    duration: int
    country: str
    avg_vote: float
    public_vote: int
    total_votes: int
    humor: int
    rhythm: int
    effort: int
    tension: int
    erotism: int


@app.post("/recommend_film", response_class=JSONResponse)


def recommend_film(client_preferences: RequestBody):

    try:
        client_preference =  {'year': client_preferences.year, 'genre': client_preferences.genre,
        'duration': client_preferences.duration,'country': client_preferences.country,
        'avg_vote': client_preferences.avg_vote, 'public_vote':client_preferences.public_vote,
        'total_votes':client_preferences.total_votes, 'humor':client_preferences.humor,
        'rhythm': client_preferences.rhythm, 'effort':client_preferences.effort,
        'tension': client_preferences.tension,'erotism':client_preferences.erotism}

        recommended_film  = recommend_film_cosine(client_preference)
        #Convertir le DataFrame des recommandations en format Dict
        recommended_list = recommended_film.to_dict(orient='records')

        return JSONResponse(content=recommended_list)



    except NotFittedError:
        return {"message": "Le préprocesseur n'est pas ajusté. Veuillez ajuster le préprocesseur avant de faire des prédictions."}
