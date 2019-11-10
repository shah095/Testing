"""
The following code is to test the booking of a hotel room in Paris, France on SnapTravel.com
Steps to be taken
- Start with https://www.snaptravel.com/search?encrypted_user_id=5xqebwRCiWusH08KS2yJKA&otp=5549929985 and run a search for Paris
- Choose any hotel
- Choose any room for the given hotel
- Pretend to make a booking
    - Use any guest name, any phone number
    - test@snaptravel.com for the email
    - 4111 1111 1111 1111 for the credit card number
    - any CVV and expiry date and any billing address

"""
import logging as log
import sys
import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# setting up system logger
root = log.getLogger()
root.setLevel(log.DEBUG)

handler = log.StreamHandler(sys.stdout)
handler.setLevel(log.DEBUG)
formatter = log.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

driver = webdriver.Chrome()

url = 'https://www.snaptravel.com/search?encrypted_user_id=5xqebwRCiWusH08KS2yJKA&otp=5549929985'
search_box = "//*[@class='omnisearch__input ']"
search_submit = '//*[@class="sixteen wide column search-container__action"]'
suggested_search = '//*[@class="omnisearch__suggestion_title" and text()="Paris, France"]'
clear_search = "//*[@class='omnisearch__close-icon']"

review_path_1 = '//*[contains(text(),"VS")]/../..'
review_path_2 = '//*[contains(text(),"vs")]/../..'
cad_xpath = "//*[@class='currency-list src-common-Currency-___Currency__currency-list___5h0vp']/option[text()='CAD $']"

select_first_room = '//*[text()="Select Room"]'
reserve_path = '//*[text()="Reserve"]'
view_details = '//*[text()="View Details"]'

continue_to_billing = 'btn-continue'
first_name = "//*[@id='first-name']"
last_name = "//*[@id='last-name']"

next_to_billing = "btn-next-to-payment"
email = "//*[@id='email']"
phone_number = "//*[@id='phone-number']"
special_req = "//*[@id='special-request']"

to_payment_btn = "//*[@id='btn-next-to-payment']"

credit_card_radio = 'credit-card-radio'
credit_card_number = '//*[@id="pan"]'
credit_card_number2 = '//*[@id="origin"]'
credit_card_number3 = '//*[@id="pan"]'
credit_card_number4 = '//*[@id="tokenex"]'
credit_card_exp_date = '//*[@id="expiry-year"]'
credit_card_cvv = 'cvv'

billing_name = '//*[@name="nameoncard"]'
billing_address = 'billing-address'
billing_country_CA = '//*[@name="country-name"]/option[@value="CA"]'
billing_state_ON = '//*[@name="state"]/option[@value="ON"]'
billing_city = 'city'
billing_address_suggested = "geosuggest__item"

sumbit_billing = 'submit-payment'


def find_elem(_value: str = None, by: str = 'xpath', tries: int = 10):
    """ tries to find web element on page for a total of 10 tries (500ms delay in between tries)

    :param by: option: "id", "xpath", "link text", "partial link text", "name", "tag name", "class name", "css selector"
    :param _value: value corresponding to the 'by' argument
    :param tries: number of times to try to find element by
    :return: webdriver element
    """

    try:
        element = WebDriverWait(driver, tries).until(lambda x: x.find_element(by=by, value=_value))
        log.debug(f"Element found: '{_value}'.")
        return element
    except:
        raise Exception("Could not Find Element.")


def find_multiple_elems(_value: str = None, by: str = 'xpath', tries: int = 10) -> list:
    """ tries to find multiple web element on page for a total of 10 tries (500ms delay in between tries)

    :param by: option: "id", "xpath", "link text", "partial link text", "name", "tag name", "class name", "css selector"
    :param _value: value corresponding to the 'by' argument
    :param tries: number of times to try to find element by
    :return: multiple webdriver elements
    """
    try:
        elements = WebDriverWait(driver, tries).until(lambda x: x.find_elements(by=by, value=_value))
        log.debug("Elements found")
        return elements
    except:
        raise Exception("Could not Find Element.")


def click_elem(_value: str = None, by: str = 'xpath', tries: int = 10):
    """ finds and clicks web element

    :param by: option: "id", "xpath", "link text", "partial link text", "name", "tag name", "class name", "css selector"
    :param _value: value corresponding to the 'by' argument
    :param tries: number of times to try to find element by
    """
    log.debug(f"clicking '{_value}'.")
    find_elem(by=by, _value=_value, tries=tries).click()


