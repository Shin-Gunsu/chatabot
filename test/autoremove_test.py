import os
import time

# 파일 생성
filename = f"./utils/cookietxt/test.txt"
with open(filename, 'w') as f:
    f.write("이 파일은 30초 후에 자동으로 삭제됩니다.")

print(f"{filename} 생성 완료. 30초 후 자동 삭제됩니다.")

# 30초 대기
time.sleep(30)

# 파일 삭제
os.remove(filename)
print(f"{filename} 삭제 완료.")
