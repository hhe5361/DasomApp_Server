from bs4 import BeautifulSoup
import requests

baseurl = "https://www.itworld.co.kr/topnews"

def GetCardNewList(param_page: int):
    try:
        res = requests.get(baseurl, params={"page": param_page})
        res.raise_for_status() 

        soup = BeautifulSoup(res.text, "html.parser")
        cardNewsList = soup.find("div", {"class": "node-list"}).find_all("div", {"class": "mb-4"})
        return cardNewsList
    except requests.RequestException as e:
        print(f"Error making request: {e}")
        return None  

def GetData(obj: BeautifulSoup):
    temp = {}
    try:
        temp['img'] = obj.select_one('img')['src']
        temp['link'] = obj.select_one('a')['href']
        temp['headline'] = obj.select_one("h5.card-title").get_text(strip=True)
        temp['content'] = obj.select_one("p.card-text").get_text(strip=True)
        temp['timeline'] = obj.select_one("small").get_text(strip=True)
    except AttributeError as e:
        print(f"Error parsing data: {e}")
        return None  

    return temp

def GetAllData():
    data = []

    data.clear()

    for page in range(5):
        soup = GetCardNewList(page)
        if soup:
            for temp in soup:
                parser_data = GetData(temp)
                if parser_data:
                    data.append(parser_data)
        else: return None
    return data
