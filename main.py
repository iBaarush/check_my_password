import requests
import hashlib
import sys

def request_api_data(query_char):                           #called in check_pass function
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res

def times_leaked(all_hashes, hash_to_check):                #called in check_pass function
    all_hashes = (line.split(':')for line in all_hashes.text.splitlines())
    for h, count in all_hashes:
        if h == hash_to_check:
            return count                            #checks if any of the hash matches the tail has to check
    return 0
def check_pass(password):
    hashed_password = (hashlib.sha1(password.encode('utf-8')).hexdigest().upper())
    first5_chars, tail = hashed_password[:5], hashed_password[5:]
    response = request_api_data(first5_chars)         #get all hashes that match first 5 characters
    return times_leaked(response, tail)               #to check which hash matches the tail and how many times pwned


def main():
    pass_words=[]
    file_name = ""           #text file path, where you give the password to check
    file = open(file_name,'r')
    for line in file:
        l = len(line)
        pass_words.append(line[:l-1])
 
    for password in pass_words:
        count = check_pass(password)
        if count:
            print(f"{password} was pwned {count} times, and you should probably change your password")
        else:
            print(f"Great password! {password} not pwned yet")
    return 'done!'
if __name__ == '__main__':                          #runs only if name of the file is "main"
    sys.exit(main())
    
