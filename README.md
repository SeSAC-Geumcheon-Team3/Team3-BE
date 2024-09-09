# 설치 및 실행 가이드

## 1. 환경 설정
1. 해당 디렉토리를 클론한다.
   ```
   > git clone origin https://github.com/SeSAC-Geumcheon-Team3/Team3-BE.git
   ```

2. venv 환경을 설정한다.
   ```
   > python -m venv venv
   ```

3. cmd 창에서 해당 venv 환경을 실행한다.
   ```
   > venv\Scripts\activate
   ```

4. requiremetns.txt를 설치한다.
   ```
   > pip install requirements.txt
   ```

5. DB 및 이미지 저장용 폴더를 원하는 환경에 생성한 후 .env 파일을 수정한다.
   ```
   # DB 연결 설정: 스키마는 생성해 두어야 한다.
   DATABASE_URL=mysql+mysqlconnector://{{사용자명(ex.root)}}:{{비밀번호}}@{{접속주소}}:{{접속포트(ex.3306)}}/{{스키마명}}

   # 토큰
   EXP=360000
   ALGORITHM=HS256
   SECRET_KEY=XYEl7FtgVaSGNola3b9REPIfy133h8UL6OOqkkdZXr4
   
   # 사진 업로드 디렉토리
   UPLOAD_DIRECTORY={{디렉토리 절대경로}}
   ```

## 2. 실행
개발환경에서 해당 프로그램을 실행하기 위해서는 다음 명령어를 입력하라
```
> python main.py
```
