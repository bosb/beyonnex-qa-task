import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pages
import time

class TestWeatherShop(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("lang=de-DE")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("start-maximized")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.get("https://weathershopper.pythonanywhere.com")

    def test_e2e(self):
        """
        Tests "Order flow".
        Populates the fields, submits the forms and verifies the success message
        """

        # Load the main page.
        temperature_page = pages.TemperaturePage(self.driver)

        # Checks temperature
        temperature = temperature_page.get_temperature()
        # 19-34?

        # init products + prices for later reference
        products = []
        prices = []

        if (temperature < 19):
            # Shop for moisturizers if the weather is below 19 degrees.
            temperature_page.click_buy_moisturizers_button()

            # Add two moisturizers to your cart.
            # First, select the least expensive mositurizer that contains Aloe.
            # For your second moisturizer, select the least expensive moisturizer that contains almond.
            products_page = pages.ProductsPage(self.driver)
            products = ['aloe','almond']

        elif (temperature > 34):
            # Shop for suncreens if the weather is above 34 degrees.
            temperature_page.click_buy_sunscreens_button()

            # Add two sunscreens to your cart.
            # First, select the least expensive sunscreen that is SPF-50.
            # For your second sunscreen, select the least expensive sunscreen that is SPF-30.
            products_page = pages.ProductsPage(self.driver)
            products = ['spf-50','spf-30']

        prices = products_page.put_cheapest_products_in_cart(products)
        assert len(prices) == 2 # Expect the 2 cheapest prices

        # Click on the cart when you are done.
        products_page.click_cart_button()

        # Verify that the shopping cart looks correct.
        cart_page = pages.CartPage(self.driver)
        # find products, prices and sum on page
        assert cart_page.find_on_page(products[0])
        assert cart_page.find_on_page(products[1])
        assert cart_page.find_on_page(prices[0])
        assert cart_page.find_on_page(prices[1])
        assert cart_page.find_on_page(str(int(prices[0]) + int(prices[1])))

        # let's pay
        cart_page.click_pay_button()

        # Then, fill out your payment details and submit the form. You can Google for 'Stripe test card numbers' to use valid cards.
        # Note: The payment screen will error 5% of the time by design
        payment_page = pages.PaymentPage(self.driver)
        payment_page.switch_to_frame()
        payment_page.email_input = 'example@example.com'
        payment_page.card_number_input = '4242'
        payment_page.card_number_input = '4242'
        payment_page.card_number_input = '4242'
        payment_page.card_number_input = '4242'
        payment_page.card_expire_date_input = '01'
        payment_page.card_expire_date_input = '42'
        payment_page.card_verification_code_input = '142'
        payment_page.zip_input = '12345'
        # some recalculation takes place after every input, wait until it settles
        time.sleep(1)

        # verify payment value for credit card
        assert payment_page.verify_payment_value(str(int(prices[0]) + int(prices[1])))
        payment_page.click_pay_button()
        payment_page.switch_to_default()

        # Verify if the payment was successful. The app is setup so there is a 5% chance that your payment failed.
        confirmation_page = pages.ConfirmationPage(self.driver)
        #self.driver.save_screenshot("screenshot.png")
        assert confirmation_page.is_displayed()
        assert confirmation_page.success_message_is_displayed()

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
