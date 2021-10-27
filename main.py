from selenium import webdriver
from selenium.webdriver.common.keys import Keys #For 2FA
from time import sleep
from secrets import pw
from secrets import username


class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(10)
        self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div[1]/div/form/div[2]/button").send_keys(Keys.ENTER)
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(2)

    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()
        following = self._get_names_following()
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
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
        scroll_box = self.driver.find_element_by_xpath(
            "/html/body/div[6]/div/div/div[3]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script(
                """
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/div/div[2]/button")\
            .click()
        return names

    def _get_names_followers(self):
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath(
            "/html/body/div[6]/div/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script(
                """
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/div/div[2]/button")\
            .click()
        return names


my_bot = InstaBot(username, pw)
my_bot.get_unfollowers()
