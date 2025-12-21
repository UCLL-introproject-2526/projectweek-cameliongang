from Game.profanity import ProfanityFilter
import time

def test_profanity():
    print("Initializing ProfanityFilter...")
    pf = ProfanityFilter()
    
    # Wait a bit for remote fetch (it's threaded)
    print("Waiting 2 seconds for remote fetch...")
    time.sleep(2)
    
    tests = [
        ("Good Word", "Hello World", False),
        ("Bad Word", "fuck", True),
        ("Leetspeak", "h3ll0", False), # "hello" is not bad
        ("Leetspeak Bad", "f*ck", True), # "damn" is usually bad? wait f*ck -> fuck
        ("Leetspeak Bad 2", "a$$", True),
        ("Repeats", "fuuuuuck", True),
        ("Sentence", "This is a shit outcome", True),
        ("Scunthorpe (False Positive)", "Class", False),
        ("Scunthorpe 2", "Assessment", False),
        #("Remote List Check", "2g1c", True) # Assuming this is in the remote list? (LDNOOBW usually has it)
    ]
    
    print("\n--- Running Tests ---")
    passed = 0
    for name, text, expected in tests:
        result = pf.is_profane(text)
        status = "PASS" if result == expected else "FAIL"
        if status == "PASS": passed += 1
        print(f"[{status}] {name}: '{text}' -> {result} (Expected: {expected})")
        
    print(f"\nResult: {passed}/{len(tests)} passed.")
    print(f"Total words in filter: {len(pf.words)}")

if __name__ == "__main__":
    test_profanity()
