from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from xgboost import XGBClassifier



app = FastAPI()

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )  

with open(r"C:\Users\RPC\Desktop\jupyter files\machine learning & data science projects-github\Music_recommendation_system_regression_project\XGBRegressor_model.pkl","rb") as f : 
    XGBClassifier_model = pickle.load(f)

class musicInput(BaseModel):
    valence : float
    year : int 
    acousticness : float
    danceability : float
    energy : float
    explicit : int 
    instrumentalness : float
    key : int
    liveness : float
    loudness : float
    mode : int 
    speechiness : float
    tempo : float
    duration_ms : int


@app.post("/predict/")
def predict(music_data:musicInput):
    try :
        df = pd.DataFrame([music_data.dict()])

        # Feature Extraction
        df['duration_min'] = df['duration_ms'].apply(lambda x: x / 60000)
        df = df.drop('duration_ms',axis=1)

        def GetTypeOfValence(valence) : 
            valence = float(valence)
            if valence < 0.3 : 
                return 'Sad song'
            elif  valence >= 0.3 and valence < 0.6 :
                return 'Balance song between sadness and joy'
            elif  valence >= 0.6 and valence <= 1.0 : 
                return 'Happy song'
            
        df['type_of_song_by_valence'] = df['valence'].apply( lambda x : GetTypeOfValence(x))

        def GetTypeOfAcousticness(acousticness) : 
            acousticness = float(acousticness)
            if acousticness < 0.3 : 
                return 'Highly electronic song'
            elif  acousticness >= 0.3 and acousticness < 0.6 :
                return 'Mix of acoustic and electronic instruments'
            elif  acousticness >= 0.6 and acousticness <= 1.0 : 
                return 'Mostly acoustic song'
            
        df['type_of_song_by_acousticness'] = df['acousticness'].apply(lambda x : GetTypeOfAcousticness(x))

        def GetTypeOfDanceability(danceability) : 
            danceability = float(danceability)
            if danceability < 0.4 :
                return 'Not suitable for dance'
            if danceability >= 0.4 and danceability < 0.7 :
                return 'Medium-paced song'                                                                           
            if danceability >= 0.7 and danceability <= 1.0:
                return 'Highly danceable song'
            
        df['type_of_song_by_danceability'] = df['danceability'].apply( lambda x : GetTypeOfDanceability(x))

        def Energy_Level_of_the_Song(energy) : 
            energy = float(energy)
            if energy < 0.3 : 
                return 'Slow song'
            elif  energy >= 0.3 and energy < 0.6 :
                return 'Medium-energy song'
            elif  energy >= 0.6 and energy <= 1.0 : 
                return 'High-energy song (Enthusiastic)'
            
        df['Energy_Level_of_the_Song'] = df['energy'].apply( lambda x : Energy_Level_of_the_Song(x))

        def type_of_song_by_instrumentalness(instrumentalness) : 
            instrumentalness = float(instrumentalness)
            if instrumentalness < 0.3 :
                return 'Song clearly contains lyrics'
            if instrumentalness >= 0.3 and instrumentalness < 0.7 :
                return 'Song contain some words'                                                                           
            if instrumentalness >= 0.7 and instrumentalness <= 1.0:
                return 'Nearly purely instrumental song'

        df['type_of_song_by_instrumentalness'] = df['instrumentalness'].apply( lambda x : type_of_song_by_instrumentalness(x))

        def type_of_song_by_liveness(liveness) : 
            liveness = float(liveness)
            if liveness < 0.3 :
                return 'Pure studio recordings'
            if liveness >= 0.3 and liveness < 0.7 :
                return 'Records may have a simple reaction with the audience'                                                                           
            if liveness >= 0.7 and liveness <= 1.0:
                return 'Clearly a live recording with an audience'

        df['type_of_song_by_liveness'] = df['liveness'].apply( lambda x : type_of_song_by_liveness(x))

        def type_of_song_by_loudness(loudness) : 
            loudness = float(loudness)
            if loudness > -60 and loudness <= -30 :
                return 'Quieter Sound'
            if loudness > -30 and loudness <= -5 :
                return 'Quiet song'                                                                           
            if loudness > -5:
                return 'Loud song'
            
        df['type_of_song_by_loudness(dB)'] = df['loudness'].apply(lambda x : type_of_song_by_loudness(x))

        def typeOfSongByMode(mode) : 
            mode = int(mode)
            if mode == 0:
                return 'Sad tone (Minor)'
            if mode == 1 :
                return 'Happy tone (Major)'                                                                           
                
        df['type_of_song_by_mode'] = df['mode'].apply(lambda x : typeOfSongByMode(x))                                                                                                                                                                                                                                                       

        def typeOfSongBySpeechiness(speechiness):
            speechiness = float(speechiness)     
            if speechiness < 0.3 :
                return 'Mostly instrumental song'
            if speechiness >= 0.3 and speechiness < 0.7 :
                return 'Song with some speech'                                                                
            if speechiness >= 0.7 and speechiness <= 1.0:
                return 'Podcasts or speech-heavy rap'

        df['type_of_song_by_speechiness'] = df['speechiness'].apply(lambda x : typeOfSongBySpeechiness(x))

        def typeOftempoInBeatsPerMinute(tempo):
            tempo = float(tempo)
            if tempo >= 0.0 and tempo < 80.0 :
                return 'Slow song'
            if tempo >= 80. and tempo < 120.0 :
                return 'Medium-paced song'                                                                   
            if tempo >= 120.0:
                return 'Fast-paced song'

        df['type_of_tempo_in_Beats_Per_Minute(BPM)'] = df['tempo'].apply(lambda x: typeOftempoInBeatsPerMinute(x))

        df['type_of_song_by_valence']= df['type_of_song_by_valence'].replace('Happy song',1)
        df['type_of_song_by_valence']= df['type_of_song_by_valence'].replace('Balance song between sadness and joy',2)
        df['type_of_song_by_valence']= df['type_of_song_by_valence'].replace('Sad song',3)

        df['type_of_song_by_acousticness']= df['type_of_song_by_acousticness'].replace('Mostly acoustic song',1)
        df['type_of_song_by_acousticness']= df['type_of_song_by_acousticness'].replace('Mix of acoustic and electronic instruments',2)
        df['type_of_song_by_acousticness']= df['type_of_song_by_acousticness'].replace('Highly electronic song',3)

        df['type_of_song_by_danceability']= df['type_of_song_by_danceability'].replace('Not suitable for dance',1)
        df['type_of_song_by_danceability']= df['type_of_song_by_danceability'].replace('Medium-paced song',2)
        df['type_of_song_by_danceability']= df['type_of_song_by_danceability'].replace('Highly danceable song',3)

        df['Energy_Level_of_the_Song']= df['Energy_Level_of_the_Song'].replace('High-energy song (Enthusiastic)',3)
        df['Energy_Level_of_the_Song']= df['Energy_Level_of_the_Song'].replace('Medium-energy song',2)
        df['Energy_Level_of_the_Song']= df['Energy_Level_of_the_Song'].replace('Slow song',1)

        df['type_of_song_by_instrumentalness']= df['type_of_song_by_instrumentalness'].replace('Song clearly contains lyrics',1)
        df['type_of_song_by_instrumentalness']= df['type_of_song_by_instrumentalness'].replace('Song contain some words',2)
        df['type_of_song_by_instrumentalness']= df['type_of_song_by_instrumentalness'].replace('Nearly purely instrumental song',3)

        df['type_of_song_by_liveness']= df['type_of_song_by_liveness'].replace('Pure studio recordings',1)
        df['type_of_song_by_liveness']= df['type_of_song_by_liveness'].replace('Records may have a simple reaction with the audience',2)
        df['type_of_song_by_liveness']= df['type_of_song_by_liveness'].replace('Clearly a live recording with an audience',3)

        df['type_of_song_by_loudness(dB)']= df['type_of_song_by_loudness(dB)'].replace('Quieter Sound',1)
        df['type_of_song_by_loudness(dB)']= df['type_of_song_by_loudness(dB)'].replace('Quiet song',2)
        df['type_of_song_by_loudness(dB)']= df['type_of_song_by_loudness(dB)'].replace('Loud song',3)

        df['type_of_song_by_mode']= df['type_of_song_by_mode'].replace('Happy tone (Major)',1)
        df['type_of_song_by_mode']= df['type_of_song_by_mode'].replace('Sad tone (Minor)',2)

        df['type_of_song_by_speechiness']= df['type_of_song_by_speechiness'].replace('Mostly instrumental song',1)
        df['type_of_song_by_speechiness']= df['type_of_song_by_speechiness'].replace('Song with some speech',2)
        df['type_of_song_by_speechiness']= df['type_of_song_by_speechiness'].replace('Podcasts or speech-heavy rap',3)

        df['type_of_tempo_in_Beats_Per_Minute(BPM)']= df['type_of_tempo_in_Beats_Per_Minute(BPM)'].replace('Slow song',1)
        df['type_of_tempo_in_Beats_Per_Minute(BPM)']= df['type_of_tempo_in_Beats_Per_Minute(BPM)'].replace('Medium-paced song',2)
        df['type_of_tempo_in_Beats_Per_Minute(BPM)']= df['type_of_tempo_in_Beats_Per_Minute(BPM)'].replace('Fast-paced song',3)

        # Prediction
        prediction =  XGBClassifier_model.predict(df)
        return {"Prediction":int(prediction[0])}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
