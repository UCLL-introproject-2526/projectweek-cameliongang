
import os
import re

def verify():
    build_dir = r"game_itch/build/web"
    
    files_to_check = [
        ("index.html", 100),
        ("pythons.js", 1000),
        ("cpython312/main.js", 1000),
        ("cpython312/main.data", 1000000), # Expecting ~7MB
        ("cpython312/main.wasm", 100000),
        ("main.wasm", 100000), # Root fallback
        ("vtx.js", 0), # Dummy
        ("gui.js", 0)  # Dummy
    ]
    
    print("--- VERIFICATION REPORT ---")
    all_good = True
    
    for fname, min_size in files_to_check:
        path = os.path.join(build_dir, fname)
        if not os.path.exists(path):
             print(f"[FAIL] Missing: {fname}")
             all_good = False
        else:
             size = os.path.getsize(path)
             if size < min_size:
                 print(f"[FAIL] Too small: {fname} ({size} bytes, expected > {min_size})")
                 all_good = False
             else:
                 print(f"[OK] {fname} ({size} bytes)")

    # Check index.html patch
    index_path = os.path.join(build_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'https://pygame-web.github.io' in content:
            print("[FAIL] Index.html still contains CDN links!")
            all_good = False
        else:
            print("[OK] Index.html clean of CDN links.")
            
        if 'data-os="vtx' in content:
             print("[FAIL] Index.html still asks for vtx module!")
             all_good = False
        else:
             print("[OK] Index.html data-os patched.")

    if all_good:
        print("\n>>> BUILD VERIFIED SUCCESFULLY <<<")
    else:
        print("\n>>> BUILD FAILED VERIFICATION <<<")

if __name__ == "__main__":
    verify()
