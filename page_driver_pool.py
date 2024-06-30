import config
from page_driver import PageDriver
import logging

console_logger = logging.getLogger('console_logger')


class PageDriverPool:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.page_drivers = {}
            cls._instance.max_drivers = config.get_max_web_drivers()
        return cls._instance

    def create_driver(self, user_id=None):
        if len(self.page_drivers) >= self.max_drivers:
            console_logger.warning("Maximum number of WebDrivers reached. Cannot create new driver.")
            return None

        if (user_id):
            driver = PageDriver(user_id)
        else:
            driver = PageDriver()
        self.page_drivers[driver.id] = driver
        console_logger.info(f"Created new PageDriver with id {driver.id}")
        return driver.id

    def get_driver(self, driver_id):
        driver = self.page_drivers.get(driver_id)
        if driver is None:
            console_logger.warning(f"No PageDriver found with id {driver_id}")
        return driver

    def remove_driver(self, driver_id):
        driver = self.page_drivers.pop(driver_id, None)
        if driver:
            driver.quit_web_driver()
            del driver
            console_logger.info(f"Removed PageDriver with id {driver_id}")
        else:
            console_logger.warning(f"No PageDriver found with id {driver_id} to remove")

    def reset_pool(self):
        console_logger.info(f"Start reset PageDriver Pool")
        for driver_id in self.page_drivers.keys():
            self.remove_driver(driver_id)
        console_logger.info(f"Successfully reset PageDriver Pool")

    def __len__(self):
        return len(self.page_drivers)

    def __del__(self):
        self.reset_pool()


page_driver_pool = PageDriverPool()