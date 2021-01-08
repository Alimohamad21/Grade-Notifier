import json
import tkinter
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from selenium import webdriver

data = json.load(open('D:\passwords.json'))
password = data['site_password']
username = data['site_username']
driver = webdriver.Edge('/Users/Mohamed/Downloads/msedgedriver')
driver.maximize_window()
driver.get("https://std.eng.alexu.edu.eg/static/index.html")
while True:
    try:
        driver.find_element_by_id("details-button").click()
        break
    except:
        pass
driver.find_element_by_id("proceed-link").click()
while True:
    try:
        driver.find_element_by_id("usertype_1").click()
        break
    except:
        pass
driver.find_element_by_id("name").send_keys(username)
driver.find_element_by_id("password").send_keys(password)
driver.find_element_by_id("login_btn").click()


def midterm_marks_notifier():
    while True:
        for i in range(1, 7):
            while True:
                try:
                    course = driver.find_element_by_xpath(
                        "/html/body/div/section[2]/div/div/div[2]/table/tbody/tr[{}]/ td[4]".format(i)).text
                    break
                except:
                    pass
            while True:
                try:
                    grade = driver.find_element_by_xpath(
                        "/html/body/div/section[2]/div/div/div[2]/table/tbody/tr[{}]/ td[5]".format(i)).text
                    break
                except:
                    pass

            if len(grade) > 1:
                root = tkinter.Tk()
                root.withdraw()
                messagebox.showerror(course, grade)
                directory = tkinter.filedialog.askdirectory()
                f = open(directory + '/results.txt', 'a+')
                f.write(grade)
        driver.refresh()


midterm_marks_notifier()
