from gensim.models import FastText
import numpy as np
import os
import sys

file_path = os.path.dirname(__file__)  # 현재 파일의 절대 경로를 가져옵니다.
sys.path.append(file_path+'../../../')
from utils.Scrap import Scrap
from utils.LoadLectureData import LoadLectureData

class Recommender:
    def __init__(self, lecture_dic_path, model_path):
        with open(lecture_dic_path, 'r', encoding='utf8') as file:
            lecture_dic = {}
            for line in file:
                key, value = line.strip().split(' ', 1)
                value = value.split()
                lecture_dic[key] = value
        self.lecture_dic = lecture_dic
        self.model = FastText.load(model_path)
        self.length = len(self.lecture_dic)      
    
    def get_list_vector(self, list_input):
        list_vector = np.mean([self.model.wv[word] for word in list_input if word in self.model.wv], axis=0)
        return list_vector
    
    def get_input_list(self, host_response, user_id):
        studentnumscrap = Scrap()
        r = studentnumscrap.scrapStudentNumber(host_response)
        start_year = ''.join(filter(str.isdigit, r))[:4]
        coursehistoryscrap = Scrap()
        chlist = coursehistoryscrap.scrapCourseHistory(user_id, int(start_year))
        loader = LoadLectureData()
        code_list = []

        for i in chlist:
            name = i.split('(')[0]
            code = loader.getCode(name)
            if len(code) > 0:
                code_list.append(code.split('-')[0])
            else:
                continue
        result = []
        for code in code_list:
            if code in self.lecture_dic:
                result += self.lecture_dic[code]
        print(code_list)
        return result


    def find_similar_list(self, input_list, top_n):
        input_vector = self.get_list_vector(input_list)
        similarities = {}
        for key, lst in self.lecture_dic.items():
            list_vector = self.get_list_vector(lst)
            similarity = np.dot(input_vector, list_vector) / (np.linalg.norm(input_vector) * np.linalg.norm(list_vector))
            similarities[key] = (lst, similarity)
        top_similarities = sorted(similarities.items(), key=lambda x: x[1][1], reverse=True)[:top_n]
        aa = [item[0] for item in list(top_similarities)]
        
        return aa
    
#a = Recommaender(file_path + '\\lecture_dic.txt', file_path + '\\lecture_model.bin')