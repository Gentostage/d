from deeppavlov.skills.pattern_matching_skill import PatternMatchingSkill
from deeppavlov.agents.default_agent.default_agent import DefaultAgent
from deeppavlov.agents.processors.highest_confidence_selector import HighestConfidenceSelector
from deeppavlov.contrib.skills.similarity_matching_skill import SimilarityMatchingSkill

class deep:
    TRAIN = False 
    DATANAME = 'dataset.csv'
    MODELNAME = 'model1'

    def learn(self):
        hello = PatternMatchingSkill(responses=['Привет!', 'Здравствуйте', 'Добрый день'], patterns=['Привет', 'Здравствуйте', 'Добрый день'])
        bye = PatternMatchingSkill(responses=['Пока!', 'До свидания, надеюсь смог вам помочь', 'До встречи!'], patterns=['До свидания', 'Пока', 'Спасибо за помощь'])
        fallback = PatternMatchingSkill(responses=['Я не понял, но могу попробовать ответить на другой вопрос', 'Я не понял, задайте другой вопрос'], default_confidence = 0.1)

        faq = SimilarityMatchingSkill(data_path = './data/'+self.DATANAME,
                                x_col_name = 'Question', 
                                y_col_name = 'Answer',
                                save_load_path = './model/'+self.MODELNAME,
                                config_type = 'tfidf_autofaq',
                                train = self.TRAIN)
        self.d = DefaultAgent([hello, bye, faq, fallback], skills_selector=HighestConfidenceSelector())

    def __init__(self):
            self.learn()
 
    def FAQ(self,text):
            text = self.d([text])
            return text

    def relern(self):
            self.TRAIN=True
            self.learn()
            self.TRAIN=False
            return "ok"
