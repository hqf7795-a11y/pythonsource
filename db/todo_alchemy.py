# ==== Todo 관리 ====
# 1. 추가. 2. 목록 3. 완료처리 4. 삭제 5. 종료
# 선택 : 1
# 할 일 내용을 입력하세요: 내용입력...
# 등록되었습니다.
# ==== Todo 관리 ====
# 1. 추가. 2. 목록 3. 완료처리 4. 삭제 5. 종료
# 선택 : 2
# ---------------------
# 1. [미완료] 강아지 목욕(2026-08-20 12:38:07)
# 선택 : 3
# 완료 처리할 일 번호를 입력하세요 : 1
# 완료 처리되었습니다.
# ==== Todo 관리 ====
# 1. 추가. 2. 목록 3. 완료처리 4. 삭제 5. 종료
# 선택 : 4
# 삭제 처리할 일 번호를 입력하세요: 1
# 삭제 처리되었습니다.

# 데이터베이스 테이블 구조
# todo_id 자동증가,pk
# title not null
# is_done number(1) default 0
# crated_at 작성일자 sysdate

import datetime
from random import choice
from typing import Optional, final

import oracledb
#  엔진 구문


# 테이블 생성 > 클래스 생성

from sqlalchemy import Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Identity
from sqlalchemy import text, create_engine
from dotenv import load_dotenv
import os
from sqlalchemy import select

load_dotenv()
password = os.getenv("ORACLE_PASSWORD")

engine = create_engine(f"oracle+oracledb://python_user:{password}@localhost:1521/?service_name=xe",echo=True)

#  부모 클래스를 만드는 두번째 방법

from sqlalchemy.orm import declarative_base
Base = declarative_base()
class Todo(Base):

    __tablename__ =  "todos"
    todo_id:Mapped[int] = mapped_column(Numeric(10,0), Identity(start=1, increment=1),primary_key=True)
    title:Mapped[str] = mapped_column(String(200))
    is_done:Mapped[bool] = mapped_column(default=False)
    #
    created_at:Mapped[Optional[datetime = mapped_column(DateTime, defaul=datetime.now())]]
    # created_at:Mapped[Optional[datetime = mapped_column(DateTime, sercer_default=func.sysdate())]]
    def __repr__(self):
        status = "완료" if self.is_done else "미완료"
        return f"{self.todo_id}. title={self.title}[{status}] {self.created_at}"

Base.metadata.create_all(engine)


# todo 추가
def add_todo():
    '''create'''
    # 할 일 내용을 입력하세요: 내용입력...
    title = input("할 일 내용을 입력하세요:").strip()
    # insert 구문 실행
    with Session(engine) as session:
        todo = Todo(title=title)
        session.add(todo)
        session.commit()
        print("등록되었습니다.\n")


def list_todos():
    # select 구문
    sql = "select * from todos order by todo_id"
    cursor.execute(sql)
    rows = cursor.fetchall()
    # todo 내용이 없는 경우
    if not rows:
        print("등록된 할 일 목록이 없습니다.\n")
        return
    print("-"*50)

    for row in rows:
        status = "완료" if row[2] == 1 else "미완료"
        print(f"{row[0]}. [{status}] {row[1]}({row[3]})")
    print("-"*50)
    print()

def update_todo():
    # 목록 보여주기
    list_todos()
    todo_id = input("완료 처리할 번호를 입력하세요:").strip()
    # 업데이트구문
    sql = "update todos set is_done = 1 where todo_id = :1"
    cursor.execute(sql,(todo_id,))
    conn.commit()

    #카운트 받아오기
    if cursor.rowcount == 0:
        print("해당 번호가 없습니다.")
    else:
        print("완료되었습니다.\n")

def delete_todo():
    # delete
    list_todos()
    todo_id = input("삭제 처리할 번호를 입력하세요:").strip()
    sql = "delete from todos where todo_id = :1"
    cursor.execute(sql,(todo_id,))
    conn.commit()

    #카운트 받아오기
    if cursor.rowcount == 0:
        print("해당 번호가 없습니다.\n")
    else:
        print("삭제 처리되었습니다.\n")

def menu():
    while True:
        print("=== Todo")
        print("1. 추가. 2. 목록 3. 완료처리 4. 삭제 5. 종료")

        choice = input("선택 : ")

        if choice =="1":
            add_todo()
        elif choice == "2":
            list_todos()
        elif choice =="3":
            update_todo()
        elif choice =="4":
            delete_todo()
        elif choice == "5":
            print("종료합니다")
            break
        else:
            print("번호를 확인해 주세요")


# 테스트용 구문(모듈 불러와서 쓰는 개념)
if __name__=="__main__":
    try:
        menu()
    finally:
        cursor.close()
        conn.close()