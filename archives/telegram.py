import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
from urllib.parse import unquote

site = "https://web.telegram.org/#/im?p=@UpscMaterials"


def main(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    target = [f"{url[:25]}{item.get('href')}"
              for item in soup.findAll("a", title="Annual Report")]
    return target


def parse(url):
    with requests.Session() as req:
        r = req.get(url)
        match = [unquote(f"{r.url[:25]}{match.group(1)}") for match in re.finditer(
            r"Override=(.+?)\"", r.text)]
        return match


with ThreadPoolExecutor(max_workers=50) as executor:
    futures = [executor.submit(parse, url) for url in main(site)]

links = []
for future in futures:
    links.extend(future.result())

print(f"Collected {len(links)}")


def download(url):
    with requests.Session() as req:
        r = req.get(url)
        if r.status_code == 200 and r.headers['Content-Type'] == "application/pdf;charset=UTF-8":
            name = r.url.rfind("/") + 1
            name = r.url[name:]
            return f"Saving {name}"
            with open(f"{name}", 'wb') as f:
                f.write(r.content)
        else:
            pass


with ThreadPoolExecutor(max_workers=50) as executor:
    futures = [executor.submit(download, url) for url in links]

for future in as_completed(futures):
    print(future.result())