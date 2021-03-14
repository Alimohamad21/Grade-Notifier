import json
import tkinter
from tkinter import messagebox

from selenium import webdriver

option = input('1- Coursework Notifier\n2- Final Grade Notifier\n\nPlease choose an option from the above:')
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
        updated_grades = json.load(open('latest_results.json', 'r'))
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

            if grade != updated_grades[course]:
                updated_grades[course] = grade
                root = tkinter.Tk()
                root.withdraw()
                messagebox.showinfo(course, grade)
                json.dump(updated_grades, open('latest_results.json', 'w'))
        driver.refresh()


def final_grade_notifier():
    while True:
        while True:
            try:
                driver.find_element_by_xpath('/html/body/div/section[1]/nav/ul/li[8]/a').click()
                if driver.find_element_by_xpath('/html/body/div/section[2]/div/div/h1').text == 'Courses Grades':
                    break
            except:
                pass
        updated_grades = json.load(open('final_grades.json', 'r'))
        for i in range(1, 7):
            while True:
                try:
                    course = driver.find_element_by_xpath(
                        f"/html/body/div/section[2]/div/table[5]/tbody/tr[{i}]/td[2]").text
                    break
                except:
                    pass
            while True:
                try:
                    grade = driver.find_element_by_xpath(
                        f"/html/body/div/section[2]/div/table[5]/tbody/tr[{i}]/td[4]").text
                    break
                except:
                    pass

            if grade != updated_grades[course]:
                updated_grades[course] = grade
                root = tkinter.Tk()
                root.withdraw()
                messagebox.showinfo(course, grade)
                json.dump(updated_grades, open('final_grades.json', 'w'))
        driver.refresh()


if option == '1':
    midterm_marks_notifier()
if option == '2':
    final_grade_notifier()
