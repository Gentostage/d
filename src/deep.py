from deeppavlov.skills.pattern_matching_skill import PatternMatchingSkill
from deeppavlov.agents.default_agent.default_agent import DefaultAgent
from deeppavlov.agents.processors.highest_confidence_selector import HighestConfidenceSelector
from deeppavlov.contrib.skills.similarity_matching_skill import SimilarityMatchingSkill

import pandas as pd
import os

class deep:
    TRAIN = False
    DATANAME = 'dataset.csv'
    MODELNAME = 'model1'

    def learn(self, train):
        hello = PatternMatchingSkill(responses=['Привет!', 'Здравствуйте', 'Добрый день'],
                                     patterns=['Привет', 'Здравствуйте', 'Добрый день'])
        bye = PatternMatchingSkill(responses=['Пока!', 'До свидания, надеюсь смог вам помочь', 'До встречи!'],
                                   patterns=['До свидания', 'Пока', 'Спасибо за помощь'])
        fallback = PatternMatchingSkill(responses=['Я не понял, но могу попробовать ответить на другой вопрос',
                                                   'Я не понял, задайте другой вопрос'], default_confidence=0.1)

        faq = SimilarityMatchingSkill(data_path='./data/' + self.DATANAME,
                                      x_col_name='Question',
                                      y_col_name='Answer',
                                      save_load_path='./model/' + self.MODELNAME,
                                      config_type='tfidf_autofaq',
                                      train=train)
        self.d = DefaultAgent([hello, bye, faq, fallback], skills_selector=HighestConfidenceSelector())

    def __init__(self):
        self.learn(False)

    def FAQ(self, text):
        text = self.d([text])
        return text

    def relern(self):
        filenames = os.listdir(path="./data")
        filenames.remove('deleted')
        filenames.remove(self.DATANAME)
        combined_csv = pd.concat([pd.read_csv('./data/' + f) for f in filenames])
        combined_csv.to_csv('./data/' + self.DATANAME, index=False)
        self.learn(True)
        return "ok"
