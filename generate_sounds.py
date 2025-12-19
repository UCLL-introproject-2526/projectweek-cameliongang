import wave
import math
import struct
import random
import os

def generate_tone(filename, duration=0.1, freq=440, vol=0.5, type='sine'):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1) # Mono
        wav_file.setsampwidth(2) # 16-bit
        wav_file.setframerate(sample_rate)
        
        for i in range(n_samples):
            t = i / sample_rate
            if type == 'sine':
                val = math.sin(2 * math.pi * freq * t)
            elif type == 'noise':
                val = random.uniform(-1, 1)
            elif type == 'square':
                val = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
            
            # Decay envelope (linear)
            envelope = 1.0 - (i / n_samples)
            
            # Scale to 16-bit
            sample = int(val * vol * envelope * 32767.0)
            wav_file.writeframes(struct.pack('h', sample))
    print(f"Generated {filename}")

if __name__ == "__main__":
    if not os.path.exists("resources"):
        os.makedirs("resources")
        
    # Button Click: Short, high pitch chirp (Click)
    # 0.03s duration, rapid frequency drop (simulating mechanical click)
    duration = 0.03
    n_samples = int(44100 * duration)
    with wave.open("resources/button_click.wav", 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(44100)
        data = []
        for i in range(n_samples):
            t = i / n_samples
            # Freq drop from 4000 to 100
            freq = 4000 * (1 - t)
            val = math.sin(2 * math.pi * freq * (i/44100))
            envelope = 1
            data.append(int(val * 0.5 * 32767))
        f.writeframes(struct.pack('h'*len(data), *data))
    
    # Walk: Short, low pitch, noise (thud) - Boosted Volume
    # Increased volume from 0.2 to 0.5 and changed to a more percussive envelope
    duration = 0.1
    n_samples = int(44100 * duration)
    with wave.open("resources/walk.wav", 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(44100)
        data = []
        for i in range(n_samples):
            val = random.uniform(-1, 1)
            # Envelope: Sharp attack, fast decay
            envelope = 1.0 - (i / n_samples)**0.5 
            sample = int(val * 0.5 * 32767 * envelope)
            sample = max(-32767, min(32767, sample))
            data.append(sample)
        f.writeframes(struct.pack('h'*len(data), *data))

    # Jump: Ascending slide (Whoosh/Jump)
    # Sine wave sliding from 300Hz to 600Hz
    duration = 0.3
    n_samples = int(44100 * duration)
    with wave.open("resources/jump.wav", 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(44100)
        data = []
        for i in range(n_samples):
            t = i / duration
            freq = 300 + (300 * t) # 300 -> 600
            val = math.sin(2 * math.pi * freq * (i/44100))
            envelope = 1.0 - t
            sample = int(val * 0.4 * 32767 * envelope)
            sample = max(-32767, min(32767, sample))
            data.append(sample)
        f.writeframes(struct.pack('h'*len(data), *data))

    # Level Complete: Victory Jingle (Rising major arpeggio)
    # C major: C(523), E(659), G(784), C(1046)
    duration = 0.6
    n_samples = int(44100 * duration)
    with wave.open("resources/level_complete.wav", 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(44100)
        data = []
        for i in range(n_samples):
            t = i / 44100
            # Sequence notes
            if t < 0.15: freq = 523.25
            elif t < 0.3: freq = 659.25
            elif t < 0.45: freq = 783.99
            else: freq = 1046.50
            
            val = math.sin(2 * math.pi * freq * t)
            # Add some harmonics for "chiptune" feel
            val += 0.5 * math.sin(2 * math.pi * freq * 2 * t)
            
            envelope = 1.0 # Simple envelope could be added per note but this is fine
            sample = int(val * 0.3 * 32767)
            sample = max(-32767, min(32767, sample))
            data.append(sample)
        f.writeframes(struct.pack('h'*len(data), *data))
