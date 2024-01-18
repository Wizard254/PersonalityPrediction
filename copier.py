import sys
import os
import shutil

import shutil
import os


def copy_file_or_folder(source_path, destination_path):
    # Check if the source path exists
    if not os.path.exists(source_path):
        print(f"Source path '{source_path}' does not exist.")
        return

    # Determine if the source path is a file or folder
    if os.path.isfile(source_path):
        # Copy the file to the destination path
        shutil.copy2(source_path, destination_path)
        print(f"File copied: {source_path} to {destination_path}")
    elif os.path.isdir(source_path):
        # Copy the entire folder to the destination path
        shutil.copytree(source_path, destination_path)
        print(f"Folder copied: {source_path} to {destination_path}")
    else:
        print(f"Source path '{source_path}' is neither a file nor a folder.")


def copy_files(source_dir, destination_dir, exclude_file):
    # Read exclude file line by line into a list
    with open(exclude_file, 'r') as f:
        exclude_list = [line.strip() for line in f.readlines()]

    # Iterate over files in the source directory
    for file in os.listdir(source_dir):
        # Check if the file or folder should be excluded
        if file in exclude_list:
            print(f"Excluded: {file}")
        else:
            print(f"Copying: {file}")
            source_path = os.path.join(source_dir, file)
            destination_path = os.path.join(destination_dir, file)

            try:
                # Copy the file or folder to the destination directory
                copy_file_or_folder(source_path, destination_path)
                pass
            except PermissionError:
                pass

            pass


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python copy_files.py source_directory destination_directory exclude_file.txt")
        sys.exit(1)

    source_directory = sys.argv[1]
    destination_directory = sys.argv[2]
    exclude_file = sys.argv[3]

    copy_files(source_directory, destination_directory, exclude_file)
    pass

#  python copier.py . "C:\Users\Anyona\AWork\Mandela\Unit\PersonalityPredictionP2\Deploy\2\app4" copier_exclude.txt
