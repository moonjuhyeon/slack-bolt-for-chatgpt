# Base image 설정
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일들을 복사
COPY requirements.txt .

# 패키지 설치
RUN pip3 install --no-cache-dir -r requirements.txt

# 소스코드 복사
COPY . .

# Flask 애플리케이션 실행
CMD ["python3", "main.py"]