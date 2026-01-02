
import os
import shutil
import subprocess
import sys
import urllib.request
import re

def clean_build():
    project_root = os.getcwd() # Should be game_web
    print(f"Project Root: {project_root}")
    
    # Define what to copy
    include_dirs = ['Game', 'resources']
    include_files = ['main.py']
    
    # Verify sources exist
    for d in include_dirs:
        if not os.path.exists(d):
            print(f"Error: Missing directory {d}")
            return
    for f in include_files:
        if not os.path.exists(f):
            print(f"Error: Missing file {f}")
            return

    # Create temp dir
    temp_dir = os.path.join(project_root, 'temp_build_src')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    print(f"Created temp src: {temp_dir}")
    
    # Copy files
    try:
        for d in include_dirs:
            shutil.copytree(d, os.path.join(temp_dir, d))
        for f in include_files:
            shutil.copy2(f, os.path.join(temp_dir, f))
            
        if os.path.exists('requirements.txt'):
             shutil.copy2('requirements.txt', os.path.join(temp_dir, 'requirements.txt'))

    except Exception as e:
        print(f"Copy failed: {e}")
        return

    # Run Pygbag on temp_dir
    print("Running Pygbag on temp src...")
    cmd = [sys.executable, "-m", "pygbag", "--build", "--archive", temp_dir]
    
    try:
        subprocess.check_call(cmd, cwd=project_root)
    except subprocess.CalledProcessError as e:
        print(f"Pygbag failed: {e}")
        return

    # Result should be in temp_dir/build/web
    built_web_dir = os.path.join(temp_dir, 'build', 'web')
    
    if not os.path.exists(built_web_dir):
        print("Error: Build output not found!")
        return
        
    # --- PATCHING FOR OFFLINE / ITCH.IO FIX ---
    print("Patching for Offline/Itch.io...")
    index_path = os.path.join(built_web_dir, 'index.html')
    
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # URL to match (based on typical pygbag output)
        cdn_base = "https://pygame-web.github.io/archives/0.9/"
        
        # Checking content for specific version if needed, but 0.9 is standard for now.
        if cdn_base in content:
            print(f"Found CDN links to {cdn_base}. Downloading local copies...")
            
            # Replace in HTML
            new_content = content.replace(cdn_base, "./")
            
            # REGEX Patch for data-os
            # Capture data-os=... until space or >
            new_content = re.sub(r'data-os=["\']?.*?["\']?(\s|>)', r'data-os=""\1', new_content)
            print("Patched data-os attribute via Regex.")
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            # Create cpython312 directory
            cpython_dir = os.path.join(built_web_dir, 'cpython312')
            if not os.path.exists(cpython_dir):
                os.makedirs(cpython_dir)

            # Download CPython runtime files
            cpython_files = ['main.js', 'main.wasm', 'python312.zip', 'main.data']
            
            for cfile in cpython_files:
                url = cdn_base + f"cpython312/{cfile}"
                local_path = os.path.join(cpython_dir, cfile)
                try:
                    print(f"Downloading {cfile} to cpython312/...")
                    urllib.request.urlretrieve(url, local_path)
                    
                    # Copy main.wasm to root as well, just in case
                    if cfile == 'main.wasm':
                        root_wasm = os.path.join(built_web_dir, 'main.wasm')
                        shutil.copy2(local_path, root_wasm)
                        print("Copied main.wasm to root for safety.")
                        
                except Exception as e:
                    print(f"Failed to download {cfile}: {e}")

            # Download Core files
            files_to_mirror = [
                "pythons.js",
                "browserfs.min.js", 
                "pythonrc.py",
                "cpythonrc.py",
                "favicon.png"
            ]
            
            for fname in files_to_mirror:
                url = cdn_base + fname
                local_path = os.path.join(built_web_dir, fname)
                try:
                    print(f"Downloading {fname}...")
                    urllib.request.urlretrieve(url, local_path)
                except Exception as e:
                    print(f"Failed to download {fname}: {e}")

            # VT (xterm) files
            vt_dir = os.path.join(built_web_dir, 'vt')
            if not os.path.exists(vt_dir):
                os.makedirs(vt_dir)

            vt_files = ["xterm.js", "xterm-addon-image.js"]
            for vt_file in vt_files:
                url = cdn_base + f"vt/{vt_file}"
                local_path = os.path.join(vt_dir, vt_file)
                try:
                    print(f"Downloading vt/{vt_file}...")
                    urllib.request.urlretrieve(url, local_path)
                except Exception as e:
                     print(f"Failed to download vt/{vt_file}: {e}")
                     # Create dummy if download fails
                     with open(local_path, 'w') as f: f.write("// Dummy xterm")

            # Create DUMMY files for the dynamic modules
            dummy_modules = ["vtx.js", "fs.js", "snd.js", "gui.js"]
            for mod in dummy_modules:
                mod_path = os.path.join(built_web_dir, mod)
                if not os.path.exists(mod_path):
                    print(f"Creating dummy {mod}...")
                    with open(mod_path, 'w') as f:
                        f.write("// Dummy file to prevent 404\n")

    # Copy to predictable release folder
    release_dir = os.path.join(project_root, 'release_web')
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    shutil.copytree(built_web_dir, release_dir)
    print(f"Build SUCCESS. Artifacts copied to: {release_dir}")
    print("Use this valid path for Butler.")
    
if __name__ == '__main__':
    clean_build()
