from flask import Flask 
from time import sleep
from playwright.sync_api import sync_playwright 
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_page(author_id):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' }
        page.set_extra_http_headers(headers)
        url = f'https://scholar.google.com/citations?user={author_id}'
        page.goto(url)
        while True:
            try:
                load_more_button = page.locator('#gsc_bpf_more')
                if load_more_button.is_enabled(): load_more_button.click()
                else: break
            except: break
        content = page.content()
        browser.close()
        return content


@app.route('/get/<author_id>')
def get_author_pubs(author_id):
    try:
        html_content = fetch_page(author_id=author_id)
        soup = BeautifulSoup(html_content, 'html.parser')
        author = soup.find(id='gsc_prf_in')
        if not author: return 'No Author Found'

        author_pubs = dict()
        author_pubs['name'] = author.get_text()

        author_deatils = soup.find(id='gsc_rsb_st').find('tbody').find_all('tr')
        author_pubs['cits'] = author_deatils[0].find(class_='gsc_rsb_std').get_text()
        author_pubs['h'] = author_deatils[1].find(class_='gsc_rsb_std').get_text()

        co_auths = []
        co_auths_list = soup.find(class_='gsc_rsb_a')
        for co_auth in co_auths_list.find_all('li'):
            co_auths.append(co_auth.find('a').get_text())
        author_pubs['co_authors'] = co_auths

        publications = []
        journals = []
        pub_table = soup.find(id='gsc_a_t')
        if pub_table: 
            pub_tbody = pub_table.find('tbody')
            if pub_tbody: 
                for trow in pub_tbody.find_all('tr'):
                    pub_details = dict()
                    tdata = trow.find_all('td')
                    pub_details['title'] = tdata[0].find('a').get_text()
                    more_info = tdata[0].find_all('div')
                    pub_details['co_auhtors'] = more_info[0].get_text()
                    pub_details['desc'] = more_info[1].get_text()
                    journals.append("".join(filter(lambda x: x.isalpha() or x.isspace(), pub_details['desc'].split(',')[0])).strip())
                    pub_details['cits'] = tdata[1].get_text()
                    pub_details['year'] = tdata[2].get_text()
                    publications.append(pub_details)
                author_pubs["pubs"] = publications
        journal_cnt = dict()
        for journal in journals:
            if journal in journal_cnt: journal_cnt[journal] += 1
            else: journal_cnt[journal] = 1
        return [author_pubs,f"No. of Journals and Conferences : {len(journals)}",  journals,f"No. of Unique Journals and Conferences: {len(journal_cnt)}", journal_cnt]
    except: return 'Failed to Load'
