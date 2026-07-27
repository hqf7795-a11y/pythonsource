# 사용자 정의 모듈
# 함수 2개 정의
def add(a, b):
        return a + b

def sub(a, b):
        return a - b


PI = 3.141592

class Math:
    def solv(self, r):
        return PI * (r ** 2)

# module test
if __name__ == "__main__":
        print(add(3,3))
        print(sub(3,3))
        m=Math()
        print(m.solv(6))