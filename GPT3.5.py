import openai
import json


openai.api_key = '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'


with open('documentation.json', 'r') as json_file:
    data = json.load(json_file)
    context_list = data['data']


def generate_qa_pairs(context_list, num_questions=5):
    qa_pairs = []
    for context_data in context_list:
        context = context_data['context']
        prompt = f"Generate {num_questions} questions and answers based on the following information:\nContext: {context}\n"
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=100,
            n=num_questions * 2,  # Generate double the number of tokens to accommodate for potential incomplete answers
            stop=None,
            temperature=0.7
        )
        answers = response.choices[0].text.strip().split('?')
        for i in range(num_questions):
            answer_index = i * 2
            if answer_index < len(answers):
                question = answers[answer_index] + '?'
                if answer_index + 1 < len(answers):
                    answer = answers[answer_index + 1]
                else:
                    answer = ""
                qa_pairs.append({
                    'question': question,
                    'answer': answer
                })
    return qa_pairs

qa_pairs = generate_qa_pairs(context_list)

output_data = {'data': qa_pairs}

with open('generated_qa_pairs.json', 'w') as output_file:
    json.dump(output_data, output_file, indent=4)


