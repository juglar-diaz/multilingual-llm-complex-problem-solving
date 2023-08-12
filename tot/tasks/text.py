import os
import re
from tasks.base import Task, DATA_PATH
from prompts.text import dict_prompts
from backend import call_llm_tot



dict_str_code_en = {
    'Passage': 'Passage', 
    'coherency score is': 'coherency score is',
    'Choice': 'Choice',
    'more coherent passage is': 'more coherent passage is',
    'two passages are similarly coherent': 'two passages are similarly coherent',
    'best choice is': 'best choice is'

    }

dict_str_code_es = {
    'Passage': 'Pasaje', 
    'coherency score is': 'puntuación de coherencia es',
    'Choice': 'Elección',
    'more coherent passage is': 'pasaje más coherente es',
    'two passages are similarly coherent': 'dos pasajes son igualmente coherentes',
    'best choice is': 'mejor opción es'

    }

dict_str_code_pt = {
    'Passage': 'Passagem', 
    'coherency score is': 'pontuação de coerência é',
    'Choice': 'Escolha',
    'more coherent passage is': 'passagem mais coerente é',
    'two passages are similarly coherent': 'duas passagens são similarmente coerentes',
    'best choice is': 'melhor escolha é'

    }

dict_str_code_fr = {
    'Passage': 'Passage', 
    'coherency score is': 'le score de cohérence est de',
    'Choice': 'Choix',
    'more coherent passage is': 'passage le plus cohérent est',
    'two passages are similarly coherent': 'deux passages sont également cohérents',
    'best choice is': 'meilleur choix est'

    }

dict_str_code_it = {
    'Passage': 'Passaggio', 
    'coherency score is': 'punteggio di coerenza è',
    'Choice': 'Scelta',
    'more coherent passage is': 'passaggio più coerente è',
    'two passages are similarly coherent': 'due passaggi sono similmente coerenti',
    'best choice is': 'scelta migliore è'

    }

dict_str_code = {
    'en': dict_str_code_en,
    'es': dict_str_code_es,
    'pt': dict_str_code_pt,
    'fr': dict_str_code_fr,
    'it': dict_str_code_it,
    }


class TextTask(Task):
    """
    Input (x)   : a text instruction
    Output (y)  : a text generation
    Reward (r)  : # TODO
    Input Example: 
    Output Example: 
    """
    def __init__(self, file='', lang=''):
        """
        file: a text file, each line is some sentences
        """
        super().__init__()
        path = os.path.join(DATA_PATH, 'text', file)
        self.data = open(path).readlines()
        self.steps = 1
        self.lang = lang
        Passage = dict_str_code[self.lang]['Passage']
        self.stops = [f"\n{Passage}:\n", None]

    def __len__(self) -> int:
        return len(self.data)
    
    def get_input(self, idx: int) -> str:
        return self.data[idx]
    
    def test_output(self, idx: int, output: str, model: str):
        Passage = dict_str_code[self.lang]['Passage']
        output = output.split(f"{Passage}:\n")[-1]
        prompt = dict_prompts[self.lang]['score_prompt'] + output

        score_outputs = call_llm_tot(prompt, n=3, model=model)
        scores = []
        for score_output in score_outputs:
            coherency = dict_str_code[self.lang]['coherency score is']
            pattern = rf".*{coherency} (\d+).*"
            match = re.match(pattern, score_output, re.DOTALL)
            if match:
                score = int(match.groups()[0])
                scores.append(score)
            else:
                print(f'------------------score no match: {[score_output]}')
        # print('------------')
        info = {'rs': scores, 'r': sum(scores) / len(scores) if scores else 0}
        return info
    
    @staticmethod
    def standard_prompt_wrap(x: str, y:str='', lang: str='') -> str:
        return dict_prompts[lang]['standard_prompt'].format(input=x) + y

    @staticmethod
    def cot_prompt_wrap(x: str, y:str='', lang: str='') -> str:
        return dict_prompts[lang]['cot_prompt'].format(input=x) + y

    @staticmethod
    def vote_prompt_wrap(x: str, ys: list, lang: str) -> str:
        prompt = dict_prompts[lang]['vote_prompt']
        Choice = dict_str_code[lang]['Choice']
        for i, y in enumerate(ys, 1):
            # y = y.replace('Plan:\n', '')
            # TODO: truncate the plan part?
            prompt += f'{Choice} {i}:\n{y}\n'
        return prompt
    
    @staticmethod
    def vote_outputs_unwrap(vote_outputs: list, n_candidates: int, lang: str) -> list:
        vote_results = [0] * n_candidates

        best_choice_is = dict_str_code[lang]['best choice is']
        pattern = rf".*{best_choice_is} .*(\d+).*"

        for vote_output in vote_outputs:
            match = re.match(pattern, vote_output, re.DOTALL)
            if match:
                vote = int(match.groups()[0]) - 1
                if vote in range(n_candidates):
                    vote_results[vote] += 1
            else:
                print(f'vote no match: {[vote_output]}')
        
        return vote_results

    @staticmethod
    def compare_prompt_wrap(x: str, ys: list, lang: str) -> str:
        assert len(ys) == 2, 'compare prompt only supports 2 candidates'
        Passage = dict_str_code[lang]['Passage']
        ys = [y.split(f'{Passage}:\n')[-1] for y in ys]
        prompt = dict_prompts[lang]['compare_prompt'] + f'{Passage} 1:\n{ys[0]}\n\n{Passage} 2:\n{ys[1]}\n'
        return prompt
    
    @staticmethod
    def compare_output_unwrap(compare_output: str, lang: str):
        coherent_passage = dict_str_code[lang]['more coherent passage is']
        two_passages = dict_str_code[lang]['two passages are similarly coherent']

        if f'{coherent_passage} 1' in compare_output:
            return 0
        elif f'{coherent_passage} 2' in compare_output:
            return 1
        elif f'{two_passages}' in compare_output:
            return 0.5
        else:
            print(f'-----------------compare no match: {[compare_output]}')
            return -1