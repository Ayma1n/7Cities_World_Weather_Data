import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import pandas as pd

def scrape_city(driver, url):
    """Scrape weather data from a single city URL"""
    driver.get(url)
    sleep(random.uniform(2, 5))  # Random delay

    # Skip page if not found
    if "404" in driver.title or "Not Found" in driver.page_source:
        print(f"Page not found: {url}")
        return None

    try:
        location = driver.find_element(By.CLASS_NAME, "bk-focus__info")\
                         .find_element(By.XPATH, "/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[1]/td").text
        temp = driver.find_element(By.ID, "qlook").find_element(By.CLASS_NAME, "h2").text
        status = driver.find_element(By.ID, "qlook").find_element(By.TAG_NAME, "p").text
        humidity = driver.find_element(By.CLASS_NAME, "bk-focus__info")\
                         .find_element(By.XPATH, "/html/body/div[5]/main/article/section[1]/div[2]/table/tbody/tr[6]/td").text
        three_details = driver.find_element(By.XPATH, "//*[@id='qlook']/p[2]").text.split("\n")
        feels_like = three_details[0].replace("Feels Like: ","")
        forecast = three_details[1].replace("Forecast: ", "")
        winds = three_details[2].replace("Wind: ", "")

        return {
            "Location": location,
            "Temperature": temp,
            "Status": status,
            "Feels Like": feels_like,
            "Forecast": forecast,
            "Winds": winds,
            "Humidity": humidity
        }
    except Exception as ex:
        print(f"Error scraping {url}: {ex}")
        return None

def main():
    # City URLs
    cities = [
        "https://www.timeanddate.com/weather/usa/nome",
        "https://www.timeanddate.com/weather/saudi-arabia/makkah",
        "https://www.timeanddate.com/weather/nigeria/lagos",
        "https://www.timeanddate.com/weather/australia/hobart",
        "https://www.timeanddate.com/weather/switzerland/zurich",
        "https://www.timeanddate.com/weather/brazil/brasilia",
        "https://www.timeanddate.com/weather/antarctica/vostok-station"
    ]
    random.shuffle(cities)

    driver = webdriver.Chrome()
    weather_data = []

    for url in cities:
        data = scrape_city(driver, url)
        if data:
            weather_data.append(data)
            print(f"Scraped: {data['Location']}")

    driver.quit()

    # Save CSV
    keys = weather_data[0].keys()
    with open("weather_report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(weather_data)

    # Save Excel
    df = pd.DataFrame(weather_data)
    df.to_excel("weather_report.xlsx", index=False, engine="openpyxl")

    print("Weather data saved to CSV and Excel ✅")

if __name__ == "__main__":
    main()
