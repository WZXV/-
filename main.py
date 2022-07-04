from bs4 import BeautifulSoup
import requests
import re
import csv

res = ""
i = 1


def pars(page):
    global i, res

    req = requests.get("https://vuzopedia.ru/region/city/59?s=tekhnicheskie&page=" + str(page)).text
    soup = BeautifulSoup(req, "html.parser")

    for card in soup.find_all("div", {"class": ["itemVuz", "itemVuzPremium"]}):
        for content in card.find_all(class_="vuzesfullnorm"):
            res += f"https://vuzopedia.ru/{content.select_one('div > a')['href']}\n"
            i += 1


for b in range(1, 3):
    pars(b)
with open("links.txt", "w") as f:
    f.write(res)




with open("links.txt") as f:
    for link in f.readlines():
        inf_tech = requests.get(f"{link[:-1]}/napr/43")
        inf_security = requests.get(f"{link[:-1]}/napr/39")
        just_inf = requests.get(f"{link[:-1]}/napr/91")
        math_inf = requests.get(f"{link[:-1]}/napr/98")
        with open("res.csv", "a") as csv_file:
            writer = csv.writer(csv_file)
            tmp = [inf_tech, inf_security, just_inf, math_inf]
            for el in tmp:
                if el.history:
                    continue
                else:
                    source = el
                    break
            soup = BeautifulSoup(source.text, "html.parser")
            regx = re.compile(r"в\s+(.+?):")
            try:
                result = re.search(regx, soup.find(class_="mainTitle").text.strip()).group(1)
                writer.writerow([result])
            except AttributeError:
                writer.writerow([link])
            if inf_tech.history:
                writer.writerow(['Информатика и вычислительная техника', "НЕТУ"])
            else:
                soup = BeautifulSoup(inf_tech.text, "html.parser")
                result_1 = soup.find("div", {"class": "optItem"}).find("p", {"class": "optTitle"}).text
                writer.writerow(['Информатика и вычислительная техника', result_1])
            if inf_security.history:
                writer.writerow(['Информационная безопасность', "НЕТУ"])
            else:
                soup = BeautifulSoup(inf_security.text, "html.parser")
                result_2 = soup.find("div", {"class": "optItem"}).find("p", {"class": "optTitle"}).text
                writer.writerow(['Информационная безопасность', result_2])
            if just_inf.history:
                writer.writerow(['Прикладная информатика', "НЕТУ"])
            else:
                soup = BeautifulSoup(just_inf.text, "html.parser")
                result_3 = soup.find("div", {"class": "optItem"}).find("p", {"class": "optTitle"}).text
                writer.writerow(['Прикладная информатика', result_3])
            if math_inf.history:
                writer.writerow(['Прикладная математика и информатика', "НЕТУ"])
            else:
                soup = BeautifulSoup(math_inf.text, "html.parser")
                result_4 = soup.find("div", {"class": "optItem"}).find("p", {"class": "optTitle"}).text
                writer.writerow(['Прикладная математика и информатика', result_4])
            writer.writerow("\n")

