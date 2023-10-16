import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select



def select_random_date_of_birth(driver):
    selDate = Select(driver.find_element(By.ID, "day"))
    selMonth = Select(driver.find_element(By.ID, "month"))
    selYear = Select(driver.find_element(By.ID, "year"))

    # Select a random day, month, and year
    random_day = random.randint(1, 28)  # You can adjust the range as needed
    random_month = random.randint(1, 12)  # You can adjust the range as needed
    random_year = random.randint(1980, 2000)  # You can adjust the range as needed

    # Convert integers to strings
    day_str = str(random_day)
    month_str = str(random_month)
    year_str = str(random_year)

    # Select the random values
    selDate.select_by_visible_text(day_str)
    selMonth.select_by_value(month_str)
    selYear.select_by_visible_text(year_str)
  

def generate_random_name():
    first_names = ["John", "Jane", "Michael", "Emily", "Robert", "Sarah", "William", "Ava", "James", "Olivia"]
    last_names = ["Smith", "Johnson", "Brown", "Davis", "Wilson", "Lee", "Anderson", "White", "Harris", "Martin"]

    random_first_name = random.choice(first_names)
    random_last_name = random.choice(last_names)

    return random_first_name, random_last_name
