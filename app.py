import streamlit as st
import requests
from transformers import pipeline
import tensorflow as tf
from youtube_transcript_api import YouTubeTranscriptApi


# Create a function to summarize the transcript
def summarize_transcript(transcript, max_length=512):
    transcript_text = ' '.join([t['text'] for t in transcript])
    summarizer = pipeline("summarization",max_length=max_length)
    summary = summarizer(transcript_text)[0]["summary_text"]
    return summary

# Create the main Streamlit app

def main():
    
    st.title("Video Transcript Summarizer")
    video_url = st.text_input("Enter the URL of the video:")
    try:
        video_id = video_url.split("=")[1]
    except IndexError:
        st.write("Error: Invalid video URL")
        return

    try:
        YouTubeTranscriptApi.get_transcript(video_id)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except requests.exceptions.RequestException as e:
        st.write("Error retrieving transcript:", e)
        return

    # Display the video preview and transcript
    st.markdown("**Video Preview:**")
    st.video(video_url)
    transcript_text = ' '.join([t['text'] for t in transcript])
    st.markdown("**Transcript:**")
    st.text_area("transcript", transcript_text, height=400)

    # Create a slider widget for customizing the size of the summary
    max_length = st.slider("Summary size:", min_value=256, max_value=1024, value=512, step=256)

    # Display the summary of the transcript
    st.markdown("**Summary:**")
    st.text_area("summary", summarize_transcript(transcript, max_length=max_length))
