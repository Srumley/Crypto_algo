import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_fear_and_greed_index():
    url = 'https://alternative.me/crypto/fear-and-greed-index/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.prettify())  # Pour débogage
    index_value = soup.find('div', class_='fng-circle').text.strip()  # Assurez-vous que ce sélecteur est correct
    return index_value

def get_cbbi():
    url = 'https://colintalkscrypto.com/cbbi/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.prettify())  # Pour débogage
    cbbi_value = soup.find('span', id='total_score_number').text.strip()  # Assurez-vous que ce sélecteur est correct
    return cbbi_value

def get_pi_cycle_top_indicator(driver):
    url = 'https://www.bitcoinmagazinepro.com/charts/pi-cycle-top-indicator/'
    driver.get(url)
    element = driver.find_element(By.XPATH, '//*[contains(@class, "jsx-2857591045")]')  # Assurez-vous que ce sélecteur est correct
    print(element.text)  # Pour débogage
    pi_cycle_value = element.text
    return pi_cycle_value

def get_bitcoin_price_prediction():
    url = 'https://coincodex.com/crypto/bitcoin/price-prediction/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.prettify())  # Pour débogage
    prediction_value = soup.find('div', class_='pred-value').text.strip()  # Assurez-vous que ce sélecteur est correct
    return prediction_value

def get_rhodl_ratio(driver):
    url = 'https://www.bitcoinmagazinepro.com/charts/rhodl-ratio/'
    driver.get(url)
    element = driver.find_element(By.XPATH, '//*[contains(@class, "jsx-2857591045")]')  # Assurez-vous que ce sélecteur est correct
    print(element.text)  # Pour débogage
    rhodl_value = element.text
    return rhodl_value

def main():
    # Setup Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Get Fear and Greed Index
        fear_and_greed_index = get_fear_and_greed_index()
        print(f'Fear and Greed Index: {fear_and_greed_index}')

        # Get CBBI
        cbbi = get_cbbi()
        print(f'CBBI: {cbbi}')

        # Get Pi Cycle Top Indicator
        pi_cycle_top_indicator = get_pi_cycle_top_indicator(driver)
        print(f'Pi Cycle Top Indicator: {pi_cycle_top_indicator}')

        # Get Bitcoin Price Prediction
        bitcoin_price_prediction = get_bitcoin_price_prediction()
        print(f'Bitcoin Price Prediction: {bitcoin_price_prediction}')

        # Get RHODL Ratio
        rhodl_ratio = get_rhodl_ratio(driver)
        print(f'RHODL Ratio: {rhodl_ratio}')
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
