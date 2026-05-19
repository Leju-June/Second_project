from fastapi import FastAPI

app = FastAPI() # 인스턴스 생성

@app.get("/") # get method로 '/'에 해당하는 페이지 생성
def root():
	return {'message' : 'welcome to mnist service'}