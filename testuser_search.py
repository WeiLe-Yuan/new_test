from selenium import webdriver
import time,unittest,csv,io
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from public.initial_configuration.browser_config import browser_config
from public.initial_configuration import testFile_path

class TestuserSearch(unittest.TestCase):
    '''管理信息门户测试'''

    def setUp(self):
        self.driver = browser_config.user_config()  # 调用浏览器配置模块中的配置函数
        self.driver.get("http://192.168.1.203:8080/ips/login.real.jsp")
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_user_search(self):
        '''搜索用户测试'''

        '''登陆被测系统'''
        driver = self.driver
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("111111")
        driver.find_element_by_id("btnLogin").click()
        try:
            element = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, "html/body/div[10]/div[1]/a")))
        except BaseException:
            print("加载失败")

        '''用户查询测试'''
        driver.find_element_by_xpath("html/body/div[10]/div[1]/a").click()
        driver.find_element_by_xpath("//div[@id='navMenu']/ul/li[7]/a/img").click()
        time.sleep(3)
        driver.switch_to_frame("fNav")
        driver.find_element_by_id("spage.data.tree39").click()
        driver.switch_to_default_content()
        driver.switch_to_frame("fMain")
        driver.switch_to_frame("fRight")
        time.sleep(2)

        driver.find_element_by_xpath("//input[@name='userName' and @type='text']").clear()
        driver.find_element_by_xpath("//input[@name='userName' and @type='text']").click()
        driver.find_element_by_xpath("//input[@name='userName' and @type='text']").send_keys("小红")
        driver.find_element_by_class_name("button001").click()
        time.sleep(2)

        divs = self.driver.find_elements_by_tag_name("div")
        test = False
        for i in divs:
            if i.get_attribute("data-name") == "loginId":
                if i.text == "xiaohong":
                    test = True
        self.assertTrue(test, "查询失败")

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()