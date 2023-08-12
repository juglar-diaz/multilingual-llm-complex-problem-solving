import os
import json
import itertools
import argparse
import numpy as np
from functools import partial
from backend import call_llm_tot
from tasks import get_task

def get_value(task, x, y, n_evaluate_sample, cache_value=True, lang=''):
    value_prompt = task.value_prompt_wrap(x, y, lang)
    #print('value_prompt', value_prompt)
    if cache_value and value_prompt in task.value_cache:
        return task.value_cache[value_prompt]
    value_outputs = call_llm_tot(value_prompt, n=n_evaluate_sample, stop=None)
    #print('value_outputs', value_outputs)

    value = task.value_outputs_unwrap(x, y, value_outputs, lang=lang)
    #print('value_outputs_unwrap', value)

    if cache_value:
        task.value_cache[value_prompt] = value
    return value

def get_values(task, x, ys, n_evaluate_sample, cache_value=True, lang=''):
    values = []
    local_value_cache = {}
    for y in ys:  # each partial output
        if y in local_value_cache:  # avoid duplicate candidates
            value = 0
        else:    
            value = get_value(task, x, y, n_evaluate_sample, cache_value=cache_value, lang=lang)
            local_value_cache[y] = value
        values.append(value)
    return values

def get_votes(task, x, ys, n_evaluate_sample, lang):
    vote_prompt = task.vote_prompt_wrap(x, ys, lang)
    vote_outputs = call_llm_tot(vote_prompt, n=n_evaluate_sample, stop=None)
    values = task.vote_outputs_unwrap(vote_outputs, len(ys), lang)
    return values

def get_proposals(task, x, y, lang):
    #print('x', 'y', x, y,)
    
    propose_prompt = task.propose_prompt_wrap(x, y, lang)
    #print('propose_prompt', propose_prompt)

    proposals = call_llm_tot(propose_prompt, n=1, stop=None)[0].split('\n')
    #print('proposals', proposals)

    result = [y + _ + '\n' for _ in proposals]
    #print('result proposals', result)

    return result

def get_samples(task, x, y, n_generate_sample, prompt_sample, stop, lang):
    if prompt_sample == 'standard':
        prompt = task.standard_prompt_wrap(x, y, lang)
    elif prompt_sample == 'cot':
        prompt = task.cot_prompt_wrap(x, y, lang)
    else:
        raise ValueError(f'prompt_sample {prompt_sample} not recognized')
    samples = call_llm_tot(prompt, n=n_generate_sample, stop=stop)
    return [y + _ for _ in samples]

def solve(args, task, idx, to_print=False, lang=''):
    x = task.get_input(idx)  # input
    ys = ['']  # current output candidates
    infos = []

    for step in range(task.steps):
        #print('Step #', step)
        
        # generation
        if args.method_generate == 'sample':
            new_ys = [get_samples(task, x, y, args.n_generate_sample, prompt_sample=args.prompt_sample, stop=task.stops[step], lang=lang) for y in ys]
        elif args.method_generate == 'propose':
            new_ys = [get_proposals(task, x, y, lang) for y in ys]
        new_ys = list(itertools.chain(*new_ys))

        ids = list(range(len(new_ys)))
        
        #print('Got new_ys of len ', len(new_ys))
        # evaluation
        if args.method_evaluate == 'vote':
            values = get_votes(task, x, new_ys, args.n_evaluate_sample, lang)
        elif args.method_evaluate == 'value':
            values = get_values(task, x, new_ys, args.n_evaluate_sample, lang=lang)

        # selection
        if args.method_select == 'sample':
            ps = np.array(values) / sum(values)
            select_ids = np.random.choice(ids, size=args.n_select_sample, p=ps).tolist()
        elif args.method_select == 'greedy':
            select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[:args.n_select_sample]
        select_new_ys = [new_ys[select_id] for select_id in select_ids]


        # log
        if to_print: 
            sorted_new_ys, sorted_values = zip(*sorted(zip(new_ys, values), key=lambda x: x[1], reverse=True))
            print(f'-- new_ys --: {sorted_new_ys}\n-- sol values --: {sorted_values}\n-- choices --: {select_new_ys}\n')
        
        infos.append({'step': step, 'x': x, 'ys': ys, 'new_ys': new_ys, 'values': values, 'select_new_ys': select_new_ys})
        ys = select_new_ys
    
    if to_print: 
        print(ys)
    return ys, {'steps': infos}

