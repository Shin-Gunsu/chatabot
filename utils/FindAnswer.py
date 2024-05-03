class FindAnswer:
    def __init__(self) -> None:
        pass
    # def __init__(self, db):
    #     self.db = db

    # 검색 쿼리 생성
    # def _make_query(self, intent_name, ner_tags):
        # sql = "select * from chatbot_train_data"
        # if intent_name != None and ner_tags == None:
        #     sql = sql + " where intent='{}' ".format(intent_name)

        # elif intent_name != None and ner_tags != None:
        #     where = ' where intent="%s" ' % intent_name
        #     if (len(ner_tags) > 0):
        #         where += 'and ('
        #         for ne in ner_tags:
        #             where += " ner like '%{}%' or ".format(ne)
        #         where = where[:-3] + ')'
        #     sql = sql + where

        # # 동일한 답변이 2개 이상인 경우, 랜덤으로 선택
        # sql = sql + " order by rand() limit 1"
        # return sql



    # 답변 검색
    def search(self, intent_name, ner_tags):
        answer = ['청솔관은 여기','이미지없음']
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
