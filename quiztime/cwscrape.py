"""
Script to extract accommodation letters and extra time multipliers from Clockwork

to set up run in the terminal:

```
python -m venv venv
source venv/bin/activate
pip install playwright
playwright install chromium

mkdir letters
```

run first with -a flag to authenticate
then without it to scrape the letters

```
ptyhon cwscrape.py -a
ptyhon cwscrape.py
```

"""


from playwright.sync_api import sync_playwright, Playwright
import time
import argparse
import re
from dataclasses import dataclass

@dataclass
class Config:
    username: str = '123456789' # GBC id (numbers only)
    my_pwd: str = 'GBCpassword'
# config = Config()

# or create a secret_cfg.py file with the class above:
from secret_cfg import config

re_dur = re.compile(r'>[^<>]+ Duration')


login_url = 'https://cw.georgebrown.ca/Clockwork/user/instructor/login.aspx'

def run_auth(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://cw.georgebrown.ca/Clockwork/user/instructor/login.aspx")
    print(page.title())
    page.fill('input[id="placeholder_main_placeholder_content_cwLogin1_Login1_UserName"]', config.username)
    page.fill('input[id="placeholder_main_placeholder_content_cwLogin1_Login1_Password"]', config.my_pwd)
    page.click('input[id="placeholder_main_placeholder_content_cwLogin1_Login1_LoginButton"]')
    # Store the authed state as a context
    time.sleep(3)
    page.context.storage_state(path="auth.json")
    # time.sleep(10)
    browser.close()

all_links = []

def run(playwright: Playwright):
    
    browser = playwright.chromium.launch(headless=False)
    # Load authed context frm the file
    context = browser.new_context(storage_state="auth.json")
    page = context.new_page()

    # for page_num in range(0, 2):
    page.goto("https://cw.georgebrown.ca/Clockwork/user/instructor/letters.aspx")
    time.sleep(1)

    # select max letters per page
    page.locator("div.rgAdvPart button").click()
    page.locator("ul.rcbList li:last-child").click()
    time.sleep(1)

    # get all links containing text "View letter"
    links = page.locator("a:has-text('View letter')").all()
    # print(links)

    link_ids = [lnk.get_attribute('id') for lnk in links]

    # Call js function to click on each link
    # The function in a.href looks like this:
    # javascript:__doPostBack('ctl00$ctl00$placeholder_main$placeholder_content$gv_courses$ctl00$ctl28$btn_letter','')
    for i, link_id in enumerate(link_ids):
        if i >= 20:
            page.locator("div.rgAdvPart button").click()
            page.locator("ul.rcbList li:last-child").click()
            time.sleep(1)
        print(f"Clicking on link {i} - {link_id}")
        page.evaluate(f"document.getElementById('{link_id}').click()")
        time.sleep(1)
        page.locator("#placeholder_main_placeholder_content_btn_viewLetterHtml").click()
        main = page.locator("div.mainarea_nomenu")
        letter = main.locator("#placeholder_main_placeholder_content_p_letter").inner_html()
        m = re_dur.search(letter)
        dur = ''
        if m:
            dur = m.group(0)

        ttl = main.locator("#placeholder_main_placeholder_content_lbl_title").inner_text()
        sttl = main.locator("#placeholder_main_placeholder_content_lbl_subTitle").inner_text()

        print(ttl, sttl, dur)
        with open('summary.tsv', 'at') as summary:
            nttl = ttl.replace(' . ', '\t')
            summary.write(f"{nttl}\t{sttl}\t{dur}\n")
        # print('\n'.join(letter))

        ## Save the letter to a file, only needed when debugging
        # with open(f'letters/letter_{i:02}.html', 'wt') as f:
        #     f.write(enp(ttl))
        #     f.write(enp(sttl))
        #     f.write(letter)

        page.goto("https://cw.georgebrown.ca/Clockwork/user/instructor/letters.aspx")
        time.sleep(1)

        # page.click('button[title="Next Page"]') 
        # time.sleep(1)
    
    time.sleep(3)
    browser.close()

def enp(s):
    return f'<p>{s}</p>\n'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some flags.')
    parser.add_argument('-a', '--auth', action='store_true', help='Run authentication')

    args = parser.parse_args()

    with sync_playwright() as p:
        # there is -a flag, use run_aut()
        if args.auth:
            print('Authenticating...')
            run_auth(p)
        else:
            run(p)
