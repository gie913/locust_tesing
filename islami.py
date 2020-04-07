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

def consultationUstadList(l):
    mydb = mysql.connector.connect(
    host= CONST_HOST,
    user= CONST_USER,
    passwd= CONST_PSWD,
    database= CONST_DTBS
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT access_token from token  order by rand()limit 1")
    myresult = mycursor.fetchall()
    timezone = "Asia/Jakarta"
 
    for rows in myresult:      
        l.client.headers['Authorization'] = "Bearer " + rows[0] 
        l.client.headers['Accept'] = "application/json"
        l.client.headers['x-Timezone'] = timezone
        response = l.client.get("/api/v1/consultation/asuser/ustads/list?page=1&per_page=10")
        json_response_dict = response.json()
        if json_response_dict['code'] != 200:
           raise FlowException('comment not created')

def consultationOnGoing(l):
    mydb = mysql.connector.connect(
    host= CONST_HOST,
    user= CONST_USER,
    passwd= CONST_PSWD,
    database= CONST_DTBS
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT access_token from token  order by rand()limit 1")
    myresult = mycursor.fetchall()
    timezone = "Asia/Jakarta"
 
    for rows in myresult:      
        l.client.headers['Authorization'] = "Bearer " + rows[0] 
        l.client.headers['Accept'] = "application/json"
        l.client.headers['x-Timezone'] = timezone
        response = l.client.get("/api/v1/consultation/asuser/sessions/ongoing")
        json_response_dict = response.json()
        if json_response_dict['code'] != 200:
           raise FlowException('comment not created')


def storeItemList(l):
    mydb = mysql.connector.connect(
    host= CONST_HOST,
    user= CONST_USER,
    passwd= CONST_PSWD,
    database= CONST_DTBS
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT access_token from token  order by rand()limit 1")
    myresult = mycursor.fetchall()
    timezone = "Asia/Jakarta"
 
    for rows in myresult:      
        l.client.headers['Authorization'] = "Bearer " + rows[0] 
        l.client.headers['Accept'] = "application/json"
        l.client.headers['x-Timezone'] = timezone
        response = l.client.get("/api/v1/store-items/lists")
        json_response_dict = response.json()
        if json_response_dict['code'] != 200:
           raise FlowException('comment not created') 
           
def storeItemListGroup(l):
    mydb = mysql.connector.connect(
    host= CONST_HOST,
    user= CONST_USER,
    passwd= CONST_PSWD,
    database= CONST_DTBS
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT access_token from token  order by rand()limit 1")
    myresult = mycursor.fetchall()
    timezone = "Asia/Jakarta"
 
    for rows in myresult:      
        l.client.headers['Authorization'] = "Bearer " + rows[0] 
        l.client.headers['Accept'] = "application/json"
        l.client.headers['x-Timezone'] = timezone
        response = l.client.get("/api/v1/store-items/lists/group-by-code/LATIH_QURAN")
        json_response_dict = response.json()
        if json_response_dict['code'] != 200:
           raise FlowException('comment not created') 


def SelfReminderCategoryList(l):
    mydb = mysql.connector.connect(
    host= CONST_HOST,
    user= CONST_USER,
    passwd= CONST_PSWD,
    database= CONST_DTBS
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT otp_code,code FROM otp  order by rand()limit 1")
    myresult = mycursor.fetchall()
    list_of_categories_id = []
    
    for rows in myresult:
        otp_code = rows[0]  #urutan pada db
        code = rows[1]
        l.client.headers['Authorization'] = "Bearer " + rows[0] 
        l.client.headers['Accept'] = "application/json"
        l.client.headers['x-Timezone'] = timezone
        response = l.client.get("/api/v1/quotes/self-reminders/categories") 
        json_response_dict = response.json()
        if json_response_dict['code'] != 200:
            raise FlowException('comment not created') 
       

def SelfReminderCategoryIds():
    mydb = mysql.connector.connect(
    host= CONST_HOST,
    user= CONST_USER,
    passwd= CONST_PSWD,
    database= CONST_DTBS
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT otp_code,code FROM otp  order by rand()limit 1")
    myresult = mycursor.fetchall()
    list_of_categories_id = []
    
    for rows in myresult:
        otp_code = rows[0]  #urutan pada db
        code = rows[1]
        l.client.headers['Authorization'] = "Bearer " + rows[0] 
        l.client.headers['Accept'] = "application/json"
        l.client.headers['x-Timezone'] = timezone
        response = l.client.get("/api/v1/quotes/self-reminders/categories") 
        json_response_dict = response.json()
        category_id = json_response_dict['result']['data']['id']
        list_of_categories_id.append(category_id)

    return list_of_categories_id


def SelfReminderCategoryChoose(l):
    mydb = mysql.connector.connect(
    host= CONST_HOST,
    user= CONST_USER,
    passwd= CONST_PSWD,
    database= CONST_DTBS
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT otp_code,code FROM otp  order by rand()limit 1")
    myresult = mycursor.fetchall()
    
    for rows in myresult:
        l.client.headers['Authorization'] = "Bearer " + rows[0] 
        l.client.headers['Accept'] = "application/json"
        l.client.headers['x-Timezone'] = timezone
        response = l.client.post("/api/v1/quotes/self-reminders/user-categories",
        {"category_ids": SelfReminderCategoryIds() }
        ) 
        json_response_dict = response.json()
        if json_response_dict['code'] != 200:
            raise FlowException('comment not created') 

def SelfReminderList(l):
    mydb = mysql.connector.connect(
    host= CONST_HOST,
    user= CONST_USER,
    passwd= CONST_PSWD,
    database= CONST_DTBS
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT otp_code,code FROM otp  order by rand()limit 1")
    myresult = mycursor.fetchall()
    list_of_categories_id = []
    
    for rows in myresult:
        otp_code = rows[0]  #urutan pada db
        code = rows[1]
        l.client.headers['Authorization'] = "Bearer " + rows[0] 
        l.client.headers['Accept'] = "application/json"
        l.client.headers['x-Timezone'] = timezone
        response = l.client.get("/api/v1/quotes/self-reminders") 
        json_response_dict = response.json()
        if json_response_dict['code'] != 200:
            raise FlowException('comment not created') 
    
def landingPageGetTopUstad(l):
    l.client.headers['Accept'] = "application/json"
    l.client.get("/api/v1/landing/ustads")
    
def landingPageRandomSelfReminder(l):
    l.client.headers['Accept'] = "application/json"
    l.client.get("/api/v1/landing/self-reminders")    


class UserBehavior(TaskSet):
    tasks = {sholatTime:1, landingPageGetTopUstad:2, landingPageRandomSelfReminder:2, 
                consultationOnGoing:1, consultationUstadList:1, storeItemList:1, storeItemListGroup:1,
                SelfReminderCategoryList:1,SelfReminderCategoryChoose:1,SelfReminderList:1 }
    #tasks = {register:1, signin: 3, profile: 1}

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000