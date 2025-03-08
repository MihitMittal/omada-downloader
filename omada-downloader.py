from bs4 import BeautifulSoup
import requests

def get_latest():
    web_data = requests.get("https://support.omadanetworks.com/us/product/omada-software-controller/?resourceType=download")
    assert web_data.status_code in range(200, 300)
    soup = BeautifulSoup(web_data.content, "html.parser")
    urls = soup.find_all("a", attrs={"data-vars-event-category": "Product_Download_Download"})
    urls = [i["href"] for i in urls if ".deb" in i["href"]]
    urls.sort(reverse=True)
    return urls[0]

def main():
    with open("omada_latest.deb", "wb") as file:
        file.write(requests.get(get_latest()).content)

if __name__ == '__main__':
    main()