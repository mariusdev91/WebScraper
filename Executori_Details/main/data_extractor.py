import csv
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

driver = webdriver.Chrome("E:/Informatica/Executori_Details/chromedriver.exe")


def _accept_cookies():
    time.sleep(2)
    try:
        accept_button = driver.find_element(By.XPATH,
                                            '//button[@class="v-btn v-btn--contained v-btn--tile theme--dark v-size--large success"]')
        accept_button.click()
    except NoSuchElementException:
        pass


def _access_bailiffs_list():
    driver.maximize_window()
    time.sleep(3)
    bailiffs_table = driver.find_element(By.XPATH, '//span[text()="Tabloul executorilor"]')
    bailiffs_table.click()
    bailiffs_table_all = driver.find_element(By.XPATH, '//div[text()="Tabloul Executorilor 2021"]')
    bailiffs_table_all.click()
    time.sleep(2)


def _get_table_headers():
    headers = driver.find_elements(By.XPATH, '//*[@id="tablou"]/div/div[1]/div[2]/div[1]/table/thead/tr/th')
    table_headers = []
    for el in headers:
        header_value = el.text
        table_headers.append(header_value)
    return table_headers


def _get_no_rows_cols():
    rows = len(driver.find_elements(By.XPATH, '//*[@id="tablou"]/div/div[1]/div[2]/div[1]/table/tbody/tr'))
    cols = len(driver.find_elements(By.XPATH, '//*[@id="tablou"]/div/div[1]/div[2]/div[1]/table/tbody/tr[1]/td'))
    return rows, cols


def _get_table_data():
    rows, cols = _get_no_rows_cols()
    bailiffs = []

    for r in range(1, rows + 1):
        temp_list = []
        for p in range(1, cols + 1):
            value = str(driver.find_element(By.XPATH,
                                            "//*[@id='tablou']/div/div[1]/div[2]/div[1]/table/tbody/tr[" + str(
                                                r) + "]/td[" + str(p) + "]").text)
            # if len(value) > 0 and value is not "-":
            temp_list.append(value)
        bailiffs.append(temp_list)
    return bailiffs


def _get_data():
    next_page_button = driver.find_element(By.XPATH, '//*[@id="tablou"]/div/div[1]/div[2]/div[2]/div[4]/button')
    final_list = []
    while next_page_button.is_enabled():
        next_page_button.click()
        current_page_data = _get_table_data()
        final_list.append(current_page_data)

    # for el in final_list:
    #     for bailiff in el:
    #         print(bailiff)
    return final_list


def write_data_to_csv(path):
    headers = ['EXECUTOR', 'SEDIU', 'ASOCIAT', 'CEJ', 'E-MAIL', 'TELEFON']
    with open(path, 'w', encoding='utf-8', newline='') as f:

        writer = csv.writer(f)
        writer.writerow(headers)
        bailiffs = _get_data()

        for item in bailiffs:
            for bailiff in item:
                writer.writerow(bailiff)


def _main():
    link = "https://www.executori.ro/"
    file_path = 'E:/Informatica/Executori_Details/main/scraped_data.csv'

    driver.get(link)
    _accept_cookies()
    _access_bailiffs_list()
    write_data_to_csv(file_path)
    driver.close()


_main()
