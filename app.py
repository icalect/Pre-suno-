import streamlit as st
import google.generativeai as genai

# --- SECURE CONFIGURATION ---
# This looks for your key in Streamlit Cloud "Secrets"
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Missing API Key! Go to Streamlit Cloud Settings > Secrets and add: GEMINI_API_KEY = 'your_key_here'")
    st.stop()

# Configure the library
genai.configure(api_key=GEMINI_API_KEY)

def generate_suno_prompt(song, artist):
    # We use 'gemini-1.5-flash' as it is the most stable and has the highest free quota
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt_text = f"""
    Research the song '{song}' by '{artist}'. 
    Identify its genres, sub-genres, BPM, and any famous samples it uses.
    
    Create a 'Suno AI Style Prompt'. 
    Format: Return ONLY a comma-separated list of descriptive keywords.
    Rules: NO artist names, NO song titles. 
    Include the 'DNA' of samples (e.g., if it samples 70s Soul, include '1970s soulful horns, vintage grit').
    """

    try:
        response = model.generate_content(prompt_text)
        return response.text.strip().replace("```", "").replace("text", "").strip()
    except Exception as e:
        return f"Error: {str(e)}"

# --- UI ---
st.set_page_config(page_title="Suno DNA Architect", page_icon="🪄")
st.title("🪄 Suno AI Prompt Architect")
st.markdown("Instantly extract a song's musical DNA for Suno AI.")

col1, col2 = st.columns(2)
with col1:
    song_title = st.text_input("Song Title", placeholder="e.g. Stayin' Alive")
with col2:
    artist_name = st.text_input("Artist", placeholder="e.g. Bee Gees")

if st.button("Generate DNA Prompt", use_container_width=True):
    if song_title and artist_name:
        with st.spinner(f"Analyzing {song_title}..."):
            result = generate_suno_prompt(song_title, artist_name)
            
            if "Error" in result:
                st.error("There was a connection issue with Gemini.")
                st.info(f"Details: {result}")
            else:
                st.subheader("🚀 Suno Style Box:")
                st.code(result, language="text")
                st.success("Prompt Ready!")
    else:
        st.error("Please enter both a song title and an artist.")

st.divider()
st.caption("Deployment Tip: Ensure your 'requirements.txt' contains 'google-generativeai'.")
