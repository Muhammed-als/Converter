import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from moviepy.editor import VideoFileClip
import os
import whisper;
from pydub import AudioSegment
from PIL import Image
from pdf2docx import Converter
import yt_dlp
model = whisper.load_model("base")
# Function to handle file selection
def select_file():
    conversion_type = conversion_type_var.get()
    if conversion_type == "MP4 to WAV" or "MP4 to GIF":
        file_types = [("MP4 files", "*.mp4"), ("All files", "*.*")]
    elif conversion_type == "WAV to Text" or conversion_type == "WAV to MP3":
        file_types = [("WAV files", "*.wav"), ("All files", "*.*")]
    elif conversion_type == "JPG to PNG" or conversion_type == "JPG to WebP":
        file_types = [("JPG files", "*.JPG"), ("All files", "*.*")]
    elif conversion_type == "PNG to JPG" or conversion_type == "PNG to WebP":
        file_types = [("PNG files", "*.png"), ("All files", "*.*")]
    elif conversion_type == "PDF to Word (DOCX)":
        file_types = [("PDF files", "*.pdf"), ("All files", "*.*")]
    else:
        file_types = [("All files", "*.*")]  # Default to all file types if no specific conversion type is selected

    # Open file dialog with the appropriate file filter
    file_path = filedialog.askopenfilename(filetypes=file_types)

    # If a file was selected, insert it into the entry field
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

# Function to convert MP4 to WAV
def convert_mp4_to_wav(input_file):
    try:
        # Load the MP4 video file
        video = VideoFileClip(input_file)
        
        # Extract the audio
        audio = video.audio
        
        # Set output file name (same as input file, but with .wav extension)
        output_file = os.path.splitext(input_file)[0] + ".wav"
        
        # Write the audio to WAV file
        audio.write_audiofile(output_file)
        
        messagebox.showinfo("Success", f"Converted to WAV: {output_file}")
    except Exception as e:
        messagebox.showerror("Conversion Error", f"An error occurred: {e}")

# Function to transcribe audio (WAV) to text
def audio_to_text(audio_path):
    result = model.transcribe(audio_path, fp16=False)
    return result["text"]
