import streamlit as st
import requests
from transformers import pipeline
import tensorflow as tf
from youtube_transcript_api import YouTubeTranscriptApi

# Create a function to summarize the transcript
def summarize_video(url):
    video_id = url.split("=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    result = ""
    for i in transcript:
        result += ' ' + i['text']
    summarizer = pipeline('summarization')
    num_iters = int(len(result)/1000)
    summarized_text = []
    for i in range(0, num_iters + 1):
        start = 0
        start = i * 1000
        end = (i + 1) * 1000
        out = summarizer(result[start:end])
        out = out[0]
        out = out['summary_text']
        summarized_text.append(out)
    return " ".join(summarized_text)

st.title("YouTube Video Summarizer")
url = st.text_input("Enter a YouTube URL:")
if st.button("Summarize"):
    summary = summarize_video(url)
    st.success(summary)

    # Display the video preview and transcript
st.markdown("**Video Preview:**")
st.video(video_url)
st.markdown("**Transcript:**")
transcript_text = ' '.join([t['text'] for t in transcript])
st.text_area("transcript", transcript_text, height=400)

 # Display the summary of the transcript
st.markdown("**Summary:**")
st.text_area("summary", summarize_transcript(transcript))