import json
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from core.llm_engine import get_healed_locator

# Setup paths for the cache directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, "cache")
CACHE_FILE = os.path.join(CACHE_DIR, "healed_locators.json")

class HealingDriver:
    """Wrapper for Selenium WebDriver with AI Self-Healing and Caching."""
    
    def __init__(self, driver):
        self.driver = driver
        self.by_map = {
            "id": By.ID, "name": By.NAME, "class name": By.CLASS_NAME,
            "css selector": By.CSS_SELECTOR, "xpath": By.XPATH
        }
        os.makedirs(CACHE_DIR, exist_ok=True)
        self.healed_cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.healed_cache, f, indent=4)

    def __getattr__(self, attr):
        return getattr(self.driver, attr)

    def find_element(self, by, value):
        locator_key = f"{by}:{value}"

        # 1. Performance: Check local cache first
        if locator_key in self.healed_cache:
            cached_data = self.healed_cache[locator_key]
            print(f"\n[CACHE] Using healed locator: {cached_data['by']}='{cached_data['value']}'")
            return self.driver.find_element(self.by_map[cached_data['by']], cached_data['value'])

        # 2. Execution: Standard find or AI Healing
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            print(f"\n[SELF-HEALING] Failure detected for: {by}='{value}'")
            healed_data = get_healed_locator(self.driver.page_source, by, value)
            
            if healed_data:
                new_by = healed_data["by"].lower()
                new_val = healed_data["value"]
                print(f"[SELF-HEALING] AI suggested: {new_by}='{new_val}'")
                
                element = self.driver.find_element(self.by_map[new_by], new_val)
                self.healed_cache[locator_key] = {"by": new_by, "value": new_val}
                self._save_cache()
                return element
            raise