import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
# from webdriver_manager.chrome import ChromeDriverManager

def search_krs(krs_number):
    # Set up the WebDriver
    gecko_driver = r'C:\Users\Sebastian\Desktop\geckodriver.exe'
    service = FirefoxService(executable_path=gecko_driver)
    driver = webdriver.Firefox(service=service)

    try:
        # Navigate to the website
        driver.get("https://ekrs.ms.gov.pl/rdf/pd/search_df#")

        # Allow the page to load
        time.sleep(5)

        # Find the search input field and enter the KRS number
        search_input = driver.find_element(By.ID, "unloggedForm:krs0")
        search_input.send_keys(krs_number)
        search_input.send_keys(Keys.RETURN)

        # Allow time for the search results to load
        time.sleep(5)

        # Find the table rows
        rows = driver.find_elements(By.CSS_SELECTOR, "#searchForm\\:docTable_data tr")

        for row in rows:
            # Get the "Rodzaj dokumentu" cell
            document_type = row.find_elements(By.TAG_NAME, "td")[1].text
            if document_type == "Roczne sprawozdanie finansowe" or document_type == "Skonsolidowane roczne sprawozdanie finansowe":
                # Click the "Pokaż szczegóły" link in the "Akcje" column
                details_link = row.find_elements(By.TAG_NAME, "td")[6]
                details_link.click()
                break

        # Allow time for the details to load
        time.sleep(5)

        # Click the "Pobierz dokumenty" link
        download_link = driver.find_element(By.ID, "searchForm:j_idt333")
        download_link.click()

        # Allow time for the documents to load
        time.sleep(5)

        # Click the "Pobierz" link to download the XML
        file_row = driver.find_element(By.CSS_SELECTOR, "tr.ui-widget-content.ui-panelgrid-even")
        file_name = file_row.find_elements(By.TAG_NAME, "td")[0].text
        download_link = file_row.find_element(By.CSS_SELECTOR, "a.ui-commandlink")
        download_link.click()

        # Allow time for the download to complete
        time.sleep(10)

        # Rename the downloaded file to the KRS number
        cwd = str(os.getcwd())
        download_dir = r'C:\Users\Sebastian\Downloads'  # Adjust the download directory as needed
        downloaded_file = os.path.join(download_dir, f'{file_name}.xml')  # Adjust the filename as needed
        new_file_name = os.path.join(download_dir, f'{krs_number}.xml')
        os.rename(downloaded_file, new_file_name)

        # Allow time to view the details
        time.sleep(100)

    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    krs_number = "0000021314"  # Replace with the desired KRS number
    search_krs(krs_number)