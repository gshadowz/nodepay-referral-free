import os
import sys
import random
import string
import time
from colorama import init, Fore, Style
import requests

#colorama init
init(autoreset=True)

# Logo For script 
logo = """
 __  __              __                                              ____               ___    ___                      ___      
/\ \/\ \            /\ \                                            /\  _`\           /'___\ /'___\                    /\_ \     
\ \ `\\ \    ___    \_\ \     __   _____      __     __  __         \ \ \L\ \     __ /\ \__//\ \__/   __   _ __    __  \//\ \    
 \ \ , ` \  / __`\  /'_` \  /'__`\/\ '__`\  /'__`\  /\ \/\ \  _______\ \ ,  /   /'__`\ \ ,__\ \ ,__\/'__`\/\`'__\/'__`\  \ \ \   
  \ \ \`\ \/\ \L\ \/\ \L\ \/\  __/\ \ \L\ \/\ \L\.\_\ \ \_\ \/\______\\ \ \\ \ /\  __/\ \ \_/\ \ \_/\  __/\ \ \//\ \L\.\_ \_\ \_ 
   \ \_\ \_\ \____/\ \___,_\ \____\\ \ ,__/\ \__/.\_\\/`____ \/______/ \ \_\ \_\ \____\\ \_\  \ \_\\ \____\\ \_\\ \__/.\_\/\____\
    \/_/\/_/\/___/  \/__,_ /\/____/ \ \ \/  \/__/\/_/ `/___/> \         \/_/\/ /\/____/ \/_/   \/_/ \/____/ \/_/ \/__/\/_/\/____/
                                     \ \_\               /\___/                                                                  
                                      \/_/               \/__/                                                                   
"""

proxy_list = open('proxy.txt', 'r').read().splitlines()

# Line Function 
def linex():
    print('\033[0m================================================')

# Get Captcha token 
def get_token():
    while True:
        res = requests.get('http://localhost:5000/get').text
        if 'None' not in res:
            print(f"{Fore.GREEN}Successfuly Get Captcha Token!{Style.RESET_ALL}")
            return res
        else:
            time.sleep(0.5)

# Clear terminal session & print logo
def clear_screen():
    if sys.platform.startswith('win'):
        os.system('cls')
        print(logo)
    else:
        os.system('clear')
        print(logo)

# Get IP using proxy / not using for speed up
def get_ip(proxy_url):
    proxy = {'http': proxy_url, 'https': proxy_url}
    try:
        response = requests.get('http://ip-api.com/json', proxies=proxy)
        return response.json()['query']
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        return None

# Get headers set / with `auth_token` or head only
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

# Login account and get authorization token
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

# def get_nodepay_token(email, password, captcha_token, proxy_url):
#     max_retry = 5;
#     for i in range(max_retry):
#         try:
#             print(f"{Fore.GREEN}Getting Nodepay Token within {max_retry - i}{Style.RESET_ALL}")

#             get_tokens = login_accounts(email, password, captcha_token, proxy_url)

#             if get_tokens['msg'] == 'Success':
#                 auth_token = get_tokens['token']
#                 print(f"{Fore.GREEN}Login Success, Auth Token: {auth_token}{Style.RESET_ALL}")
#                 with open('token_list.txt', 'w') as file:
#                     file.write(f"{email}:{auth_token}\n")
#                 return auth_token
#             else:
#                 msg = get_tokens['msg']
#                 print(f"{Fore.RED}Login Failed: {msg}, retrying {max_retry - i}{Style.RESET_ALL}")
#         except Exception as e:
#             print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

#     print(f"{Fore.RED}Failed to get Nodepay Token after {max_retry} retries{Style.RESET_ALL}")
#     return None
    

def read_credentials(file_path):
   credentials = []
   try:
       with open(file_path, 'r') as file:
           for line in file:
               line = line.strip()  # Menghapus whitespace
               if line:  # Pastikan baris tidak kosong
                   parts = line.split('|')
                   if len(parts) == 2:  # Pastikan ada dua elemen
                       email, password = parts
                       credentials.append((email, password))  # Menyimpan sebagai tuple
                   else:
                       print(f'Invalid line format: {line}')  # Menangani format yang salah
   except Exception as e:
       print(f'Error reading file: {str(e)}')
   return credentials

