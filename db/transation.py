import oracledb
from datetime import datetime
conn = oracledb.connect(user="PYTHON_USER",password="54321",dsn="localhost/XE")
cursor = conn.cursor()


def add_transation():
    # 내역추가 인설트구문
    tx_type = input("구분을 입력하세요 ex:수입/지출").strip()
    amount = input("금액을 입력하세요 ex:1000").strip()
    memo = input("내역을 입력하세요 ex:수입처/지출처").strip()
    reg_date = input("날짜를 입력하세요 ex:YYYY-MM-DD, 엔터 입력시 오늘").strip()

    if not reg_date: #엔터시 오늘 구문
        reg_date = datetime.now().strftime("%Y-%m-%d")

    # insert 구문 실행
    sql = "insert into transation(tx_type,amount,memo,reg_date) values(:1,:2,:3,:4)"
    cursor.execute(sql,(tx_type,amount,memo,reg_date,))
    conn.commit()
    if cursor.rowcount >0:
        print("등록되었습니다.\n")

def list_transation():
    # 전체조회 'reg_date asc'
    # 번호 [지출] 300000원 - 용돈 (날짜)
    """reg_date asc"""
    sql = "select * from transation order by reg_date"
    cursor.execute(sql)
    rows = cursor.fetchall()
    if not rows:
        print("등록된 내역이 없습니다.\n")
        return
    print("-"*50)

    for row in rows:
        print(f"{row[0]} [{row[1]}] {row[2]}원-{row[3]}({row[4]})")
    print("-"*50)
    print()

def monthly_summary():
    # 월별합계, 사용자한테 입력받을거임

    month = input("조회하실 달을 입력하세요. EX)YYYY-MM: ").strip()

    sql = """SELECT tx_type, sum(amount) FROM transation WHERE reg_date LIKE :1 GROUP BY tx_type;"""

    # ㅈㄴ어렵다
    cursor.execute(sql,(month+'%',))
    rows = cursor.fetchall()

    if not rows:
        print("등록된 내역이 없습니다.\n")
        return
    print("-"*50)
    for row in rows:
        print(f"{row[0]} : [{row[1]}]원")
    print("-"*50)
    print()



def menu():
    # 1. 내역 추가 2. 전체 조회 3. 월별 합계 4. 종료
    while True:
            print("=== Transations ===")
            print("1. 추가. 2. 전체 조회 3. 월 별 합계 4. 종료")
    
            choice = input("선택 : ")
    
            if choice =="1":
                add_transation()
            elif choice == "2":
                list_transation()
            elif choice =="3":
                monthly_summary()
            elif choice =="4":
                print("종료합니다.")
                break
            else:
                print("번호를 확인해 주세요")



if __name__ == "__main__":
    try:
        menu()
    finally:
        cursor.close()
        conn.close()