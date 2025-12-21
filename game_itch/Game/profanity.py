import re
import requests
import threading
import os
import sys

class ProfanityFilter:
    def __init__(self):
        self.words = set()
        self.lock = threading.Lock()
        
        # 1. Load defaults immediately
        self._load_defaults()
        
        # 2. Try to load from cache
        self.cache_path = self._get_resource_path("profanity_list.txt")
        self._load_from_cache()
        
        # 3. Start background fetch
        self.remote_url = "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/en"
        threading.Thread(target=self._fetch_remote_list, daemon=True).start()

    def _get_resource_path(self, filename):
        """Determines the correct path for resources in both dev and EXE."""
        if getattr(sys, 'frozen', False):
            # Running as EXE
            base_path = os.path.dirname(sys.executable)
        else:
            # Running as Script
            base_path = os.path.join(os.path.dirname(__file__), "..", "resources")
        
        # Ensure directory exists if we are in dev mode (for updates)
        if not getattr(sys, 'frozen', False) and not os.path.exists(base_path):
            os.makedirs(base_path, exist_ok=True)
            
        return os.path.join(base_path, filename)

    def _load_defaults(self):
        """Minimal fallback list."""
        defaults = ["badword", "admin", "null", "fuck", "shit", "bitch", "ass", "cunt", "nigger", "faggot"]
        with self.lock:
            self.words.update(defaults)

    def _load_from_cache(self):
        """Loads words from local file."""
        if not os.path.exists(self.cache_path):
            return
            
        try:
            with open(self.cache_path, "r", encoding="utf-8") as f:
                loaded_words = [line.strip().lower() for line in f if line.strip()]
            
            with self.lock:
                self.words.update(loaded_words)
            print(f"[Profanity] Loaded {len(loaded_words)} words from cache.")
        except Exception as e:
           print(f"[Profanity] Failed to load cache: {e}")

    def _fetch_remote_list(self):
        """Fetches the latest list from GitHub."""
        try:
            print(f"[Profanity] Fetching remote list from {self.remote_url}...")
            response = requests.get(self.remote_url, timeout=5)
            if response.status_code == 200:
                raw_text = response.text
                new_words = [line.strip().lower() for line in raw_text.splitlines() if line.strip()]
                
                # Update memory
                with self.lock:
                    self.words.update(new_words)
                
                # Save to cache
                try:
                    with open(self.cache_path, "w", encoding="utf-8") as f:
                        f.write("\n".join(sorted(list(self.words))))
                    print(f"[Profanity] Remote updated. Cache saved. Total words: {len(self.words)}")
                except Exception as e:
                    print(f"[Profanity] Failed to write cache: {e}")
            else:
                print(f"[Profanity] Fetch failed with status {response.status_code}")
        except Exception as e:
            print(f"[Profanity] Fetch error: {e}")

    def normalize(self, text):
        """
        Normalizes text:
        1. Leetspeak (h3ll0 -> hello)
        2. Repeated chars (fuuuck -> fuck)
        3. Lowercase
        """
        if not text: return ""
        text = text.lower()
        
        # Leetspeak Map
        leetspeak = {
            '0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', 
            '7': 't', '8': 'b', '@': 'a', '$': 's', '!': 'i',
            '+': 't'
        }
        for char, repl in leetspeak.items():
            text = text.replace(char, repl)
            
        # Remove non-alphanumeric chars (spaces are important for exact checks, but for broad checks we might remove them)
        # Strategy: Keep spaces to detect words, but maybe also check "spaceless" version?
        # For now, let's keep spaces and punctuation is removed.
        text = re.sub(r'[^a-z0-9\s]', '', text)
        
        # Collapse repeated chars (e.g. "heeello" -> "helo")
        # However, this destroys legitimate double letters (hello -> helo).
        # Better strategy: Collapse >2 repeats to 2? or 1?
        # Profanity often relies on repeats. "fuuck" match "fuck".
        # Let's try collapsing repeats to single char for checking.
        # "hello" -> "helo". If "helo" is bad, then it flags.
        # But "ass" -> "as". "as" might be okay?
        # Actually collapsing to 1 char is aggressive. 
        # Safe strategy: Check original, check leetspeak, check collapsed.
        
        return text

    def is_profane(self, text):
        if not text: return False
        
        # 1. Simple direct check (fast)
        if self._check_against_list(text.lower()): return True
        
        # 2. Normalize (Leetspeak)
        normalized = self.normalize(text)
        if self._check_against_list(normalized): return True
        
        # 3. Collapse Repeats (Aggressive: "fuuuck" -> "fuck")
        # Collapse all repeats to 1 char.
        collapsed = re.sub(r'(.)\1+', r'\1', normalized) 
        if self._check_against_list(collapsed): return True
        
        return False

    def _check_against_list(self, clean_text):
        """Checks if any word in the text is in the blacklist."""
        # We need to be careful about substrings. "Class" contains "ass".
        # We should check WORD boundaries.
        
        user_words = clean_text.split()
        with self.lock:
             for word in user_words:
                 if word in self.words:
                     return True
        
        # Also check for exact string match if it's a short phrase?
        # Or maybe check if any bad word is a substring of the text?
        # Substring is dangerous for "Scunthorpe" problem (Massive, Assembly).
        # We stick to word tokenization for safety, UNLESS the bad word is explicit/severe.
        # But this list is huge and contains normal substrings.
        # Ideally, we rely on the list having precise words.
        
        return False
