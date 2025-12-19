import os
import shutil

src_dir = "resources/hmm"
files = sorted([f for f in os.listdir(src_dir) if f.startswith("IMG") and f.endswith(".jpg")])

for i, f in enumerate(files):
    src = os.path.join(src_dir, f)
    dst = os.path.join(src_dir, f"frame_{i}.jpg")
    if src != dst:
        os.rename(src, dst)
        print(f"Renamed {src} -> {dst}")

sound_src = os.path.join(src_dir, "screamm.aac")
sound_dst = os.path.join(src_dir, "scream.aac")
if os.path.exists(sound_src):
    os.rename(sound_src, sound_dst)
    print(f"Renamed {sound_src} -> {sound_dst}")
