from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def handle_survey_popup(driver, wait):
    """Click the 'No thanks' button if the survey popup appears."""
    try:
        survey_popup = wait.until(
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
    except Exception:
        print("Survey popup not found or 'No thanks' button could not be clicked.")


def choose_by_office_tab(driver, wait):
    """Select the 'By Office' tab in the booking dialog."""
    try:
        by_office_tab = wait.until(
            EC.element_to_be_clickable((By.ID, "mat-tab-label-1-1"))
        )
        by_office_tab.click()
        print("'By Office' tab selected.")
    except Exception as e:
        print(f"Failed to select 'By Office' tab: {e}")


def click_office_option(driver, wait, office_name):
    """Directly click the specific office option in the dropdown."""
    try:
        office_input = wait.until(EC.element_to_be_clickable((By.ID, "mat-input-4")))
        office_input.click()
        print("Dropdown opened.")

        options = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".mat-option-text"))
        )
        for option in options:
            if office_name in option.text:
                option.click()
                print(f"Clicked on office: {office_name}")
                return
        print(f"Office '{office_name}' not found in the dropdown options.")
    except Exception as e:
        print(f"Failed to click on office option: {e}")


def select_first_available_slot(driver, wait):
    """Select the first available time slot."""
    try:
        first_slot = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "mat-button-toggle:first-of-type button"))
        )
        first_slot.click()
        print("First available slot selected.")
    except Exception as e:
        print(f"Failed to select the first slot: {e}")


def click_review_appointment(driver, wait):
    """Click the 'Review Appointment' button."""
    try:
        # Locate the "Review Appointment" button using multiple strategies
        review_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'primary') and contains(span, 'Review Appointment')]")
            )
        )
        review_button.click()
        print("Review Appointment button clicked.")
    except Exception as e:
        print(f"Failed to click 'Review Appointment' button: {e}")


def icbc_booking_process():
    """Run the full ICBC booking process."""
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)
    wait = WebDriverWait(driver, 20)

    try:
        # Navigate to the ICBC login page
        driver.get("https://onlinebusiness.icbc.com/webdeas-ui/login;type=driver")

        # Perform login actions
        last_name_field = wait.until(EC.presence_of_element_located((By.ID, "mat-input-0")))
        last_name_field.clear()
        last_name_field.send_keys("Beikahmadi")

        licence_number_field = wait.until(EC.presence_of_element_located((By.ID, "mat-input-1")))
        licence_number_field.clear()
        licence_number_field.send_keys("30381426")

        keyword_field = wait.until(EC.presence_of_element_located((By.ID, "mat-input-2")))
        keyword_field.clear()
        keyword_field.send_keys("Mohammad12498")

        terms_checkbox_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='mat-checkbox-1-input']")))
        terms_checkbox_label.click()

        sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Sign in')]")))
        sign_in_button.click()
        print("Sign-in process initiated.")

        # Wait for navigation to the booking page
        wait.until(EC.url_contains("https://onlinebusiness.icbc.com/webdeas-ui/booking"))
        print("Navigated to the booking page.")

        # Close the survey popup if it appears
        handle_survey_popup(driver, wait)

        # Wait for the booking dialog to load
        booking_dialog = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "mat-dialog-container"))
        )
        print("Booking dialog detected.")

        # Choose the 'By Office' tab
        choose_by_office_tab(driver, wait)

        # Click on the specific office
        click_office_option(driver, wait, "Burnaby claim centre (Wayburne Drive)")

        # Select the first available time slot
        select_first_available_slot(driver, wait)

        # Click the 'Review Appointment' button
        click_review_appointment(driver, wait)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        input("Press Enter to close the browser...")
        driver.quit()


# Run the script
icbc_booking_process()
