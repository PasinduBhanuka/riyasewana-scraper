import pandas as pd
from urllib.request import Request,urlopen
from bs4 import BeautifulSoup
import os

main_url = "https://riyasewana.com/search"


def get_no_results(soup):
    try:
        gr = soup.find("h2", attrs={"class": "results lside"})
    except AttributeError:
        gr = " "
    return gr


def get_title(soup):
    try:
        title = soup.find("h1").get_text(strip=True)
    except AttributeError:
        title = ""
    return title


def date_time_loc(soup):
    try:
        dt = soup.find("h2").get_text(strip=True).split()
        date = dt[-4]
        time = dt[-3] + dt[-2].replace(",", "")
        loc = dt[-1]
    except AttributeError:
        date, time, loc = "", "", ""
    return date, time, loc


def get_contact(soup):
    try:
        gc = soup.find("span", attrs={"class": "moreph"}).get_text(strip=True).replace(" ", "")
    except AttributeError:
        gc = ""
    return gc


def get_makeOprice(soup, spec_name):
    label = soup.find("p", class_="moreh", string=lambda t: t and spec_name.lower() in t.lower())
    if label:
        value_div = label.find_next("td", class_="aleft tfiv")
        return value_div.get_text(strip=True) if value_div else ""
    return ""


def get_modeYOMextra(soup, spec_name):
    label = soup.find("p", class_="moreh", string=lambda t: t and spec_name.lower() in t.lower())
    if label:
        value_div = label.find_next("td", class_="aleft")
        return value_div.get_text(strip=True) if value_div else ""
    return ""


def get_details(soup, spec_name):
    label = soup.find("p", class_="moreh", string=lambda t: t and spec_name.lower() in t.lower())
    if label:
        value_div = label.find_next("td", class_="aleft")
        return value_div.get_text(strip=True) if value_div else ""
    return ""


default_headers = {
    "authority": "www.google.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0"
}

user_agent = input("Hello there!\n, Behold… a data-hungry bot munching through Riyasewana.com!\nCrafted by PasinduBhanuka\n \nGo to httpbin.org/get and copy your User Agent.\nPaste it here: ").strip()
default_headers['User-Agent'] = user_agent

key_word = input("Enter the model to scrape : ").replace(" ", "-").lower()
base_url1 = (main_url + "/" + key_word)
web_req1 = Request(base_url1, headers=default_headers)
webpage1 = urlopen(web_req1).read()

soupt = BeautifulSoup(webpage1, "html.parser")
pp = get_no_results(soupt).text.split()

print(f"There are {pp[5]} results ")
no_results = int(input("How many results to scrape : "))

no_pages = int((no_results / 40) + 1)
scrap_counter = 0
main_list = []

d = {"Title": [], "Date": [], "Time": [], "Location": [], "Contact": [], "Make": [], "Model": [], "YOM": [],
     "Mileage(km)": [], "Gear": [],
     "Fuel Type": [], "Options": [], "Engine(cc)": [], "Price": [], "Details": [],"Link":[]}

for page in range(1, no_pages + 1):
    if page == 1:
        base_url = (main_url + "/" + key_word)
        search_urlp = base_url

    else:
        base_url = (main_url + "/" + key_word)
        search_urlp = (base_url + f"?page={page}")

    link_list = []
    web_req = Request(search_urlp, headers=default_headers)
    webpage = urlopen(web_req).read()

    soupt = BeautifulSoup(webpage, "html.parser")

    links = soupt.find_all("h2", attrs={"class": "more"})

    for link in links:
        a_tag = link.find("a")
        if a_tag:
            if scrap_counter >= no_results + no_pages:
                break
            link_list.append(a_tag.get("href")[1:])
            scrap_counter = scrap_counter + 1


    for link in link_list:
        product_req = Request("h" + link, headers=default_headers)
        product_page = urlopen(product_req).read()

        prdct_soup = BeautifulSoup(product_page, "html.parser")

        d["Title"].append(get_title(prdct_soup))
        date, time, loc = date_time_loc(prdct_soup)
        d["Date"].append(date)
        d["Time"].append(time)
        d["Location"].append(loc)
        d["Contact"].append(get_contact(prdct_soup))
        d["Make"].append(get_makeOprice(prdct_soup, "Make"))
        d["Model"].append(get_modeYOMextra(prdct_soup, "Model"))
        d["YOM"].append(get_modeYOMextra(prdct_soup, "YOM"))
        d["Mileage(km)"].append(get_modeYOMextra(prdct_soup, "Mileage (km)"))
        d["Gear"].append(get_modeYOMextra(prdct_soup, "Gear"))
        d["Fuel Type"].append(get_modeYOMextra(prdct_soup, "Fuel Type"))
        d["Options"].append(get_modeYOMextra(prdct_soup, "Options"))
        d["Engine(cc)"].append(get_modeYOMextra(prdct_soup, "Engine (cc)"))
        d["Price"].append(get_makeOprice(prdct_soup, "Price"))
        d["Details"].append(get_details(prdct_soup, "Details"))
        d["Link"].append(link)


    df = pd.DataFrame(d) 

save_name = input("Enter file name to save : ")

save_path = os.getcwd()
file_path = os.path.join(save_path, save_name + ".xlsx")
df.to_excel(file_path,index=False,sheet_name=save_name)
print("File saved at:", os.path.abspath(save_name))



















