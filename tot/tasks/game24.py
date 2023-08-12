import re
import os
import sympy
import pandas as pd
from tasks.base import Task, DATA_PATH
from prompts.game24 import dict_prompts 



dict_str_code_en = {
    'left': 'left', 
    'answer': 'answer',
    'Steps': 'Steps',
    'impossible': 'impossible', 
    'likely': 'likely',
    'sure': 'sure',
    }


dict_str_code_es = {
    'left': 'quedan', 
    'answer': 'respuesta',
    'Steps': 'Pasos',
    'impossible': 'imposible', 
    'likely': 'probable',
    'sure': 'seguro',
    }


dict_str_code_fr = {
    'left': 'rester', 
    'answer': 'réponse',
    'Steps': 'Étapes',
    'impossible': 'impossible', 
    'likely': 'probable',
    'sure': 'sûr',
    }


dict_str_code_pt = {
    'left': 'restantes', 
    'answer': 'resposta',
    'Steps': 'Passos',
    'impossible': 'impossível', 
    'likely': 'provável',
    'sure': 'certo',
    }


dict_str_code_it = {
    'left': 'rimanere', 
    'answer': 'risposta',
    'Steps': 'Passi',
    'impossible': 'impossibile', 
    'likely': 'probabile',
    'sure': 'sicuro',
    }

dict_str_code = {
    'en': dict_str_code_en,
    'es': dict_str_code_es,
    'pt': dict_str_code_pt,
    'fr': dict_str_code_fr,
    'it': dict_str_code_it,
    }

def get_current_numbers(y: str, lang: str) -> str:
    last_line = y.strip().split('\n')[-1]
    left = dict_str_code[lang]['left']
    return last_line.split(f'{left}: ')[-1].split(')')[0]


class Game24Task(Task):
    """
    Input (x)   : a string of 4 numbers
    Output (y)  : a trajectory of 3 steps to reach 24
    Reward (r)  : 0 or 1, depending on whether the trajectory is correct
    Input Example: 
        1 2 3 4
    Output Example: 
        1 + 2 = 3 (left: 3 3 4)
        3 + 3 = 6 (left: 4 6)
        6 * 4 = 24 (left: 24)
        (1 + 2 + 3) * 4 = 24
    """
    def __init__(self, file='24.csv', lang: str=''):
        """
        file: a csv file (fixed)
        """
        super().__init__()
        path = os.path.join(DATA_PATH, '24', file)
        self.data = list(pd.read_csv(path)['Puzzles'])
        self.value_cache = {}
        self.steps = 4
        self.stops = ['\n'] * 4
        self.lang = lang

    def __len__(self) -> int:
        return len(self.data)
    
    def get_input(self, idx: int) -> str:
        return self.data[idx]

    def test_output(self, idx: int, output: str, _):
        answer = dict_str_code[self.lang]['answer']
        expression = output.strip().split('\n')[-1].lower().replace(f'{answer}: ', '').split('=')[0]
        #print('output', output)
        #print('expression', expression)
        numbers = re.findall(r'\d+', expression)
        problem_numbers = re.findall(r'\d+', self.data[idx])
        if sorted(numbers) != sorted(problem_numbers):
            #print('different numbers')
            return {'r': 0}
        try:
            #print('sympy', sympy.simplify(expression))
            return {'r': int(sympy.simplify(expression) == 24)}
        except Exception as e:
            # print(e)
            return {'r': 0}
            
    @staticmethod
    def standard_prompt_wrap(x: str, y:str='', lang: str='') -> str:
        return dict_prompts[lang]['standard_prompt'].format(input=x) + y

    @staticmethod
    def cot_prompt_wrap(x: str, y:str='', lang: str='') -> str:
        return dict_prompts[lang]['cot_prompt'].format(input=x) + y
    
    @staticmethod
    def propose_prompt_wrap(x: str, y: str='', lang: str='') -> str:
        current_numbers = get_current_numbers(y if y else x, lang)
        if current_numbers == '24':
            Steps = dict_str_code[lang]['Steps']
            prompt = dict_prompts[lang]['cot_prompt'].format(input=x) + f'{Steps}:' + y
            # print([prompt])
        else:
            prompt = dict_prompts[lang]['propose_prompt'].format(input=current_numbers)
        return prompt
    
    @staticmethod
    def value_prompt_wrap(x: str, y: str, lang: str='') -> str:
        last_line = y.strip().split('\n')[-1]
        left = dict_str_code[lang]['left']
        answer = dict_str_code[lang]['answer']

        if f'{left}: ' not in last_line:  # last step
            ans = last_line.lower().replace(f'{answer}: ', '')
            # print([value_last_step_prompt.format(input=x, answer=ans)])
            return dict_prompts[lang]['value_last_step_prompt'].format(input=x, answer=ans)
        current_numbers = get_current_numbers(y, lang)
        return dict_prompts[lang]['value_prompt'].format(input=current_numbers)
    
    @staticmethod
    def value_outputs_unwrap(x: str, y: str, value_outputs: list, lang: str='') -> float:
        answer = dict_str_code[lang]['answer']
        impossible = dict_str_code[lang]['impossible']
        likely = dict_str_code[lang]['likely']
        sure = dict_str_code[lang]['sure']

        if len(y.strip().split('\n')) == 4 and f'{answer}' not in y.lower():
            return 0
        value_names = [_.split('\n')[-1] for _ in value_outputs]
        value_map = {f'{impossible}': 0.001, f'{likely}': 1, f'{sure}': 20}  # TODO: ad hoc
        value = sum(value * value_names.count(name) for name, value in value_map.items())
        return value