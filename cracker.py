import hashlib
import itertools
import string

def detect_hash(input_hash): 
    hash_length = len(input_hash)
    if hash_length == 32: 
        return "md5"
    elif hash_length == 40: 
        return "sha1"
    elif hash_length == 64: 
        return "sha256"
    elif hash_length == 128: 
        return "sha512"

    else: 
        raise ValueError("unknown hash type")

def hash_string(word, a): 
    h = hashlib.new(a)
    h.update(word.encode("utf-8"))
    return h.hexdigest()


def dictionary_attack(input_hash, a): #dictionary attack
    try: 
        with open("list.txt", "r") as file:
            for password in file: 
                password = password.strip()
                check = hash_string(password, a)

                if check == input_hash: 
                    return password
        return None

    except FileNotFoundError: 
            print("Could not find the file!")
            return None

def brute_force(input_hash, a, max_length=8, exact_len=None):
    chars = string.ascii_lowercase + string.digits
    lengths = [exact_len] if exact_len else range(1, max_length + 1)

    for l in lengths:
        print(f"[*] Trying length {l}...")
        for guess in itertools.product(chars, repeat=l):
            guess = ''.join(guess)
            hashed_guess = hash_string(guess, a)
            if hashed_guess == input_hash:
                return guess
    return None

def crack_hash(input_hash, max_length=8):
    try:
        a = detect_hash(input_hash)
        print(f"[*] Detected hash algorithm: {a.upper()}")
    except ValueError as e:
        print(e)
        return

    # Step 1: Dictionary attack
    password = dictionary_attack(input_hash, a)
    if password:
        print(f"[+] Password found (dictionary): {password}")
        return

    # Step 2: Ask user if they know the password length
    exact_len = input("Do you know the exact password length? (Press Enter if not): ").strip()
    exact_len = int(exact_len) if exact_len.isdigit() else None

    print("[*] Trying brute force... (this may take a while)")
    password = brute_force(input_hash, a, max_length, exact_len)
    if password:
        print(f"[+] Password found (brute-force): {password}")
    else:
        print("[-] Password not found.")

if __name__ == '__main__':
    input_hash = input("Enter the hash you want to crack: ").strip()
    crack_hash(input_hash, max_length=8)
