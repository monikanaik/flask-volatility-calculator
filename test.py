import os
import zipfile

for root, directories, files in os.walk('.'):
    for filename in files:
        print(os.path.join(root, filename))

# File paths
a_file = 'NIFTY 50-20-12-2023-to-20-01-2024.csv'
zip_file = 'file.zip'
unzip_path = 'unzipped/'

# Zip the file
with zipfile.ZipFile(zip_file, 'w') as zipf:
    zipf.write(a_file, os.path.basename(a_file))

# Unzip the file
with zipfile.ZipFile(zip_file, 'r') as zipf:
    zipf.extractall(unzip_path)

# Rename the unzipped file to file.csv
os.rename(os.path.join(unzip_path, os.path.basename(a_file)), os.path.join(unzip_path, 'files.csv'))
