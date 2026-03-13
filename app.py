import streamlit as st
import google.generativeai as genai

# --- SECURE CONFIGURATION ---
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Missing API Key! Go to Streamlit Cloud Settings > Secrets and add: GEMINI_API_KEY = 'your_key_here'")
    st.stop()

# Configure the library
genai.configure(api_key=GEMINI_API_KEY)

def get_best_model():
    """Finds the best available model on the user's account to avoid 404 errors."""
    try:
        # List all models available to this API key
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Priority list of models we want to use
        priority = [
            'models/gemini-1.5-flash-latest', 
            'models/gemini-1.5-flash', 
            'models/gemini-pro'
        ]
        
        for model_name in priority:
            if model_name in available_models:
                return model_name
        
        # Fallback to the first available if none of the priority ones exist
        return available_models[0] if available_models else 'models/gemini-pro'
    except:
        # Absolute fallback if listing fails
        return 'gemini-pro'

def generate_suno_prompt(song, artist):
    # Auto-detect the working model for your key
    working_model = get_best_model()
    model = genai.GenerativeModel(working_model)

    prompt_text = f"""
    You are a musicology expert. Analyze the song '{song}' by '{artist}'. 
    Identify its genres, sub-genres, BPM, and famous samples.
    
    Create a 'Suno AI Style Prompt'. 
    Format: Return ONLY a comma-separated list of descriptive keywords.
    Rules: NO artist names, NO song titles. 
    Include the 'DNA' of samples (e.g., if it samples 70s Soul, include '1970s soulful horns, vintage grit').
    """

    try:
        response = model.generate_content(prompt_text)
        return response.text.strip().replace("```", "").replace("text", "").strip(), working_model
    except Exception as e:
        return f"Error: {str(e)}", "None"

# --- UI ---
st.set_page_config(page_title="Suno DNA Architect", page_icon="🪄")
st.title("🪄 Suno AI Prompt Architect")
st.markdown("Instantly extract a song's musical DNA for Suno AI.")

col1, col2 = st.columns(2)
with col1:
    song_title = st.text_input("Song Title", placeholder="e.g. Mask Off")
with col2:
    artist_name = st.text_input("Artist", placeholder="e.g. Future")

if st.button("Generate DNA Prompt", use_container_width=True):
    if song_title and artist_name:
        with st.spinner(f"Analyzing {song_title}..."):
            result, model_used = generate_suno_prompt(song_title, artist_name)
            
            if "Error" in result:
                st.error("API Error. Your key might not have access to this model yet.")
                st.info(f"Details: {result}")
            else:
                st.subheader("🚀 Suno Style Box:")
                st.code(result, language="text")
                st.caption(f"Success! Model used: {model_used}")
    else:
        st.error("Please enter both a song title and an artist.")

st.divider()
st.caption("Self-healing version: Now auto-detects model availability.")
