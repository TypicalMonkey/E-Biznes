import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestWikipedia(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_page_tools_menu(self):
        home_page_url = "https://en.wikipedia.org/wiki/Main_Page"
        self.driver.get(home_page_url)
        self.assertIn("Wikipedia", self.driver.title)
        page_tools_button = self.driver.find_element(By.ID, "vector-page-tools-dropdown-checkbox")
        self.assertIsNotNone(page_tools_button)
        self.assertFalse(page_tools_button.get_attribute("aria-expanded") == "true")
        page_tools_button.click()

    def test_page_tools_menu_main_site(self):
        home_page_url = "https://en.wikipedia.org/wiki/Main_Page"
        self.driver.get(home_page_url)
        self.assertIn("Wikipedia", self.driver.title)
        page_tools_button = self.driver.find_element(By.ID, "vector-page-tools-dropdown-checkbox")
        self.assertIsNotNone(page_tools_button)
        page_tools_button.click()
        what_links_here_option = self.driver.find_element(By.ID, "t-whatlinkshere")
        self.assertTrue(what_links_here_option.is_displayed())
        what_links_here_option.find_element(By.TAG_NAME, "a").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/Special:WhatLinksHere/Main_Page"))
        self.assertIn("/Special:WhatLinksHere/Main_Page", self.driver.current_url)

    def test_page_tools_menu_recent_change(self):
        home_page_url = "https://en.wikipedia.org/wiki/Main_Page"
        self.driver.get(home_page_url)
        self.assertIn("Wikipedia", self.driver.title)
        page_tools_button = self.driver.find_element(By.ID, "vector-page-tools-dropdown-checkbox")
        self.assertIsNotNone(page_tools_button)
        page_tools_button.click()

        what_links_here_option = self.driver.find_element(By.ID, "t-recentchangeslinked")
        self.assertTrue(what_links_here_option.is_displayed())
        what_links_here_option.find_element(By.TAG_NAME, "a").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/Special:RecentChangesLinked/Main_Page"))
        self.assertIn("/Special:RecentChangesLinked/Main_Page", self.driver.current_url)
    
    def test_page_tools_menu_get_shortened_url(self):
        home_page_url = "https://en.wikipedia.org/wiki/Main_Page"
        self.driver.get(home_page_url)
        self.assertIn("Wikipedia", self.driver.title)

        page_tools_button = self.driver.find_element(By.ID, "vector-page-tools-dropdown-checkbox")
        self.assertIsNotNone(page_tools_button)
        page_tools_button.click()

        get_shortened_url_option = self.driver.find_element(By.ID, "t-urlshortener")
        self.assertTrue(get_shortened_url_option.is_displayed())
        get_shortened_url_option.find_element(By.TAG_NAME, "a").click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "ooui-2")))
        shortened_url_input = self.driver.find_element(By.ID, "ooui-2")
        shortened_url_value = shortened_url_input.get_attribute("value")

        self.assertNotEqual(shortened_url_value, "")

    def test_page_tools_menu_copy_shortened_url(self):
        home_page_url = "https://en.wikipedia.org/wiki/Main_Page"
        self.driver.get(home_page_url)
        self.assertIn("Wikipedia", self.driver.title)

        page_tools_button = self.driver.find_element(By.ID, "vector-page-tools-dropdown-checkbox")
        self.assertIsNotNone(page_tools_button)
        page_tools_button.click()

        get_shortened_url_option = self.driver.find_element(By.ID, "t-urlshortener")
        self.assertTrue(get_shortened_url_option.is_displayed())
        get_shortened_url_option.find_element(By.TAG_NAME, "a").click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "ooui-2")))
        shortened_url_input = self.driver.find_element(By.ID, "ooui-2")
        shortened_url_value = shortened_url_input.get_attribute("value")
        shortened_url_input.send_keys(Keys.CONTROL, "a")
        shortened_url_input.send_keys(Keys.CONTROL, "c")

        self.driver.execute_script("window.open()")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(shortened_url_value)     

    def test_main_menu_options(self):
        home_page_url = "https://en.wikipedia.org/wiki/Main_Page"
        self.driver.get(home_page_url)
        self.assertIn("Wikipedia", self.driver.title)
        main_menu_button = self.driver.find_element(By.ID, "vector-main-menu-dropdown-checkbox")
        self.assertIsNotNone(main_menu_button)
        main_menu_button.click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "vector-menu-content")))
        menu_options = self.driver.find_elements(By.CLASS_NAME, "vector-menu-content-list")
        for option in menu_options:
            if option.is_displayed():
                option_text = option.text
                ActionChains(self.driver).move_to_element(option).perform()
                if option_text == "Main Page" or option_text == "Contents" or option_text == "Current events" or option_text == "Random article" or option_text == "About Wikipedia" or option_text == "Contact us":
                    option.click()
                    WebDriverWait(self.driver, 10).until(EC.url_contains("/wiki/"))
                    self.assertIn(option_text.lower().replace(" ", "_"), self.driver.current_url.lower())

    def test_create_account_link_on_home_page(self):
        home_page_url = "https://en.wikipedia.org/wiki/Main_Page"
        self.driver.get(home_page_url)
        self.assertIn("Wikipedia", self.driver.title)
        create_account_li = self.driver.find_element(By.CSS_SELECTOR, "li#pt-createaccount-2")
        self.assertIsNotNone(create_account_li)
        create_account_link = create_account_li.find_element(By.CSS_SELECTOR, "a[href*='Special:CreateAccount']")
        self.assertIsNotNone(create_account_link)
        create_account_link.click()
        self.assertIn("https://en.wikipedia.org/w/index.php?title=Special:CreateAccount&returnto=Main+Page", self.driver.current_url)


    def test_wikipedia_pages(self):
        pages_to_test = [
            "https://en.wikipedia.org/wiki/Main_Page",
            "https://en.wikipedia.org/wiki/Python_(programming_language)",
            "https://en.wikipedia.org/wiki/Artificial_intelligence",
            "https://en.wikipedia.org/wiki/SpaceX",
            "https://en.wikipedia.org/wiki/Leonardo_da_Vinci",
        ]

        for page in pages_to_test:
            self.driver.get(page)
            self.assertTrue("Wikipedia" in self.driver.title)
    
    def test_search_on_wikipedia(self):
        home_page_url = "https://en.wikipedia.org/wiki/Main_Page"
        self.driver.get(home_page_url)
        self.assertIn("Wikipedia", self.driver.title)
        search_input = self.driver.find_element(By.NAME, "search")
        self.assertTrue(search_input.is_displayed())
        search_input.send_keys("kurt von hammerstein")
        search_input.submit()

    def test_search_on_wikipedia(self):
        home_page_url = "https://en.wikipedia.org/wiki/Main_Page"
        self.driver.get(home_page_url)

        self.assertIn("Wikipedia", self.driver.title)
        search_input = self.driver.find_element(By.NAME, "search")
        search_input.send_keys("xabucfbaj")
        search_input.submit()
        
        no_results_message = self.driver.find_element(By.CLASS_NAME, "mw-search-nonefound")
        self.assertTrue(no_results_message.is_displayed())


    def test_operation_keelhaul_page(self):
        page_url = "https://en.wikipedia.org/wiki/Operation_Keelhaul"
        self.driver.get(page_url)
        self.assertIn("Operation Keelhaul", self.driver.title)
        time.sleep(3)
        lang_checkbox = self.driver.find_element(By.ID, "p-lang-btn-checkbox")
        lang_checkbox.click()

    def test_search_on_mars_to_sun(self):
        home_page_url = "https://en.wikipedia.org/wiki/Main_Page"
        self.driver.get(home_page_url)

        self.assertIn("Wikipedia", self.driver.title)
        search_input = self.driver.find_element(By.NAME, "search")
        search_input.send_keys("mars")
        search_input.submit()
        links = self.driver.find_elements(By.TAG_NAME, "a")
        sun_found = False
        for link in links:
            if link.get_attribute("href") == "https://en.wikipedia.org/wiki/Sun":
                sun_found = True
                break
        self.assertTrue(sun_found, "Link to Sun not found on Mars page")

    def test_mars_to_sun_to_star_link(self):
        home_page_url = "https://en.wikipedia.org/wiki/Main_Page"
        self.driver.get(home_page_url)

        self.assertIn("Wikipedia", self.driver.title)
        search_input = self.driver.find_element(By.NAME, "search")
        search_input.send_keys("mars")
        search_input.submit()

        sun_link = self.driver.find_element(By.XPATH, "//a[@title='Sun']")
        sun_link.click()

        star_link = self.driver.find_element(By.XPATH, "//a[@title='Star']")
        self.assertTrue(star_link.is_displayed())

    def test_wikipedia_logo_size_and_source(self):
        home_page_url = "https://en.wikipedia.org/wiki/Main_Page"
        self.driver.get(home_page_url)

        wikipedia_logo = self.driver.find_element(By.CLASS_NAME, "mw-logo-icon")
        logo_height = wikipedia_logo.get_attribute("height")
        logo_width = wikipedia_logo.get_attribute("width")
        logo_source = wikipedia_logo.get_attribute("src")

        self.assertEqual(logo_height, "50", "Not equal 50px")
        self.assertEqual(logo_width, "50", "Not equal 50px")

        expected_logo_source = "/static/images/icons/wikipedia.png"
        self.assertIn(expected_logo_source, logo_source, "Wrong source of logo")

    def test_cookie_statement_language_change(self):
        cookie_statement_url = "https://foundation.wikimedia.org/wiki/Special:MyLanguage/Policy:Cookie_statement"
        self.driver.get(cookie_statement_url)
        time.sleep(2)
        language_link = self.driver.find_element(By.XPATH, "//a[@href='/wiki/Policy:Cookie_statement/pl']")
        language_link.click()
        expected_polish_url = "https://foundation.wikimedia.org/wiki/Policy:Cookie_statement/pl"
        current_url = self.driver.current_url
        self.assertEqual(current_url, expected_polish_url, "Nieprawidłowe przekierowanie na stronę w języku polskim")
        time.sleep(2)
        
    def test_which_hard(self):
        home_page_url = "https://en.wikipedia.org/wiki/Main_Page"
        self.driver.get(home_page_url)
        self.assertIn("Wikipedia", self.driver.title)
        
        search_input = self.driver.find_element(By.NAME, "search")
        search_input.send_keys("hard")
        search_input.submit()

        hard_link = self.driver.find_element(By.CSS_SELECTOR, "a[href='https://en.wiktionary.org/wiki/hard']")
        hard_link.click()           

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)
