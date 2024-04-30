import csv
import sys
import os
file_path = os.path.dirname(__file__)  # 현재 파일의 절대 경로를 가져옵니다.

file = file_path + '/../ner/ner_train.txt'

# 학습 파일 불러오기
def read_file(file_name):
    sents = []
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for idx, l in enumerate(lines):
            if l[0] == ';' and lines[idx + 1][0] == '$':
                l = l.replace('; ', '')
                l = l.replace('\n', '')
                sents.append(l)
            else:
                continue
    return sents



corpus = read_file(file)
file = open(file_path + "/corpus_userdict.txt", 'w',encoding='utf-8')
for c in corpus:
    c = "{}\t{}\t{}\n".format('0000', c, 0)
    file.write(c)
file.close()