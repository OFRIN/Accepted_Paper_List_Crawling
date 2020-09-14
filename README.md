# 설명
- 해당 코드는 https://openaccess.thecvf.com/ 사이트를 기준으로 크롤링할 수 있도록 작성했습니다.

# 설치
```bash
# for Windows
pip install requests
pip install bs4

# for Linux
python3 -m pip install requests
python3 -m pip install bs4
```

# To-Do List

- [X] 다중 링크를 입력 받고 한번에 XLSX로 저장해야 함. (제목 중 ','가 있을 경우 문제 발생)
- [X] Excel 파일 읽는 코드 추가해야 함. (제목 중 ','가 있을 경우 문제 발생)
- [ ] PDF로 자동 저장해야 함. (통신 관련 에러 발생하는지 확인해야 함.)
- [ ] 만약 시간 당 콜 수 제한이 있다면 엑셀 중 원하는 인덱스 다운받을 수 있도록 개발해야 함.
- [ ] 엑셀 서식 추가하여 첫번째 열에 색 및 BOLD 효과, 길이 조정 등 추가
