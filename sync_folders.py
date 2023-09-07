import os
import sys
import time
import shutil
import logging
import argparse
import hashlib

# Parse the command line arguments
parser = argparse.ArgumentParser(description="Synchronize two folders")
parser.add_argument("source", help="The source folder path")
parser.add_argument("replica", help="The replica folder path")
parser.add_argument("interval", type=int, help="The synchronization interval in seconds")
parser.add_argument("logfile", help="The log file path")
args = parser.parse_args()

# Set up the logging
logging.basicConfig(filename=args.logfile, level=logging.INFO, format="%(asctime)s %(message)s")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

# Define a function to calculate the MD5 hash of a file
def md5(file):
    hash = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()

# Define a function to synchronize two folders
def sync(source, replica):
    try:
        logging.info(f"Starting synchronization from {source} to {replica}")
        # Get the list of files and subfolders in the source folder
        source_files = set(os.listdir(source))
        # Get the list of files and subfolders in the replica folder
        replica_files = set(os.listdir(replica))
        # Loop through the files and subfolders in the source folder
        for file in source_files:
            # Get the full paths of the source and replica files/subfolders
            source_path = os.path.join(source, file)
            replica_path = os.path.join(replica, file)
            # If the file/subfolder does not exist in the replica folder, copy it
            if file not in replica_files:
                if os.path.isfile(source_path):
                    logging.info(f"Copying file {source_path} to {replica_path}")
                    shutil.copy2(source_path, replica_path)
                elif os.path.isdir(source_path):
                    logging.info(f"Copying folder {source_path} to {replica_path}")
                    shutil.copytree(source_path, replica_path)
            # If the file/subfolder exists in both folders, check if they are identical
            else:
                if os.path.isfile(source_path) and os.path.isfile(replica_path):
                    # Compare the MD5 hashes of the files
                    source_hash = md5(source_path)
                    replica_hash = md5(replica_path)
                    # If the hashes are different, overwrite the replica file with the source file
                    if source_hash != replica_hash:
                        logging.info(f"Overwriting file {replica_path} with {source_path}")
                        shutil.copy2(source_path, replica_path)
                elif os.path.isdir(source_path) and os.path.isdir(replica_path):
                    # Recursively synchronize the subfolders
                    sync(source_path, replica_path)
                else:
                    # If the file types are different, remove the replica file/subfolder and copy the source file/subfolder
                    logging.info(f"Removing {replica_path}")
                    if os.path.isfile(replica_path):
                        os.remove(replica_path)
                    elif os.path.isdir(replica_path):
                        shutil.rmtree(replica_path)
                    logging.info(f"Copying {source_path} to {replica_path}")
                    if os.path.isfile(source_path):
                        shutil.copy2(source_path, replica_path)
                    elif os.path.isdir(source_path):
                        shutil.copytree(source_path, replica_path)
        # Loop through the files and subfolders in the replica folder
        for file in replica_files:
            # Get the full paths of the source and replica files/subfolders
            source_path = os.path.join(source, file)
            replica_path = os.path.join(replica, file)
            # If the file/subfolder does not exist in the source folder, remove it from the replica folder
            if file not in source_files:
                logging.info(f"Removing {replica_path}")
                if os.path.isfile(replica_path):
                    os.remove(replica_path)
                elif os.path.isdir(replica_path):
                    shutil.rmtree(replica_path)
        logging.info(f"Finished synchronization from {source} to {replica}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Run the synchronization function periodically with the given interval
while True:
    sync(args.source, args.replica)
    time.sleep(args.interval)