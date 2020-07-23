import requests
from bs4 import BeautifulSoup


class Section:
    name = ""
    items = []

    def __init__(self, name):
        self.name = name
        self.items = []

    def add_item(self, item):
        self.items.append(item)


class Item:
    name = ""
    description = ""
    price = []

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price


def scrape():
    section_names = ["Signature Collection", "Classic Collection", "Shakes"]
    URL = 'https://www.thedejavueffect.com/menu'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(id="page")

    menu_sections = result.find_all('div', class_='menu-section')
    menu = []

    for i in range(len(menu_sections)):
        section = Section(section_names[i])
        section_items = menu_sections[i].find_all('div', class_="menu-item")
        for x in range(len(section_items)):
            item = Item(section_items[x].contents[3].text, section_items[x].contents[5].text, section_items[x].contents[7].text)
            section.add_item(item)
        menu.append(section)

    return menu


def create_html(menu):
    for x in range(len(menu)):
        html = open("index.html")
        soup = BeautifulSoup(html, "html.parser")

        soup.find(text="TITLE_PLACEHOLDER").replaceWith(menu[x].name)

        for i in range(12):
            if i < len(menu[x].items):
                soup.find(text="COCKTAIL_" + str(i)).replaceWith(menu[x].items[i].name)
                soup.find(text="PRICE_" + str(i)).replaceWith(menu[x].items[i].price)
                soup.find(text="DESCRIPTION_" + str(i)).replaceWith(menu[x].items[i].description)
            else:
                soup.find(text="COCKTAIL_" + str(i)).replaceWith("")
                soup.find(text="PRICE_" + str(i)).replaceWith("")
                soup.find(text="DESCRIPTION_" + str(i)).replaceWith("")

        Html_file = open(menu[x].name+".html", "w")
        Html_file.write(soup.prettify(formatter="html"))
        Html_file.close()


def main():
    menu = scrape()
    create_html(menu)


if __name__ == "__main__":
    main()
