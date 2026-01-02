import zipfile
import os

zip_path = 'web-build.zip'
if not os.path.exists(zip_path):
    print(f"Zip not found at {zip_path}")
else:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        print(f"Contents of {zip_path}:")
        for name in zip_ref.namelist():
            print(f" - {name}")
