from locust import HttpLocust, TaskSet
import random
import string
import mysql.connector

def randomString(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return  ''.join(random.choice(letters) for i in range(string_length))
#ini me-random 
def randomNumber(number_length=12):
    return ''.join(str(random.randint(1,9)) for j in range(number_length))

def requestOTP(l):
    l.client.headers['Content-Type'] = "application/x-www-form-urlencoded"
    l.client.headers['Accept'] = "application/json"
    l.client.post("/v1/oauth/provider/login",
    {"provider":"sms",
    "response_type":"otp_code",
    "scope":"free",
    "phone_number":"",
    "calling_code":"+62",
    "client_id":"5d8218f2f48c3d6b94645142",
    "client_id":"client1id"
    })

def register(l):
    mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="admin",
    passwd="password",
    database="aminin_testing"
    )

    mycursor = mydb.cursor()
    num_loop = 10
    provider = "sms"
    response_type="otp_code"
    client_id = "5d8218f2f48c3d6b94645142"
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
        people['phone_number'] = str(randomNumber(12))
        peoples[k] = people
        l.client.headers['Content-Type'] = "application/x-www-form-urlencoded"
        response =  l.client.post("/v1/oauth/otp/register",
                                        {"name":people['name'],
                                        "email":people['email'],
                                        "calling_code":people['calling_code'],
                                        "phone_number":people['phone_number'],
                                        "state":people['state'],
                                        "client_id":client_id,
                                        "state":state,
                                        "scope":scope,
                                        "provider":provider,
                                        "response_type":response_type
                                        })
        #insert to users
        sql_insert_user = "INSERT INTO users (email,name,calling_code,phone_number) VALUES (%s, %s, %s, %s)"
        val_insert_user = (people['email'], people['name'],people['calling_code'],people['phone_number'])
        mycursor.execute(sql_insert_user, val_insert_user)
        #get token from response
        json_response_dict = response.json()
        token = json_response_dict['data']['oauth']['access_token']
        #insert to login
        sql_insert_login = "INSERT INTO login (email,token) VALUES (%s, %s)"
        val_insert_login = (people['email'], token)
        mycursor.execute(sql_insert_login, val_insert_login)
        
    mydb.commit()

def signin(l):
    mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="admin",
    passwd="password",
    database="locust_log"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT email,password FROM users  order by rand()limit 1")
    myresult = mycursor.fetchall()
    
    for rows in myresult:
        email = rows[0]  #urutan pada db
        password = rows[1]
        l.client.headers['Content-Type'] = "application/x-www-form-urlencoded"
        response =  l.client.post("/api/v3/signin",{
                                        "username":email,
                                        "password":password,
                                        "grant_type":"password",
                                        "client_secret":"client1secret",
                                        "client_id":"client1id"})
        #get token from response
        json_response_dict = response.json()
        token = json_response_dict['data']['oauth']['access_token']
        #insert to login
        sql_insert_login = "INSERT INTO login (email,token) VALUES (%s, %s)"
        val_insert_login = (email, token)
        mycursor.execute(sql_insert_login, val_insert_login)

    mydb.commit()

def logout(l):
    l.client.post("/api/v3/signout", {"username":"system", "password":"systembahaso"})

def index(l):
    l.client.get("/")

def profile(l):
    l.client.get("/profile")

class UserBehavior(TaskSet):
    tasks = {register:1, signin: 3, profile: 1}

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000