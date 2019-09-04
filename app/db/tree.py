import json

from difflib import get_close_matches, SequenceMatcher

json_string = """
{
    "1": {
        "name": "паспор",
        "description": "Получение паспорта"
    },

    "2": {
        "name": "Снилс",
        "description": "Снилс страховое свидетельство пенсиодный доки"
    },
    
    "3": {
        "name": "Снилс",
        "description": "Снилс страховое свидетельство пенсиодный доки"
    }
}
"""

test_question_1 = 'Я бы хотел востановить снилс'

test_question_2 = 'Я бы хотел получть паспорт'


json = json.loads(json_string)
name = str
best = 0
for key, value in json.items():
    seq = SequenceMatcher(None, str(value['description']), test_question_1)
    scope = seq.ratio() * 100
    if best < scope:
        best = scope
        name = value['name']

print(name)
