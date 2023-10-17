import time
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from PIL import Image
from io import BytesIO

with open('config_tw.yaml', encoding='utf-8') as file:
    file_data = yaml.safe_load(file)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(file_data['sleep'])

action = ActionChains(driver)

driver.get(file_data['website'])

# Предварительная настройка поиска акции (выбор страны, переключение на вкладку акции)
go_search_page = driver.find_element(By.XPATH, file_data['search_page']).click()
stock_tab = driver.find_element(By.XPATH, file_data['switch_stock_tab']).click()
select_instrument_country = driver.find_element(By.XPATH, file_data['select_country_search']).click()
country_search_field = driver.find_element(By.XPATH, file_data['country_entry'])
country_search_field.send_keys(file_data['country'])
select_country = driver.find_element(By.XPATH, file_data['click_country']).click()

# Поиск самой акции
tool_search_field = driver.find_element(By.XPATH, file_data['search_field'])
entering_instrument_name = tool_search_field.send_keys(file_data['financial_asset'])
time.sleep(1)
select_stock = driver.find_element(By.XPATH, file_data['click_stock']).click()
go_parameters_stock = driver.find_element(By.XPATH, file_data['parameters_stock']).click()

# Переключение на другую вкладку окна
original_tab = driver.current_window_handle

for tab in driver.window_handles:
    if tab != original_tab:
        driver.switch_to.window(tab)

time.sleep(1)
# Делаем скриншот основных параметров, сохраняем его в буфере и загружаем из буфера
save_header_buffer = BytesIO(driver.get_screenshot_as_png())
open_screenshot_header = Image.open(save_header_buffer)

# Определяем координаты и размеры области основных параметров, которые нужно вырезать
top = 125
bottom = 350
left = 0
right = open_screenshot_header.width
cropped_screenshot_header = open_screenshot_header.crop((left, top, right, bottom))
save_cropped_screenshot_header = BytesIO()


# Изменение временного периода на графике и переключение графика на японские свечи
switching_chart_candlesticks = driver.find_element(By.XPATH, file_data['candlestick_chart']).click()
changing_time_period = driver.find_element(By.XPATH, file_data['chart_period']).click()
time.sleep(1)

# Прокрутка до графика
stock_chart = driver.find_element(By.XPATH, file_data['scroll_to_chart'])
driver.execute_script("arguments[0].scrollIntoView();", stock_chart)

# Делаем скриншот графика, сохраняем его в буфере и загружаем из буфера
save_chart_buffer = BytesIO(driver.get_screenshot_as_png())
open_screenshot_chart = Image.open(save_chart_buffer)

# Определяем координаты и размеры области графика, которую нужно вырезать
top = 125
bottom = 525
left = 0
right = open_screenshot_chart.width
cropped_screenshot_chart = open_screenshot_chart.crop((left, top, right, bottom))
save_cropped_screenshot_chart = BytesIO()

# Склеиваем скриншоты
combined_image = Image.new('RGB', (cropped_screenshot_header.width, cropped_screenshot_header.height
                                   + cropped_screenshot_chart.height))
combined_image.paste(cropped_screenshot_header, (0, 0))
combined_image.paste(cropped_screenshot_chart, (0, cropped_screenshot_header.height))

# Сохраняем объединенный скриншот
combined_image.save(file_data['filename'])

driver.quit()
