import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import moviepy.editor as mp
import whisper

# Determine the base path for the executable
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# Load Whisper model globally
model = whisper.load_model("base")

# Function to extract audio from video and save as WAV
def video_to_audio(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)
    audio.close()
    video.close()

# Function to transcribe audio (WAV) to text
def audio_to_text(audio_path):
    result = model.transcribe(audio_path, fp16=False)
    return result["text"]

# Function to handle video processing
def process_video():
    video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("MP4 files", "*.mp4")])
    if not video_path:
        messagebox.showwarning("No file selected", "Please select a video file.")
        return

    try:
        video_path = os.path.normpath(video_path)
        audio_path = video_path.replace('.mp4', '.wav')
        transcript_path = video_path.replace('.mp4', '.txt')

        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file {video_path} not found.")

        status_label.config(text="Converting video to audio...")
        root.update_idletasks()
        video_to_audio(video_path, audio_path)
        
        status_label.config(text="Transcribing audio...")
        root.update_idletasks()
        text = audio_to_text(audio_path)

        with open(transcript_path, 'w') as f:
            f.write(text)

        status_label.config(text=f"Transcription saved to {transcript_path}")
        messagebox.showinfo("Success", f"Transcription saved to {transcript_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to handle audio processing
def process_audio():
    audio_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("WAV files", "*.wav")])
    if not audio_path:
        messagebox.showwarning("No file selected", "Please select an audio file.")
        return

    try:
        audio_path = os.path.normpath(audio_path)
        transcript_path = audio_path.replace('.wav', '.txt')

        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file {audio_path} not found.")

        status_label.config(text="Transcribing audio...")
        root.update_idletasks()
        text = audio_to_text(audio_path)

        with open(transcript_path, 'w') as f:
            f.write(text)

        status_label.config(text=f"Transcription saved to {transcript_path}")
        messagebox.showinfo("Success", f"Transcription saved to {transcript_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create main window
root = tk.Tk()
root.title("Video/Audio to Text Transcription")
root.geometry("500x350")
root.configure(bg="#2e2e2e")

# Create and add widgets
title_label = tk.Label(root, text="Video/Audio to Text Transcription", font=("Helvetica", 16), bg="#2e2e2e", fg="#ffffff")
title_label.pack(pady=10)

description_label = tk.Label(root, text="Choose an option to transcribe audio.", font=("Helvetica", 12), bg="#2e2e2e", fg="#ffffff")
description_label.pack(pady=5)

video_button = tk.Button(root, text="Convert Video (MP4) to WAV and Transcribe", command=process_video, font=("Helvetica", 12), bg="#4caf50", fg="#ffffff", relief=tk.RAISED)
video_button.pack(pady=10, padx=20, fill=tk.X)

audio_button = tk.Button(root, text="Transcribe Audio (WAV) to Text", command=process_audio, font=("Helvetica", 12), bg="#2196f3", fg="#ffffff", relief=tk.RAISED)
audio_button.pack(pady=10, padx=20, fill=tk.X)

status_label = tk.Label(root, text="", font=("Helvetica", 10), bg="#2e2e2e", fg="#ffffff")
status_label.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
