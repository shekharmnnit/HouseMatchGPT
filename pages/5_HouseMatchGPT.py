import json
import traceback

import streamlit as st
from services import prompts
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES
st.set_page_config(
    page_title="HouseMatchGPT",
    page_icon="📄",
    layout="wide"
)

import asyncio
import io
import os
import pathlib
from os.path import isfile, join
import pandas as pd
import helpers.sidebar
import helpers.util
import services.prompts
import services.llm
import helpers.util
import pandas as pd
import spacy
from sklearn.preprocessing import MinMaxScaler

helpers.sidebar.show()

st.header("Find you dream home with HouseMatchGPT")
st.write("HouseMatchGPT is an AI-driven search engine for your real estate needs.")

homes_df = pd.read_csv("data/boston.csv")
# homes_df.index =
homes_df['Distance to Park'] = 1 / homes_df['Industrial Area']
scaler = MinMaxScaler()
homes_df[['Crime Rate', 'Nitric Oxide', 'Property Tax']] = scaler.fit_transform(homes_df[['Crime Rate', 'Nitric Oxide', 'Property Tax']])
homes_df['School Rating'] = 1 - (0.5 * homes_df['Crime Rate'] + 0.3 * homes_df['Nitric Oxide'] + 0.2 * homes_df['Property Tax'])
# homes_list = [
#         {"name": "Home 1", "distance_to_park": 0.5, "school_rating": 9, "crime_rate": "low"},
#         {"name": "Home 2", "distance_to_park": 2.0, "school_rating": 8, "crime_rate": "medium"},
#         {"name": "Home 3", "distance_to_park": 1.0, "school_rating": 10, "crime_rate": "low"}
#     ]
homes = homes_df.to_string()


if 'reset_counter' not in st.session_state:
    st.session_state['reset_counter'] = 0

code_review_input_key = f"code_review_input_{st.session_state['reset_counter']}"
code_debug_input_key = f"code_debug_input_{st.session_state['reset_counter']}"
def reset_page():
    st.session_state['reset_counter'] += 1
    st.session_state.code_debug_error_input = 0
    st.session_state.code_modify_input = 0
    st.experimental_rerun()

if 'code_debug_error_input' not in st.session_state:
    st.session_state.code_debug_error_input = ""

    # preferences = {
    #     "parks": False,
    #     "schools": False,
    #     "quiet": False
    # }

    # Basic keyword matching
    # if "parks" in prompt.lower():
    #     preferences["parks"] = True
    # if "schools" in prompt.lower():
    #     preferences["schools"] = True
    # if "quiet" in prompt.lower() or "low crime" in prompt.lower():
    #     preferences["quiet"] = True
def extract_preferences(prompt):
    # Load the spaCy model for NLP
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(query.lower())

    # Extract keywords (lemmas of the tokens)
    keywords = set()
    for token in doc:
        # Exclude stop words and punctuation
        if not token.is_stop and not token.is_punct:
            keywords.add(token.lemma_)


    # Example usage
    # query_string = "I am looking for a quiet neighborhood near parks and schools with good facilities."
    keywords_string = " ".join(keywords)
    print("Keywords:", keywords_string)

    return keywords_string

# def search_real_estate(homes, preferences):
#     filtered_homes = []
#     for home in homes:
#         if preferences["parks"] and home["distance_to_park"] > 1.5:
#             continue
#         if preferences["schools"] and home["school_rating"] < 9:
#             continue
#         if preferences["quiet"] and home["crime_rate"] != "low":
#             continue
#         filtered_homes.append(home)
#
#     return filtered_homes

# Debugging Column
st.subheader("HouseMatchGPT")
query = st.text_input("Enter your query", placeholder="Ex. I am looking for a quiet neighborhood near parks and schools with good facilities.")
keywords = extract_preferences(query)
# preferences = extract_preferences(query)
# preferences_list = json.dumps(preferences, indent=4)
# filtered_homes = search_real_estate(homes_list, preferences)
# filtered_homes_string = json.dumps(homes_list, indent=4)
if st.button("Find Homes", type="primary"):
    advice = st.markdown("HouseMatchGPT Says...")
    housematchgpt_prompt = services.prompts.debug_prompt(homes, keywords, query)
    messages = services.llm.create_conversation_starter(services.prompts.general_housematchgpt_prompt())
    messages.append({"role": "user", "content": housematchgpt_prompt})
    asyncio.run(helpers.util.run_conversation(messages, advice))


