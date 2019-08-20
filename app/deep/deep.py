from deeppavlov.skills.pattern_matching_skill import PatternMatchingSkill
from deeppavlov.agents.default_agent.default_agent import DefaultAgent
from deeppavlov.agents.processors.highest_confidence_selector import HighestConfidenceSelector
from deeppavlov.contrib.skills.similarity_matching_skill import SimilarityMatchingSkill

import pandas as pd
import os


class deep:
    TRAIN = False
    DATANAME = './app/model/dataset.csv'
    MODELNAME = './app/model/model1'

    def learn(self, train):
        h = pd.read_csv('./app/database/hello_skill.csv')
        hello = PatternMatchingSkill(responses=[x for x in h['responses'].tolist() if x != ' ' and x == x],
                                     patterns=[x for x in h['patterns'].tolist() if x != ' ' and x == x])

        b = pd.read_csv('./app/database/bye_skill.csv')
        bye = PatternMatchingSkill(responses=[x for x in b['responses'].tolist() if x != ' ' and x == x],
                                   patterns=[x for x in b['patterns'].tolist() if x != ' ' and x == x])

        f = pd.read_csv('./app/database/fallback_skill.csv')
        fallback = PatternMatchingSkill(responses=[x for x in f['responses'].tolist() if x != ' ' and x == x],
                                        default_confidence=0.1)
        faq = SimilarityMatchingSkill(data_path=self.DATANAME,
                                      x_col_name='Question',
                                      y_col_name='Answer',
                                      save_load_path=self.MODELNAME,
                                      config_type='tfidf_autofaq',
                                      train=train)

        self.d = DefaultAgent([hello, bye, faq, fallback], skills_selector=HighestConfidenceSelector())

    def __init__(self):
        self.learn(False)

    def FAQ(self, text):
        text = self.d([text])
        return text

    def new_pattern_matching_skill(self):
        self.learn(False)
        return 'ok'

    def relern(self):
        filenames = os.listdir(path="./data")
        filenames.remove('deleted')
        filenames.remove(self.DATANAME)
        combined_csv = pd.concat([pd.read_csv('./data/' + f) for f in filenames])
        combined_csv.to_csv('./data/' + self.DATANAME, index=False)
        self.learn(True)
        return "ok"
