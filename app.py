import streamlit as st
import requests
from transformers import pipeline
import tensorflow as tf
from youtube_transcript_api import YouTubeTranscriptApi


# Create a function to summarize the transcript
def summarize_transcript(transcript, max_length=512):
    summarizer = pipeline("summarization")
    summary = summarizer(transcript)[0]["summary_text"]
    return summary

# Create the main Streamlit app
def main():
    st.title("Video Transcript Summarizer")

    # Retrieve the transcript for the video
    video_url = st.text_input("Enter the URL of the video:")
    video_id = video_url.split("=")[1]
    try:
        # video_id = video_url.split("=")[1]
        YouTubeTranscriptApi.get_transcript(video_id)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except requests.exceptions.RequestException as e:
        st.write("Error retrieving transcript:", e)
        return

    # Display the video preview and transcript
    st.markdown("**Video Preview:**")
    st.video(video_url)
    st.markdown("**Transcript:**")
    st.text_area("transcript", transcript, height=400)

    # Display the summary of the transcript
    st.markdown("**Summary:**")
    st.text_area("summary", summarize_transcript(transcript))

if __name__ == "__main__":
    main()