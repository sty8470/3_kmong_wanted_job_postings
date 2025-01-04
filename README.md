# 원티드 공고 크롤러

이 프로젝트는 Python을 사용하여 원티드의 주요업무, 자격요건, 우대사항, 혜택 및 복지등의 키워드들을 직무 별로 크롤링 하여서, 빈도 수 별로 그 키워드등을 파싱하는 프로그램 입니다.

## 기능 설명

- **검색 키워드 선택**: 사용자는 검색하고자 하는 직무 키워드를 선택합니다. 그러면 20분에서 30분 정도 셀레니윰 크롤링을 시작합니다.
- **데이터 저장**: 추출된 데이터를 Pandas DataFrame으로 정리하고, 이를 CSV 파일로 저장합니다.
- **데이터 추출**: "직무ID", "직무", "회사", "주요업무", "자격요건", "우대사항", "혜택 및 복지", "채용보상금" 중의 추출하고픈 키워드 등을 입력합니다. 


## 사용 방법

1. **필요 라이브러리 설치**:
   ```bash
   pip install requests pandas beautifulsoup4