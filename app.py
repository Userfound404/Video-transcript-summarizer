import streamlit as st
import requests
from transformers import pipeline
import tensorflow as tf
from youtube_transcript_api import YouTubeTranscriptApi


# Create a function to summarize the transcript
def summarize_transcript(transcript, max_length=512):
    summarizer = pipeline("summarization")
    transcript_text = [t['text'] for t in transcript]
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

if __name__ == "__main__":
    main()
