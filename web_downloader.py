import os
import requests
from colorama import Fore, init

init(autoreset=True)

where_to_save = input(Fore.GREEN + "Enter the directory where you want to save the downloaded files: ")

if not os.path.exists(where_to_save):
    try:
        os.makedirs(where_to_save)
        print(Fore.BLUE + f"Directory '{where_to_save}' created successfully.")
    except Exception as e:
        print(Fore.RED + f"Error creating directory '{where_to_save}': {e}")
        exit(1)
else:
    print(Fore.BLUE + f"Directory '{where_to_save}' already exists.")

qst = input(Fore.GREEN + "Give the domain to download from (e.g., example.com): ").replace("http://", "").replace("https://", "").strip()
if not qst:
    print(Fore.RED + "No domain provided. Exiting.")
    exit(1)

url = "http://" + qst
print(Fore.BLUE + f"Collecting from URL: {url}")

os.system(f"katana -u {url} -cs {url} -o {where_to_save}/urls.txt > /dev/null 2>&1")
os.system(f"waybackurls {url} >> {where_to_save}/urls.txt")
os.system(f"httpx -l {where_to_save}/urls.txt -mc 200 -o {where_to_save}/valid_urls.txt > /dev/null 2>&1")
os.system(f"sort -u {where_to_save}/valid_urls.txt -o {where_to_save}/valid_urls.txt")

print(Fore.BLUE + f"All valid URLs have been saved to '{where_to_save}/valid_urls.txt'")

print(Fore.GREEN + "\nStarting HTML downloads...\n")

with open(f"{where_to_save}/valid_urls.txt", "r") as f:
    urls = [line.strip() for line in f.readlines() if line.strip()]

for u in urls:
    try:
        path = u.replace("http://", "").replace("https://", "")
        path_parts = path.split("/", 1)

        if len(path_parts) == 1:
            local_path = os.path.join(where_to_save, "index.html")
        else:
            local_path = os.path.join(where_to_save, path_parts[1])

        if local_path.endswith("/"):
            local_path = os.path.join(local_path, "index.html")

        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        r = requests.get(u, timeout=10)
        if r.status_code == 200:
            with open(local_path, "wb") as out:
                out.write(r.content)
            print(Fore.BLUE + f"[OK] {u} -> {local_path}")
        else:
            print(Fore.YELLOW + f"[WARN] {u} returned status {r.status_code}")

    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to download {u}: {e}")

print(Fore.GREEN + "\nAll downloads completed successfully!\n")