def select_hotels_by_review(hotels_list):
    """ search through reviews and select hotel with most reviews

    :param hotels_list: list of hotels as webdriver elements
    """
    log.info("Selecting a hotel with most reviews.")
    prev_review = 0
    index = 0
    for i in hotels_list:
        hotel_info = i.text.splitlines()
        reviews = int(hotel_info[1].replace(',', '').replace(' Reviews', '')) if 'Reviews' in hotel_info[1] else 0
        if reviews > prev_review:
            index = hotels_list.index(i)
            prev_review = reviews

    hotels_list[index].click()


def fill_form(_value: str = None, by: str = 'xpath', data: str or int = None, tries: int = 10):
    """ fills out form

    :param by: option: "id", "xpath", "link text", "partial link text", "name", "tag name", "class name", "css selector"
    :param _value: value corresponding to the 'by' argument
    :param data: data to input into the text field
    :param tries: number of times to try to find element by
    """
    log.debug(f'Filling "{_value}" by "{by}" with "{data}".')

    _element = find_elem(_value=_value, by=by, tries=tries)
    WebDriverWait(driver, 30).until(EC.visibility_of(_element))
    _element.send_keys(Keys.CONTROL + "a")
    _element.send_keys(Keys.DELETE)
    _element.send_keys(data)
    time.sleep(0.5)


def enter_cc_num(xpath, cc_num):
    """ enter credit card number

    :param xpath: xpath of Card Number field
    :param cc_num: Card number
    """
    try:
        log.debug(f"Filling '{xpath}' info with '{cc_num}'")
        iframe = find_elem("//iframe[@id='iframe']", by='xpath')
        driver.switch_to.frame(iframe)
        fill_form(xpath, by='xpath', data=cc_num)
        driver.switch_to.default_content()
    except:
        raise Exception("Could not enter CC info.")


log.info("Starting test.")
starting_time = time.time()

log.info("Navigating to website and searching for Paris, France.")
driver.get(url)
elem = find_elem(_value=search_box, by='xpath')
click_elem(clear_search, by='xpath')
elem.send_keys("Paris, France")
time.sleep(2)
try:
    log.info("checking is there is a suggested search element pop up.")
    click_elem(suggested_search, tries=3)
except:
    log.debug("No suggested search element.")
click_elem(search_submit, by='xpath')
log.debug("setting currency to CAD")
click_elem(cad_xpath, tries=35)

log.info("Gathering all the hotels shown")
# due to the element not visible in certain window size we're looking for different elements
try:
    hotels = find_multiple_elems(review_path_1, by='xpath', tries=30)
except:
    hotels = find_multiple_elems(review_path_2, by='xpath', tries=30)

select_hotels_by_review(hotels)
click_elem(select_first_room, tries=20)

try:
    reserve = find_multiple_elems(reserve_path, tries=20)
    reserve[0].click()
except:
    try:
        reserve = find_multiple_elems(view_details, tries=20)
        reserve[0].click()
    except:
        raise Exception("could not click element")

log.info("Navigating to Billing and filling out information requested.")
try:
    click_elem(continue_to_billing, by='id', tries=30)
except:
    log.error(f'Could not find "{continue_to_billing}"')

log.info("Entering personal information.")
fill_form(first_name, by='xpath', data="John")
fill_form(last_name, by='xpath', data="Doe")
fill_form(email, by='xpath', data="test@snaptravel.com")
fill_form(phone_number, by='xpath', data="6470001111")

click_elem(to_payment_btn, by='xpath')

log.info("Entering Credit Card information.")
enter_cc_num(credit_card_number, "4111111111111111")
fill_form(credit_card_exp_date, by='xpath', data="0925")
fill_form(credit_card_cvv, by='id', data="125")

log.info("Entering billing information")
fill_form(billing_name, by='xpath', data="John Doe")
fill_form(billing_address, by='id', data="1 Canada's Wonderland Drive")

suggested_address = find_multiple_elems(billing_address_suggested, by="class name")
suggested_address[0].click()

fill_form(billing_city, by='id', data="Vaughan")
click_elem(billing_state_ON)
click_elem(billing_country_CA)

log.debug(f'\n\nFinished in {time.time()-starting_time}s.')
