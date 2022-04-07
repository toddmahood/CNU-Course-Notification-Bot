from cnu_schedule import * 
import ezgmail
import requests
import time
import json
import mysql.connector

with open('secrets.json', 'r+') as f:
    data = json.load(f)
    password = data["password"]
    discord_webhook = data["webhook"]

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    autocommit=True
)

mycursor = mydb.cursor()
mycursor.execute("use sys")

while True:
    # Assume all classes to snipe are in May semester for demonstration purposes. 
    mycursor.execute("select UserCRN from Courses where UserSemester = 'May 2022';")
    result = mycursor.fetchall()
    crn_list = [crn_tuple[0] for crn_tuple in result]
    print(crn_list)
    schedule = CNUSchedule("May 2022")
    for course in schedule.courses:
        if course.crn in crn_list:
            if course.seats_available > 0: # Probably ought to change some of the course attribute types.
                print("CLASS OPEN")
                print(course)
                payload={"username": "CNU Notifier", "avatar_url": "https://cdn.discordapp.com/attachments/749755539331874898/961422345849933884/unknown.png",'content': f'<@457580945269063710> {course.course_name}: {course.title} is open for registration!'}
                response = requests.post(f"{discord_webhook}", data=payload)
                # send email here using ezgmail once html email template is done.
    
    time.sleep(3) # Small sleep time so we don't spam CNU's servers to oblivion

mydb.close()