# Copyright 2022 PAL Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from llms import call_llm

#import sys
#sys.path.append("../../..")



def call_llm_pal(model, max_tokens, stop, prompt, temperature, top_p, n, best_of, lang):
    content_instruction = {
        'en': 'You are a helpful assistant that can write Python code that solves mathematical reasoning questions similarly to the examples that you will be provided.',
        'es': 'Usted es un asistente útil que puede escribir código Python que resuelve preguntas de razonamiento matemático de manera similar a los ejemplos que se le proporcionarán.',
        'it': 'Sei un utile assistente in grado di scrivere codice Python che risolve domande di ragionamento matematico in modo simile agli esempi che ti verranno forniti.',
        'pt': 'Você é um assistente útil que pode escrever código Python que resolve questões de raciocínio matemático de forma semelhante aos exemplos que serão fornecidos.',
        'fr': 'Vous êtes un assistant utile qui peut écrire du code Python qui résout des questions de raisonnement mathématique de la même manière que les exemples qui vous seront fournis.',
    }
    
    instruction_run = content_instruction[lang]

    if model.startswith('gpt-4') or model.startswith('gpt-3.5-turbo'):
        response = call_llm(
            model= model,
            parameters= {
                'messages': [
                        {"role": "system", "content": instruction_run},
                        {"role": "user", "content": prompt},
                    ],
                'temperature': temperature,
                'max_tokens': max_tokens,
                'stop': stop,
                'top_p': top_p,
                'n': n
                }
            )
    
    if model.startswith('chat-bison@') or model.startswith('codechat-bison@'):
        response = call_llm(
        model= model,
        n= n,
        parameters= {
            'message': f"""{instruction_run}""" + "\n" + prompt,
            'temperature': temperature,
            'max_output_tokens': max_tokens,
            'top_p': top_p,
            'top_k': n
            }
        )    
    
    if model.startswith('text-bison@'):
        response= call_llm(
        model= model,
        n= n,
        parameters= {
            'prompt': f"""{instruction_run}""" + "\n" + prompt,
            'temperature': temperature,
            'max_output_tokens': max_tokens,
            'top_p': top_p
            }
        )
    
    if model.startswith('code-bison@'):
        response= call_llm(
        model= model,
        n= n,
        parameters= {
            'prefix': f"""{instruction_run}""" + "\n" + prompt,
            'temperature': temperature,
            'max_output_tokens': max_tokens,
            'top_p': top_p,
            }
        )
    
    return response
    
    

#def call_gpt(prompt, model='code-davinci-002', stop=None, temperature=0., top_p=1.0, max_tokens=128, majority_at=None):
def call_gpt(prompt, model='gpt-3.5-turbo', stop=None, temperature=0., top_p=1.0, max_tokens=128, majority_at=None, lang=''):
    num_completions = majority_at if majority_at is not None else 1
    num_completions_batch_size = 5
    
        
    completions = []
    for i in range(20 * (num_completions // num_completions_batch_size + 1)):
        #try:
            requested_completions = min(num_completions_batch_size, num_completions - len(completions))
            ans = call_llm_pal(
                model=model,
                max_tokens=max_tokens,
                stop=stop,
                prompt=prompt,
                temperature=temperature,
                top_p=top_p,
                n=requested_completions,
                best_of=requested_completions,
                lang=lang
                )
            
            completions.extend(ans)
            if len(completions) >= num_completions:
                return completions[:num_completions]
        #except openai.error.RateLimitError as e:
        #    time.sleep(min(i**2, 60))
    #raise RuntimeError('Failed to call LLM API')
