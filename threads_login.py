import random
import string
import time
from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def generate_random_string(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def initialize_driver(bundle_id):
    options = XCUITestOptions()
    options.platform_name = 'iOS'
    options.automation_name = 'XCUITest'
    options.udid = 'DEVICE_UUID'
    options.xcode_org_id = 'XCODE_ORG_ID'
    options.xcode_signing_id = 'TEAM_ID'
    options.bundle_id = bundle_id
    options.set_capability('showXcodeLog', True)
    return webdriver.Remote('http://localhost:4723', options=options)


def install_threads():
    driver = None
    try:
        driver = initialize_driver('com.apple.AppStore')
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Search"))
        ).click()
        print("Clicked Search tab")

        search_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((AppiumBy.CLASS_NAME, "XCUIElementTypeSearchField"))
        )
        search_field.click()
        search_field.clear()
        search_field.send_keys("Threads by Instagram")
        print("Entered search text")

        search_field.send_keys("\n")
        time.sleep(3)

        threads_app = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Threads, Connect and share ideas"))
        )
        threads_app.click()
        print("Selected Threads app")
        try:
            install_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "GET"))
            )
            install_button.click()
            print("Clicked GET button")
        except:
            cloud_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "RedownloadCloudIcon"))
            )
            cloud_button.click()
            print("Clicked Cloud download button")
        try:
            confirm_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Install"))
            )
            confirm_button.click()
            print("Confirmed installation")
        except:
            pass
        print("Waiting 50 seconds for download to complete...")
        start_time = time.time()
        while time.time() - start_time < 55:
            try:
                driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Search")
                time.sleep(5)
            except:
                break

    except Exception as e:
        print(f"Error during installation: {str(e)}")
        if driver:
            driver.save_screenshot("ios_install_error.png")
        raise
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass


def login_to_threads():
    driver = None
    try:
        driver = initialize_driver('com.burbn.barcelona')
        print(driver.page_source)
        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((AppiumBy.XPATH,
                                        "//XCUIElementTypeButton[contains(@name, 'Log in as ')]"))
        )
        login_button.click()
        time.sleep(10)
        print("Clicked login button")
        return True

    except Exception as e:
        print(f"Error during login: {str(e)}")
        if driver:
            driver.save_screenshot("login_error.png")
        return False
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass


def main():
    install_threads()
    login_success = login_to_threads()
    print(f"Login {'successful' if login_success else 'failed'}")


if __name__ == '__main__':
    main()