import streamlit as st
import requests
from transformers import pipeline
import tensorflow as tf
# from IPython.display import YouTubeVideo
from youtube_transcript_api import YouTubeTranscriptApi

# Create a function to summarize the transcript
def summarize_transcript(result):
    summarizer = pipeline('summarization')
    num_iters = int(len(result) / 1000)
    summarized_text = []
    for i in range(0, num_iters + 1):
        start = 0
        start = i * 1000
        end = (i + 1) * 1000
        st.text_area("input text \n" + result[start:end])
        out = summarizer(result[start:end])
        out = out[0]
        out = out['summary_text']
        st.text_area("Summarized text\n" + out)
        summarized_text.append(out)


# Create the main Streamlit app
def main():
    st.title("Video Transcript Summarizer")

    # Retrieve the transcript for the video
    video_url = st.text_input("Enter the URL of the video:")
    video_parts = video_url.split("=")
    try:
        if len(video_parts) < 2:
            st.write("Error: Invalid video URL")
            return
        video_id = video_parts[1]
        # video_id = video_url.split("=")[1]
        YouTubeTranscriptApi.get_transcript(video_id)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript[0:5]
    except requests.exceptions.RequestException as e:
        st.write("Error retrieving transcript:", e)
        return

    # Display the transcript and a summary of it
    st.markdown("**Transcript:**")
    st.text_area("transcript", transcript, height=400)
    st.markdown("**Summary:**")
    st.text_area("summary", summarize_transcript(transcript))


# Run the Streamlit app
if __name__ == "__main__":
    main()