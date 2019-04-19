# from deeppavlov.skills.pattern_matching_skill import PatternMatchingSkill
# from deeppavlov.agents.default_agent.default_agent import DefaultAgent
# from deeppavlov.agents.processors.highest_confidence_selector import HighestConfidenceSelector
# from deeppavlov.contrib.skills.similarity_matching_skill import SimilarityMatchingSkill


# hello = PatternMatchingSkill(responses=['Привет!', 'Здравствуйте', 'Добрый день'], patterns=['Привет', 'Здравствуйте', 'Добрый день'])
# bye = PatternMatchingSkill(responses=['Пока!', 'До свидания, надеюсь смог вам помочь', 'До встречи!'], patterns=['До свидания', 'Пока', 'Спасибо за помощь'])
# fallback = PatternMatchingSkill(responses=['Я не понял, но могу попробовать ответить на другой вопрос', 'Я не понял, задайте другой вопрос'], default_confidence = 0.5)


# faq = SimilarityMatchingSkill(data_path = 'http://files.deeppavlov.ai/faq/dataset.csv',
#                               x_col_name = 'Question', 
#                               y_col_name = 'Answer',
#                               save_load_path = './model',
#                               config_type = 'tfidf_autofaq',
#                               train = True)



# agent = DefaultAgent([hello, bye, faq, fallback], skills_selector=HighestConfidenceSelector())

from flask import Flask
from flask import render_template

import csv
import json

app = Flask(__name__)

@app.route("/<text>")
def index(text):
    
    # answer = agent([text])
    # answer = str(answer)
    return 'helo' #answer

@app.route("/answer")
def answer():
    return render_template('answer.html')


@app.route("/get")
def get():
    with open('dataset.csv', 'r') as fp:
        reader = csv.reader(fp, delimiter=',', quotechar='"')
        # next(reader, None)  # skip the headers
        data_read = [row for row in reader]
    json_string = json.dumps(data_read)

    return json_string

@app.route("/set")
def set():
    csv = request.args.get('csv')
    with open('dataset.csv', 'w') as fp:
        writer = csv.writer(fp, delimiter=',')
        # writer.writerow(["your", "header", "foo"])  # write header
        writer.writerows(data)
    return json_string

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000 )


