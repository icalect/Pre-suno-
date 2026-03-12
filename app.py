import streamlit as st
from google import genai
from google.genai import types

# --- SECURE CONFIGURATION ---
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Missing API Key! Please add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# Initialize the new GenAI Client
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_suno_prompt(song, artist):
    # Setup the Google Search Tool using the correct Gemini 2.0 syntax
    search_tool = types.Tool(
        google_search=types.GoogleSearch()
    )
    
    config = types.GenerateContentConfig(
        tools=[search_tool],
        temperature=1.0  # Recommended for creative grounding
    )

    prompt_text = f"""
    Deep research on the song '{song}' by '{artist}'. 
    1. Check WhoSampled.com for samples (identify genre and era of the sampled track).
    2. Check Discogs.com for specific 'Style' and 'Genre' tags.
    3. Identify the BPM and rhythmic feel.
    4. Describe the vocal style and key instruments.

    Generate a 'Suno AI Style Prompt'. 
    Format: Return ONLY a comma-separated list of descriptive keywords.
    Rules: No artist names, no song titles, focus on 'DNA' and textures.
    """

    try:
        # Generate content using the new SDK method
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt_text,
            config=config
        )
        # Clean up output
        return response.text.strip().replace("```", "").replace("text", "").strip()
    except Exception as e:
        return f"Error: {str(e)}"

# --- STREAMLIT UI ---
st.set_page_config(page_title="Suno DNA Architect", page_icon="🪄")
st.title("🪄 Suno AI Prompt Architect")
st.markdown("Grounding musical DNA via **Gemini 2.0** and Google Search.")

song_title = st.text_input("Song Title", placeholder="e.g. C.R.E.A.M.")
artist_name = st.text_input("Artist", placeholder="e.g. Wu-Tang Clan")

if st.button("Generate DNA Prompt", use_container_width=True):
    if song_title and artist_name:
        with st.spinner("Analyzing samples and musical style..."):
            result = generate_suno_prompt(song_title, artist_name)
            
            if "Error" in result:
                st.error(result)
            else:
                st.subheader("🚀 Suno Style Box:")
                st.code(result, language="text")
                st.success("DNA extraction successful.")
    else:
        st.error("Please enter both a song title and an artist.")

st.divider()
st.caption("Migrated to the 2026 Google GenAI SDK (v2.0).")