def naive_solve(args, task, idx, to_print=False, lang=''):
    x = task.get_input(idx)  # input
    ys = get_samples(task, x, '', args.n_generate_sample, args.prompt_sample, stop=None, lang=lang)
    return ys, {}

def run(args):
    task = get_task(args.task, args.task_file_path, args.lang)
    logs, cnt_avg, cnt_any = [], 0, 0
    global call_llm_tot
    call_llm_tot = partial(call_llm_tot, model=args.backend, temperature=args.temperature)
    if args.naive_run:
        file = f'logs/{args.task}/{args.backend}_{args.temperature}_naive_{args.prompt_sample}_sample_{args.n_generate_sample}_start{args.task_start_index}_end{args.task_end_index}.json'
    else:
        file = f'logs/{args.task}/{args.backend}_{args.temperature}_{args.method_generate}{args.n_generate_sample}_{args.method_evaluate}{args.n_evaluate_sample}_{args.method_select}{args.n_select_sample}_start{args.task_start_index}_end{args.task_end_index}.json'
    os.makedirs(os.path.dirname(file), exist_ok=True)

    for i in range(args.task_start_index, args.task_end_index):
        # solve
        if args.naive_run:
            ys, info = naive_solve(args, task, i, lang=args.lang) 
        else:
            ys, info = solve(args, task, i, lang=args.lang)

        # log
        infos = [task.test_output(i, y, args.backend) for y in ys]


        info.update({'idx': i, 'ys': ys, 'infos': infos,})
        logs.append(info)
        with open(file, 'w') as f:
            json.dump(logs, f, indent=4)
        

        # log main metric
        accs = [info['r'] for info in infos]
        cnt_avg += sum(accs) / len(accs)
        cnt_any += any(accs)
        avg_so_far = cnt_avg / (i + 1 - args.task_start_index)
        
        if args.task == 'text':
            scores = [info['rs'] for info in infos]
            print(i+1, 'scores', scores, 'accs', accs, 'cnt_avg', cnt_avg, 'avg_so_far', avg_so_far, '\n')
        else:
            print(i, 'sum(accs)', sum(accs), 'cnt_avg', cnt_avg, 'cnt_any', cnt_any, '\n')

    n = args.task_end_index - args.task_start_index
    print(cnt_avg / n, cnt_any / n)


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument('--backend', type=str, default='gpt-3.5-turbo')
    args.add_argument('--temperature', type=float, default=0.7)
    args.add_argument('--lang', type=str, required=True, choices=['en', 'es', 'fr', 'pt', 'it'])
    args.add_argument('--task', type=str, required=True, choices=['game24', 'text', 'crosswords'])
    args.add_argument('--task_file_path', type=str, required=True)
    args.add_argument('--task_start_index', type=int, default=900)
    args.add_argument('--task_end_index', type=int, default=1000)

    args.add_argument('--naive_run', action='store_true')
    args.add_argument('--prompt_sample', type=str, choices=['standard', 'cot'])  # only used when method_generate = sample, or naive_run

    args.add_argument('--method_generate', type=str, choices=['sample', 'propose'])
    args.add_argument('--method_evaluate', type=str, choices=['value', 'vote'])
    args.add_argument('--method_select', type=str, choices=['sample', 'greedy'])
    args.add_argument('--n_generate_sample', type=int, default=1)  # only thing needed if naive_run
    args.add_argument('--n_evaluate_sample', type=int, default=1)
    args.add_argument('--n_select_sample', type=int, default=1)

    args = args.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    print(args)
    run(args)