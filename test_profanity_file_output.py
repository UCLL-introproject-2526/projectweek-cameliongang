from Game.profanity import ProfanityFilter
import time
import sys

def test_profanity():
    log = []
    def log_msg(msg):
        log.append(msg)
        print(msg)

    log_msg("Initializing ProfanityFilter...")
    pf = ProfanityFilter()
    
    log_msg("Waiting 2 seconds for remote fetch...")
    time.sleep(2)
    
    tests = [
        ("Good Word", "Hello World", False),
        ("Bad Word", "fuck", True),
        ("Leetspeak", "h3ll0", False),
        ("Leetspeak Bad", "f*ck", True),
        ("Leetspeak Bad 2", "a$$", True),
        ("Repeats", "fuuuuuck", True),
        ("Sentence", "This is a shit outcome", True),
        ("Scunthorpe (False Positive)", "Class", False),
        ("Scunthorpe 2", "Assessment", False),
    ]
    
    log_msg("\n--- Running Tests ---")
    passed = 0
    for name, text, expected in tests:
        result = pf.is_profane(text)
        status = "PASS" if result == expected else "FAIL"
        if status == "PASS": passed += 1
        log_msg(f"[{status}] {name}: '{text}' -> {result} (Expected: {expected})")
        
    log_msg(f"\nResult: {passed}/{len(tests)} passed.")
    log_msg(f"Total words in filter: {len(pf.words)}")
    
    with open("verification_result.log", "w", encoding="utf-8") as f:
        f.write("\n".join(log))

if __name__ == "__main__":
    test_profanity()
