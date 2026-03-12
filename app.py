import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

# --- CONFIGURATION ---
# Your Discogs Token is now integrated
DISCOGS_TOKEN = "NhcAlMBiHPZCcJThCcjvzmTQcFWfTMDQDUzPGgQh"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

def get_discogs_metadata(title, artist):
    """Fetches high-fidelity style and genre tags from Discogs."""
    search_url = "https://api.discogs.com/database/search"
    params = {
        "release_title": title,
        "artist": artist,
        "type": "release",
        "token": DISCOGS_TOKEN
    }
    try:
        response = requests.get(search_url, params=params, headers=HEADERS)
        data = response.json()
        if data.get('results'):
            res = data['results'][0]
            return {
                "genres": res.get("genre", []),
                "styles": res.get("style", []),
                "year": res.get("year", "Unknown"),
                "label": res.get("label", [""])[0]
            }
    except Exception as e:
        return None
    return None

def trace_samples(title, artist):
    """Scrapes WhoSampled to find the 'Source DNA' of a track."""
    # Format query for WhoSampled
    query = f"{artist} {title}".replace(" ", "+")
    search_url = f"https://www.whosampled.com/search/it/?q={query}"
    
samples_found = []
    try:
        # Step 1: Search for the song
        res = requests.get(search_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Get the first result link
        first_result = soup.select_one('li.listEntry h3 a')
        if first_result:
            track_url = "https://www.whosampled.com" + first_result['href']
            # Step 2: Go to the track page
            track_res = requests.get(track_url, headers=HEADERS, timeout=10)
            track_soup = BeautifulSoup(track_res.text, 'html.parser')
            
            # Find sample entries
            sample_sections = track_soup.select('.sampleEntry')
            for entry in sample_sections[:3]: # Analyze top 3 samples
                s_title = entry.select_one('.trackName').text.strip()
                s_artist = entry.select_one('.artistName').text.strip()
                samples_found.append({"title": s_title, "artist": s_artist})
    except:
        pass
    return samples_found

def create_suno_prompt(main_info, samples):
    """Synthesizes all metadata into a Suno-optimized string."""
    prompt_elements = []
    
    # 1. Base Genre/Style from Main Song
    if main_info:
        # Use 'Styles' (Discogs styles are very specific like 'Boom Bap' or 'G-Funk')
        prompt_elements.extend(main_info['styles'][:3])
        
    # 2. Add Sample DNA (The secret sauce)
    sample_styles = []
    for s in samples:
        s_meta = get_discogs_metadata(s['title'], s['artist'])
        if s_meta and s_meta['styles']:
            # We add keywords like 'Vintage' or 'Sampled' to the sample's style
            sample_styles.append(f"sampled {s_meta['styles'][0].lower()}")
            
    if sample_styles:
        prompt_elements.extend(sample_styles[:2])
        prompt_elements.append("warm analog textures")
        prompt_elements.append("vinyl crackle")
    
    # 3. Tone & Texture defaults for Suno
    prompt_elements.append("high quality production")
    
    # Clean up and join
    final_prompt = ", ".join(list(dict.fromkeys(prompt_elements))).lower()
    return final_prompt

# --- STREAMLIT UI ---
st.set_page_config(page_title="Suno DNA Architect", page_icon="🧬")

st.title("🧬 Suno DNA Architect")
st.markdown("Using **Discogs** and **WhoSampled** to extract the exact musical blueprint of a song.")

col1, col2 = st.columns(2)
with col1:
    song_input = st.text_input("Song Title", placeholder="e.g. C.R.E.A.M.")
with col2:
    artist_input = st.text_input("Artist", placeholder="e.g. Wu-Tang Clan")

if st.button("Generate Accurate Prompt", use_container_width=True):
    if song_input and artist_input:
        with st.status("Analyzing Musical Heritage...") as status:
            # 1. Main Song Search
            st.write("Searching Discogs for primary styles...")
            main_meta = get_discogs_metadata(song_input, artist_input)
            
            # 2. WhoSampled Search
            st.write("Tracing sample lineage on WhoSampled...")
            samples = trace_samples(song_input, artist_input)
            
            # 3. Final Prompt
            st.write("Synthesizing prompt...")
            final_prompt = create_suno_prompt(main_meta, samples)
            
            status.update(label="Analysis Complete!", state="complete")

        # RESULTS DISPLAY
        st.subheader("🚀 Optimized Suno Style Box:")
        st.code(final_prompt, language="text")
        
        with st.expander("View Data Sources"):
            st.write("**Discogs Styles Identified:**")
            st.write(main_meta['styles'] if main_meta else "None found")
            st.write("**Samples Traced:**")
            if samples:
                for s in samples: st.write(f"- {s['title']} by {s['artist']}")
            else:
                st.write("No samples detected in database.")
    else:
        st.warning("Please enter both song and artist.")

st.divider()
st.caption("Tip: Copy the code above into the 'Style of Music' box in Suno's Custom Mode.")