import streamlit as st
import hashlib
import itertools
import os
import concurrent.futures
from time import time

# ----------------------------
# Hash detection based on length
# ----------------------------
def detect_hash(input_hash):
    length = len(input_hash)
    if length == 32:
        return "md5"
    elif length == 40:
        return "sha1"
    elif length == 64:
        return "sha256"
    elif length == 128:
        return "sha512"
    else:
        return None

# ----------------------------
# Hash a string using given algo
# ----------------------------
def hash_string(text, algo):
    h = hashlib.new(algo)
    h.update(text.encode())
    return h.hexdigest()

# ----------------------------
# Dictionary attack
# ----------------------------
def dictionary_attack(input_hash, algo, wordlist="rockyou.txt"):
    try:
        with open(wordlist, "r", encoding="latin-1") as file:
            for word in file:
                word = word.strip()
                if hash_string(word, algo) == input_hash:
                    return word
        return None
    except FileNotFoundError:
        st.error("RockYou wordlist not found!")
        return None

# ----------------------------
# Hybrid attack
# ----------------------------
def hybrid_attack(input_hash, algo, base_words, max_numbers=4, symbols="!@#$%", years=("2023","2024","2025")):
    subs = {"a": "@", "i": "1", "e": "3", "o": "0", "s": "$", "g": "9"}
    numbers = [str(n) for n in range(0, 10 ** max_numbers)]
    patterns = numbers + list(symbols) + list(years)

    for word in base_words:
        # Leet variants
        leet = "".join([subs.get(ch.lower(), ch) for ch in word])
        variants = {word, leet}

        for base in variants:
            # Append/prepend patterns
            for pattern in patterns:
                candidate1 = base + pattern
                candidate2 = pattern + base
                if hash_string(candidate1, algo) == input_hash:
                    return candidate1
                if hash_string(candidate2, algo) == input_hash:
                    return candidate2
    return None

# ----------------------------
# Brute force worker
# ----------------------------
def brute_worker(chars, length, input_hash, algo):
    for guess in itertools.product(chars, repeat=length):
        pwd = "".join(guess)
        if hash_string(pwd, algo) == input_hash:
            return pwd
    return None

# ----------------------------
# Multi-threaded brute force
# ----------------------------
def brute_force(input_hash, algo, max_len=6, threads=4, mask=None):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"

    if mask:
        mask_map = {
            "?l": "abcdefghijklmnopqrstuvwxyz",
            "?u": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "?d": "0123456789",
            "?s": "!@#$%^&*",
            "?a": chars
        }
        positions = [mask_map.get(mask[i:i+2], mask[i]) for i in range(0, len(mask), 2)]
        for guess in itertools.product(*positions):
            pwd = "".join(guess)
            if hash_string(pwd, algo) == input_hash:
                return pwd
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for length in range(1, max_len + 1):
            futures = [executor.submit(brute_worker, chars, length, input_hash, algo)]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    return result
    return None

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("🔐 Universal Hash Cracker")

st.warning("⚠️ This tool is for educational purposes only. Do not use it on unauthorized accounts or systems.")

input_hash = st.text_input("Enter the hash to crack:")
algo = st.selectbox("Select hashing algorithm", ["Auto Detect", "md5", "sha1", "sha256", "sha512"])
mask = st.text_input("Optional mask pattern (e.g. ?l?l?l?d?d)")
threads = st.slider("Number of Threads", 1, os.cpu_count(), 4)
max_len = st.slider("Max password length (for brute force)", 1, 8, 5)
attack_style = st.selectbox(
    "Select attack style",
    ["Dictionary Only", "Hybrid Only", "Brute Force Only", "Dictionary → Hybrid → Brute Force"]
)

if st.button("Crack Hash"):
    if not input_hash:
        st.error("Please enter a hash!")
    else:
        # Detect hash if Auto Detect selected
        if algo == "Auto Detect":
            algo = detect_hash(input_hash)
            if not algo:
                st.error("Unknown hash type! Please select manually.")
            else:
                st.info(f"Auto-detected algorithm: **{algo.upper()}**")

        start = time()
        pwd = None

        # Dictionary Attack
        if attack_style in ["Dictionary Only", "Dictionary → Hybrid → Brute Force"]:
            st.write("Step 1: Dictionary Attack")
            pwd = dictionary_attack(input_hash, algo)
            if pwd:
                st.success(f"Password found via dictionary: `{pwd}` in {time()-start:.2f}s")
                if attack_style != "Dictionary → Hybrid → Brute Force":
                    st.stop()

        # Hybrid Attack
        if attack_style in ["Hybrid Only", "Dictionary → Hybrid → Brute Force"]:
            st.write("Step 2: Hybrid Attack")
            base_words = [pwd] if pwd else []
            pwd = hybrid_attack(input_hash, algo, base_words)
            if pwd:
                st.success(f"Password found via hybrid: `{pwd}` in {time()-start:.2f}s")
                if attack_style != "Dictionary → Hybrid → Brute Force":
                    st.stop()

        # Brute Force
        if attack_style in ["Brute Force Only", "Dictionary → Hybrid → Brute Force"]:
            st.write("Step 3: Brute Force")
            pwd = brute_force(input_hash, algo, max_len, threads, mask)
            if pwd:
                st.success(f"Password found via brute-force: `{pwd}` in {time()-start:.2f}s")
            else:
                st.error("Password not found.")
