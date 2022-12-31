import streamlit as st
import requests
from transformers import pipeline
import tensorflow as tf
from youtube_transcript_api import YouTubeTranscriptApi

# Create a function to summarize the transcript
def summarize_transcript(transcript, buffer_length=50):
    summarizer = pipeline("summarization",model='t5-base')
    transcript_text = ' '.join([t['text'] for t in transcript])
    max_length = len(transcript_text) + buffer_length
    # Divide the transcript into shorter chunks
    chunk_size = max_length - 2  # Leave some space for the summarizer to add punctuation
    chunks = [transcript_text[i:i + chunk_size] for i in range(0, len(transcript_text), chunk_size)]

    # Summarize each chunk separately
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=max_length)[0]["summary_text"]
        summaries.append(summary)

    # Join the summaries back together
    summary = ' '.join(summaries)

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
    transcript_text = ' '.join([t['text'] for t in transcript])
    st.text_area("transcript", transcript_text, height=400)

    # Display the summary of the transcript
    st.markdown("**Summary:**")
    st.text_area("summary", summarize_transcript(transcript))

if __name__ == "__main__":
    main()