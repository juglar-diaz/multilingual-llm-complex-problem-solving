import sys
sys.path.append("..")

from llms import call_llm


def call_llm_react(model, prompt, stop=["\n"]):
    if model.startswith('gpt-3.5-turbo'):
        response = call_llm(
            model=model,
            parameters={
                'messages': [
                        {"role": "user", "content": prompt},
                    ],
                'temperature': 0,
                'max_tokens': 128,
                'top_p': 1,
                'frequency_penalty': 0.0,
                'presence_penalty': 0.0,
                'stop': stop
                }
            )
            
    if model.startswith('text-bison@'):
        response = call_llm(
            model=model,
            parameters= {
                'prompt': prompt,
                'temperature': 0,
                'max_output_tokens': 128,
                'top_p': 1,
                },
            stop=stop
            )
            
    if model.startswith('chat-bison@'):
        response = call_llm(
            model=model,
            parameters= {
                'message': prompt,
                'temperature': 0,
                'max_output_tokens': 128,
                'top_p': 1,
                },
            stop=stop
            )
        
    return response[0]
