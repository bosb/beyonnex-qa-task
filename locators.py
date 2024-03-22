from selenium.webdriver.common.by import By

class TemperaturePageLocators(object):
    """
    A class for all Temperature page locators.
    """
    TEMPERATURE = (By.XPATH, "//span[@id='temperature']")
    BUY_MOISTURIZERS_BUTTON = (By.XPATH, "//button[text()='Buy moisturizers']/..")
    BUY_SUNSCREENS_BUTTON = (By.XPATH, "//button[text()='Buy sunscreens']/..")

class ProductsPageLocators(object):
    ARTICLES = (By.XPATH, "//button[contains(@class,'btn')]")
    CART_BUTTON = (By.XPATH, "//button //span[@id='cart']")
    def ARTICLE_ADD_BUTTTON(article_text):
        return (By.XPATH, "//button[@onclick=\"" + article_text + "\"]")

class CartPageLocators(object):
    PAY_BUTTON = (By.XPATH, "//button[@type='submit']")

class PaymentPageLocators(object):
    PAY_BUTTON = (By.XPATH, "//button[@id='submitButton']")
    PAY_BUTTON_TEXT = (By.XPATH, "//button[@id='submitButton'] //span")
    IFRAME =  (By.XPATH, "//iframe")
    EMAIL_INPUT = (By.XPATH, "//input[@id='email']")
    CARDNUMBER_INPUT = (By.XPATH, "//input[@id='card_number']")
    CARDEXPIREDATE_INPUT = (By.XPATH, "//input[@id='cc-exp']")
    CVC_INPUT = (By.XPATH, "//input[@id='cc-csc']")
    ZIP_INPUT = (By.XPATH, "//input[@id='billing-zip']")
