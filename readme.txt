1. Download VBCable_MACDriver_Pack108.zip for Mac from
https://vb-audio.com/Cable/index.htm

2. Install Driver.

3. Start Driver.

4. Open Mac Settings > Sound
Select VB-Cable as Output AND Input device (Type "Virtual"). Note that you will not be able to hear the sound through your speakers or headphones any more, since it is routed to VB Audio.
Create an Aggregate Device in MacOS "MIDI Audio Setup" with VB-Cable and your speakers with VB-Cable being the clock giver. 
Configure speakers with Channel 1 to VB-Cable and Channel 3 to your speakers. 
The stereo signal will be split and you will hear one half and the other will be routed to whisper.

5. in CLI install python packages: pip install whisper sounddevice numpy torch

5. You are ready to run live_transcribe.py in the Terminal!

6. Play a youtube video or any other speech media and see the Transcript being generated live (every buffer_duration period) and saved in an output .txt file !

30 seconds as buffer duration is recommended.
You can specify different model sizes. "small" performs very well for German language already. (read more on https://huggingface.co/docs/transformers/model_doc/whisper)

To enable MPS / apple GPU, try modifying the code according to advice on:
https://huggingface.co/docs/transformers/model_doc/whisper