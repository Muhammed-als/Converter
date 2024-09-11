import os
import ffmpeg

def convert_m3u8_to_mp4(m3u8_url, output_path):
    try:
        # Input M3U8 stream (from URL)
        stream = ffmpeg.input(m3u8_url)
        
        # Convert and output to MP4 format
        stream = ffmpeg.output(stream, output_path)
        
        # Execute the conversion
        ffmpeg.run(stream)
        
        print(f"Conversion successful! Saved as {output_path}")
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode('utf8')}")

# Example usage with URL from your m3u8 file
m3u8_url = 'https://vod-cache.kaltura.nordu.net/hls/p/282/sp/28200/serveFlavor/entryId/0_wkq9s9h3/v/2/ev/2/flavorId/0_km6nvnd4/name/a.mp4/index.m3u8'
output_file = 'output_video8.mp4'

convert_m3u8_to_mp4(m3u8_url, output_file)
