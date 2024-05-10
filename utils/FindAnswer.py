class FindAnswer:
    def __init__(self) -> None:
        pass

    # 답변 검색
    def search(self, intent_name, ner_tags):
        answer = ['답변출력','이미지출력']
        return (answer[0], answer[1])

    # NER 태그를 실제 입력된 단어로 변환
    def tag_to_word(self, ner_predicts, answer):
        for word, tag in ner_predicts:

            # 변환해야하는 태그가 있는 경우 추가
            if tag == 'B_LOC' or tag == 'B_CLUB' or tag == 'B_ORG' or tag=='B_MAJOR':
                answer = answer.replace(tag, word)

        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
        return answer
