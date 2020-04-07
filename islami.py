from locust import HttpLocust, TaskSet
import random
import string
import mysql.connector
import configparser

config = configparser.RawConfigParser()
config.read('Config.properties')

CONST_HOST = config.get('DatabaseSection', 'database.mysql.host')
CONST_USER = config.get('DatabaseSection', 'database.mysql.user')
CONST_PSWD = config.get('DatabaseSection', 'database.mysql.password')
CONST_DTBS = config.get('DatabaseSection', 'database.mysql.name')

def sholatTime(l):
    mydb = mysql.connector.connect(
    host= CONST_HOST,
    user= CONST_USER,
    passwd= CONST_PSWD,
    database= CONST_DTBS
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT access_token from token  order by rand()limit 1")
    myresult = mycursor.fetchall()
    
    #aceh : 4.695135, 96.749397, jakarta : -6.198790, 106.784379, palangkaraya : 
    latlong = [["-6.198790","106.784379"],[]]
    response_type="otp_code"
    client_id = "5d8218f2f48c3d6b94645142"
    state= "Indonesia"
    scope="free"
    calling_code = "+62"
    
    for rows in myresult:
        calling_code = rows[0]  #urutan pada db
        phone_number = rows[1]
        l.client.headers['Content-Type'] = "application/x-www-form-urlencoded"
        l.client.headers['Accept'] = "application/json"
        response = l.client.post("/api/v1/oauth/otp/code",
        {"provider":"sms",
        "response_type":"otp_code",
        "scope":"free",
        "phone_number":phone_number,
        "calling_code":calling_code,
        "client_id":"5d8218f2f48c3d6b94645142",
        "scope":"free"
        })
        json_response_dict = response.json()
        code = json_response_dict['result']['code']
        otp_code= json_response_dict['result']['otp_code']
        #insert to otp
        sql_insert_login = "INSERT INTO otp (code,otp_code) VALUES (%s, %s)"
        val_insert_login = (code, otp_code)
        mycursor.execute(sql_insert_login, val_insert_login)

    mydb.commit()
    

def logout(l):
    l.client.post("/api/v3/signout", {"username":"system", "password":"systembahaso"})

def index(l):
    l.client.get("/")

def profile(l):
    l.client.get("/profile")

class UserBehavior(TaskSet):
    tasks = {register:1, requestOTP:1, validateOTP:1}
    #tasks = {register:1, signin: 3, profile: 1}

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000