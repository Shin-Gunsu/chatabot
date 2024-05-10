import requests
from http.cookiejar import LWPCookieJar
from bs4 import BeautifulSoup
from datetime import datetime
import json

class LoginScrap:
    def __init__(self, user_id, user_pw, year):
        self.user_id = user_id
        self.user_pw = user_pw
        self.year = year
        self.login_data = {
                            "anchor": "",
                            "id": "EL2",
                            "RelayState": "/local/sso/index.php",
                            "user_id": self.user_id,
                            "user_password": self.user_pw
                        }
        self.headers = {'Referer': 'https://el2.koreatech.ac.kr/' }
        self.login_url = "https://tsso.koreatech.ac.kr/svc/tk/Login.do"

    def scrapHW(self):
        filename = f"./utils/cookietxt/{self.user_id}.txt"

        session = requests.Session()

        session.cookies = LWPCookieJar(filename)

        try:
            session.cookies.load(ignore_discard=True)
        except FileNotFoundError:
        # If the cookie file does not exist, it will be created upon saving
            pass

        response = session.post(self.login_url, data=self.login_data, headers=self.headers)

        session.cookies.save(ignore_discard=True)

        callback_url = response.url

        if "login.php" in callback_url:
            print("로그인 실패")
            return 0

        else:
            print("로그인 성공")
        
        session.close()
        myHW = []
        #과제 가져오기
        soup = BeautifulSoup(response.text, 'lxml')
        target_element = soup.select('.oklassur-theme.oklassur-skin01 .bg-light')
        for todo in target_element:
            if todo.select_one('a div:nth-child(1)'):
                # 마감일
                date = todo.select_one('a div:nth-child(1)').text.replace("Due : ","")
                # 과목명
                subject= todo.select_one('a div:nth-child(2)').text
                # 과제명
                name = " ".join(todo.select_one('a div:nth-child(3)').text.strip().split(" ")[0:-2])
                myHW.append(f"과목: {subject} / 과제명 : {name} / 마감일 : {date}")
        return myHW





        

'''


# Setup user-specific variables
userid = "june573166"
password = "rlaalswns9!"
start_year = 2019

data = {
    "anchor": "",
    "id": "EL2",
    "RelayState": "/local/sso/index.php",
    "user_id": userid,
    "user_password": password
}

# Define the filename for cookie persistence based on the user ID
filename = f"./cookie_data/{userid}.txt"

# Initialize a session object
session = requests.Session()

# Setup cookie jar to handle cookies; this will load and save cookies to/from the file
session.cookies = LWPCookieJar(filename)
try:
    session.cookies.load(ignore_discard=True)
except FileNotFoundError:
    # If the cookie file does not exist, it will be created upon saving
    pass

# Set headers with a referrer
headers = {
    'Referer': 'https://el2.koreatech.ac.kr/'
}

# URL for the login
login_url = "https://tsso.koreatech.ac.kr/svc/tk/Login.do"

# Perform the POST request
response = session.post(login_url, data=data, headers=headers)

# Save cookies to the file after login
session.cookies.save(ignore_discard=True)

callback_url = response.url
print(callback_url)
# Check if there was an error with the request (Fail on error)
if "login.php" in callback_url:
    print("로그인 실패")

else:
    print("로그인 성공")


# 과제 가져오기
print("\n\n\n\n현재 과재")

soup = BeautifulSoup(response.text, 'lxml')
target_element = soup.select('.oklassur-theme.oklassur-skin01 .bg-light')
for todo in target_element:
    if todo.select_one('a div:nth-child(1)'):
        # 마감일
        date = todo.select_one('a div:nth-child(1)').text.replace("Due : ","")
        # 과목명
        subject= todo.select_one('a div:nth-child(2)').text
        # 과제명
        name = " ".join(todo.select_one('a div:nth-child(3)').text.strip().split(" ")[0:-2])
        print(f"과목: {subject} / 과제명 : {name} / 마감일 : {date}")


# 지금까지 수강한 과목 가져오기
print("\n\n\n\n지금까지 수강한 과목")
for year in range(start_year,datetime.today().year):
    for semester in [10,20]:
        response = session.post(f"https://el2.koreatech.ac.kr/local/lmscourse/index.php?year={year}&semester={semester}")
        soup = BeautifulSoup(response.text, 'lxml')

        courses = soup.select('.border-top')
        for course in courses:
            if course.select('.courseprofessor'):
                if "교수: " in course.select_one('.courseprofessor').text:
                    print(course.select_one('.coursefullname').text)

# Close session
session.close()'''