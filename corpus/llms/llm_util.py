import ollama

class LlmUtil:
    def __init__(self):
        pass

    def prompt_ollama(prompt):

        response = ollama.chat(model='llama3.1', messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        return response['message']['content']

