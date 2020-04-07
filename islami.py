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
    
    #aceh : 4.695135, 96.749397, jakarta : -6.198790, 106.784379, palangkaraya : -2.2136, 113.9108, papua : -0.861453, 134.062042
    latlong = [["4.695135", "96.749397"],["-6.198790","106.784379"],["-2.2136", "113.9108"],["-0.861453", "134.062042"]]
   
    
    for rows in myresult:
        random_latlong = random.choice(latlong)
        latitude = random_latlong[0]
        longitude = random_latlong[1]
       
        l.client.headers['Authorization'] = "Bearer " + rows[0] 
        l.client.headers['Accept'] = "application/json"
        response = l.client.get("/api/v1/sholat-time?latitude="+ latitude +"&longitude="+longitude)
        json_response_dict = response.json()
        if json_response_dict['code'] != 200:
           raise FlowException('comment not created')
    
def landingPageGetTopUstad(l):
    l.client.get("/api/v1/landing/ustads",{"Accept":"application/json"})
    
def landingPageRandomSelfReminder(l):
    l.client.get("/api/v1/landing/self-reminders",{"Accept":"application/json"})    

def logout(l):
    l.client.post("/api/v3/signout", {"username":"system", "password":"systembahaso"})

def index(l):
    l.client.get("/")

def profile(l):
    l.client.get("/profile")

class UserBehavior(TaskSet):
    tasks = {sholatTime:1, landingPageGetTopUstad:2, landingPageRandomSelfReminder:2}
    #tasks = {register:1, signin: 3, profile: 1}

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000