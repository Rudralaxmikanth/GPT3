import openai
import json

# Set up OpenAI API
openai.api_key = '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'

with open('documentation.json', 'r') as json_file:
    data = json.load(json_file)
    context_list = data['data']


def generate_qa_pairs(context_list):
    qa_pairs = []
    for context_data in context_list:
        title = context_data['title']
        context = context_data['context']
        prompt = f"Generate a question and answer pair based on the following information:\nTitle: {title}\nContext: {context}\n"
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7
        )
        answer = response.choices[0].text.strip().split('?')
        qa_pairs.append({
            'title': title,
            'context': context,
            'question': answer[0] + '?',
            'answer': answer[1]
        })
    return qa_pairs


qa_pairs = generate_qa_pairs(context_list)
data_dict = {'data': qa_pairs}

with open('output.json', 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)
