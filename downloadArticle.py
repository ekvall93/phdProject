import selenium
import requests
import time
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options() 
chrome_options.add_argument("--headless")

year2url = {"2019":"https://papers.nips.cc/book/advances-in-neural-information-processing-systems-32-2019",
 "2018": "https://papers.nips.cc/book/advances-in-neural-information-processing-systems-31-2018",
 "2017": "https://papers.nips.cc/book/advances-in-neural-information-processing-systems-30-2017",
 "2016": "https://papers.nips.cc/book/advances-in-neural-information-processing-systems-29-2016",
 "2015": "https://papers.nips.cc/book/advances-in-neural-information-processing-systems-28-2015"
}

def downloadPaperData(did, url):

    driver2.get(url)
    title = driver2.find_element_by_class_name("subtitle").text
    abstract = driver2.find_element_by_class_name("abstract").text
    authors = getAuthors()
    downloadPdf(did)

    return {"title":title, "abstract":abstract, "authors":authors}

def getAuthors():
    ulElements = driver2.find_elements_by_tag_name("ul")
    ul = ulElements[1]
    liElemetns = ul.find_elements_by_tag_name("li")

    authors = list()
    for li in liElemetns:
        authors.append(li.find_element_by_tag_name("a").text)
    return authors

def downloadPdf(did):
    url = None
    aTags = driver2.find_elements_by_tag_name("a")
    for a in aTags:
        if a.text == "[PDF]":
            url = a.get_attribute('href')

    if url:
        response = requests.get(url)
        with open('/hdd/dataPhdProject/{}.pdf'.format(did), 'wb') as f:
            f.write(response.content)

def downloadAllPaper(mainUrl, year):
    did2data = {}
    
    
    driver.get(mainUrl)
    ulElements = driver.find_elements_by_tag_name("ul")
    ul = ulElements[1]
    liElemetns = ul.find_elements_by_tag_name("li")

    for i, li in enumerate(liElemetns):
        did = str(year) + "_"+ str(i)


        aElements = li.find_element_by_tag_name("a")

        paperUrl = aElements.get_attribute('href')
        did2data[did] = downloadPaperData(did, paperUrl)
        time.sleep(0.2)

    return did2data


dataList = list()
for y, url in year2url.items():
    driver = webdriver.Chrome(options=chrome_options)
    driver2 = webdriver.Chrome(options=chrome_options)

    data = downloadAllPaper(url, y)
    dataList.append(data)


result = {}
for d in dataList:
    result.update(d)

print(result)
pickle.dump(result, open('/hdd/dataPhdProject/dataDict', "wb"))
