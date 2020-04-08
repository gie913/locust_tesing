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
CONST_CLIENT_ID = config.get('ClientSection', 'client.id')
CONST_CLIENT_SECRET = config.get('ClientSection', 'client.secret')


def randomString(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return  ''.join(random.choice(letters) for i in range(string_length))
#ini me-random 
def randomNumber(number_length=12):
    return ''.join(str(random.randint(1,9)) for j in range(number_length))

def requestOTP(l):
    mydb = mysql.connector.connect(
    host= CONST_HOST,
    user= CONST_USER,
    passwd= CONST_PSWD,
    database= CONST_DTBS
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT calling_code,phone_number FROM users  order by rand()limit 1")
    myresult = mycursor.fetchall()
    
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
        "client_id":CONST_CLIENT_ID,
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
    

def register(l):
    mydb = mysql.connector.connect(
    host= CONST_HOST,
    user= CONST_USER,
    passwd= CONST_PSWD,
    database= CONST_DTBS
    )

    mycursor = mydb.cursor()
    num_loop = 1
    provider = "sms"
    response_type="otp_code"
    client_id = CONST_CLIENT_ID
    state= "Indonesia"
    scope="free"
    calling_code = "+62"
   
    #sebagai struct / dictionaries
    peoples = {}
    for k in range(num_loop):
        # print "Perulangan ke-"+str(k)
        # random.seed(k)
        people = {}
        random_string_firstname = randomString(10)
        people['name'] = str(random_string_firstname)
        people['email'] = str(random_string_firstname)+str(k)+'@test.com'
        people['phone_number'] = str(randomNumber(10))
        peoples[k] = people
        l.client.headers['Content-Type'] = "application/x-www-form-urlencoded"
        response =  l.client.post("/api/v1/oauth/otp/register",
                                        {"name":people['name'],
                                        "email":people['email'],
                                        "calling_code":calling_code,
                                        "phone_number":people['phone_number'],
                                        "state":state,
                                        "client_id":client_id,
                                        "state":state,
                                        "scope":scope,
                                        "provider":provider,
                                        "response_type":response_type
                                        })
        #insert to users
        sql_insert_user = "INSERT INTO users (email,name,calling_code,phone_number) VALUES (%s, %s, %s, %s)"
        val_insert_user = (people['email'], people['name'],calling_code,people['phone_number'])
        mycursor.execute(sql_insert_user, val_insert_user)
        #get token from response
        json_response_dict = response.json()
        code = json_response_dict['result']['code']
        otp_code= json_response_dict['result']['otp_code']
        #insert to otp
        sql_insert_login = "INSERT INTO otp (code,otp_code) VALUES (%s, %s)"
        val_insert_login = (code, otp_code)
        mycursor.execute(sql_insert_login, val_insert_login)
        
    mydb.commit()


def validateOTP(l):
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
        otp_code = rows[0]  #urutan pada db
        code = rows[1]
        l.client.headers['Content-Type'] = "application/x-www-form-urlencoded"
        l.client.headers['Accept'] = "application/json"
        response = l.client.post("/api/v1/oauth/otp/validate",
        {"grant_type":"authorization_otp_code",
        "otp_code":code, #ini memang tertukar
        "otp":otp_code,
        "client_id":CONST_CLIENT_ID,
        "client_secret":CONST_CLIENT_SECRET
        }) 
        json_response_dict = response.json()
        email = json_response_dict['result']['user']['email']
        access_token= json_response_dict['result']['oauth']['access_token']
        #insert to otp
        sql_insert_login = "INSERT INTO token (email,access_token) VALUES (%s, %s)"
        val_insert_login = (email, access_token)
        mycursor.execute(sql_insert_login, val_insert_login)

    mydb.commit()
    


def logout(l):
    l.client.get("/api/v1/signout")

def index(l):
    l.client.get("/")

def profile(l):
    l.client.get("/profile")

class UserBehavior(TaskSet):
    tasks = {register:2, requestOTP:1, validateOTP:1}
    #tasks = {register:1, signin: 3, profile: 1}

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
