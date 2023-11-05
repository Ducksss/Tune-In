from pydub import AudioSegment

voice = AudioSegment.from_file("sing.wav")
music = AudioSegment.from_file("bg.wav")

from aubio import source, pitch

voice = voice.set_channels(1)  # Convert to mono
voice = voice.set_frame_rate(44100)  # Set the sample rate to 44.1 kHz

voice_data = voice.raw_data
aubs_voice = source(voice_data, 0, 256)

pDetection = pitch("yin", 2048, 512, 44100)

voice_pitches = []
while True:
    samples, read = aubs_voice()
    pitch_value = pDetection(samples)[0]
    if pitch_value != 0:
        voice_pitches.append(pitch_value)