# Function to handle audio processing
def convert_wav_to_text(input_file):
    if not input_file.endswith('.wav'):
        messagebox.showwarning("Invalid file type", "Please select a WAV audio file.")
        return
    try:
        audio_path = os.path.normpath(input_file)  # Use the input_file directly
        transcript_path = audio_path.replace('.wav', '.txt')

        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file {audio_path} not found.")

        root.update_idletasks()  # This will keep the UI responsive during processing
        text = audio_to_text(audio_path)  # Convert the audio to text using the transcribe function

        # Write the transcribed text to a file
        with open(transcript_path, 'w') as f:
            f.write(text)

        messagebox.showinfo("Success", f"Transcription saved to {transcript_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
# Function to convert WAV to MP3
def convert_wav_to_mp3(input_file):
    if not input_file.endswith('.wav'):
        messagebox.showwarning("Invalid file type", "Please select a WAV audio file.")
        return

    try:
        # Load the WAV file
        audio = AudioSegment.from_wav(input_file)
        
        # Set output file name (same as input file, but with .mp3 extension)
        output_file = os.path.splitext(input_file)[0] + ".mp3"
        
        # Export the audio to MP3
        audio.export(output_file, format="mp3")
        
        messagebox.showinfo("Success", f"Converted to MP3: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
# Function to convert MP4 to GIF
def convert_mp4_to_gif(input_file):
    if not input_file.endswith('.mp4'):
        messagebox.showwarning("Invalid file type", "Please select an MP4 video file.")
        return

    try:
        # Load the MP4 video file
        video = VideoFileClip(input_file)
        
        # Set output file name (same as input file, but with .gif extension)
        output_file = os.path.splitext(input_file)[0] + ".gif"
        
        # Write the video to GIF file
        video.write_gif(output_file)
        
        messagebox.showinfo("Success", f"Converted to GIF: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
# Function to convert JPG to PNG
def convert_jpg_to_png(input_file):
    if not input_file.lower().endswith('.jpg') and not input_file.lower().endswith('.jpeg'):
        messagebox.showwarning("Invalid file type", "Please select a JPG image file.")
        return

    try:
        # Open the JPG file
        with Image.open(input_file) as img:
            # Set output file name (same as input file, but with .png extension)
            output_file = os.path.splitext(input_file)[0] + ".png"
            # Convert and save the image as PNG
            img.save(output_file, 'PNG')
        
        messagebox.showinfo("Success", f"Converted to PNG: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
# Function to convert JPG to WebP
def convert_jpg_to_webp(input_file):
    if not input_file.lower().endswith('.jpg') and not input_file.lower().endswith('.jpeg'):
        messagebox.showwarning("Invalid file type", "Please select a JPG image file.")
        return

    try:
        # Open the JPG file
        with Image.open(input_file) as img:
            # Set output file name (same as input file, but with .webp extension)
            output_file = os.path.splitext(input_file)[0] + ".webp"
            # Convert and save the image as WebP
            img.save(output_file, 'WEBP')
        
        messagebox.showinfo("Success", f"Converted to WebP: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
def convert_png_to_jpg(input_file):
    if not input_file.lower().endswith('.png'):
        messagebox.showwarning("Invalid file type", "Please select a PNG image file.")
        return

    try:
        # Open the PNG file
        with Image.open(input_file) as img:
            # Set output file name (same as input file, but with .jpg extension)
            output_file = os.path.splitext(input_file)[0] + ".jpg"
            # Convert to RGB (JPG doesn't support alpha channel)
            rgb_img = img.convert('RGB')
            # Save the image as JPG
            rgb_img.save(output_file, 'JPEG')
        
        messagebox.showinfo("Success", f"Converted to JPG: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
# Function to convert PNG to WebP
def convert_png_to_webp(input_file):
    if not input_file.lower().endswith('.png'):
        messagebox.showwarning("Invalid file type", "Please select a PNG image file.")
        return

    try:
        # Open the PNG file
        with Image.open(input_file) as img:
            # Set output file name (same as input file, but with .webp extension)
            output_file = os.path.splitext(input_file)[0] + ".webp"
            # Save the image as WebP
            img.save(output_file, 'WEBP')
        
        messagebox.showinfo("Success", f"Converted to WebP: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
# Function to convert PDF to Word (DOCX)
def convert_pdf_to_word(input_file):
    if not input_file.lower().endswith('.pdf'):
        messagebox.showwarning("Invalid file type", "Please select a PDF file.")
        return

    try:
        # Set output file name (same as input file, but with .docx extension)
        output_file = os.path.splitext(input_file)[0] + ".docx"
        
        # Convert PDF to DOCX
        cv = Converter(input_file)
        cv.convert(output_file)
        cv.close()

        messagebox.showinfo("Success", f"Converted to Word (DOCX): {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
# Function to download a video from a social media URL as MP4
def download_video_as_mp4(url):
    if not url:
        messagebox.showwarning("Invalid URL", "Please provide a valid video URL.")
        return

    try:
        # Set up yt-dlp options for MP4 format
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',  # Select the best video and audio and combine them into MP4
            'outtmpl': '%(title)s.%(ext)s',  # Save the file with the title of the video
        }
        
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        messagebox.showinfo("Success", "Video downloaded as MP4 successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
# Function to perform the conversion
def convert_file():
    input_file = file_entry.get()
    conversion_type = conversion_type_var.get()
    
    if not input_file:
        messagebox.showwarning("Input Error", "Please select a file to convert.")
        return

    if conversion_type == "Select conversion":
        messagebox.showwarning("Conversion Error", "Please select a conversion type.")
        return
    
    if conversion_type == "MP4 to WAV":
        convert_mp4_to_wav(input_file)
    elif conversion_type == "WAV to Text (TXT)":
        convert_wav_to_text(input_file)
    elif conversion_type == "WAV to MP3":
        convert_wav_to_mp3(input_file)
    elif conversion_type ==  "MP4 to GIF":
        convert_mp4_to_gif(input_file)
    elif conversion_type == "JPG to PNG":
        convert_jpg_to_png(input_file)
    elif conversion_type == "JPG to WebP":
        convert_jpg_to_webp(input_file)
    elif conversion_type == "PNG to JPG":
        convert_png_to_jpg(input_file)
    elif conversion_type == "PNG to WebP":
        convert_png_to_webp(input_file)
    elif conversion_type == "PDF to Word (DOCX)":
        convert_pdf_to_word(input_file)


# Create the main window
root = tk.Tk()
root.title("File Converter")

# Conversion Type Label and Dropdown
conversion_type_label = tk.Label(root, text="Select conversion type:")
conversion_type_label.grid(row=0, column=0, padx=10, pady=10)

conversion_type_var = tk.StringVar(root)
conversion_type_var.set("Select conversion")  # Default option

conversion_type_menu = ttk.Combobox(root, textvariable=conversion_type_var)
conversion_type_menu['values'] = ("Select conversion", "MP4 to WAV", "WAV to Text", "WAV to MP3", 
                                  "MP4 to GIF", "JPG to PNG", "JPG to WebP", "PNG to JPG", 
                                  "PNG to WebP", "PDF to Word (DOCX)")
conversion_type_menu.grid(row=0, column=1, padx=10, pady=10)

# File Selection
file_label = tk.Label(root, text="Select file:")
file_label.grid(row=1, column=0, padx=10, pady=10)

file_entry = tk.Entry(root, width=50)
file_entry.grid(row=1, column=1, padx=10, pady=10)

browse_button = tk.Button(root, text="Browse", command=select_file)
browse_button.grid(row=1, column=2, padx=10, pady=10)
convert_button = tk.Button(root, text="Convert", command=convert_file)
convert_button.grid(row=2, column=1, padx=5, pady=5)

# Create a label and entry field for the URL
url_label = tk.Label(root, text="Enter video URL:")
url_label.grid(row=3, column=0, padx=10, pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.grid(row=3, column=1, padx=10, pady=10)

# Create a button to download the video from URL
download_button = tk.Button(root, text="Download Video", command=lambda: download_video_as_mp4(url_entry.get()))
download_button.grid(row=3, column=2, padx=10, pady=10)

# Run the main loop
root.mainloop()
