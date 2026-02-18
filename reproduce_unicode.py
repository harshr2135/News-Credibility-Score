
import sys
import io

# Apply the fix
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def test_unicode_print():
    print(f"Stdout encoding: {sys.stdout.encoding}")
    
    # Test string with various unicode characters:
    # 1. Emoji (😊)
    # 2. Hindi (नमस्ते)
    # 3. Smart quotes (“”)
    # 4. Math symbol (∑)
    test_str = "Unicode test: 😊 नमस्ते “Smart Quotes” ∑"
    
    try:
        print(f"Attempting to print: {test_str}")
        print("Success!")
    except UnicodeEncodeError as e:
        print(f"\nFAILURE: UnicodeEncodeError caught: {e}")
        print("This confirms that printing unicode characters to this console causes a crash.")
    except Exception as e:
        print(f"\nFAILURE: Other error caught: {e}")

if __name__ == "__main__":
    test_unicode_print()
