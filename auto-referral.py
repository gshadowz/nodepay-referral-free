import os
import sys
import random
import string
import time
from colorama import init, Fore, Style
import requests

init(autoreset=True)

PROXY_FILE = 'proxy.txt'
TOKEN_FILE = 'token_list.txt'
ACCOUNTS_FILE = 'accounts.txt'

logo = r"""
   _  __       __                      ___      ___                 __
  / |/ ___ ___/ ___ ___ ___ ___ ______/ _ \___ / ____ ___________ _/ /
 /    / _ / _  / -_/ _ / _ `/ // /___/ , _/ -_/ _/ -_/ __/ __/ _ `/ / 
/_/|_/\___\_,_/\__/ .__\_,_/\_, /   /_/|_|\__/_/ \__/_/ /_/  \_,_/_/  
                 /_/       /___/                                      
"""

def linex():
    print(f"{Fore.LIGHTWHITE_EX}========================================================={Style.RESET_ALL}")

def clear_screen():
    if sys.platform.startswith('win'):
        os.system('cls')
        print(f"{Fore.LIGHTCYAN_EX}{logo}{Style.RESET_ALL}")
    else:
        os.system('clear')
        print(f"{Fore.LIGHTCYAN_EX}{logo}{Style.RESET_ALL}")

def get_token():
    while True:
        res = requests.get('http://localhost:5000/get').text
        if 'None' not in res:
            if 'Not Found' in res:
                print(f"{Fore.LIGHTRED_EX}Error: {res}{Style.RESET_ALL}")
            else:    
                print(f"{Fore.LIGHTGREEN_EX}Successfuly Get Captcha Token!{Style.RESET_ALL}")
            return res
        else:
            time.sleep(0.5)

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

def write_credentials(credentials):
    with open(ACCOUNTS_FILE, 'a') as file:
        for email, password in credentials:
            file.write(f"{email}|{password}\n")

def write_token(token):
    with open(TOKEN_FILE, 'a') as file:
        file.write(f"{token}\n")

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

def register_accounts(email, password, username, ref_code, proxy_url=None, captcha_token=None):
    try:
        if proxy_url:
            print(f"{Fore.LIGHTGREEN_EX}Using Proxy : {proxy_url}{Style.RESET_ALL}")
            proxy_url = {'http': proxy_url,'https': proxy_url}
        register_data = {
            'email': email,
            'password': password,
            'username': username,
            'referral_code': ref_code,
            'recaptcha_token': captcha_token
        }
        headers = get_headers()
        url = "https://api.nodepay.ai/api/auth/register"
        response = requests.post(url,headers=headers,json=register_data,proxies=proxy_url,timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Error: {str(e)}{Style.RESET_ALL}")
        linex()
        time.sleep(1)

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
        print(f"{Fore.LIGHTRED_EX}Error: {str(e)}{Style.RESET_ALL}")
        linex()
        time.sleep(1)

def activate_account(auth_token,proxy_url):
    try:
        json_data={}
        url = "https://api.nodepay.ai/api/auth/active-account"
        headers = get_headers(auth_token)
        proxy_url = {'http': proxy_url,'https': proxy_url}

        response = requests.post(url, headers=headers,json=json_data,proxies=proxy_url,timeout=5)
        response.raise_for_status()

        if response.json()['msg'] != 'Success':
            response = requests.post(url, headers=headers,json=json_data,proxies=proxy_url,timeout=5)
            response.raise_for_status()

        return response.json()
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Error: {str(e)}{Style.RESET_ALL}")
        linex()
        time.sleep(1)


def main():
    proxy = read_proxy(PROXY_FILE)
    success = 0
    fail = 0
    clear_screen()

    if os.path.exists(TOKEN_FILE):
        print(f"{Fore.LIGHTYELLOW_EX}Detected {TOKEN_FILE} in current directory, will be deleted for new token{Style.RESET_ALL}")
        os.remove(TOKEN_FILE)
        linex()

    ref_amount = int(input(f'{Fore.LIGHTCYAN_EX}>> Input Your Reff Amount: {Style.RESET_ALL}'))
    ref_code = input(f'{Fore.LIGHTCYAN_EX}>> Input Your Referral Code: {Style.RESET_ALL}')

    if ref_amount < 0 or ref_amount == 0:
        print(f"{Fore.LIGHTRED_EX}Error: Value Must Be Greater Than 0!{Style.RESET_ALL}")
        exit()

    if ref_code == "":
        print(f"{Fore.LIGHTRED_EX}Error: Referral Code Cannot Be Empty!{Style.RESET_ALL}")
        exit()
    
    for ref in range(ref_amount):
        try:
            print(f"{Fore.LIGHTGREEN_EX}Processing Referral... {str(ref+1)}/{str(ref_amount)}, Complete: {((ref+1) / ref_amount) * 100:.2f}%{Style.RESET_ALL}")
            
            domains = ["@gmail.com", "@outlook.com", "@yahoo.com", "@hotmail.com"]
            characters = string.ascii_letters + string.digits
            username = str(''.join(random.choice(characters) for _ in range(12))).lower()
            password = str(''.join(random.choice(string.ascii_letters) for _ in range(6)) + 'Rc3@' + ''.join(random.choice(string.digits) for _ in range(3)))
            email = f"{username}{str(random.choice(domains))}"
            proxy_url = random.choice(proxy)
            captcha_token = get_token()
            
            response = register_accounts(email, password, username, ref_code, proxy_url, captcha_token)

            if response['msg'] == 'Success':
                print(f"{Fore.LIGHTGREEN_EX}Register {email} Success!{Style.RESET_ALL}")

                captcha_token = get_token()

                response = login_accounts(email, password, captcha_token, proxy_url)

                if response['msg'] == 'Success':
                    print(f"{Fore.LIGHTGREEN_EX}Login into {email} Success!{Style.RESET_ALL}")
                    auth_token = response['data']['token']
                    response = activate_account(auth_token,proxy_url)

                    if response['msg'] == 'Success':
                        print(f"{Fore.LIGHTGREEN_EX}Referral Success!{Style.RESET_ALL}")
                        write_credentials([(email, password)])
                        write_token(auth_token)
                        success += 1
                        linex()
                    else:
                        print(f"{Fore.LIGHTRED_EX}Error: {response['msg']}{Style.RESET_ALL}")
                        fail += 1
                        linex()
                else:
                    print(f"{Fore.LIGHTRED_EX}Error: {response['msg']}{Style.RESET_ALL}")
                    fail += 1
                    linex()
            else:
                print(f"{Fore.LIGHTRED_EX}Error: {response['msg']}{Style.RESET_ALL}")
                fail += 1
                linex()

        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}Error: {str(e)}{Style.RESET_ALL}")
            fail += 1
            linex()

    print(f"{Fore.LIGHTGREEN_EX}Referral Completed!{Style.RESET_ALL}\n")

    print(f"{Fore.LIGHTGREEN_EX}All Account Credentials is Saved into {ACCOUNTS_FILE}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTGREEN_EX}All Account Token is Saved into {TOKEN_FILE}\n{Style.RESET_ALL}")

    print(f"{Fore.LIGHTGREEN_EX}Total Success: {success}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTRED_EX}Total Failed: {fail}{Style.RESET_ALL}")
    exit()
    
if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}\nCtrl + C is pressed..., Exiting...{Style.RESET_ALL}")
        exit()
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}\nError: {str(e)}{Style.RESET_ALL}")
        exit()

