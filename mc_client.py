import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class McMenuScraper:
    def __init__(self):
        self.root_url = 'https://www.mcdonalds.com/'

    def scrape_menu(self):
        driver = webdriver.Chrome()
        driver.get(self.root_url + 'ua/uk-ua/eat/fullmenu.html')

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.cmp-category__row .cmp-category__item')))

        items = driver.find_elements(By.XPATH, "//li[@class='cmp-category__item']/a")

        href_values = [item.get_attribute('href') for item in items]
        menu_data = []
        for href in href_values:
            driver.get(href)
            title_element = driver.find_element(By.XPATH, '//meta[@name="title"]')
            name = title_element.get_attribute("content")

            description_element = driver.find_element(By.XPATH,
                                                      '//div[@class="cmp-product-details-main__description"]')
            description = description_element.text
            wait = WebDriverWait(driver, 5)

            button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'cmp-accordion__header')))

            button.click()
            time.sleep(1)
            primary_xpath = '//li[contains(@class, "cmp-nutrition-summary__heading-primary-item")]'
            calories_element = driver.find_element(By.XPATH,
                                                   f'{primary_xpath}[1]/span[@class="value"]')
            calories_value = calories_element.text

            fats_element = driver.find_element(By.XPATH,
                                               f'{primary_xpath}[2]/span[@class="value"]')
            fats_value = fats_element.text

            carbs_element = driver.find_element(By.XPATH,
                                                f'{primary_xpath}[3]/span[@class="value"]')
            carbs_value = carbs_element.text

            proteins_element = driver.find_element(By.XPATH,
                                                   f'{primary_xpath}[4]/span[@class="value"]')
            proteins_value = proteins_element.text

            primary_xpath = '//div[contains(@class, "cmp-nutrition-summary__details-column-view-desktop")]'

            unsaturated_fats_element = driver.find_element(By.XPATH, f'{primary_xpath}//li[1]/span[@class="value"]')
            unsaturated_fats_value = unsaturated_fats_element.text

            sugar_element = driver.find_element(By.XPATH, f'{primary_xpath}//li[2]/span[@class="value"]')
            sugar = sugar_element.text

            salt_element = driver.find_element(By.XPATH, f'{primary_xpath}//li[3]/span[@class="value"]')
            salt = salt_element.text

            portion_element = driver.find_element(By.XPATH, f'{primary_xpath}//li[4]/span[@class="value"]')
            portion = portion_element.text

            product_data = {
                "name": name,
                "description": description,
                "calories": calories_value,
                "fats": fats_value,
                "carbs": carbs_value,
                "proteins": proteins_value,
                "unsaturated_fats": unsaturated_fats_value,
                "sugar": sugar,
                "salt": salt,
                "portion": portion
            }
            menu_data.append(product_data)
        driver.quit()
        self.save_data_to_json(menu_data, "menu_data.json")

    @staticmethod
    def save_data_to_json(data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    scraper = McMenuScraper()
    scraper.scrape_menu()
