import shutil
import os

def make_zip():
    src_dir = os.path.join(os.getcwd(), 'build', 'web')
    output_filename = os.path.join(os.getcwd(), 'web-build')
    
    print(f"Zipping {src_dir} to {output_filename}.zip...")
    shutil.make_archive(output_filename, 'zip', src_dir)
    print("Zip created successfully.")

if __name__ == "__main__":
    make_zip()
