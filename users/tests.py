from django.test import TestCase,LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Create your tests here.

class CustomerFormTesting(LiveServerTestCase):

    def testform(self):
        path = "C:\Program Files (x86)\chromedriver.exe"
        browser = webdriver.Chrome(path)
        browser.get('http://127.0.0.1:8000/accounts/customer_register/')

        
        username = browser.find_element_by_id("id_username")
        email = browser.find_element_by_id("id_email")
        password1 = browser.find_element_by_id("id_password1")
        password2 = browser.find_element_by_id("id_password2")

        


        # # sending values
        username.send_keys("Customer1")
        email.send_keys("monicaanna6548@gmail.com")
        password1.send_keys("testing123@")
        password2.send_keys("testing123@")


        browser.find_element_by_id("cust_form").submit()

# Create your tests here.
