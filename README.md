# Folder Synchronization Tool

This Python script is a simple folder synchronization tool that periodically synchronizes two folders, maintaining an identical copy of the source folder at the replica folder. It logs file creation, copying, and removal operations to both a file and the console output.

## Features

- One-way synchronization: Ensures that the content of the replica folder exactly matches the source folder.
- Periodic synchronization: The tool runs at regular intervals to keep the folders synchronized.
- Logging: All file operations are logged to a specified log file and the console output.

## Usage

To use this tool, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/MarcinIgna/FolderSync.git
   ```

2. Navigate to the project directory:

   ```bash
   cd folder-synchronization
   ```

3. Install the required dependencies from the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a log file (if it doesn't already exist) in the directory where you want to run the synchronization. For example:

   ```bash
   touch sync_log.txt
   ```

5. Ensure that both the source and replica folders exist before running the synchronization.

6. Run the script with the following command:

   ```bash
   python sync_folders.py /path/to/source/folder /path/to/replica/folder <interval> /path/to/logfile.txt
   ```

   - `/path/to/source/folder`: The path to the source folder you want to synchronize.
   - `/path/to/replica/folder`: The path to the replica folder where you want to maintain the copy.
   - `<interval>`: The synchronization interval in seconds.
   - `/path/to/logfile.txt`: The path to the log file where synchronization details will be recorded.

7. The script will run periodically, keeping the replica folder synchronized with the source folder.

## Requirements

This script requires Python 3. Make sure you have Python installed on your system.

## Error Handling

The script includes error handling to handle unexpected situations gracefully. If any errors occur during synchronization, they will be logged as error messages.
