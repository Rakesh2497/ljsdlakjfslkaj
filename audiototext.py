import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.utils import which
import subprocess
import sys

class AudioToText:
    def __init__(self):
        """Initialize the AudioToText converter with speech recognition."""
        self.recognizer = sr.Recognizer()
        self._check_ffmpeg()
    
    def _check_ffmpeg(self):
        """Check if FFmpeg is available for OPUS file conversion."""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: FFmpeg not found. OPUS files require FFmpeg for conversion.")
            print("Install FFmpeg:")
            print("  macOS: brew install ffmpeg")
            print("  Ubuntu/Debian: sudo apt install ffmpeg")
            print("  Windows: Download from https://ffmpeg.org/download.html")
    
    def convert_opus_to_wav(self, opus_file, output_file=None):
        """
        Convert OPUS file to WAV using FFmpeg directly for better compatibility.
        
        Args:
            opus_file (str): Path to OPUS audio file
            output_file (str): Path to output WAV file (optional)
            
        Returns:
            str: Path to the converted WAV file
        """
        if not output_file:
            base_name = os.path.splitext(opus_file)[0]
            output_file = f"{base_name}_converted.wav"
        
        try:
            # Use FFmpeg to convert OPUS to WAV
            cmd = [
                'ffmpeg', '-i', opus_file,
                '-acodec', 'pcm_s16le',  # 16-bit PCM
                '-ar', '16000',          # 16kHz sample rate (good for speech recognition)
                '-ac', '1',              # Mono channel
                '-y',                    # Overwrite output file
                output_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"FFmpeg conversion failed: {result.stderr}")
            
            return output_file
            
        except FileNotFoundError:
            raise Exception("FFmpeg not found. Please install FFmpeg to convert OPUS files.")
        except Exception as e:
            raise Exception(f"Error converting OPUS file: {e}")
        
    def convert_audio_format(self, input_file, output_file=None):
        """
        Convert audio file to WAV format if needed.
        
        Args:
            input_file (str): Path to input audio file
            output_file (str): Path to output WAV file (optional)
            
        Returns:
            str: Path to the WAV file
        """
        if not output_file:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_converted.wav"
        
        # Handle OPUS files specifically
        if input_file.lower().endswith('.opus'):
            return self.convert_opus_to_wav(input_file, output_file)
        
        # Handle other formats with pydub
        try:
            audio = AudioSegment.from_file(input_file)
            audio.export(output_file, format="wav")
            return output_file
        except Exception as e:
            # Fallback to FFmpeg for any format pydub can't handle
            print(f"Pydub failed, trying FFmpeg: {e}")
            return self.convert_opus_to_wav(input_file, output_file)
    
    def transcribe_audio(self, audio_file, language='en-US'):
        """
        Convert audio file to text transcript.
        
        Args:
            audio_file (str): Path to audio file
            language (str): Language code for recognition (default: 'en-US')
            
        Returns:
            str: Transcribed text
        """
        try:
            # Convert to WAV if not already (especially important for OPUS)
            if not audio_file.lower().endswith('.wav'):
                print(f"Converting {audio_file} to WAV format...")
                audio_file = self.convert_audio_format(audio_file)
            
            # Load audio file
            with sr.AudioFile(audio_file) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Record the audio
                audio_data = self.recognizer.record(source)
            
            # Perform speech recognition
            text = self.recognizer.recognize_google(audio_data, language=language)
            
            return text
            
        except sr.UnknownValueError:
            return "Could not understand the audio"
        except sr.RequestError as e:
            return f"Error with the speech recognition service: {e}"
        except FileNotFoundError:
            return f"Audio file not found: {audio_file}"
        except Exception as e:
            return f"An error occurred: {e}"
    
    def transcribe_long_audio(self, audio_file, chunk_length_ms=60000, language='en-US'):
        """
        Transcribe long audio files by splitting into chunks.
        
        Args:
            audio_file (str): Path to audio file
            chunk_length_ms (int): Length of each chunk in milliseconds (default: 60 seconds)
            language (str): Language code for recognition
            
        Returns:
            str: Complete transcribed text
        """
        try:
            # Convert OPUS to WAV first if needed
            if audio_file.lower().endswith('.opus'):
                print(f"Converting OPUS file {audio_file} to WAV format...")
                audio_file = self.convert_opus_to_wav(audio_file)
            
            # Load the audio file
            audio = AudioSegment.from_file(audio_file)
            
            # Split audio into chunks
            chunks = []
            for i in range(0, len(audio), chunk_length_ms):
                chunk = audio[i:i + chunk_length_ms]
                chunks.append(chunk)
            
            # Transcribe each chunk
            full_transcript = []
            
            for i, chunk in enumerate(chunks):
                # Export chunk to temporary file
                chunk_file = f"temp_chunk_{i}.wav"
                chunk.export(chunk_file, format="wav")
                
                # Transcribe chunk
                chunk_text = self.transcribe_audio(chunk_file, language)
                full_transcript.append(chunk_text)
                
                # Clean up temporary file
                os.remove(chunk_file)
                
                print(f"Processed chunk {i+1}/{len(chunks)}")
            
            return " ".join(full_transcript)
            
        except Exception as e:
            return f"Error processing long audio: {e}"

def main():
    """Example usage of the AudioToText converter."""
    converter = AudioToText()
    
    # Example usage
    audio_file = input("Enter the path to your audio file: ").strip()
    
    if not os.path.exists(audio_file):
        print(f"File not found: {audio_file}")
        return
    
    print("Transcribing audio... This may take a moment.")
    
    # For files longer than 1 minute, use chunk processing
    audio = AudioSegment.from_file(audio_file)
    if len(audio) > 60000:  # 60 seconds
        print("Long audio detected. Processing in chunks...")
        transcript = converter.transcribe_long_audio(audio_file)
    else:
        transcript = converter.transcribe_audio(audio_file)
    
    print("\n" + "="*50)
    print("TRANSCRIPT:")
    print("="*50)
    print(transcript)
    
    # Save transcript to file
    output_file = f"{os.path.splitext(audio_file)[0]}_transcript.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(transcript)
    
    print(f"\nTranscript saved to: {output_file}")

if __name__ == "__main__":
    main()
