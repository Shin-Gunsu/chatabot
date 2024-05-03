class FindIntent:
    def __init__(self,model) -> None:
        self.model = model

    # 답변 검색
    def classification(self,query):
        predict = self.model.predict_class(query)
        predict_label = self.model.labels[predict]
        return (predict,predict_label)

