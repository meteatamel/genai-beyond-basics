import sys
import time


def main():
    text = sys.stdin.read().strip()
    words = text.split()
    for i, word in enumerate(words, 1):
        print(f"[{i}/{len(words)}] {word.upper()}", flush=True)
        time.sleep(0.3)


if __name__ == "__main__":
    main()
