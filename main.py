import json
import smtplib
import ssl
import tkinter
from tkinter import messagebox

from selenium import webdriver


class Email:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def send_email(self, receiver, subject, message):
        smtp_server = "smtp.gmail.com"
        port = 587
        message = f"""\
        {subject}

        {message}"""
        context = ssl.create_default_context()
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(self.username, self.password)
            server.sendmail(self.username, receiver, message)
        except Exception as e:
            print(e)
        finally:
            server.quit()


class Whatsapp:
    def __init__(self, driver):
        self.driver = driver

    def send_message(self, receiver, message):
        contact = self.driver.find_element_by_xpath(f'//span[@title = "{receiver}"]')
        contact.click()
        msgBox = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]')
        msgBox.send_keys(message)
        sendButton = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]')
        sendButton.click()


class Site:
    def __init__(self, driver, username, password):
        self.username = username
        self.password = password
        self.driver = driver

    def open_site(self):
        self.driver.maximize_window()
        driver.get("https://std.eng.alexu.edu.eg/static/index.html")
        driver.execute_script('''window.open("https://web.whatsapp.com/","_blank");''')
        input('Please scan QR code then press any button to proceed:')
        driver.switch_to.window(driver.window_handles[0])
        while True:
            try:
                self.driver.find_element_by_id("details-button").click()
                break
            except:
                pass
        self.driver.find_element_by_id("proceed-link").click()
        while True:
            try:
                self.driver.find_element_by_id("usertype_1").click()
                break
            except:
                pass
        self.driver.find_element_by_id("name").send_keys(self.username)
        self.driver.find_element_by_id("password").send_keys(self.password)
        self.driver.find_element_by_id("login_btn").click()

    def midterm_marks_notifier(self):
        self.open_site()
        while True:
            updated_grades = json.load(open('latest_results.json', 'r'))
            for i in range(1, 7):
                while True:
                    try:
                        course = self.driver.find_element_by_xpath(
                            "/html/body/div/section[2]/div/div/div[2]/table/tbody/tr[{}]/ td[4]".format(i)).text
                        break
                    except:
                        pass
                while True:
                    try:
                        grade = self.driver.find_element_by_xpath(
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
            self.driver.refresh()

    def final_grade_notifier(self):
        data = json.load(open('D:\passwords.json'))
        self.open_site()
        while True:
            while True:
                try:
                    self.driver.find_element_by_xpath('/html/body/div/section[1]/nav/ul/li[8]/a').click()
                    if self.driver.find_element_by_xpath(
                            '/html/body/div/section[2]/div/div/h1').text == 'Courses Grades':
                        break
                except:
                    pass
            updated_grades = json.load(open('final_grades.json', 'r'))
            for i in range(1, 7):
                while True:
                    try:
                        course = self.driver.find_element_by_xpath(
                            f"/html/body/div/section[2]/div/table[5]/tbody/tr[{i}]/td[2]").text
                        break
                    except:
                        pass
                while True:
                    try:
                        grade = self.driver.find_element_by_xpath(
                            f"/html/body/div/section[2]/div/table[5]/tbody/tr[{i}]/td[4]").text
                        break
                    except:
                        pass

                if grade != updated_grades[course]:
                    updated_grades[course] = grade
                    driver.switch_to.window(driver.window_handles[1])
                    whatsapp = Whatsapp(self.driver)
                    for receiver in data['grade_receivers']:
                        receiver += ' 🏠'
                        whatsapp.send_message(receiver, f'{course} {grade}')
                    for receiver in data['notification_receivers']:
                        whatsapp.send_message(receiver, f'grade el {course} 3al site')
                    driver.switch_to.window(driver.window_handles[0])
                    email = Email(data['email_username'], data['email_password'])
                    email_receiver = data['personal_email']
                    email_subject = course + ' : ' + grade
                    email_message = f'{course} grade is out! grade: {grade}'
                    email.send_email(email_receiver, email_subject, email_message)
                    # root = tkinter.Tk()
                    # root.withdraw()
                    # messagebox.showinfo(course, grade)
                    json.dump(updated_grades, open('final_grades.json', 'w'))
            self.driver.refresh()


option = input('1- Coursework Notifier\n2- Final Grade Notifier\n\nPlease choose an option from the above:')
data = json.load(open('D:\passwords.json'))
driver = webdriver.Edge('/Users/Mohamed/Downloads/msedgedriver')
site = Site(driver, data['site_username'], data['site_password'])
if option == '1':
    site.midterm_marks_notifier()
if option == '2':
    site.final_grade_notifier()
