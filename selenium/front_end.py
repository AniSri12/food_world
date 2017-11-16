import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys


driver = webdriver.Remote(
   command_executor='http://selenium-chrome:4444/wd/hub',
   desired_capabilities=DesiredCapabilities.CHROME)

driver.get("http://web:8000")

sign_up = driver.find_element_by_xpath('/html/body/nav/div/ul/li[4]/a')
sign_up.click()
print(sign_up)
print(driver.current_url)



# class PythonOrgSearch(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Firefox()

#     def test_search_in_python_org(self):
#         driver = self.driver
#         driver.get("http://www.python.org")
#         self.assertIn("Python", driver.title)
#         elem = driver.find_element_by_name("q")
#         elem.send_keys("pycon")
#         elem.send_keys(Keys.RETURN)
#         assert "No results found." not in driver.page_source


#     def tearDown(self):
#         self.driver.close()

# if __name__ == "__main__":
#     unittest.main()
