import csv
import sys
import os

file_path = os.path.dirname(__file__) 
word_file = file_path + '/keyword.csv'
word_file2 =file_path + '/keyword2.csv'
word_file3 = file_path + '/keyword3.csv'

output_file = file_path + '/suttle.csv'

with open(output_file, mode='w',newline='', encoding='utf-8') as f_out:
    with open(word_file, mode='r', encoding='utf-8') as f1:
        reader1 = csv.reader(f1)
        for i2, row2 in enumerate(reader1):
            word2 = str(row2[0])
            with open(word_file2, mode='r', encoding='utf-8') as f2:
                reader2 = csv.reader(f2)
                for i, row in enumerate(reader2):
                    word = word2 +' '+ str(row[0])

                    with open(word_file3, mode="r", encoding="utf-8") as qf:
                        qreader = csv.reader(qf)
                        for j, qrow in enumerate(qreader):
                            q = word + ' ' + qrow[0] + ',5\n'
                            f_out.write(q)
