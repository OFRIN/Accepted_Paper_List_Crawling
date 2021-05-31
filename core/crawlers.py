def get_soup(url, option='requests', delay=1):
    if option == 'requests':
        req = requests.get(url)
        page_source = req.text
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')

        driver = webdriver.Chrome("./data/chromedriver", chrome_options=options)
        driver.get(url)

        time.sleep(delay)

        page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
    return soup