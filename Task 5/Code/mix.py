import wave  # Import the `wave` module to work with WAV audio files
import numpy as np  # Import NumPy for numerical operations on audio data


def mix_wav_files(file1, file2, output_file, gain=1.0):
    # Define a function to mix two WAV files and save the result to a new file
    # `file1` and `file2` are the input WAV files
    # `output_file` is the path to the output WAV file
    # `gain` is a multiplier to adjust the volume of the mixed audio


    # Open the first WAV file
    with wave.open(file1, 'rb') as wav1:  # Open `file1` in read-binary mode
        params1 = wav1.getparams()  # Get the parameters (e.g., channels, framerate) of the WAV file
        frames1 = wav1.readframes(params1.nframes)  # Read all audio frames from the file
        data1 = np.frombuffer(frames1, dtype=np.int16)  # Convert the audio frames to a NumPy array of type int16


    # Open the second WAV file
    with wave.open(file2, 'rb') as wav2:  # Open `file2` in read-binary mode
        params2 = wav2.getparams()  # Get the parameters of the second WAV file
        frames2 = wav2.readframes(params2.nframes)  # Read all audio frames from the second file
        data2 = np.frombuffer(frames2, dtype=np.int16)  # Convert the audio frames to a NumPy array of type int16


    # Pad the shorter audio with zeros to match the length of the longer audio
    max_length = max(len(data1), len(data2))  # Determine the length of the longer audio file
    if len(data1) < max_length:  # If the first file is shorter
        data1 = np.pad(data1, (0, max_length - len(data1)), mode='constant', constant_values=0)  # Pad with zeros
    if len(data2) < max_length:  # If the second file is shorter
        data2 = np.pad(data2, (0, max_length - len(data2)), mode='constant', constant_values=0)  # Pad with zeros


    # Mix the audio data
    mixed_data = data1 // 2 + data2 // 2  # Combine the two audio files by averaging their values


    # Apply gain to increase volume
    mixed_data = (mixed_data * gain).clip(-32768, 32767)  # Multiply by `gain` and clip values to fit int16 range


    # Write the mixed data to the output file
    with wave.open(output_file, 'wb') as output_wav:  # Open the output file in write-binary mode
        output_wav.setparams(params1)  # Use the parameters of the first file for the output file
        output_wav.writeframes(mixed_data.astype(np.int16).tobytes())  # Write the mixed audio data to the file


def check_wav_params(file):
    # Define a function to print the parameters of a WAV file
    with wave.open(file, 'rb') as wav:  # Open the WAV file in read-binary mode
        params = wav.getparams()  # Get the parameters of the WAV file
        print(f"File: {file}")  # Print the file name
        print(f"  Channels: {params.nchannels}")  # Print the number of channels (e.g., mono or stereo)
        print(f"  Sample Width: {params.sampwidth}")  # Print the sample width in bytes
        print(f"  Frame Rate: {params.framerate}")  # Print the sample rate (frames per second)
        print(f"  Number of Frames: {params.nframes}")  # Print the total number of frames
        print(f"  Duration: {params.nframes / params.framerate:.2f} seconds\n")  # Calculate and print the duration


# Define the input and output file paths
file1 = "recorded_audio.wav"  # Path to the first input WAV file
file2 = "converted_midi.wav"  # Path to the second input WAV file
output_file = "mixed_output.wav"  # Path to the output WAV file


# Check and print the parameters of the input files
check_wav_params(file1)  # Print the parameters of the first WAV file
check_wav_params(file2)  # Print the parameters of the second WAV file


# Mix the two files with increased volume (gain = 3.0)
mix_wav_files(file1, file2, output_file, gain=3.0)  # Call the function to mix the files and save the result
