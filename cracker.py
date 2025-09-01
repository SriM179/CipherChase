import hashlib

def crackHash(inputPass): 
    try: 
        with open("list.txt", "r") as file:
            for password in file: 
                password = password.strip()
                pwd = password.encode("utf-8")
                check = hashlib.md5(pwd).hexdigest()

                if check == inputPass: 
                    print("password: " + password)
                    return

            print("password is not found!!")
    except FileNotFoundError: 
            print("Could not find the file!")


if __name__ == '__main__':
    crackHash("827ccb0eea8a706c4c34a16891f84e7b")