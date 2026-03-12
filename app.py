import streamlit as st
import google.generativeai as genai

# --- SECURE CONFIGURATION ---
# This looks for your key in the Streamlit Cloud settings instead of the code
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Missing API Key! Please add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

def generate_suno_prompt(song, artist):
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        tools=[{'google_search_retrieval': {}}]
    )

    query = f"""
    Deep research on '{song}' by '{artist}'. 
    1. Check WhoSampled for samples (genre/era).
    2. Check Discogs for 'Style' tags.
    3. Identify BPM, instruments, and vocal style.
    Create a Suno AI Style Prompt (comma-separated keywords only).
    """

    try:
        response = model.generate_content(query)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# --- UI ---
st.set_page_config(page_title="Suno DNA Architect", page_icon="🪄")
st.title("🪄 Suno AI Prompt Architect")

song_title = st.text_input("Song Title")
artist_name = st.text_input("Artist")

if st.button("Generate Prompt"):
    if song_title and artist_name:
        with st.spinner("Researching..."):
            result = generate_suno_prompt(song_title, artist_name)
            st.code(result.replace("```", "").strip(), language="text")
    else:
        st.error("Enter both fields.")
