import streamlit as st
import google.generativeai as genai

# --- SECURE CONFIGURATION ---
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Missing API Key! Please add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# Use the stable configuration
genai.configure(api_key=GEMINI_API_KEY)

def generate_suno_prompt(song, artist):
    # Using the most stable model ID
    model = genai.GenerativeModel('gemini-1.5-flash')

    # We use a sophisticated prompt so the AI acts like a musicologist
    prompt_text = f"""
    You are a musicology expert and Suno AI prompt engineer.
    Analyze the song '{song}' by '{artist}'.
    
    Tasks:
    1. Identify the primary genres (e.g., East Coast Hip Hop, Synth-pop).
    2. Identify the 'DNA' (What famous samples does it use? What era is the sound?).
    3. Identify the technicals (BPM, specific instruments like 808s, Juno-60 synths, or Rhodes piano).
    4. Identify the vocal style.

    Output:
    Provide a Suno AI 'Style of Music' prompt. 
    It must be a single paragraph of comma-separated keywords.
    Include the textures of any sampled music (e.g., if it samples 70s Soul, include '1970s soulful horns, vintage grit').
    NO artist names. NO song titles.
    """

    try:
        response = model.generate_content(prompt_text)
        # Clean the output to ensure it's just the keywords
        clean_text = response.text.strip().replace("```", "").replace("text", "").strip()
        return clean_text
    except Exception as e:
        return f"Error: {str(e)}"

# --- STREAMLIT UI ---
st.set_page_config(page_title="Suno DNA Architect", page_icon="🪄")
st.title("🪄 Suno AI Prompt Architect")
st.markdown("Instantly extract a song's musical DNA for Suno AI.")

col1, col2 = st.columns(2)
with col1:
    song_title = st.text_input("Song Title", placeholder="e.g. C.R.E.A.M.")
with col2:
    artist_name = st.text_input("Artist", placeholder="e.g. Wu-Tang Clan")

if st.button("Generate DNA Prompt", use_container_width=True):
    if song_title and artist_name:
        with st.spinner(f"Extracting DNA for {song_title}..."):
            result = generate_suno_prompt(song_title, artist_name)
            
            if "Error" in result:
                st.error("API Connection Issue. Please check your API Key in Streamlit Secrets.")
                st.info("Technical details: " + result)
            else:
                st.subheader("🚀 Suno Style Box:")
                st.code(result, language="text")
                st.success("DNA Prompt Generated!")
                
                with st.expander("How to use this"):
                    st.write("1. Open Suno AI.")
                    st.write("2. Switch to **Custom Mode**.")
                    st.write("3. Paste the code above into the **'Style of Music'** box.")
    else:
        st.error("Please enter both a song title and an artist.")

st.divider()
st.caption("v3.0 - High Compatibility Mode (No-Search)")
