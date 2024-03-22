from elements import BasePageElement
from locators import TemperaturePageLocators
from locators import ProductsPageLocators
from locators import CartPageLocators
from locators import PaymentPageLocators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EmailElement(BasePageElement):
    locator = PaymentPageLocators.EMAIL_INPUT

class CardNumberElement(BasePageElement):
    locator = PaymentPageLocators.CARDNUMBER_INPUT

class CardExpireDateElement(BasePageElement):
    locator = PaymentPageLocators.CARDEXPIREDATE_INPUT

class CvcElement(BasePageElement):
    locator = PaymentPageLocators.CVC_INPUT

class ZipElement(BasePageElement):
    locator = PaymentPageLocators.ZIP_INPUT

class BasePage(object):
    """
    Base class to initialize the base page that will be called from all pages
    """

    def __init__(self, driver):
        self.driver = driver

class TemperaturePage(BasePage):
    """
    Temperature page action methods come here
    """

    def get_temperature(self):
        return int(self.driver.find_element(*TemperaturePageLocators.TEMPERATURE).text.split(' ')[0])

    def click_buy_moisturizers_button(self):
        element = self.driver.find_element(*TemperaturePageLocators.BUY_MOISTURIZERS_BUTTON)
        element.click()

    def click_buy_sunscreens_button(self):
        element = self.driver.find_element(*TemperaturePageLocators.BUY_SUNSCREENS_BUTTON)
        element.click()

class ProductsPage(BasePage):
    """
    Products page action methods come here
    """

    def put_cheapest_products_in_cart(self,search_for_articles):
        print(self.driver.current_url)

        articles = self.driver.find_elements(*ProductsPageLocators.ARTICLES)
        articles_prices = []

        # get through all articles on page and put each price in list per category
        for i,search_for_article in enumerate(search_for_articles):
            articles_prices.append([])
            for article in articles:
                article_text = article.get_attribute('onclick')
                #print(article_text)
                # article_text to parse: "addToCart('Paul Magnificient SPF-30',121)"
                price = article_text.replace(')','').split(',')[1]
                #print(price)
                if (article_text.lower().find(search_for_article) >0):
                    articles_prices[i].append(price)

        # now we have all prices and can identify the cheapest product per category

        # find each category cheapest prize product and insert that product into cart
        for i,search_for_article in enumerate(search_for_articles):
            #print(articles_prices[i])
            if (len(articles_prices[i]) > 0):
                #print(min(articles_prices[i]))
                for article in articles:
                    article_text = article.get_attribute('onclick')
                    if (article_text.lower().find(search_for_article) >0):
                        price = article_text.replace(')','').split(',')[1]
                        if (min(articles_prices[i]) == price):
                            self.driver.find_element(*ProductsPageLocators.ARTICLE_ADD_BUTTTON(article_text)).click()
                            break
            else:
                # return empty prices, since one product does not exist at all
                return []

        # return both minimal prices
        return [min(articles_prices[0]),min(articles_prices[1])]

    def click_cart_button(self):
        element = self.driver.find_element(*ProductsPageLocators.CART_BUTTON)
        element.click()

class CartPage(BasePage):

    def click_pay_button(self):
        element = self.driver.find_element(*CartPageLocators.PAY_BUTTON)
        element.click()

    def find_on_page(self,string_to_find):
        return string_to_find in self.driver.page_source.lower()

class PaymentPage(BasePage):

    # Declares text input fields
    email_input = EmailElement()
    card_number_input = CardNumberElement()
    card_expire_date_input = CardExpireDateElement()
    card_verification_code_input = CvcElement()
    zip_input = ZipElement()

    def switch_to_frame(self):
        self.driver.switch_to.frame(self.driver.find_element(*PaymentPageLocators.IFRAME))

    def switch_to_default(self):
        self.driver.switch_to.default_content()

    def click_pay_button(self):
        element = self.driver.find_element(*PaymentPageLocators.PAY_BUTTON)
        element.click()

    def verify_payment_value(self,value):
        element = self.driver.find_element(*PaymentPageLocators.PAY_BUTTON_TEXT)
        return value in element.text

class ConfirmationPage(BasePage):

    def is_displayed(self):
        # since it takes some time until payment process is done, wait a little for page is available
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.title_is("Confirmation"))
        return True

    def success_message_is_displayed(self):
        #print(self.driver.current_url)
        success_message = 'PAYMENT SUCCESS'
        return success_message in self.driver.page_source
