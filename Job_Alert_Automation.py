import csv
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

edge_driver_path = "msedgedriver.exe" # ENTER YOUR KNOWN PATH
service = Service(edge_driver_path)

driver = webdriver.Edge(service = service)

driver.get("https://www.naukri.com/")
time.sleep(3)

search_box = driver.find_element(By.CSS_SELECTOR, "input.suggestor-input")
search_box.send_keys("Python Developer")
search_box.send_keys(Keys.RETURN)
time.sleep(3)

jobs = driver.find_elements(By.CSS_SELECTOR, "a.title")
companies = driver.find_elements(By.CSS_SELECTOR, "a.comp-name")
locations = driver.find_elements(By.CSS_SELECTOR, "span.locWdth")

valid_keyword = ["Python", "SQL", "Senior Python"] # Edit it of your preference
valid_location = ["Bengaluru", "Bangalore", "Chennai", "Remote"]

job_list = []
for i in range(min(len(jobs), len(companies), len(locations))):
    job_title = jobs[i].text
    Company_name = companies[i].text
    Location = locations[i].text
    Job_url = jobs[i].get_attribute("href")

    if any(keyword.lower() in job_title.lower() for keyword in valid_keyword) and Location in valid_location:
        job_list.append([job_title, Company_name, Location, Job_url])

if job_list:
    with open("Filtered_Naukri_jobs.csv", "w", newline = "", encoding = "utf-8")as file:
        writer = csv.writer(file)
        writer.writerow(["Job Title", "Company", "Location", "Job URL"])
        writer.writerows(job_list)
    print("Filtered jobs have been saved")
else:
    print("No matching jobs found")

# ****(OPTIONAL)***
# These below code will append all the jobs without filtering

# with open("Naukri_Jobs_list.csv", "w", newline = "", encoding = "utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Job Title", "Company Name", "Location", "Job URL"])
#     writer.writerows(job_list)
#
# print("✅ Job data saved to naukri_jobs.csv")

driver.quit()

#Email using SMTP Access

import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_mail = "sender@gmail.com"
sender_password = "Your 16-digit password generated at youe Google account"
receiver_mail = "receiver@gmail.com"

job_list = []
with open("Filtered_Naukri_jobs.csv", "r", encoding = "utf-8") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        job_list.append(row)

email_content = "<h2>Job Alert - Python & SQL Jobs</h2><ul>"

for job in job_list:
    job_title, Company, Location, Job_URL = job
    email_content += f'<li><b>{job_title} at {Company} {Location} - <a href="{Job_URL}"> Apply Here</a></li>'

email_content += "</ul>"

#Create email message
msg = MIMEMultipart()
msg["From"] = "sender@gmail.com"
msg["To"] = "receiver@gmail.com"
msg["Subject"] = "🔔 Job Alerts: Python & SQL Jobs"
msg.attach(MIMEText(email_content, "html"))

#Connect to SMTP server and send mail
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_mail, sender_password)
    server.sendmail(sender_mail, receiver_mail, msg.as_string())
    server.quit()
    print("✅ Success")
except Exception as e:
    print(f"❌ Error sending email: {e}")

