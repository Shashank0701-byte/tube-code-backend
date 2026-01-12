from youtube_transcript_api import YouTubeTranscriptApi

print("--- INSPECTING LIBRARY ---")
print("Library Version found on system.")

# This prints every single function available inside the class
print(dir(YouTubeTranscriptApi))

print("\n--- TRYING ALTERNATIVE ---")
try:
    # The modern API often prefers 'list_transcripts'
    print("Trying list_transcripts...")
    transcript_list = YouTubeTranscriptApi.list_transcripts("kqtD5dpn9C8")
    print("SUCCESS! 'list_transcripts' works.")
except Exception as e:
    print(f"list_transcripts failed: {e}")