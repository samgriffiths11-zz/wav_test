import os
import glob
import sys
import wave


def grab_wav_files(base_dir):
    """Function to get a list of wav files within a
        specified directory.

        Args: base_dir (str) directory containing wav files

        Returns: wav_file_paths (list)"""

    search_string = os.path.join(base_dir, '*.wav')
    wav_file_paths = glob.glob(search_string)

    if len(wav_file_paths) < 1:
        print('No wave files found, exiting program')
        sys.exit()

    return wav_file_paths

def grab_wav_metadata(wav_file):
    """ Function to grab the following from a WAV file:
        - the number of channels
        - the sample rate
        - the number of bits per sample

        Args: wav_file, str: Full path to WAV file to query.

        Returns: wav_metadata (dict): Contains wav file info"""

    wav_filename = os.path.basename(wav_file)
    wav_metadata = {}

    try:
        print('Processing {}'.format(wav_filename))
        with wave.open(wav_file, 'rb') as wav_reader:
            num_channels = wav_reader.getnchannels()
            # NOTE sample rate is the same as frame rate for PCM formats
            sample_rate = wav_reader.getframerate()
            sample_width_bytes = wav_reader.getsampwidth()
            sample_width_bits = sample_width_bytes * 8

            wav_metadata[wav_filename] = {'num channels' : num_channels,
                                          'sample rate' : sample_rate,
                                          'sample width' : sample_width_bits}

    except wave.Error:
        raise

    return wav_metadata

def main():
    """This script will get requested information from
        WAV files stored in the same directory as the script itself
        and store the results in dictionary format"""

    # Change this variable if wav files are located
    # somewhere different to the script
    wav_file_directory = os.path.dirname(sys.argv[0])

    wav_file_paths = grab_wav_files(wav_file_directory)

    all_wav_metadata = {}
    for wav_file in wav_file_paths:
        wav_metadata = grab_wav_metadata(wav_file)
        all_wav_metadata.update(wav_metadata)

    print('Done!')

if __name__ == '__main__':
    main()
