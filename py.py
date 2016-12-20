import requests
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
#import sys
import re
import urllib

filepath = "./"  # "/home/vinayak/mini project data/".encode('utf-8')


def imagefun(url, modname, manname, year):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "lxml")
    hed = soup.title.text  # .encode('utf-8')
    hed = re.sub('[!@#$/~)(*&^%//\.]', '', hed)
    table = soup.find("div", class_="addstable")
    if table is not None:
        for row in table.findAll('img', class_="dbimage"):
            print(row['src'])
            urllib.request.urlretrieve(
                "http://www.carfolio.com" + row['src'],
                filepath + hed + ".jpg")


def fun(url, modname, manname, year):
    val = {1: '1', 2: '2', 3: "3"}
    valdim = {1: "mm", 2: "inch", 3: "null"}
    print(modname, manname, year)
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", class_="specs")
    if table is None:
        return
    hed = soup.title.text
    try:
        hed = re.sub('[!@#$/~)(*&^%//\.]', '', hed)
    except:
        print(hed)
    root = Element("vinyaks_car_data", car=hed)
    dat = SubElement(root, "dat", name="modelname")
    cel = SubElement(dat, "val", value="1")
    cel.text = modname
    dat = SubElement(root, "dat", name="manname")
    cel = SubElement(dat, "val", value="1")
    cel.text = manname
    dat = SubElement(root, "dat", name="modelyear")
    cel = SubElement(dat, "val", value="1")
    cel.text = year
    for row in table.findAll('tr'):
        c = row.get('class')
        if c is not None and 'dimhead' in c:
            print('')
        elif c is not None and 'dimrow' in c:
            for head in row.findAll('th'):
                dat = SubElement(root, "dat", name=head.text)  # .encode('utf-8'))
                i = 1
                for cell in row.findAll('td'):
                    cel = SubElement(dat, "val", value=valdim[i])
                    cel.text = cell.text  # .encode('utf-8')
                    i = i + 1

        else:

            for head in row.findAll('th'):
                dat = SubElement(root, "dat", name=head.text)  #  .encode('utf-8'))
                i = 1
                for cell in row.findAll('td'):
                    cel = SubElement(dat, "val", value=val[i])
                    cel.text = cell.text  # .encode('utf-8')
                    i = i + 1
    tree = ElementTree(root)
    # pl = "/home/vinayak/mini project data/".encode('utf-8')
    tree.write(filepath + hed + ".xml", "utf-8")


def fun2(url2):
    print("Entered second level")
    response = requests.get(url2)
    html = response.content
    soup = BeautifulSoup(html, "lxml")
    i = 0
    table = soup.find("ol", class_="longlist rightspace")
    if table is None:
        return
    for li in table.findAll('li', class_="detail"):
        for a in li.findAll('a', class_="addstable"):
            i = i + 1
            t = "http://www.carfolio.com/specifications/models/" + a['href']
            print(str(i) + " " + t)

            if a.find("span", class_="modelyear") is None:
                if a.find("span", class_="Year") is None:
                    year = ""
                else:
                    year = a.find("span", class_="Year").text
            else:
                year = a.find("span", class_="modelyear").text

            if a.find("span", class_="model name") is None:
                modname = ""
            else:
                modname = a.find("span", class_="model name").text
            if a.find("span", class_="manufacturer") is None:
                manname = ""
            else:
                manname = a.find("span", class_="manufacturer").text
            if (i > 0):  # can be used for special conditions
                fun(t, modname, manname, year)
                imagefun(t, modname, manname,
                         year)  # edit here to dowload image and xml file


def fun3(url3):
    print("Entered first level")
    response = requests.get(url3)
    html = response.content
    soup = BeautifulSoup(html, "lxml")
    table = soup.findAll("li", class_="m")
    i = 0

    if table is None:
        return
    for tab in table:
        for ln in tab.findAll("a", class_="man"):
            i = i + 1
            print(
                str(i) + " http://www.carfolio.com/specifications/" + ln[
                    'href'])

            if (i > 0):  # use to start from middle
                fun2("http://www.carfolio.com/specifications/" + ln['href'])


fun3("http://www.carfolio.com/specifications")
# fun2("http://www.carfolio.com/specifications/models/?man=513")
