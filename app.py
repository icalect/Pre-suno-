import streamlit as st
from google import genai
from google.genai import types
import time

# --- SECURE CONFIGURATION ---
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Missing API Key! Please add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_suno_prompt(song, artist):
    # Prompt for the AI
    prompt_text = f"""
    Research the song '{song}' by '{artist}'. 
    Identify its genres, sub-genres, BPM, key instruments, and any famous samples it uses.
    Create a 'Suno AI Style Prompt' consisting ONLY of a comma-separated list of descriptive keywords.
    Include textures like 'vintage soul' if it uses old samples. 
    NO artist names, NO song titles.
    """

    # Attempt 1: Gemini 1.5 Flash WITH Search (More stable for free tier)
    try:
        search_tool = types.Tool(google_search=types.GoogleSearch())
        config_with_search = types.GenerateContentConfig(tools=[search_tool])
        
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt_text,
            config=config_with_search
        )
        return response.text.strip().replace("```", "").replace("text", ""), "Search Grounding"
    
    except Exception as e:
        # If 429 (Quota) or any other error, try Attempt 2: WITHOUT Search
        if "429" in str(e) or "limit" in str(e).lower():
            try:
                # No search tool, just AI knowledge
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt_text
                )
                return response.text.strip().replace("```", "").replace("text", ""), "AI Knowledge (Search Quota Full)"
            except Exception as e2:
                return f"Error: {str(e2)}", "Failed"
        else:
            return f"Error: {str(e)}", "Failed"

# --- STREAMLIT UI ---
st.set_page_config(page_title="Suno DNA Architect", page_icon="🪄")
st.title("🪄 Suno AI Prompt Architect")
st.markdown("Generates Suno style prompts using Gemini AI.")

song_title = st.text_input("Song Title", placeholder="e.g. Bohemian Rhapsody")
artist_name = st.text_input("Artist", placeholder="e.g. Queen")

if st.button("Generate DNA Prompt", use_container_width=True):
    if song_title and artist_name:
        with st.spinner("Analyzing song..."):
            result, source = generate_suno_prompt(song_title, artist_name)
            
            if "Error" in result:
                st.error(result)
            else:
                st.subheader("🚀 Suno Style Box:")
                st.code(result, language="text")
                st.caption(f"Data Source: {source}")
                st.success("Analysis complete.")
    else:
        st.error("Please enter both song and artist.")

st.divider()
st.caption("Free Tier users: If Search Grounding is busy, the app defaults to the AI's internal database.")
