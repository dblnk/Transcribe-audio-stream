# Transcribe-audio-stream
This small python script will enable you to perform speech to text transcription in real-time from any audio source, whether from device sound output or input, when combined with the right audio routing drivers.
The script will use OpenAI's Whisper speech-to-text AI models (read more on https://huggingface.co/docs/transformers/model_doc/whisper). 
Generation of the script was assisted by OpenAI's ChatGPT.

## Purpose
You might want to save yourself the trouble of taking notes and automatically transcribe any youtube video, podcast, call, online meeting or event in real-time. 
The audio is saved only temporarily in your memory's cache for a period defined by the audio buffer length.
By the end of the program you will have a text file with transcription of the audio that you played during execution of the script.

## Requirements
You will need to install sounddevice, numpy and whisper python packages.
```bash
pip install -r requirements.txt
```

The code was tested on MacOS Sonoma 14.7.1.  
Workflow / pipeline suggestions for other systems are greatly appreciated.

## Step-by-step instruction to use

1. Download VBCable_MACDriver_Pack108.zip for Mac from
https://vb-audio.com/Cable/index.htm 
or any other audio routing driver. Windows users might profit from Voicemeeter available from https://vb-audio.com/Voicemeeter/

2. Install Driver.

3. Start Driver.

4. 
- Option A (you won't hear the sound from your speakers any more, as the sound output is routed virtually to Whisper)  
Open Mac Settings > Sound  
Select VB-Cable as Output AND Input device (Type "Virtual"). Note that you will not be able to hear the sound through your speakers or headphones any more, since it is routed to VB Audio.  
Make sure to adjust the device definition in the script to 'VB-Cable'

```python
device_options = ['VB-Cable', 'Blackhole 2ch', 'Aggregate Device', 'MacBook Pro Microphone'] 
device = device_options[0]   
```

- Option B (you will hear one of the two stereo fields through your speaker while the other will be routed to VB Audio)  
Create an Aggregate Device in MacOS "MIDI Audio Setup" using VB-Cable and your speakers, with VB-Cable being the clock source.  
"Configure Speakers" with Channel 1 to VB-Cable and Channel 3 to your speaker.  
The stereo signal will be split and you will hear one half and the other will be routed to whisper.  
Open Mac Settings > Sound and select Aggregate Device as Output AND Input Devices.  
Make sure to adjust the device definition in the script to 'VB-Cable'

```python
device_options = ['VB-Cable', 'Blackhole 2ch', 'Aggregate Device', 'MacBook Pro Microphone'] 
device = device_options[2]   
```

5. You are ready to run transcribe-audio-stream.py in the Terminal!  
Just adjust the input language and model sizes and buffer duration for optimal performance. Medium model is recommended for non-English languages. 30 seconds audio buffer duration are set as default.

```python
# choose model
model_size = ['tiny', 'base', 'small' , 'medium', 'large', 'turbo'] # pass desired model size in the model loading line
# Load Whisper model (change 'small' to other sizes if desired) 
model = whisper.load_model(model_size[2], #device=device 
)

# choose language
languages = ['english', 'german', 'french', 'spanish', 'italian', 'chinese', 'greek', 'russian','japanese'] # complete list of languages available at https://platform.openai.com/docs/guides/speech-to-text/supported-languages
language = languages[0]

# Set parameters for audio capture
input_sample_rate = 48000  # Match VB-Audio's 48 kHz output
target_sample_rate = 16000  # Whisper requires 16 kHz input
buffer_duration = 30  # Duration to accumulate audio data in seconds
```

6. Play a youtube video or any other speech media and see the Transcript being generated live (every buffer_duration period) and saved in an output .txt file ! Press Ctrl+C to stop transcript generation.


## Future work
To enable MPS / apple GPU, try modifying the code according to advice on:  
https://huggingface.co/docs/transformers/model_doc/whisper

