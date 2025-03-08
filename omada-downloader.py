from bs4 import BeautifulSoup
import requests
import hashlib

def get_latest():
    web_data = requests.get("https://support.omadanetworks.com/us/product/omada-software-controller/?resourceType=download")
    assert web_data.status_code in range(200, 300)
    soup = BeautifulSoup(web_data.content, "html.parser")
    urls = soup.find_all("a", attrs={"data-vars-event-category": "Product_Download_Download"})
    urls = [i["href"] for i in urls if ".deb" in i["href"]]
    urls.sort(reverse=True)
    return urls[0]

def get_sha256_hash(filename):
    sha256 = hashlib.sha256()
    with open(filename, "rb") as file:
        while chunk := file.read(8192):  # Read file in chunks
            sha256.update(chunk)
    return sha256.hexdigest()

def main():
    latest_url = get_latest()
    remote_package_version = latest_url.split("/")[-1].split("_")[3]
    print(f"Downloading version: {remote_package_version}")
    with open("omada_latest.deb", "wb") as file:
        file.write(requests.get(latest_url).content)
    print(f"File SHA256: {get_sha256_hash('omada_latest.deb')}")

if __name__ == '__main__':
    main()