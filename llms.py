import os
import openai
import backoff 
import vertexai

from vertexai.preview.language_models import ChatModel as vertexaiChatModel, TextGenerationModel as vertexaiTextGenerationModel
from vertexai.preview.language_models import CodeGenerationModel as vertexaiCodeGenerationModel, CodeChatModel as vertexaiCodeChatModel

from dotenv import load_dotenv
load_dotenv()

gcp_project = os.getenv("GCP_PROJECT", "")
gcp_location = os.getenv("GCP_LOCATION", "")

api_key = os.getenv("OPENAI_API_KEY", "")


if gcp_project == "":
    print("Warning: GCP_PROJECT is not set")

if gcp_location == "":
    print("Warning: GCP_LOCATION is not set")

vertexai.init(project= gcp_project, location= gcp_location)

if api_key != "":
    openai.api_key = api_key
else:
    print("Warning: OPENAI_API_KEY is not set")
    
api_base = os.getenv("OPENAI_API_BASE", "")
if api_base != "":
    print("Warning: OPENAI_API_BASE is set to {}".format(api_base))
    openai.api_base = api_base

completion_tokens = prompt_tokens = 0

@backoff.on_exception(backoff.expo, openai.error.OpenAIError)
def completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

def gpt(prompt, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    print('gpt prompt', prompt)
    messages = [{"role": "user", "content": prompt}]
    response = chatgpt(messages, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)
    print('gpt response', response)
    return response
    
def chatgpt(messages, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    global completion_tokens, prompt_tokens
    outputs = []
    while n > 0:
        print('n: ', n)
        cnt = min(n, 20)
        n -= cnt
        if stop:
            res = completions_with_backoff(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, n=cnt, stop=stop)
        else:
            res = completions_with_backoff(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, n=cnt)

        print('res ', res)
        outputs.extend([choice["message"]["content"] for choice in res["choices"]])
        # log completion tokens
        completion_tokens += res["usage"]["completion_tokens"]
        prompt_tokens += res["usage"]["prompt_tokens"]
    return outputs
    
def gpt_usage(backend="gpt-4"):
    global completion_tokens, prompt_tokens
    if backend == "gpt-4":
        cost = completion_tokens / 1000 * 0.06 + prompt_tokens / 1000 * 0.03
    elif backend == "gpt-3.5-turbo":
        cost = (completion_tokens + prompt_tokens) / 1000 * 0.0002
    return {"completion_tokens": completion_tokens, "prompt_tokens": prompt_tokens, "cost": cost}


from tenacity import (
    retry,
    stop_after_attempt,
    wait_chain,
    wait_fixed
) 

@retry(wait=wait_chain(*[wait_fixed(3) for i in range(3)] +
                       [wait_fixed(5) for i in range(2)] +
                       [wait_fixed(10)]))
def call_llm(**kwargs):
    if kwargs['model'].startswith('gpt-3.5-turbo'):
        response = openai.ChatCompletion.create(**kwargs['parameters'])
        #response = response['choices'][0]['message']['content']
        return [choice["message"]["content"] for choice in response["choices"]]

    responses = []

    n = kwargs.get('n', 1)
    for _ in range(n):
        if kwargs['model'].startswith('chat-bison@'):
            model = vertexaiChatModel.from_pretrained(kwargs['model'])
            chat = model.start_chat(context="""""", examples=[])
            #chat = model.start_chat()
            response = chat.send_message(**kwargs['parameters'])
            response = response.text
        
        if kwargs['model'].startswith('text-bison@'):
            model = vertexaiTextGenerationModel.from_pretrained(kwargs['model'])
            response = model.predict(**kwargs['parameters'])
            response = response.text

        if kwargs['model'].startswith('codechat-bison@'):
            model = vertexaiCodeChatModel.from_pretrained(kwargs['model'])
            chat = model.start_chat()
            response = chat.send_message(**kwargs['parameters'])
            response = response.text
        
        if kwargs['model'].startswith('code-bison@'):
            model = vertexaiCodeGenerationModel.from_pretrained(kwargs['model'])
            response = model.predict(**kwargs['parameters'])
            response = response.text

        if  kwargs['model'] == "llama-2":
            pass
    

        stop = kwargs.get('stop')
        if stop and (response.find(stop[0])+1):
            response = response[:response.find(stop[0])]#+stop
        responses.append(response)

   
    return responses
