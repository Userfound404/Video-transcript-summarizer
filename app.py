import streamlit as st
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
import tensorflow as tf

# Allow user to enter YouTube video URL
youtube_video = st.text_input("Enter YouTube video URL:")

# Extract video ID and retrieve transcript
video_id = youtube_video.split("=")[1]
if len(split_url) >= 2:
  video_id = split_url[1]
else:
  st.write("Error: Invalid YouTube video URL")
transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Concatenate transcript text into single string
result = ""
for i in transcript:
    result += ' ' + i['text']

# Create text summarization pipeline
summarizer = pipeline('summarization')

# Divide result string into chunks and summarize each chunk
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

# Display summarized text to user
st.markdown("Summarized text:")
st.markdown(str(summarized_text))