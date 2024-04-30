import csv

# 입력 파일 경로
input_file = 'major_ner.csv'

# 출력 파일 경로
output_file = 'major.csv'

# 출력 파일 열기 (쓰기 모드)
with open(output_file, mode='w', encoding='utf-8') as f_out:
    # CSV 쓰기 객체 생성
    csv_writer = csv.writer(f_out)

    # 입력 파일 열기 (읽기 모드)
    with open(input_file, mode='r', encoding='utf-8') as f_in:
        # CSV 읽기 객체 생성
        csv_reader = csv.reader(f_in)

        # 각 행마다 처리
        for row in csv_reader:
            # 위치 정보 추출
            location = row[0].split(':')[0]

            # 태그 추가
            location_tag = f"{location}:B_MAJOR"

            # CSV 파일에 쓰기
            csv_writer.writerow([location_tag])