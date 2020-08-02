import requests
import bs4
import os
import sys

URL = sys.argv[1]
path = '/home/curt/Downloads'
dir_name = URL.split('/')[-1]
full_path = os.path.join(path, dir_name)

def pull_site(current_url):
    raw_site_page = requests.get(current_url)
    raw_site_page.raise_for_status()
    return raw_site_page


def scrape_parent_page(site):
    soup = bs4.BeautifulSoup(site.text, 'html.parser')
    html_list = soup.find_all('a', href=True)
    lines = [line.get('href') for line in html_list if line]
    lines = [line for line in lines if line.endswith('.mp3')]
    return lines


def scrape_mp3_page(site):
    soup = bs4.BeautifulSoup(site.text, 'html.parser')
    html_header_list = soup.select('.floatbox')
    html_list = html_header_list[2].find_all('a', href=True)
    lines = [line.get('href') for line in html_list if line]
    lines = [line for line in lines if line.endswith('.mp3')]
    return lines[0]


def download_track(url):
    r = requests.get(url, allow_redirects=True)
    name = url.split('/')[-1].replace('%20', ' ')
    print(name)
    with open(os.path.join(full_path, name), 'wb') as mp3:
        mp3.write(r.content)


if __name__ == "__main__":
    
    if dir_name in os.listdir(path):
        raise Exception('Already exists!')
    else:
        os.mkdir(full_path)
    
    parent_page = pull_site(URL)
    mp3_page_urls = scrape_parent_page(parent_page)
    for mp3_page_url in mp3_page_urls:
        mp3_page = pull_site(mp3_page_url)
        mp3_url = scrape_mp3_page(mp3_page)
        download_track(mp3_url)
