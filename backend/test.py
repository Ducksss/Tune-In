from pydub import AudioSegment
import numpy as np

speech_file = 'sing4.mp3'
music_file = 'bg1.mp3'
output_file = "output2.mp3"

# Load the speech clip
speech_clip = AudioSegment.from_file(speech_file)

# Define the desired pitch correction factor (adjust as needed)
pitch_correction_factor = 1.0  # For example, double the pitch

# Convert the speech clip to a NumPy array for processing
speech_data = np.array(speech_clip.get_array_of_samples())

print(speech_clip.get_array_of_samples())

# Apply the pitch correction by multiplying the pitch correction factor
corrected_speech_data = speech_data * pitch_correction_factor

print(speech_clip.frame_rate, speech_clip.sample_width, speech_clip.channels)

# Convert the corrected audio data back to an AudioSegment
corrected_speech_clip = AudioSegment(
    corrected_speech_data.tobytes(),
    frame_rate=speech_clip.frame_rate,
    sample_width=speech_clip.sample_width,
    channels=speech_clip.channels,
)

# Save the corrected speech to a file
corrected_speech_clip.export("corrected_speech1.mp3", format="mp3")

# Load the music clip
music_clip = AudioSegment.from_file(music_file)

volume_adjustment_dB = -7

lowered_music_clip = music_clip + volume_adjustment_dB

# Load the corrected speech clip
corrected_speech_clip = AudioSegment.from_file(speech_file)

# Adjust the length of the speech clip to match the music clip if needed
corrected_speech_clip = corrected_speech_clip[:len(lowered_music_clip)]

# Combine the speech and music
combined_audio = corrected_speech_clip.overlay(lowered_music_clip)

# Export the combined audio
combined_audio.export(output_file, format="mp3")
