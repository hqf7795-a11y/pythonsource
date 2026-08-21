# csv 파일의 내용을 테이블에 insert 하기 (단, 테이블이 비어 있는 경우만 삽입)

# 테이블의 내용을 읽어서 무작위로 추출 후 문제 내기
# Question #1 : 'apple' 뜻은?
# 1.버스
# 2.남편
# 3.수줍은
# 4.사과


# 문제 내고 meaning이 맞으면 정답처리 , 정답 개수 세기.

# 결과 : 3/5 correct

# 결과를 테이블에 저장
# total, correct,regdate

import oracledb
import random
from datetime import datetime
import csv

conn = oracledb.connect(user="PYTHON_USER",password="54321",dsn="localhost/XE")
cursor = conn.cursor()

def load_words_from_csv(path="./words.csv"):
    '''csv 파일을 읽어서 튜플 리스트로 반환'''
    pairs = []
    with open(path,"r",encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pairs.append((row['word'].strip(),row.get('meaning').strip())) # 튜플로 뽑으려고 ()괄호로 감싼거임
    return pairs



def seed_words_if_empty():
    '''words 테이블이 비어있으면 csv 파일 내용을 읽어서 넣기'''
    cursor.execute("select count(*) from words") #셀렉트구문으로 비어있는지 먼저 확인하기
    count = cursor.fetchone()[0]
    if count > 0:
        return
    
    pairs = load_words_from_csv()  # [(wife , 아내),(apple, 사과)]  
    sql = "insert into words(word,meaning) values(:1,:2)" # 인서트구문
    cursor.executemany(sql,pairs)
    conn.commit()

    print(f"csv 단어 데이터 {cursor.rowcount}개를 등록했습니다.\n")


    

def run_quiz():
    '''
    1) all_words = words 테이블 읽기
    2) 무작위로 5문제 추출 random.sample()
    3) all_words 문제를 제외한내용을 섞은 후 거기서 틀린 meaning 추출(3개)
        문제 출제 apple 사과 + meaning => 보기출제
    4) 답변 입력받은 후 정답 맞는지 확인
    5) 최종 결과 입력

    '''
    cursor.execute("select word, meaning from words") # 1번
    all_words = cursor.fetchall()

    correct = 0 # 정답 개수
    total = 5   # 문제 개수

    question = random.sample(all_words, 5) # 2번

    
    for idx, (word,meaning) in enumerate(question, start=1):  # 이너머레이트 = 목록을 받아와서 인덱스를 먹인다. start는 인덱스를 1부터 시작하도록 지정한 것
        # distractors = []
        # for w, m in all_words:
        #     if w!=word:
        #         distractors.append(m)
        distractors = [m for w, m in all_words if w!=word] # 리스트컴프리핸션으로 더 간단하게
        random.shuffle(distractors) # 차례대로 담아두었으니 섞기
        # 보기 생성
        choices = distractors [:3] + [meaning] # 섞은거에서 3개 가져오기 + 정답
        random.shuffle(choices) # 위의 초이스에 담는 과정에서 meaning(정답)이 항상 4번으로 들어오게 고정되어있다. 이것을 섞은 것

        print(f"Question {idx} : {word}의 뜻은?") # 문제 출제 idx = 퀘스천 번호, word = 문제
        for i, c in enumerate(choices, start = 1): # i = 인덱스 변수 , c = 초이스에서 가져올 변수
            print(f" {i}. {c}")

        print(f"결과 : {correct} / {total} 정답 \n")
        sql = "insert into quiz_record(total,correct,reg_date) values(:1,:2, sysdate)"
        cursor.execute(sql,(total,correct))
        conn.commit # 결과 저장

        # 정답 입력받기
        answer = input("정답 번호 입력: ").strip()

        try:
            selected = choices[int(answer) -1] #answer에서 input을 받으면 str이기 때문에 answer과 meaning을 비교하려면 int로 변환해야한다, 또한 인덱스를 -1 해야한다. 이너머레이트로 시작 번호를 1로 지정했기 때문이다.
        except:
            selected = None


        # 사용자가 입력한 답변과 정답 비교
        if selected == meaning:
            print("Pass~~\n")
            correct += 1
        else:
            print(f"zz {meaning}\n")





    

    
if __name__ == "__main__":
    try:
        seed_words_if_empty()
        run_quiz()
    finally:
        cursor.close()
        conn.close()