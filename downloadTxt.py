from bs4 import BeautifulSoup
import urllib.request

def parseContent(html, myFile):
    soup = BeautifulSoup(html, "lxml")
    elements= soup.find_all('td', attrs={'class':'t_f'})
    for element in elements:     
        myFile.write(element.text)
        myFile.write('\n')

def downloadHtml(url):
    f = urllib.request.urlopen(url)
    mybytes = f.read()
    mystr = mybytes.decode("utf8")
    f.close()
    return mystr

def getAllPageLinks(soup):
    rest_page_urls = []
    next_element = soup.find('a', attrs={'class':'nxt'})
    next_url = next_element['href']
    last_page = str(next_element.previous)
    index_of_last_dash = len(next_url) - 1 - next_url[::-1].index('-')
    # when page number excceeds 10, middle pages are ignored. hence calculate here
    last_page_number = int(last_page[4:]) if last_page.startswith('...') else int(last_page)
    for page_number in range(2,last_page_number+1):
        rest_page_urls.append('%s%s%s'%(next_url[:index_of_last_dash-1],page_number,next_url[index_of_last_dash:]))
    return rest_page_urls

def getTitle(soup):
    title_div = soup.find('div', attrs={'class':'nav'})
    current_page = str(title_div.contents[len(title_div.contents)-1])
    return current_page[current_page.index('»') + 1:].strip()

def createTxtFile(title):
    file = open(title+'.txt', 'w+')
    return file

def fetchMetadata(html):
    metadata = {}
    soup = BeautifulSoup(html, "lxml")
    title = getTitle(soup)
    rest_page_urls = getAllPageLinks(soup)
    new_file = createTxtFile(title)
    metadata['title'] = title
    metadata['rest_page_urls'] = rest_page_urls
    metadata['new_file'] = new_file
    return metadata

def main(url):
    # first time loading, get all metadata
    print('loading content from ' + url)
    html = downloadHtml(url)
    metadata = fetchMetadata(html)
    myFile = metadata['new_file']

    # get first page since we already downloaded it
    parseContent(html, myFile)

    # get rest of the pages
    all_page_urls = metadata['rest_page_urls']
    for url in all_page_urls:
        print('loading content from ' + url)
        html = downloadHtml(url)
        parseContent(html, myFile)

    myFile.close()

if __name__ == '__main__':
    main("http://91baby.mama.cn/thread-1143131-1-1.html?so_param=546W5pyI5pmefGJhYnk5MV8xMTQzMTMxfDF8MTh8MTk=")  