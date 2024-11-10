import whisper
import sounddevice as sd
import numpy as np
import torch
import queue
import sys
import time
from scipy.signal import resample  # For downsampling


print(sd.query_devices()) # show operating in- and output devices

# for future GPU implementation
if torch.backends.mps.is_available():
    device = torch.device("mps")  # Use "mps" for Apple Silicon GPU
    print("MPS backend is available.")

# choose model
model_size = ['tiny', 'base', 'small' , 'medium', 'large', 'turbo'] # pass desired model size in the model loading line
# Load Whisper model (change 'small' to other sizes if desired) 
model = whisper.load_model(model_size[3], #device=device #GPU seems not be supported currently
) # the chosen model - here the 'small' model will be downloaded upon execution of the script

# choose language
languages = ['english', 'german', 'french', 'spanish', 'italian', 'chinese', 'greek', 'russian','japanese'] # complete list of languages available at https://platform.openai.com/docs/guides/speech-to-text/supported-languages
language = languages[0]     

#choose input device
device_options = ['VB-Cable', 'Blackhole 2ch', 'Aggregate Device', 'MacBook Pro Microphone'] 
device = device_options[2]      # choose device that routes output to input - should match system output and input

# Set parameters for audio capture
input_sample_rate = 48000  # Match VB-Audio's 48 kHz output
target_sample_rate = 16000  # Whisper requires 16 kHz input
buffer_duration = 30  # Duration to accumulate audio data in seconds
q = queue.Queue()  # Queue to hold audio data for processing

# Open a file to save transcriptions
with open("transcription_output.txt", "w") as file:

    def callback(indata, frames, time, status):
        """Callback function to process audio stream data in real time."""
        if status:
            print(f"Error: {status}", file=sys.stderr)
        q.put(indata.copy())  # Add audio data to the queue

    # Start audio stream
    with sd.InputStream(device=device,
                        samplerate=input_sample_rate, channels=1, callback=callback):
        print("Listening for audio... Press Ctrl+C to stop.")

        try:
            audio_buffer = np.array([])  # Buffer to accumulate audio data

            # Continuously process audio from the queue
            while True:
                if not q.empty():
                    # Retrieve and accumulate audio data from the queue
                    audio_data = q.get()
                    audio_data = np.squeeze(audio_data)
                    audio_buffer = np.concatenate((audio_buffer, audio_data))

                    # Check if we've accumulated enough audio for transcription
                    if len(audio_buffer) >= buffer_duration * input_sample_rate:
                        # Check for silence (i.e., maximum amplitude close to zero)
                        if np.max(np.abs(audio_buffer)) < 0.01:  # Adjust threshold if needed
                            print("Silence detected, skipping transcription.")
                            audio_buffer = np.array([])  # Reset buffer
                            continue  # Skip this iteration if only silence

                        # Normalize and downsample audio data
                        audio_data = audio_buffer / np.max(np.abs(audio_buffer))
                        num_samples = int(len(audio_data) * target_sample_rate / input_sample_rate)
                        audio_data = resample(audio_data, num_samples)

                        # Convert audio data to float32 to avoid dtype mismatch
                        audio_data = audio_data.astype(np.float32)

                        # Transcribe the downsampled audio data using Whisper
                        result = model.transcribe(audio_data, fp16=False, language=language)

                        # Print and save the transcription
                        text = result["text"]
                        print("Transcription:", text)
                        file.write(text + "\n")
                        file.flush()  # Ensure the text is written to the file in real time

                        # Clear the buffer
                        audio_buffer = np.array([])

        except KeyboardInterrupt:
            print("\nTranscription stopped by user.")