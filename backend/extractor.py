import yt_dlp

def get_video_transcript(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    # Configure yt-dlp to grab metadata + subtitles only
    ydl_opts = {
        'skip_download': True,      # Don't download video
        'writesubtitles': True,     # Grab manual subs
        'writeautomaticsub': True,  # Grab auto-generated subs if manual missing
        'subtitleslangs': ['en'],   # Prefer English
        'quiet': True,              # Less noise in terminal
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 1. Extract Info
            info = ydl.extract_info(url, download=False)
            
            # 2. Find the Subtitles (Manual or Auto)
            subtitles = None
            if 'subtitles' in info and 'en' in info['subtitles']:
                subtitles = info['subtitles']['en']
            elif 'automatic_captions' in info and 'en' in info['automatic_captions']:
                subtitles = info['automatic_captions']['en']
            
            if not subtitles:
                return "Error: No English subtitles found."

            # 3. Download the JSON subtitle data
            # The structure is a list of formats. We want 'json3' or simple 'json'
            json_url = None
            for sub_format in subtitles:
                if sub_format['ext'] == 'json3' or sub_format['ext'] == 'json':
                    json_url = sub_format['url']
                    break
            
            if not json_url:
                # Fallback: If no JSON, grabbing raw text is harder without downloading.
                # Let's return a specific message if we hit this rare case.
                return "Error: Could not find JSON subtitle format."

            # 4. Fetch the actual text from the URL
            import requests
            response = requests.get(json_url)
            data = response.json()
            
            # 5. Parse the events
            full_text = ""
            events = data.get('events', [])
            for event in events:
                if 'segs' in event:
                    for seg in event['segs']:
                        if 'utf8' in seg:
                            full_text += seg['utf8'] + " "
                            
            return full_text.strip()

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    test_id = "kqtD5dpn9C8" 
    print(f"--- Extracting {test_id} ---")
    print(get_video_transcript(test_id))