import requests
from http.cookiejar import LWPCookieJar




class LoginMakeCookie:
    def __init__(self, user_id, user_pw):
        self.user_id = user_id
        self.user_pw = user_pw
        self.login_data = {
                    "anchor": "",
                    "id": "EL2",
                    "RelayState": "/local/sso/index.php",
                    "user_id": self.user_id,
                    "user_password": self.user_pw
                }
        self.headers = {'Referer': 'https://el2.koreatech.ac.kr/' }
        self.login_url = "https://tsso.koreatech.ac.kr/svc/tk/Login.do"
        self.callback_url = ""

    
    def makeCookie(self):
        filename = f"./utils/cookietxt/{self.user_id}.txt"
        session = requests.Session()

        session.cookies = LWPCookieJar(filename)

        try:
            session.cookies.load(ignore_discard=True)
        except FileNotFoundError:
        # If the cookie file does not exist, it will be created upon saving
            pass

        response = session.post(self.login_url, data=self.login_data, headers=self.headers)
        #print(response.text)
        session.cookies.save(ignore_discard=True)

        self.callback_url = response.url

        session.close()

        return response #el페이지 HOST 응답

    def isLogin(self):
        if "login.php" in self.callback_url:
            return False

        else:
            return True
        