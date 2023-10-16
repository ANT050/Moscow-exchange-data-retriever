import time
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

with open('config.yaml', encoding='utf-8') as file:
    file_data = yaml.safe_load(file)
    sleep = file_data['sleep']
    website = file_data['website']

service = Service(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(sleep)

driver.get(website)

time.sleep(1)
acceptance_of_agreement = driver.find_element(By.XPATH, file_data['agreement']).click()
checkbox_ordinary_shares = driver.find_element(By.XPATH, file_data['ordinary_shares']).click()
checkbox_preferred_shares = driver.find_element(By.XPATH, file_data['preferred_shares']).click()

search_field = driver.find_element(By.XPATH, file_data['search_field'])
stock_search = search_field.send_keys(file_data['financial_asset'])
time.sleep(1)
go_to_stock_parameters = driver.find_element(By.XPATH, file_data['financial_asset_page']).click()

original_tab = driver.current_window_handle

for tab in driver.window_handles:
    if tab != original_tab:
        driver.switch_to.window(tab)

chart_time_period = driver.find_element(By.XPATH, file_data['change_time_period']).click()

asset_price_range = driver.find_element(By.CSS_SELECTOR, file_data['price_range'])
action_chains = ActionChains(driver)
action_chains.click_and_hold(asset_price_range).move_by_offset(-500, 0).release().perform()
time.sleep(3)

driver.save_screenshot('screenshot.png')

driver.quit()
