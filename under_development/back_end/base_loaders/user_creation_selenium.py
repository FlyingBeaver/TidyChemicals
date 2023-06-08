from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


# !!! PASTE path to chromedriver inside of Chrome() below
browser = Chrome("")


users = {"LarysaHrybalova": "iLoveBATHSS55",
         "DarthVader": "Star0fDeath",
         "BillieEilish": "ILoveL@na"
        }

for user, password in users.items():
    browser.get("http://127.0.0.1:8000/registration/")
    login_field = browser.find_element(By.CSS_SELECTOR, "input[name='username']")
    password_field1 = browser.find_element(By.CSS_SELECTOR, "input[name='password1']")
    password_field2 = browser.find_element(By.CSS_SELECTOR, "input[name='password2']")
    submit_button = browser.find_element(By.CSS_SELECTOR, "input[type='submit']")

    login_field.send_keys(user_names)
    password_field1.send_keys(password)
    password_field2.send_keys(password)
    submit_button.click()
