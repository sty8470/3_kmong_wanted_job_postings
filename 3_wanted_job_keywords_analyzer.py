import gspread
from collections import Counter
import re

# 서비스 계정 키 파일을 사용하여 인증
gc = gspread.service_account(filename="/Applications/mac_kakao_json_key_file.json")

# 구글 시트 문서 열기
spreadsheet = gc.open_by_key('1s5wchjObYYZWgu2liEpEVTj9ca_fm0lCmD10_e3Ntso')

# 특정 워크시트 선택, 여기서는 gid가 1084545621인 워크시트를 선택
worksheet = spreadsheet.get_worksheet_by_id(1452087923)

# 모든 데이터를 가져오기
data = worksheet.get_all_records()

search_word_indices = ["직무ID", "직무", "회사", "주요업무", "자격요건", "우대사항", "혜택 및 복지", "채용보상금"]
search_word = input('검색할 단어를 입력하세요. 아래의 단어들 중 한개가 되어야 합니다. \n"직무ID", "직무", "회사", "주요업무", "자격요건", "우대사항", "혜택 및 복지", "채용보상금": ')

# 모든 자격요건을 하나의 문자열로 결합
total_text = ' '.join(str(row[search_word]) for row in data if search_word in row)

# 텍스트에서 불필요한 특수 문자 제거
clean_text = re.sub(r'[^\w\s]', '', total_text)

# 텍스트를 공백으로 분할하여 단어 리스트 생성
words = clean_text.split()

# 각 단어의 빈도수 계산
word_counts = Counter(words)

# 가장 빈도수가 높은 20개의 단어 추출
most_common_words = word_counts.most_common()

# # 결과 출력
# print("Top 20 most frequent words:")
# for word, count in most_common_words:
#     print(f"{word}: {count}")

# 결과를 텍스트 파일로 저장
with open(f'원티드_재무_공고_"{search_word}"_키워드_빈도수_정렬.txt', 'w') as file:
    file.write("빈도 수 가 높은 단어부터 역순으로 정렬하기:\n")
    for word, count in most_common_words:
        file.write(f"{word}: {count}\n")

print("File exported successfully.")
