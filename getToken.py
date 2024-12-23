import os
import sys
import random
import string
import time
from colorama import init, Fore, Style
import requests

#colorama init
init(autoreset=True)

#declare variable
PROXY_FILE = 'proxy.txt'
TOKEN_FILE = 'token_list.txt'
ACCOUNTS_FILE = 'accounts.txt'
FAILED_ACCOUNTS_FILE = 'failed_accounts.txt'

# Logo For script 
logo = """
   _  __       __                      ___      ___                 __
  / |/ ___ ___/ ___ ___ ___ ___ ______/ _ \___ / ____ ___________ _/ /
 /    / _ / _  / -_/ _ / _ `/ // /___/ , _/ -_/ _/ -_/ __/ __/ _ `/ / 
/_/|_/\___\_,_/\__/ .__\_,_/\_, /   /_/|_|\__/_/ \__/_/ /_/  \_,_/_/  
                 /_/       /___/                                      
"""

# Line Function 
def linex():
    print(f"{Fore.LIGHTWHITE_EX}========================================================={Style.RESET_ALL}")

# Get Captcha token 
def get_token():
    while True:
        res = requests.get('http://localhost:5000/get').text
        if 'None' not in res:
            print(f"{Fore.GREEN}Successfuly Get Captcha Token!{Style.RESET_ALL}")
            return res
        else:
            time.sleep(0.5)
# Read and Write to TXT
def read_proxy(file_path):
    proxies = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()  
                if line:  
                    proxies.append(line)  
    except Exception as e:
        print(f'{Fore.LIGHTRED_EX}Error reading file: {str(e)}{Style.RESET_ALL}')
    return proxies
def read_credentials(file_path):
    credentials = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()  
            if line:  
                parts = line.split('|')
                if len(parts) == 2:  
                    email, password = parts
                    credentials.append((email, password))
                else:
                    print(f'{Fore.LIGHTRED_EX}Invalid line format: {line}{Style.RESET_ALL}')
    except Exception as e:
        print(f'{Fore.LIGHTRED_EX}Error reading file: {str(e)}{Style.RESET_ALL}')
    return credentials

def write_token(token):
    with open(TOKEN_FILE, 'a') as file:
        file.write(f"{token} \n")

def write_failed_accounts(failed_accounts):
    with open(FAILED_ACCOUNTS_FILE, 'a') as file:
        for account in failed_accounts:
            file.write(f"{account} \n")

# Main Function
def clear_screen():
    if sys.platform.startswith('win'):
        os.system('cls')
        print(f"{Fore.CYAN}{logo}{Style.RESET_ALL}")
    else:
        os.system('clear')
        print(f"{Fore.CYAN}{logo}{Style.RESET_ALL}")

def get_ip(proxy_url):
    proxy = {'http': proxy_url,'https': proxy_url}
    try:
        response = requests.get('http://ip-api.com/json',proxies=proxy)
        return response.json()['query']
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Error: {str(e)}{Style.RESET_ALL}")
        return None

def get_headers(auth_token=None):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://app.nodepay.ai',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }
    if auth_token:
        headers['Authorization'] = f'Bearer {auth_token}'
        headers['origin'] = 'chrome-extension://lgmpfmgeabnnlemejacfljbmonaomfmm'
    return headers
def login_accounts(email, password, captcha_token, proxy_url):
    try:
        json_data = {
            'user': email,
            'password': password,
            'remember_me': True,
            'recaptcha_token': captcha_token
        }
        proxy_url = {'http': proxy_url, 'https': proxy_url}
        headers = get_headers()
        url = "https://api.nodepay.ai/api/auth/login"
        response = requests.post(url, headers=headers, json=json_data, proxies=proxy_url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        linex()
        time.sleep(1)

# Main function for processing full action
def main():
    clear_screen()

    credentials = read_credentials(ACCOUNTS_FILE)
    failed_logins = []

    if os.path.exists(FAILED_ACCOUNTS_FILE):
        print(f"{Fore.YELLOW}Detected failed_accounts.txt, will be cleared for new failed account{Style.RESET_ALL}")
        os.remove(FAILED_ACCOUNTS_FILE)
        linex()

    if os.path.exists(TOKEN_FILE):
        print(f"{Fore.YELLOW}Detected token_list.txt, will be cleared for new token{Style.RESET_ALL}")
        os.remove(TOKEN_FILE)
        linex()
    
    if not credentials:
        print(f"{Fore.LIGHTRED_EX}No accounts found in accounts.txt{Style.RESET_ALL}")
        linex()
        time.sleep(1)
        return None

    for email, password in credentials:
        print(f"Processing account: {email}, length: {len(credentials)}")
        print(f"{Fore.GREEN}Email: {email}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Password: {password}{Style.RESET_ALL}")

        captcha_token = get_token()
        proxy_url = None

        print(f"{Fore.WHITE}Captcha Token: {captcha_token}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Proxy: {proxy_url}{Style.RESET_ALL}")

        response_data = login_accounts(email, password, captcha_token, proxy_url)
        
        if response_data and response_data.get('msg') == 'Success':
            auth_token = response_data['data']['token']
            print(f"{Fore.GREEN}Login Successful! email: {email} | Auth Token: {auth_token}{Style.RESET_ALL}")
            linex()
            write_token(auth_token)
        else:
            print(f"{Fore.LIGHTRED_EX}Login Failed: {response_data.get('msg', 'Unknown error')}{Style.RESET_ALL}")
            linex()
            failed_logins.append(f"{email}|{password}")

    if failed_logins:        
        print(f"{Fore.LIGHTRED_EX}Saving Failed logins creds into failed_accounts.txt: {len(failed_logins)}{Style.RESET_ALL}")
        write_failed_accounts(failed_logins)
    
    
    print(f"{Fore.GREEN}Token has been saved into token_list.txt{Style.RESET_ALL}")
    exit()
    
if __name__ == "__main__":
    main()

