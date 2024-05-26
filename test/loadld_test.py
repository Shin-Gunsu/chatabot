import sys
import os
file_path = os.path.dirname(__file__)  # 현재 파일의 절대 경로를 가져옵니다.
sys.path.append(file_path+'../../')
from utils.LoadLectureData import LoadLectureData

lld = LoadLectureData()

#print(lld.searchLectureForName('정전기공학특론'))
#print(lld.getLectureForCode("270017-01"))
#for i in lld.searchCategorieForName('기계공학과'):
    #print(type(i))
    #print(i)
cnt=0
for i in lld.searchCategorieForName('기계공학과'):
    #print(i['courses'])
    for j in lld.getLectureForCode(i['courses']):
        for k in j:
            cnt+=1
            print(cnt, type(k))
#print(lld.searchCategorieForName('기계공학과'))

#for i in lld.getLectureForCode(['110007-01', '110008-05', '110008-15', '120086-01', '150097-01', '260025-01', '260028-01']):
    #print(i)