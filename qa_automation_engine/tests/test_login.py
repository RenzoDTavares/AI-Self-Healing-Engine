import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import our custom Proxy/Wrapper
from core.healing_driver import HealingDriver

# Target the V2 (Mutated locators version)
BASE_URL = "http://127.0.0.1:8000/login/v2/"

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    raw_driver = webdriver.Chrome(options=options)
    
    # Inject the AI superpower into the standard driver
    healed_driver = HealingDriver(raw_driver)
    
    yield healed_driver
    raw_driver.quit()

def test_ai_self_healing_login(driver):
    driver.get(BASE_URL)

    # The script uses V1 IDs, which DO NOT exist in the V2 UI
    # The AI engine will intercept the failure here and heal it at runtime
    username_input = driver.find_element(By.ID, "login-username")
    username_input.send_keys("admin_sdet")

    password_input = driver.find_element(By.ID, "login-password")
    password_input.send_keys("secure_password")

    login_button = driver.find_element(By.ID, "btn-submit-login")
    login_button.click()

    # Test Validation (Assert) checking the redirect to the dashboard
    WebDriverWait(driver, 5).until(EC.url_contains("dashboard"))
    assert "dashboard" in driver.current_url
    print("\n[TEST] V2 Login successfully executed via AI Self-Healing!")