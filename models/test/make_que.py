import csv
import sys
import os

file_path = os.path.dirname(__file__) 
word_file = file_path + '/keyword.csv'
word_file2=file_path + '/keyword2.csv'
sent_file = file_path + '/주문조합.csv'

output_file = file_path + '/train_data.csv'

with open(output_file, mode='w',newline='', encoding='utf-8') as f_out:
    with open(word_file2, mode='r', encoding='utf-8') as f2:
        reader2 = csv.reader(f2)
        for i2, row2 in enumerate(reader2):
            word2 = str(row2[0])
            with open(word_file, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    word = word2 +' '+ str(row[0])

                    with open(sent_file, mode="r", encoding="utf-8") as qf:
                        qreader = csv.reader(qf)
                        for j, qrow in enumerate(qreader):
                            q = word + ' ' + qrow[0] + ',4\n'
                            f_out.write(q)
