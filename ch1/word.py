# 영어타자 프로그램
import time
import random

# word.txt 읽어서
words = []
with open("./ch1/data/word.txt","r",encoding="utf-8") as f:
    for word in f:
        words.append(word.strip())

# print(words)
start = time.time()

# n : 반복횟수 카운트, corr_cnt : 정답 개수 카운트
n, corr_cnt = 1, 0

while n <= 5:
    # 섞는다 random.shuffle()
    random.shuffle(words)
    # 임의로 하나 추출 random.choice()
    q = random.choice(words)
    # 문제 5문제 출제
    # 정답 개수
    # Q1) then
    print(f"Q{n}")
    print(q)
    # input()
    answer = input()
    # input 결과에 따라 정답!! or 오타!!
    if answer.strip() == q.strip():
        print("정답!!")
        corr_cnt += 1
    else:
        print("오타!!")

    # 문제 개수 추가
    n += 1

# 끝난시간
end = time.time()

# 게임시간 출력
et = end - start
et = format(et, ".3f")

# 출력문 => 게임시간 : 10초, 정답개수 : 3개
print(f"게임시간 : {et}초, 정답개수 : {corr_cnt}개")
# 3개이상 정답인 경우 합격 or 불합격
if corr_cnt >= 3:
    print("합격")
else:
    print("불합격") 