# Main function for processing full action
def main():
    clear_screen()
    credentials = read_credentials('accounts.txt')
    if not credentials:
        print(f"{Fore.RED}No accounts found in accounts.txt{Style.RESET_ALL}")
        linex()
        time.sleep(1)
        return None

    print(f"{Fore.GREEN}Accounts found in accounts.txt{Style.RESET_ALL}")
    linex()

    for email, password in credentials:
        print(f"{Fore.GREEN}Email: {email}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Password: {password}{Style.RESET_ALL}")

        captcha_token = get_token()
        print(f"Captcha Token: {captcha_token}")
        proxy_url = None
        response_data = login_accounts(email, password, captcha_token, proxy_url)
        
        if response_data and response_data.get('msg') == 'Success':
            auth_token = response_data['data']['token']
            print(f"{Fore.GREEN}Login Successful! Auth Token: {auth_token}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Login Failed: {response_data.get('msg', 'Unknown error')}{Style.RESET_ALL}")
            print(f"Response Data: {response_data}")
    
    # try:
    #     ref_limit = int(input('\033[0m>>\033[1;32m Put Your Referral Amount: '))
    # except:
    #     print('\033[1;32m⚠️ Input Wrong Default Referral Amount is 1k ')
    #     ref_limit = 1000
    #     time.sleep(1)
    # ref_code = input("\033[0m>>\033[1;32m Input referral code : ")
    # clear_screen()
    # success_count = 0
    # for atm in range(ref_limit):
    #     try:
    #         print(f'\r\r\033[0m>>\033[1;32m Processing  {str(success_count)}/{str(ref_limit)} complete : {((atm + 1) / ref_limit) * 100:.2f}% ')
    #         domains = ["@gmail.com", "@outlook.com", "@yahoo.com", "@hotmail.com"]
    #         characters = string.ascii_letters + string.digits
    #         username = str(''.join(random.choice(characters) for _ in range(12))).lower()
    #         password = str(''.join(random.choice(string.ascii_letters) for _ in range(6)) + 'Rc3@' + ''.join(random.choice(string.digits) for _ in range(3)))
    #         email = f"{username}{str(random.choice(domains))}"
    #         proxy_url = random.choice(proxy_list)
    #         captcha_token = get_token()
    #         response_data = reg_account(email, password, username, ref_code, proxy_url, captcha_token)
    #         if response_data['msg'] == 'Success':
    #             print(f'\r\r\033[0m>>\033[1;32m Account Created Successfully \033[0m')
    #             captcha_token = get_token()
    #             response_data = login_accounts(email, password, captcha_token, proxy_url)
    #             if response_data['msg'] == 'Success':
    #                 print(f'\r\r\033[0m>>\033[1;32m Account Login Successfully \033[0m')
    #                 auth_token = response_data['data']['token']
    #                 response_data = activate_recent_account(auth_token, proxy_url)
    #                 if response_data['msg'] == 'Success':
    #                     print(f'\r\r\033[0m>>\033[1;32m Successfully Referral Done \033[0m')
    #                     success_count += 1
    #                     open('accounts.txt', 'a').write(f"{str(email)}|{str(password)}|{str(auth_token)}\n")
    #                     time.sleep(1)
    #                 else:
    #                     print(f'\r\r\033[1;31m🌲 Referral Error, Not Success \033[0m {response_data["msg"]}')
    #                     time.sleep(1)
    #                     linex()
    #             else:
    #                 print(f'\r\r\033[1;31m🌲 Account Login Failed \033[0m {response_data["msg"]}')
    #                 time.sleep(1)
    #                 linex()
    #         else:
    #             print(f'\r\r\033[1;31m🌲 Account Creation Failed \033[0m {response_data["msg"]}')
    #             time.sleep(1)
    #             linex()
    #         linex()
    #     except Exception as e:
    #         print(f'\r\r\033[31m⚠️ Error: {str(e)} \033[0m')
    #         linex()
    #         time.sleep(1)
    # print('\r\r\033[0m>>\033[1;32m Your Referral Completed \033[0m')
    exit()

main()
