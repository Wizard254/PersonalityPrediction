import zipfile
import os

if __name__ == '__main__':
    current_directory = os.getcwd()
    zip_files = [file for file in os.listdir(current_directory) if file.endswith(".zip")]

    for f in zip_files:
        with zipfile.ZipFile(f, 'r') as zip_ref:
            zip_ref.extractall()
            pass
        pass
    pass
