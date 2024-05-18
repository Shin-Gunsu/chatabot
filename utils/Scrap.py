import requests
from http.cookiejar import LWPCookieJar
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os.path
from os import path

class Scrap:
    def scrapEmail(self, user_id):
        myEmail = ""
        filename = f"./utils/cookietxt/{user_id}.txt"
        session = requests.Session()

        session.cookies = LWPCookieJar(filename)
        try:
            session.cookies.load(ignore_discard=True)
        except FileNotFoundError:
        # If the cookie file does not exist, it will be created upon saving
            pass
        response = session.post("https://el2.koreatech.ac.kr/user/profile.php")
        soup = BeautifulSoup(response.text, 'lxml')

        cards = soup.select('.card-body')
        for card in cards:
            if card.select('.editprofile'):
                myEmail = card.select_one('dd').text.strip()

        return myEmail

    def scrapStudentNumber(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        target_elements = soup.select('.oklassur-theme .cursor-pointer')
        studentinfo = ""
        for element in target_elements:
            nested_div = element.find('div', class_='d-inline-flex align-items-center')
            if nested_div:
                mr_2_div = nested_div.find_next('div', class_='mr-2')
                if mr_2_div:
                    
                    studentinfo = mr_2_div.text.strip()
        return studentinfo
    def handleNomenu(self, corner):
        if corner == "":
            return "미운영"
        else:
            return corner
    def scrapMenu(self):
        session = requests.Session()
        response = session.get("https://coop.koreatech.ac.kr/dining/menu.php")
        response.encoding = "euc-kr"
        soup = BeautifulSoup(response.text, 'html.parser')

        allcornermenus = []
        
        #아침 메뉴 가져오기(질문시각: 0~9시)
        if 0 <= datetime.today().hour < 10:
            tr_morning = soup.find_all('tr')[4]
            tds = tr_morning.find_all('td')
            a_corner = tds[1].text.strip()
            a_corner = "★아침★\n"+"========================\n"+"A코너: \n" + a_corner
            b_corner = tds[2].text.strip()
            b_corner = "\nB코너: \n" + b_corner
            c_corner = tds[3].text.strip()
            c_corner = "\nC코너: \n" + c_corner
            n_corner = tds[5].text.strip()
            n_corner = "\n능수관: \n" + n_corner+"\n========================"+"\n\n<전체 메뉴 보러가기>\n"
            allcornermenus = [a_corner, b_corner, c_corner, n_corner]
        #점심 메뉴 가져오기(질문시각: 10~14시)
        elif 10 <= datetime.today().hour < 15:
            tr_lunch = soup.find_all('tr')[5]
            tds = tr_lunch.find_all('td')
            a_corner = tds[1].text.strip()
            a_corner = "★점심★\n"+"========================\n"+"A코너: \n" + self.handleNomenu(a_corner)
            b_corner = tds[2].text.strip()
            b_corner = "\nB코너: \n" + self.handleNomenu(b_corner)
            c_corner = tds[3].text.strip()
            c_corner = "\nC코너: \n" + self.handleNomenu(c_corner)
            n_corner = tds[5].text.strip()
            n_corner = "\n능수관: \n" + self.handleNomenu(n_corner)+"\n========================"+"\n\n<전체 메뉴 보러가기>"
            allcornermenus = [a_corner, b_corner, c_corner, n_corner]
        #저녁 메뉴 가져오기(질문시각: 15~23시)
        elif 15 <= datetime.today().hour <= 23:
            tr_dinner = soup.find_all('tr')[6]
            tds = tr_dinner.find_all('td')
            a_corner = tds[1].text.strip()
            a_corner = "★저녁★\n"+"========================\n"+"A코너: \n" + a_corner
            b_corner = tds[2].text.strip()
            b_corner = "\nB코너: \n" + b_corner
            c_corner = tds[3].text.strip()
            c_corner = "\nC코너: \n" + c_corner
            n_corner = tds[5].text.strip()
            n_corner = "\n능수관: \n" + n_corner+"\n========================"+"\n\n<전체 메뉴 보러가기>\n"
            allcornermenus = [a_corner, b_corner, c_corner, n_corner]
        
        session.close()
        return allcornermenus #물어본 시점(아침/점심/저녁)의 A코너, B코너, C코너, 능수관 메뉴 반환
    
    def scrapHW(self, response):
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
                myHW.append(f"과목: {subject}\n과제명 : {name}\n마감일 : {date}\n")
        return myHW
    
    def scrapCourseHistory(self, user_id, start_year):
        myCourseHistory = []
        filename = f"./utils/cookietxt/{user_id}.txt"
        session = requests.Session()

        session.cookies = LWPCookieJar(filename)
        try:
            session.cookies.load(ignore_discard=True)
        except FileNotFoundError:
        # If the cookie file does not exist, it will be created upon saving
            pass
        for year in range(start_year,(datetime.today().year)+1):
            for semester in [10, 11, 20, 21]:
                response = session.post(f"https://el2.koreatech.ac.kr/local/lmscourse/index.php?year={year}&semester={semester}")
                soup = BeautifulSoup(response.text, 'lxml')

                courses = soup.select('.border-top')
                for course in courses:
                    if course.select('.courseprofessor'):
                        if "교수: " in course.select_one('.courseprofessor').text:
                            myCourseHistory.append(course.select_one('.coursefullname').text)
        
        return myCourseHistory






        

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