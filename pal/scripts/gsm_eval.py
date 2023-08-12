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


import copy
import json
import argparse
import tqdm
import os
import pickle
import sys
sys.path.append("..")
sys.path.append("../..")

from pal import interface
from pal.prompt import math_prompts

parser = argparse.ArgumentParser()
parser.add_argument('--append', action='store_true')
parser.add_argument('--verbose', action='store_true')
parser.add_argument('--dataset', default='gsm', type=str)
parser.add_argument('--model', default='gpt-3.5-turbo', type=str)
parser.add_argument('--majority_at', default=None, type=int)
parser.add_argument('--temperature', default=0.0, type=float)
parser.add_argument('--top_p', default=1.0, type=float)
parser.add_argument('--max_tokens', default=256, type=int)
parser.add_argument('--lang', default='', type=str)
parser.add_argument('--n_examples', default=1319, type=int)

args = parser.parse_args()

DATA_PATH = f'../datasets/{args.dataset}_{args.lang}.jsonl'
OUTPUT_PATH = f'eval_results/{args.dataset}.jsonl'
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

examples = list(map(json.loads, open(DATA_PATH)))
examples = examples[:args.n_examples]

answer_symbol = {
    'en': 'solution()',
    'es': 'solucion()',
    'pt': 'solução()',
    'fr': 'solution()',
    'it': 'soluzione()',


}
itf = interface.ProgramInterface(
    stop='\n\n\n',
    get_answer_expr=answer_symbol[args.lang],
    model=args.model,
    verbose=args.verbose,
    lang=args.lang,
)

if args.append:
    lines = open(OUTPUT_PATH).readlines()
    num_skip_exps = len(lines)
    scores = [x['score'] for x in map(json.loads, lines)]
else:
    num_skip_exps = 0
    scores = []

with open(OUTPUT_PATH, 'a' if args.append else 'w') as f:
    pbar = tqdm.tqdm(examples[num_skip_exps:], initial=num_skip_exps, total=len(examples))
    save_histories = []
    for x in pbar:
        question = x['input']
        result = copy.copy(x)
        try:
            ans = itf.run(math_prompts.dict_prompts[args.lang]['MATH_PROMPT'].format(
                question=question), majority_at=args.majority_at, 
                temperature=args.temperature, top_p=args.top_p,
                max_tokens=args.max_tokens)
            ans = float(ans)
            score = 1 if abs(ans - x['target']) < 1e-3 else 0
        except Exception as e:
            print(e)
            ans = ''
            score = 0
        scores.append(score)
        scores.append(score)
        
        result['answer'] = ans
        result['score'] = score
        result['generation'] = itf.history
        f.write(json.dumps(result) + '\n')
        save_histories.append(itf.history)
        itf.clear_history()
        f.flush()
    file_responses = open(OUTPUT_PATH[:-5] + 'pickle', 'wb')
    pickle.dump(save_histories, file_responses)
    file_responses.close()
print(f'Accuracy - {sum(scores) / len(scores)}')
