from selenium import webdriver
from selenium.webdriver.common.keys import Keys #For 2FA
from selenium.webdriver.common.by import By
from time import sleep
from secrets import pw
from secrets import username


class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome(executable_path='D:/PC/Downloads/chromedriver_win32/chromedriver.exe')
        self.driver.maximize_window()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element(By.XPATH, "//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element(By.XPATH, "//input[@name=\"password\"]")\
            .send_keys(pw)
        self.driver.find_element(By.XPATH, '//button[@type="submit"]')\
            .click()
        sleep(10)
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm')]")\
            .send_keys(Keys.ENTER)
        sleep(6)
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(2)
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(2)

    def get_unfollowers(self):
        self.driver.find_element(By.XPATH, "//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(5)
        self.driver.find_element(By.XPATH, "//a[contains(@href,'/following')]")\
            .click()
        following = self._get_names_following()
        self.driver.find_element(By.XPATH, "//a[contains(@href,'/followers')]")\
            .click()
        followers = self._get_names_followers()
        not_following_back = [
            user for user in following if user not in followers
        ]
        for x in not_following_back:
            profiles = "https://instagram.com/" + x
            print(profiles)

    def _get_names_following(self):
        sleep(2)
        # scroll
        scroll_box = self.driver.find_element(By.XPATH, 
            "//div[contains(@class,'_aano')]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script(
                """
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements(By.TAG_NAME, 'a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element(By.XPATH, "//div[contains(@class,'_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p  _ab9y _abcm')]//button[contains(@class,'_abl-')]")\
            .click()
        return names

    def _get_names_followers(self):
        sleep(2)
        # scroll
        scroll_box = self.driver.find_element(By.XPATH, 
            "//div[contains(@class,'_aano')]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script(
                """
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements(By.TAG_NAME, 'a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element(By.XPATH, "//div[contains(@class,'_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p  _ab9y _abcm')]//button[contains(@class,'_abl-')]")\
            .click()
        return names


my_bot = InstaBot(username, pw)
my_bot.get_unfollowers()
