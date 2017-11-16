import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys



class foodworldTest(unittest.TestCase):

	def setUp(self):
		self.driver = webdriver.Remote(
		   command_executor='http://selenium-chrome:4444/wd/hub',
		   desired_capabilities=DesiredCapabilities.CHROME)
	   

	def tearDown(self):
		self.driver.quit()

	def test_signin(self):
		self.driver.get("http://web:8000") # Start 
		sign_up = self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[4]/a')
		sign_up.click()

		first_name = self.driver.find_element_by_xpath('//*[@id="id_first_name"]')
		first_name.send_keys("Chad")

		last_name = self.driver.find_element_by_xpath('//*[@id="id_last_name"]')
		last_name.send_keys("Mango")
		email = self.driver.find_element_by_xpath('//*[@id="id_email"]')
		email.send_keys("mango@chad.com")
		password = self.driver.find_element_by_xpath('//*[@id="id_password"]')
		password.send_keys("abc123")
		phone_number = self.driver.find_element_by_xpath('//*[@id="id_phone_number"]')
		phone_number.send_keys("123-456-6789")

		sign_up_button = self.driver.find_element_by_xpath('/html/body/form/button')
		sign_up_button.click()

		email_login = self.driver.find_element_by_xpath('//*[@id="id_email"]')
		email_login.send_keys("mango@chad.com")
		pass_login = self.driver.find_element_by_xpath('//*[@id="id_password"]')
		pass_login.send_keys("abc123")

		login_butt = self.driver.find_element_by_xpath('/html/body/form/button[1]')
		self.driver.implicitly_wait(10)
		login_butt.click()
		self.driver.implicitly_wait(10)

		logout_button = self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[5]/a')
		self.assertEquals(logout_button.text, "Logout")

	def test_addsnack(self):
		self.driver.get("http://web:8000") # Start 
		sign_up = self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[4]/a')
		sign_up.click()
		self.driver.implicitly_wait(10)

		first_name = self.driver.find_element_by_xpath('//*[@id="id_first_name"]')
		first_name.send_keys("Chado")

		last_name = self.driver.find_element_by_xpath('//*[@id="id_last_name"]')
		last_name.send_keys("Mangoy")
		email = self.driver.find_element_by_xpath('//*[@id="id_email"]')
		email.send_keys("money@cnn.com")
		password = self.driver.find_element_by_xpath('//*[@id="id_password"]')
		password.send_keys("lalalala123")
		phone_number = self.driver.find_element_by_xpath('//*[@id="id_phone_number"]')
		phone_number.send_keys("123-456-6789")

		sign_up_button = self.driver.find_element_by_xpath('/html/body/form/button')
		sign_up_button.click()

		email_login = self.driver.find_element_by_xpath('//*[@id="id_email"]')
		email_login.send_keys("money@cnn.com")
		pass_login = self.driver.find_element_by_xpath('//*[@id="id_password"]')
		pass_login.send_keys("lalalala123")

		login_butt = self.driver.find_element_by_xpath('/html/body/form/button[1]')
		login_butt.click()

		add_snack = self.driver.find_element_by_xpath("/html/body/nav/div/ul/li[3]/a")
		add_snack.click()
		self.driver.implicitly_wait(10)

		name = self.driver.find_element_by_xpath('//*[@id="id_name"]')
		name.send_keys("Apples")

		nutrition_info = self.driver.find_element_by_xpath('//*[@id="id_nutrition_info"]')
		nutrition_info.send_keys('Good for you')

		country = self.driver.find_element_by_xpath('//*[@id="id_country"]')
		country.send_keys("USA")

		description = self.driver.find_element_by_xpath('//*[@id="id_description"]')
		description.send_keys("Crisp apples")

		price = self.driver.find_element_by_xpath('//*[@id="id_price"]')
		price.send_keys('5.99')
		

		add_snacky = self.driver.find_element_by_xpath('/html/body/form/button')
		add_snacky.click()

		success_message = self.driver.find_element_by_xpath('/html/body/p[2]')

		self.assertEquals(success_message.text, "Success! Your Snack Has Been Created!")


	def test_register(self):
		self.driver.get("http://web:8000") # Start 
		sign_up = self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[4]/a')
		sign_up.click()

		first_name = self.driver.find_element_by_xpath('//*[@id="id_first_name"]')
		first_name.send_keys("Chad")

		last_name = self.driver.find_element_by_xpath('//*[@id="id_last_name"]')
		last_name.send_keys("Mango")

		email = self.driver.find_element_by_xpath('//*[@id="id_email"]')
		email.send_keys("chad@mango.com")

		password = self.driver.find_element_by_xpath('//*[@id="id_password"]')
		password.send_keys("123abc")
		phone_number = self.driver.find_element_by_xpath('//*[@id="id_phone_number"]')
		phone_number.send_keys("123-456-6789")

		sign_up_button = self.driver.find_element_by_xpath('/html/body/form/button')
		sign_up_button.click()

		self.driver.implicitly_wait(10)

		self.assertEqual(self.driver.current_url, "http://web:8000/login/")

	def test_viewitem(self):
		self.driver.get("http://web:8000")
		tea = self.driver.find_element_by_xpath('/html/body/div[1]/a[2]/div/div[1]')
		tea.click()
		info = self.driver.find_element_by_xpath('/html/body/div[1]/div')
		self.assertEquals(info.text, "Choice Organic Russian Caravan Black Tea")

if __name__ == "__main__":
	unittest.main()
			
	

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

