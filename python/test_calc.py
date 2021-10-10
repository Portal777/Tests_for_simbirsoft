from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class Page:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator,time=10):
        return WebDriverWait(self.driver,time).until(EC.element_to_be_clickable(locator),
                                                      message=f"Can't find element by locator {locator}")

    def find_elements(self, locator,time=10):
        return WebDriverWait(self.driver,time).until(EC.element_to_be_clickable(locator),
                                                      message=f"Can't find elements by locator {locator}")

    def go_to_site(self, s_url):
        return self.driver.get(s_url)


# Актуально для Русскоязычного региона
class GoogleMainSearchPage:
    LOCATOR_GOOGLE_SEARCH_FIELD = (By.CSS_SELECTOR, "input[title='Поиск']")
    LOCATOR_GOOGLE_SEARCH_BUTTON = (By.CSS_SELECTOR, "input[value='Поиск в Google']")


class GoogleCalculatorForm:
    LOCATOR_GOOGLE_CALCULATOR_COUNT = (By.XPATH, "//h2[text()='Калькулятор']/following-sibling::div//table//div[text()='=']")
    LOCATOR_GOOGLE_CALCULATOR_RESULT = (By.XPATH,
                                 "//h2[text()='Калькулятор']/following-sibling::div//div[@role='presentation']//span")


class Worker(Page):
    def enter_word(self, word):
        search_field = self.find_element(GoogleMainSearchPage.LOCATOR_GOOGLE_SEARCH_FIELD)
        search_field.click()
        search_field.send_keys(word)

    def click_on_the_search_button(self):
        search_button = self.find_element(GoogleMainSearchPage.LOCATOR_GOOGLE_SEARCH_BUTTON)
        search_button.click()

    def click_count_button(self):
        count_button = self.find_element(GoogleCalculatorForm.LOCATOR_GOOGLE_CALCULATOR_COUNT)
        count_button.click()

    def expression_input(self, data: str):

        str_element = ''

        for index, calc_element in enumerate(data):
            if calc_element == '':
                continue

            elif calc_element == '-':
                calc_element = u"\u2212"

            elif calc_element == '=':
                self.click_count_button()
                continue

            elif calc_element.isalpha():
                str_element += calc_element
                if index != len(data)-1:
                    if data[index+1].isalpha():
                        continue
                calc_element = str_element

            element_in_calculator = self.find_element((By.XPATH,
                               f"//h2[text()='Калькулятор']/following-sibling::div//"
                               f"table//div[text()='{calc_element}']"))
            element_in_calculator.click()

            str_element = ''

    def check_result(self):
        result = self.find_element(GoogleCalculatorForm.LOCATOR_GOOGLE_CALCULATOR_RESULT)
        return result.text


class TestSuite:
    def test_case_1_whole_numbers(self, config_browser):
        page = Worker(config_browser)
        page.go_to_site('http://google.com')
        page.enter_word('Калькулятор')
        page.click_on_the_search_button()
        page.expression_input('(1 + 2) × 3 - 40 ÷ 5')
        page.click_count_button()
        sleep(0.5)
        result = page.check_result()
        assert '1' == result, 'Подсчет неверен'

    def test_case_2_devision_by_zero(self, config_browser):
        page = Worker(config_browser)
        page.go_to_site('http://google.com')
        page.enter_word('Калькулятор')
        page.click_on_the_search_button()
        page.expression_input('6 ÷ 0')
        page.click_count_button()
        sleep(0.5)
        result = page.check_result()
        assert 'Infinity' == result, 'Подсчет неверен'

    def test_case_3_sin(self, config_browser):
        page = Worker(config_browser)
        page.go_to_site('http://google.com')
        page.enter_word('Калькулятор')
        page.click_on_the_search_button()
        page.expression_input('sin()')
        page.click_count_button()
        sleep(0.5)
        result = page.check_result()
        assert 'Error' == result, 'Подсчет неверен'
