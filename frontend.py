import pandas as pd
import requests
import streamlit as st



def main():
    st.header("Recommandation de films par KidInnov Class")
    st.image("image.png", caption="Recommandation de films", use_column_width=True)
    run_app()


def run_app():

    req = "http://127.0.0.1:8000" 

    year = st.sidebar.number_input("year", min_value=2019, max_value=2023, value=2020, step=1)
    duration = st.sidebar.number_input("durée", min_value=45, max_value=300, value=50, step=5)
    avg_vote = st.sidebar.number_input("Vote moyenne", min_value=1, max_value=9, value=1, step=1)
    public_vote = st.sidebar.number_input("Vote public", min_value=1, max_value=10, value=1, step=1)
    total_votes = st.sidebar.number_input("Vote total", min_value=1, max_value=540, value=10, step=1)
    humor = st.sidebar.number_input("humour", min_value=0, max_value=4, value=0, step=1)
    rhythm = st.sidebar.number_input("rhythm", min_value=0, max_value=4, value=1, step=1)
    effort = st.sidebar.number_input("effort", min_value=0, max_value=4, value=0, step=1)
    tension = st.sidebar.number_input("tension", min_value=0, max_value=4, value=2, step=1)
    erotism = st.sidebar.number_input("erotis", min_value=0, max_value=4, value=1, step=1)
    genre = st.sidebar.text_input("Quel genre de film aimerize vous regarder?", value = "Comedy")
    country = st.sidebar.text_input("Tourné dans quel pays?", value = "Canada")

    if st.sidebar.button("Valider"):

        client_preference = {'year':year, 'genre':genre,'duration':duration,'country':country,
        'avg_vote':avg_vote, 'public_vote':public_vote, 'total_votes':total_votes, 'humor':humor,
        'rhythm':rhythm, 'effort':effort, 'tension':tension, 'erotism':erotism}

        reponse = requests.post(f"{req}/recommend_film", json = client_preference)
       

        if reponse.status_code == 200:
            recommanded_film = pd.DataFrame(reponse.json())
            st.subheader("Film récommander pour vous!!!!")
            st.table(recommanded_film)
        
        else:
            st.error(f"Erreur: {reponse.json()['detail']}")



if __name__ == "__main__":
    main()


