import argparse
import datetime
import os
import glob
import sqlite3
import sys
import wave

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument( "-c", "--write-csv", type=str,
                        help="Path to output CSV (including file extension)")
    parser.add_argument("-s", "--write-sqlite", type=str,
                        help="""Path to output SQLite database (including file extension)
                                NOTE: This database should already exist.""")

    args = parser.parse_args()

    csv_path = args.write_csv
    sqlite_path = args.write_sqlite

    # TODO - Verify paths before continuing

    return csv_path, sqlite_path

def grab_wav_files(base_dir):
    """Function to get a list of wav files within a
        specified directory.

        Args: 
            base_dir (str): Directory containing wav files

        Returns: 
            wav_file_paths (list) : List of wav file paths"""

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

        Args: 
            wav_file (str): Full path to WAV file to query.

        Returns: 
            wav_metadata (dict): Contains wav file info"""

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

            wav_metadata[wav_file] = {'num_channels' : num_channels,
                                          'sample_rate' : sample_rate,
                                          'sample_width' : sample_width_bits}

    except Exception as err:
        print('Unable to process WAV files with the following exception:')
        raise

    return wav_metadata

def grab_data_headers(all_wav_metadata):

    csv_headers = ['file_path',]

    for wav_name in all_wav_metadata.keys():
        all_data_types = [k for k in all_wav_metadata[wav_name].keys()]

        for data_type in all_data_types:
            csv_headers.append(data_type)

        break

    return csv_headers, all_data_types

def write_results_to_csv(all_wav_metadata, output_csv_path):

    csv_headers, all_data_types = grab_data_headers(all_wav_metadata)

    try:
        with open(output_csv_path, 'w') as out_file:
            header_string = ','.join(csv_headers)
            out_file.write('{},\n'.format(header_string))

            out_str = ''
            for wav in all_wav_metadata.keys():
                out_str += '{},'.format(wav)

                for data_type in all_data_types:
                    out_str += '{},'.format(all_wav_metadata[wav][data_type])
                out_str += '\n'

            out_file.write(out_str)

        print('Written wav stats to {}'.format(output_csv_path))

    except Exception as err:
        print('Cannot save CSV file with the following exception:')
        print(err)

def write_results_to_sqlite(all_wav_metadata, out_sqlite_path):

    with sqlite3.connect(out_sqlite_path) as con:
        cur = con.cursor()

        table_name = create_output_table(cur, all_wav_metadata)
        insert_data_to_table(cur, all_wav_metadata, table_name)

    print('Written wav stats to {}'.format(out_sqlite_path))


def create_output_table(cur, all_wav_metadata):

    try:
        col_names, _ = grab_data_headers(all_wav_metadata)
        datestamp = datetime.datetime.now()
        datestamp = datetime.datetime.strftime(datestamp, '%Y%m%d_%H%M%S')
        table_name = 'wav_stats_{}'.format(datestamp)
        wav_path = col_names[0]
        wav_path_type = 'TEXT'

        num_channels = col_names[1]
        num_channels_type = 'INT'

        sample_rate = col_names[2]
        sample_rate_type = 'INT'

        sample_size = col_names[3]
        sample_size_type = 'INT'

        query = """CREATE TABLE {table_name} 
                    ({wav_path} {wav_path_type} sas,
                    {num_channels} {num_channels_type},
                    {sample_rate} {sample_rate_type}, 
                    {sample_size} {sample_size_type}) """.format(table_name=table_name,
                                                                wav_path=wav_path,
                                                                wav_path_type=wav_path_type,
                                                                num_channels=num_channels,
                                                                num_channels_type=num_channels_type,
                                                                sample_rate=sample_rate,
                                                                sample_rate_type=sample_rate_type,
                                                                sample_size=sample_size,
                                                                sample_size_type=sample_size_type)
        cur.execute(query)

    except Exception as err:
        print('SQL create table failed with the following error')
        print(err)
        table_name = None

    return table_name

def insert_data_to_table(cur, all_wav_metadata, table_name):

    try:
        insert_queries = []
        for wav_path, data in all_wav_metadata.items():
            insert_query = """INSERT INTO {table_name} 
                              (file_path, num_channels, sample_rate, sample_width) 
                              VALUES (?, ?, ?, ?)""".format(table_name=table_name)

            params = (wav_path,
                      data['num_channels'],
                      data['sample_rate'],
                      data['sample_width'])

            cur.execute(insert_query, params)

    except Exception as err:
        print('Unable to insert data to table with following exception:')
        print(err)

def main():

    """This script will get requested information from
        WAV files stored in the same directory as the script itself
        and write the results to either a CSV or a SQLite database,
        as specified by the user."""

    # Change this variable if wav files are located
    # somewhere different to the script
    wav_file_directory = os.path.dirname(sys.argv[0])

    csv_path, sqlite_path = parse_args()

    if not csv_path and not sqlite_path:
        print('No output format specified. Please specify an output format, use --help for guidance')
        sys.exit()

    wav_file_paths = grab_wav_files(wav_file_directory)

    all_wav_metadata = {}
    for wav_file in wav_file_paths:
        wav_metadata = grab_wav_metadata(wav_file)
        all_wav_metadata.update(wav_metadata)

    if csv_path:
        write_results_to_csv(all_wav_metadata, csv_path)

    if sqlite_path:
        write_results_to_sqlite(all_wav_metadata, sqlite_path)

    print ('Done!')

if __name__ == '__main__':
    main()