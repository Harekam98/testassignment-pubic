from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Method to read and load the JSON data from a file
def load_json_data () -> dict:
    with open('UserData.json') as json_file:
        user_data = json.load(json_file)
    return user_data["users"]

# Define the data from JSON
data_to_insert = load_json_data()

# Convert data to JSON format
json_data = json.dumps(data_to_insert)

# Path to the WebDriver executable (chromedriver in this example)
webdriver_path = './chromedriver.exe'  # Replace with your chromedriver path

# Set the path for the WebDriver service
service = Service(executable_path=webdriver_path)

# Start the WebDriver
driver = webdriver.Chrome(service=service)

# Navigate to the URL
driver.get("https://testpages.herokuapp.com/styled/tag/dynamic-table.html")

try:
    # Click on Table Data button
    table_data_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//summary[text()='Table Data']")))
    table_data_button.click()

    # Find the input text box and insert data
    input_text_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "jsondata")))
    input_text_box.clear()
    input_text_box.send_keys(json_data)

    # Find and click the Refresh Table button
    refresh_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "refreshtable")))
    refresh_button.click()

    # Wait for the table to refresh
    time.sleep(2)  # Adjust the time as needed for the table to load

    # Get the dynamic ID of the table
    table_id_input_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tableid")))
    table_id = table_id_input_box.get_attribute("value")

    # Get the table data
    table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, table_id)))
    table_rows = table.find_elements(By.TAG_NAME, "tr")

    # Extracting data from the UI table
    table_data = []
    for row in table_rows[1:]:  # Skipping the header row
        columns = row.find_elements(By.TAG_NAME, "td")
        row_data = {
            "name": columns[0].text,
            "age": int(columns[1].text),
            "gender": columns[2].text if len(columns) > 2 else ""  # Assuming the gender column might be absent
        }
        table_data.append(row_data)

    # Assertions to check if stored data matches UI table data
    assert table_data == data_to_insert, "Data does not match between stored data and UI table"

    print("Data insertion and assertion successful!")

except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the browser window
    driver.quit()
