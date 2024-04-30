import csv
from random import  *
from konlpy.tag import Komoran
import sys
import os
file_path = os.path.dirname(__file__) 
sys.path.append(file_path+'../../../')
from utils.Preprocess import Preprocess

sent_file = file_path +'/cnnTraindata.csv'

pre = Preprocess(word2index_dic=file_path + '/../../train_tools/dict/chatbot_dict.bin',
               userdic=file_path + '/../../utils/user_dict.txt')

file = open(file_path + "/corpus_ner.txt", 'w',encoding='utf-8')


with open(sent_file, mode="r", encoding='utf-8') as qf:
    qreader = csv.reader(qf)
    for qi, qrow in enumerate(qreader):
        
        sentence = []
        
        q = qrow[0]
        q = q.replace('\ufeff', '')
        pos = pre.pos(q)
        for p in pos:
            x = (p[0], 'O', p[1])
            sentence.append(x)
        

        # 파일 저장
        raw_q = ""
        for i, s in enumerate(sentence):
            raw_q += "{} ".format(s[0])

        raw_q = "{}\t{}\t{}".format('0000', raw_q, 0)
        print(raw_q)
        file.write(raw_q + "\n")

file.close()