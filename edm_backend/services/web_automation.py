import time, logging

from services.helpers import *
from configs.paths import *

from selenium import webdriver


class WebAutomation:
    def __init__(self) -> None:
        self.user_name = None
        self.user_password = None
        self.login_page = None
        self.download_url = None
        self.chrome_options = None
        self.driver = None
        logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


    def set_creds(self, user_name, password, login_page, download_url) -> None:
        # Perform login
        self.user_name = user_name  # Send User Name for the website
        self.user_password = password  # Send Password for the website
        self.login_page = login_page  # Send the login page url for the website
        self.download_url = download_url  # Send the Download link url for the website


    def set_chrome_options(self) -> None:
        # Set up WebDriver in headless mode
        self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument("--headless") # Uncomment to run in headless mode
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-popup-blocking")
        self.chrome_options.add_argument("--incognito")


    def set_experimental_option(self, default_directory=r"C:\Temp") -> None:
        # TODO: "Setting of default directory is not working to be debugged"
        self.chrome_options.add_experimental_option(
            "prefs", {"download.default_directory": default_directory}
        )


    def enable_ssl(self) -> None:
        # Depending on the website browser in the final environment, you might need to enable SSL
        # chrome_options.set_capability("acceptSslCerts", True)
        pass


    def google_bot(self) -> None:
        self.driver = webdriver.Chrome(options=self.chrome_options)
        try:
            wat = {
                "driver": self.driver,
                "lgr": logging
            }
            time.sleep(3)
            self.driver.maximize_window()
            # Navigate to Google
            self.driver.get("https://www.google.com")

            time.sleep(3)
            # Find the search box using its name attribute value
            e_search_box = find_element_path(wat, element=google_input_field)

            time.sleep(3)
            wat['element'] = e_search_box
            # Type 'Selenium' in the search box
            send_keys(wat, text="Selenium")

            time.sleep(3)
            # Wait for the search button to become clickable and click it
            e_search_button = find_element_path(wat, element=google_search_btn)
            wat['element'] = e_search_button
            click_button(wat)

            time.sleep(3)
            # Wait for the results page to load and extract the results
            wait_for_element_to_load(wat, element=search_field)

        except Exception as e:
            print(e)

        finally:
            # Close the WebDriver
            if (self.driver): self.driver.quit()


    def main(self):
        self.driver = webdriver.Chrome(options=self.chrome_options)
        try:
            self.driver.get(self.login_page)
            print(f"Title of page: {self.driver.title}")

            time.sleep(2)
            e_username_field = find_element_path(self.driver, element=username_field)
            e_password_field = find_element_path(self.driver, element=password_field)
            # time.sleep(1)
            e_login_button = find_element_path(self.driver, element=login_button)

            e_username_field.clear()
            e_username_field.send_keys(self.user_name)
            e_password_field.clear()
            e_password_field.send_keys(self.user_password)

            print(f"Title of page: {self.driver.title}")
            time.sleep(1)

            # Scroll into view and click the login button
            self.driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
            e_login_button.click()

            print(f"Post login: {self.driver.page_source}")
            self.driver.get(self.download_url)
            print(f"Tpickup: {self.driver.page_source}")

            time.sleep(9)
            link_txt = "Direct Buyer_HumanaShipment.txt"
            e_password_field = find_element_path(self.driver, element=download_link)

            # Click the download link
            self.driver.execute_script("arguments[0].click();", download_link)
            time.sleep(2)
            download_link.click()
            time.sleep(2)

            try:
                time.sleep(10)  # Wait for 10 seconds
            except KeyboardInterrupt:
                pass

            # TODO: Validate if the file has been successfully downloaded

        except Exception as e:
            raise RuntimeError(e)

        finally:
            # Close the WebDriver
            if (self.driver): self.driver.quit()
