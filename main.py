from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys  # For 2FA
from selenium.webdriver.common.by import By
from time import sleep
from secrets_1 import pw, username


class InstaBot:
    def __init__(self, username, pw):
        # If server is down
        chrome_driver_path = "./chromedriver.exe"
        self.service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=self.service)

        # If server isn't down
        # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        self.driver.maximize_window()
        self.username = username
        self.driver.get("https://instagram.com")
        self.login(username, pw)

    def login(self, username, pw):
        sleep(2)
        self.driver.find_element(By.XPATH, '//input[@name="username"]').send_keys(
            username
        )
        self.driver.find_element(By.XPATH, '//input[@name="password"]').send_keys(pw)
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        sleep(10)
        self.dismiss_popups()

        # If you have 2FA
        # self.driver.find_element(
        #     By.XPATH, "//button[contains(text(), 'Confirm')]"
        # ).send_keys(Keys.ENTER)
        # sleep(6)

    def dismiss_popups(self):
        try:
            self.driver.find_element(
                By.XPATH, "//button[contains(@class,' _acan _acap _acas _aj1- _ap30')]"
            ).click()
            sleep(2)
            self.driver.find_element(
                By.XPATH, "//button[contains(text(), 'Not Now')]"
            ).click()
            sleep(2)
        except Exception as e:
            print(e)

    def get_unfollowers(self):
        self.driver.find_element(
            By.XPATH, "//a[contains(@href,'/{}')]".format(self.username)
        ).click()
        sleep(5)
        following = self._get_names("following")
        followers = self._get_names("followers")
        not_following_back = [user for user in following if user not in followers]
        for x in not_following_back:
            print(f"https://instagram.com/{x}")

    def _get_names(self, relation_type):
        sleep(3)
        self.driver.find_element(
            By.XPATH, f"//a[contains(@href,'/{relation_type}')]"
        ).click()
        sleep(3)
        # scroll
        scroll_box = self.driver.find_element(
            By.XPATH,
            "//div[contains(@class,'xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6')]",
        )
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(3)
            ht = self.driver.execute_script(
                """
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """,
                scroll_box,
            )
        names = [
            link.text
            for link in scroll_box.find_elements(By.TAG_NAME, "a")
            if link.text
        ]
        # close button
        # Update once in a while
        self.driver.find_element(
            By.XPATH,
            "//div[contains(@class,'x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1sxyh0 xurb0ha x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1')]//button[contains(@class,'_abl-')]",
        ).click()
        return names


my_bot = InstaBot(username, pw)
my_bot.get_unfollowers()
