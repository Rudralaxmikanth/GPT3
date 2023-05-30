import json
from quepy import install
from quepy import settings
from quepy.dsl import FixedType
from quepy.expression import Expression
from quepy.parsing import QuestionTemplate, Particle, Lemmas, LemmasToken

question_base = install('en')

# Custom quepy templates for generating questions
class WhatIs(QuestionTemplate):
    target_type = FixedType(LemmasToken)
    regex = Lemmas("what be") + target_type + Particle("?")
    template = "What is {0}?"

class Explain(QuestionTemplate):
    target_type = FixedType(LemmasToken)
    regex = Lemmas("explain") + target_type
    template = "Explain {0}."

class HowDoes(QuestionTemplate):
    target_type = FixedType(LemmasToken)
    regex = Lemmas("how do") + target_type + Lemmas("work")
    template = "How does {0} work?"

# Add custom templates to quepy settings
settings.TEMPLATE_CLASS += [WhatIs, Explain, HowDoes]

question_answers = pipeline(task='question-answering')

with open("documentation.json", "r") as file:
    data = json.load(file)

qa_pairs = []

for entry in data["data"]:
    context = entry["context"]
    title = entry["title"]

    # Generate questions using quepy templates
    expression = Expression(context)
    questions = expression.get_questions()
    
    for question in questions:
        answer = question_answers(question=question, context=context)["answer"]
        qa_pairs.append({"question": question, "answer": answer})

# Write the question-answer pairs to a new JSON file
output_data = {"data": qa_pairs}
with open("qa_pairs.json", "w") as file:
    json.dump(output_data, file, indent=2)
