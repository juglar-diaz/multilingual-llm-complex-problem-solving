import sys
sys.path.append("..")
from llms import call_llm


def call_llm_tot(prompt, model="gpt-4", temperature=0.7, max_tokens=1024, n=1, stop=None) -> list:
    outputs = []
    while n > 0:
        cnt = min(n, 20)
        n -= cnt
        if model.startswith('gpt-3.5-turbo'):
            response = call_llm(
                model=model,
                parameters={
                    'messages': [
                            {"role": "user", "content": prompt},
                        ],
                    'temperature': temperature,
                    'max_tokens': max_tokens,
                    'n': cnt,
                    'stop': stop
                    }
                )
                
        if model.startswith('text-bison@'):
            response = call_llm(
                model=model,
                n=cnt,

                parameters= {
                    'prompt': prompt,
                    'temperature': temperature,
                    'max_output_tokens': max_tokens,
                    },
                stop=stop
                )
                
        if model.startswith('chat-bison@'):
            response = call_llm(
                model=model,
                n=cnt,
                parameters= {
                    'message': prompt,
                    'temperature': temperature,
                    'max_output_tokens': max_tokens,
                    },
                stop=stop
                )

        outputs.extend(response)
        # log completion tokens
       
    
    return outputs        
