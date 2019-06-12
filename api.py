from flask import Flask, Response, request
from flask_cors import CORS
import json


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
import os

CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver')
GOOGLE_CHROME_BIN = os.environ.get('GOOGLE_CHROME_BIN', '/usr/bin/google-chrome')


options = Options()
options.binary_location = GOOGLE_CHROME_BIN
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.headless = True

print('Building chrome driver...')
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)

print('Starting app...')
app = Flask(__name__)
CORS(app)


# url = 'https://www.amazon.es/dp/B006CZ0LGA'
# driver.get(url)


def scrape_amazon_price(url):
    driver.get(url)

    try:
        element = driver.find_element_by_id('priceblock_ourprice').text
    except NoSuchElementException:
        element = None
    return element


@app.route("/")
def index():
    return 'Scraper alive!'


@app.route("/api/scrape", methods=['POST'])
def scrape():
    url = request.json.get('url')
    print(url)
    element = scrape_amazon_price(url)

    status = 200 if element is not None else 412
    response = json.dumps({'Price': element})

    return Response(response=response, status=status, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
