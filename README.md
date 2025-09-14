# 🔐 Universal Hash Cracker

## Description: 
An educational Streamlit app that demonstrates common password-cracking strategies—dictionary, hybrid, and multi-threaded brute force—against MD5, SHA-1, SHA-256, and SHA-512 hashes. Includes mask-based guessing, simple leet substitutions, and configurable performance settings.

Url: 

    https://cipher-chase.streamlit.app/

### Features: 
- Auto / manual hash detection: MD5, SHA-1, SHA-256, SHA-512
- Dictionary attack: tests a wordlist (e.g., rockyou.txt)
- Hybrid attack: leet substitutions + appended/prepended numbers, symbols, or years
- Brute force: multi-threaded search; optional mask patterns (e.g., ?l?l?l?d?d)
- Configurable UI: choose attack strategy, threads, max length, and masks
- Timing feedback: shows how long a successful attack took

### Usage (in the UI)
1. Enter the target hash (hex string).
2. Select algorithm or choose Auto Detect.
3. (Optional) Mask pattern for brute force (examples below).
4. Set Threads and Max password length.
5. Choose Attack style:
    - Dictionary Only
    - Hybrid Only
    - Brute Force Only
    - Dictionary → Hybrid → Brute Force (sequential)
Click Crack Hash to start. Results show per-phase progress and the total time if found.

#### How to Run: 
    streamlit run cracker.py

