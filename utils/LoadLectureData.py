import json
import os

class LoadLectureData:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir) 
        json_file_path = os.path.join(parent_dir, 'exported2.json')
        self.json_data = {}

        with open(json_file_path, 'r', encoding='utf-8') as file:
            self.json_data = json.load(file)

        self.major_categories = [{
            'name': category['name'],
            'courses': category['lect_code_list'],
        } for category in self.json_data['department']]

        self.lecture_dic = self.json_data['lecture']['list']
        self.lecture_list = [lecture for lecture in self.lecture_dic.values()]

    def searchCategorieForName(self, name):
        result = []
        lecture_code_list = [i for i in self.major_categories if i['name'] == name]
        #for code in lecture_code_list['courses']:
            #if self.lecture_dic.__contains__(code):
                #result.append(self.lecture_dic[code])
        return lecture_code_list if len(lecture_code_list) > 0 else []
    
    def getLectureForCode(self, code_list):
        lecture_list = []
        
        for code in code_list:
            if self.lecture_dic.__contains__(code):
                lecture_list.append(self.lecture_dic[code])

        return lecture_list
    
    def searchLectureForName(self, name):
        lecture_list = [lecture for lecture in self.lecture_list if lecture[1].__contains__(name)]
        return lecture_list
    
    def getLectureList(self, page, interval = 10):
        start = (page - 1) * interval 
        end = page * interval if page * interval < len(self.lecture_list) else len(self.lecture_list)
        return self.lecture_list[start:end] if start < len(self.lecture_list) else []
    
    def getMaxPage(self, interval = 10):
        # int형 조건 걸어줘야하는데 일단 귀찮
        return len(self.lecture_list) / interval
    
    def getDepartmentList(self, department):
        result = []
        for i in self.searchCategorieForName(department):
            for j in self.getLectureForCode(i['courses']):
                result.append(j)
        return result
    
    def getCode(self, name):
        for lecture in self.lecture_list:
            if lecture[1] == name:
                return lecture[0]
        return ""