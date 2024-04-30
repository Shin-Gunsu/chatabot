import csv
import sys
import os

file_path = os.path.dirname(__file__)  # 현재 파일의 절대 경로를 가져옵니다.
sys.path.append(file_path+'../../../')
from utils.Preprocess import Preprocess
from random import  *

sent_file = file_path + '/주문조합.csv'

pre = Preprocess(word2index_dic=file_path + '/../../train_tools/dict/chatbot_dict.bin',
               userdic=file_path + '/../../utils/user_dict.txt')

file = open(file_path + "/output_ner_train.txt", 'w',encoding='utf-8')

file_list = [file_path + '/club.csv', file_path + '/loc.csv',file_path + '/major.csv',file_path + '/org.csv']

for fl in file_list:
    
    with open(fl, mode='r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)

        for i, row in enumerate(reader):

            with open(sent_file, mode="r", encoding="utf-8") as qf:
                qreader = csv.reader(qf)
                for qi, qrow in enumerate(qreader):
                
                    sentence = []
                    word = row[0].split(':')
                    sentence.append(tuple(word))

                    q = qrow[0]
                    q = q.replace('\ufeff', '')
                    pos = pre.pos(q)
                    for p in pos:
                        x = (p[0], 'O', p[1])
                        sentence.append(x)
                    


                    # 파일 저장
                    raw_q = ";"
                    res_q = '$'
                    line = ""
                    for i, s in enumerate(sentence):
                        raw_q += "{} ".format(s[0])
                        res_q += "{} ".format(s[0])
                        if s[1] == 'B_CLUB':
                            line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0], 'NNG', s[1])
                        elif s[1] == 'B_LEC':
                            line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0], 'NNG', s[1])
                        elif s[1] == 'B_LOC':
                            line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0], 'NNG', s[1])
                        elif s[1] == 'B_ORG':
                            line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0], 'NNG', s[1])
                        elif s[1] == 'B_MAJOR':
                            line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0], 'NNG', s[1])
                        else:
                            line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0], s[2], s[1])

                    print(raw_q)
                    print(res_q)
                    print(line)
                    file.write(raw_q + "\n")
                    file.write(res_q + "\n")
                    file.write(line + "\n")

for fl in file_list:
    
    with open(fl, mode='r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)

        ran = randint(0,3)
        for i, row in enumerate(reader):

            with open(file_list[ran], mode='r', encoding='utf-8-sig') as df:
                dreader = csv.reader(df)
                for di, drow in enumerate(dreader):

                    with open(sent_file, mode="r", encoding="utf-8") as qf:
                        qreader = csv.reader(qf)
                        for qi, qrow in enumerate(qreader):
                        
                            sentence = []

                            word = row[0].split(':')
                            sentence.append(tuple(word))

                            dword = drow[0].split(':')
                            sentence.append(tuple(dword))

                            q = qrow[0]
                            q = q.replace('\ufeff', '')
                            pos = pre.pos(q)
                            for p in pos:
                                x = (p[0], 'O', p[1])
                                sentence.append(x)



                            # 파일 저장
                            raw_q = ";"
                            res_q = '$'
                            line = ""
                            for i, s in enumerate(sentence):
                                raw_q += "{} ".format(s[0])
                                res_q += "{} ".format(s[0])
                                if s[1] == 'B_CLUB':
                                    line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0], 'NNG', s[1])
                                elif s[1] == 'B_LEC':
                                    line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0], 'NNG', s[1])
                                elif s[1] == 'B_LOC':
                                    line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0], 'NNG', s[1])
                                elif s[1] == 'B_ORG':
                                    line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0], 'NNG', s[1])
                                elif s[1] == 'B_MAJOR':
                                    line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0], 'NNG', s[1])
                                else:
                                    line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0], s[2], s[1])

                            print(raw_q)
                            print(res_q)
                            print(line)
                            file.write(raw_q + "\n")
                            file.write(res_q + "\n")
                            file.write(line + "\n")

        

file.close()