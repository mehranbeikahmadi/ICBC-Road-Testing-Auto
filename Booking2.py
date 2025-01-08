from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def handle_survey_popup(driver, wait):
    """Handle the survey popup if it appears."""
    try:
        popup = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".QSIWebResponsiveDialog-Layout1-SI_6liPUCmE8DIlvr8_text-container")
            )
        )
        print("Survey popup detected.")
        no_thanks_button = driver.find_element(
            By.CSS_SELECTOR, ".QSIWebResponsiveDialog-Layout1-SI_6liPUCmE8DIlvr8_button-2"
        )
        no_thanks_button.click()
        print("'No thanks' button clicked.")
    except Exception as e:
        print(f"Survey popup not found or failed to handle: {e}")


def click_next_button(driver, wait):
    """Click the 'Next' button."""
    try:
        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'primary') and text()='Next']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        driver.execute_script("arguments[0].click();", next_button)
        print("Next button clicked.")
    except Exception as e:
        print(f"Failed to click 'Next' button: {e}")
        # Debugging: Save page source and button details
        try:
            with open("debug_page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Saved page source for debugging.")
            next_button_debug = driver.find_elements(By.XPATH, "//button[contains(@class, 'primary') and text()='Next']")
            if next_button_debug:
                print(f"Found {len(next_button_debug)} 'Next' buttons. Outer HTML:")
                for button in next_button_debug:
                    print(driver.execute_script("return arguments[0].outerHTML;", button))
            else:
                print("No 'Next' button elements found.")
        except Exception as debug_e:
            print(f"Additional debugging failed: {debug_e}")


def icbc_booking_process():
    """Run the full ICBC booking process."""
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)
    wait = WebDriverWait(driver, 10)

    try:
        # Navigate to the ICBC login page
        driver.get("https://onlinebusiness.icbc.com/webdeas-ui/login;type=driver")
        print("Navigated to the ICBC login page.")

        # Perform login actions
        driver.find_element(By.ID, "mat-input-0").send_keys("Beikahmadi")
        driver.find_element(By.ID, "mat-input-1").send_keys("30381426")
        driver.find_element(By.ID, "mat-input-2").send_keys("Mohammad")
        driver.find_element(By.XPATH, "//label[@for='mat-checkbox-1-input']").click()
        driver.find_element(By.XPATH, "//button[contains(text(),'Sign in')]").click()
        print("Sign-in process completed.")

        # Handle survey popup
        handle_survey_popup(driver, wait)

        # Click the 'Next' button
        click_next_button(driver, wait)
        click_next_button(driver, wait)

    except Exception as e:
        print(f"An error occurred during the booking process: {e}")
    finally:
        input("Press Enter to close the browser...")
        driver.quit()


# Run the script
if __name__ == "__main__":
    icbc_booking_process()
def click_next_button(driver, wait):
    """Click the 'Next' button."""
    try:
        # تلاش برای پیدا کردن دکمه با انتخابگر اصلی
        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'primary') and text()='Next']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        driver.execute_script("arguments[0].click();", next_button)
        print("Next button clicked.")
    except Exception as e:
        print(f"Failed to click 'Next' button with primary selector: {e}")

        # بررسی انتخابگرهای جایگزین
        try:
            alternate_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'primary')]")
            if alternate_buttons:
                print(f"Found {len(alternate_buttons)} potential 'Next' buttons. Attempting click.")
                for button in alternate_buttons:
                    if "Next" in button.text:
                        driver.execute_script("arguments[0].scrollIntoView(true);", button)
                        driver.execute_script("arguments[0].click();", button)
                        print("Alternate 'Next' button clicked.")
                        return
            else:
                print("No alternate 'Next' buttons found.")
        except Exception as alt_e:
            print(f"Failed to find or click alternate 'Next' buttons: {alt_e}")

        # ذخیره صفحه برای بررسی بیشتر
        try:
            with open("debug_page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Saved page source for debugging.")
        except Exception as debug_e:
            print(f"Failed to save page source: {debug_e}")


# سایر بخش‌های کد ثابت مانده‌اند
