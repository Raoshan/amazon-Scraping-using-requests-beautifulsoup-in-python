import csv
import requests
from bs4 import BeautifulSoup
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
def get_url(search_term):
    """Generate a url from search term"""
    template = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss_2' 
    # add term query to url
    url = template.format(search_term)
    return url  

def extract_record(item):
    '''Extract and return data from a singal record'''
    atag = item.h2.a
    Description = atag.text.strip()
    print(Description)
    Url = 'https://www.amazon.in'+atag.get('href')
    print(Url)
    try:
        Price = item.find('span', 'a-price').find('span', 'a-offscreen').text
        print(Price)
    except AttributeError:
        return
    try:
        # rank and rating
        Rating = item.i.text
        print(Rating)
        ReviewCount = item.find('span', {'class':'a-size-base'}).text
        print(ReviewCount)
    except AttributeError:
        return
    result = (Description, Price, Rating, ReviewCount, Url) 
    return result  

def main(search_term):
    records = []
    url = get_url(search_term) 
    while True:
        response = requests.get(url, headers=headers)
        # print(response)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', {'data-component-type':'s-search-result'})
        print(len(results))
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
        try:
            pages = soup.select_one('li.a-last a')
            url ="https://www.amazon.in" + pages["href"]
            print("nextLink:-",url)     
        except:
            break    

    with open('amazon.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow({'Description', 'Price', 'Rating', 'ReviewCount', 'Url'})
        writer.writerows(records)

main('laptop')

