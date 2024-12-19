import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import os

def noise_reduction(input_audio, sr):
    """Apply noise reduction using spectral gating."""
    # Perform Short-Time Fourier Transform (STFT)
    stft = librosa.stft(input_audio)
    magnitude, phase = librosa.magphase(stft)

    # Estimate the noise profile
    noise_profile = np.mean(magnitude[:, :10], axis=1)

    # Reduce noise by subtracting noise profile from the magnitude
    reduced_magnitude = np.maximum(magnitude - noise_profile[:, np.newaxis], 0)

    # Reconstruct the audio with the phase
    reduced_audio = librosa.istft(reduced_magnitude * phase)
    return reduced_audio

def separate_voice(input_audio, sr):
    """Separate vocals and accompaniment using harmonic-percussive source separation."""
    # Perform harmonic-percussive source separation
    harmonic, percussive = librosa.effects.hpss(input_audio)
    return harmonic, percussive

def main():
    # Input audio file path
    input_audio_path = r'voice_seperation/callrecording.wav'  # Use raw string or forward slashes
    output_directory = 'output/'

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Load the audio file
    print("Loading audio file...")
    audio, sr = librosa.load(input_audio_path, sr=None)

    # Step 1: Perform noise reduction
    print("Performing noise reduction...")
    reduced_audio = noise_reduction(audio, sr)

    # Ensure valid format for output
    if len(reduced_audio.shape) > 1:
        reduced_audio = reduced_audio.flatten()
    reduced_audio = reduced_audio.astype('float32')

    # Save the noise-reduced audio
    noise_reduced_path = f"{output_directory}noise_reduced.wav"
    sf.write(noise_reduced_path, reduced_audio, sr)
    print(f"Noise-reduced audio saved to: {noise_reduced_path}")

    # Step 2: Separate voice and background music
    print("Separating voice and background...")
    harmonic, percussive = separate_voice(reduced_audio, sr)

    # Save the separated components
    vocals_path = f"{output_directory}vocals.wav"
    accompaniment_path = f"{output_directory}accompaniment.wav"
    sf.write(vocals_path, harmonic, sr)
    sf.write(accompaniment_path, percussive, sr)
    print(f"Vocals saved to: {vocals_path}")
    print(f"Accompaniment saved to: {accompaniment_path}")

if __name__ == "__main__":
    main()
