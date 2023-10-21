import requests
from bs4 import BeautifulSoup


def fetch_currency_data(url):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    html_page = response.text
    return html_page


def process_currency_data(src):
    soap = BeautifulSoup(src, 'lxml')
    all_currencies = soap.find_all(class_='datatable_row__Hk3IV dynamic-table_row__fdxP8')

    currency_data = []
    for item in all_currencies:
        received_currency_link = item.find(class_='inv-link bold datatable_cell--name__link__2xqgx')
        full_currency_link = 'https://www.investing.com' + received_currency_link.get('href')

        item_data = ' '.join(item.stripped_strings)
        data_parts = item_data.split()

        currency_info = {
            'Валюта': data_parts[0],
            'Цена': data_parts[1],
            'Изменение': data_parts[5],
            'Изменение, %': data_parts[6],
            'Время': data_parts[7],
            'Ссылка': full_currency_link
        }

        currency_data.append(currency_info)

    return currency_data


def search_for_required_currency(currency_data, search_currency):
    found_currencies = [currency for currency in currency_data if currency['Валюта'] == search_currency]
    return found_currencies


def print_currency_info(currency_info):
    for key, value in currency_info.items():
        print(f"{key}: {value}")
    print()


def main():
    url = 'https://ru.investing.com/currencies/streaming-forex-rates-majors'
    currency_data = process_currency_data(fetch_currency_data(url))
    search_currency = 'USD/RUB'
    found_currencies = search_for_required_currency(currency_data, search_currency)

    for currency_info in found_currencies:
        print_currency_info(currency_info)


if __name__ == "__main__":
    main()
