import sys
import os
file_path = os.path.dirname(__file__)  # 현재 파일의 절대 경로를 가져옵니다.
sys.path.append(file_path+'../../')
from utils.LoginScrap import LoginScrap

hwscrap = LoginScrap("june573166", "rlaalswns9!", 0)
r = hwscrap.scrapHW()
for i in r:
    print(i)

