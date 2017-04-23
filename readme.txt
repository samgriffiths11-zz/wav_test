############   exercise_1.py   ############

Summary: 
	* Python script to extract the following from multiple WAV files - 
			- the number of channels
			- the sample rate
			- the number of bits per sample


	* Attributes of each WAV file are stored in a Python dictionary
	* Assumes that the WAV files are stored in the same folder as the one the Python script is stored in
	* Uses the standard Python modules shipped with Anaconda 3 (Python 3.6.0) 
	  download link: https://repo.continuum.io/archive/Anaconda3-4.3.1-Windows-x86_64.exe
	* Tested on file sizes upto 2GB

Example usage (on command line, navigated to the folder where the script (and wav files) reside):
	C:\ProgramData\Anaconda3\python.exe exercise_1.py

############   exercise_2.py   ############

Summary:
	* Python script to write out summary statistics from multiple WAV files in - 
			- CSV format
			- SQLite format

	* Script behaviour is controlled through command line arguments:
			"-c <path to CSV>"
			"-s <path to SQLite database>"

	* If no data format is given, script will fail to execute
	* The script assumes that the SQLite database already exists, for testing purposes
	  the database was created using DB Browser which is free from http://sqlitebrowser.org/
	* If SQLite database is specified, script will produce an output table with the name format - 
			"wav_stats_YYYYMMDD_HHMMSS" where Y=Year, M=Month, D=Day, H=Hour, M=Minutes, S=Seconds

	* A sample blank SQLite database has been provided in this repository ("test_wav_stats_base.db")
	* Assumes that the WAV files are stored in the same folder as the one the Python script is stored in
	* Uses the standard Python modules shipped with Anaconda 3 (Python 3.6.0)
	  download link: https://repo.continuum.io/archive/Anaconda3-4.3.1-Windows-x86_64.exe
	* Tested on file sizes upto 2GB

Example usage (on command line, navigated to the folder where the script (and wav files) reside):
	C:\ProgramData\Anaconda3\python.exe exercise_2.py -c C:\Temp\output.csv -s C:\Temp\test_wav_stats_base.db