import streamlit as st
import google.generativeai as genai

# --- SECURE CONFIGURATION ---
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Missing API Key! Please add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

def generate_suno_prompt(song, artist):
    # Using the updated model name for 2026
    # Note: 'gemini-2.0-flash' is the current stable recommendation
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash', 
        tools=[{'google_search': {}}] 
    )

    query = f"""
    Deep research on the song '{song}' by '{artist}'. 
    1. Check WhoSampled for samples (genre/era).
    2. Check Discogs for 'Style' and 'Genre' tags.
    3. Identify BPM, rhythmic instruments, and vocal delivery.
    
    Create a 'Suno AI Style Prompt'. 
    - Comma-separated keywords ONLY.
    - No artist names or song titles.
    - Include the 'DNA' of the samples (e.g., 'vintage soul textures').
    """

    try:
        response = model.generate_content(query)
        # Ensure we return clean text
        return response.text.strip().replace("```", "").replace("text", "")
    except Exception as e:
        return f"Error: {str(e)}"

# --- UI ---
st.set_page_config(page_title="Suno DNA Architect", page_icon="🪄")
st.title("🪄 Suno AI Prompt Architect")
st.markdown("Extracting musical DNA via Gemini 2.0 Search Grounding.")

song_title = st.text_input("Song Title", placeholder="e.g. Midnight City")
artist_name = st.text_input("Artist", placeholder="e.g. M83")

if st.button("Generate DNA Prompt"):
    if song_title and artist_name:
        with st.spinner("Searching the web for musical DNA..."):
            result = generate_suno_prompt(song_title, artist_name)
            
            if "Error" in result:
                st.error(result)
                st.info("Try checking if your API Key has 'Google Search' permissions enabled in AI Studio.")
            else:
                st.subheader("🚀 Suno Style Box:")
                st.code(result, language="text")
    else:
        st.error("Please enter both a song title and artist.")

st.divider()
st.caption("Updated for Gemini 2.0 API standards.")
