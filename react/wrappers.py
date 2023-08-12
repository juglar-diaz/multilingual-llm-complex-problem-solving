import json
import os
import gym
import numpy as np
import re
import string
from collections import Counter
import pandas as pd
    
DATA_DIR = "data"
HOTPOTQA_SPLIT_FILE = {
  "dev": "hotpot_dev_v1_simplified_multilingual.json",
}

FEVER_SPLIT_FILE = {
  "dev": "fever_paper_dev_multilingual.json",
}


dict_str_code_en = {
    'Action': 'Action', 
    'Observation': 'Observation',
    'yes': 'yes',
    'no': 'no',
    'noanswer': 'noanswer',
    'Episode finished, reward': 'Episode finished, reward',
    'question': 'Question',
    'claim': 'Claim',
    }

dict_str_code_es = {
    'Action': 'Acción', 
    'Observation': 'Observación',
    'yes': 'si',
    'no': 'no',
    'noanswer': 'sinrespuesta',
    'Episode finished, reward': 'Episodio terminado, recompensa',
    'question': 'Pregunta',
    'claim': 'Afirmación',
    }

dict_str_code_pt = {
    'Action': 'Ação', 
    'Observation': 'Observation',
    'yes': 'sim',
    'no': 'não',
    'noanswer': 'semresposta',
    'Episode finished, reward': 'Episódio finalizado, recompensa',
    'question': 'Pergunta',
    'claim': 'Alegação',
    }

dict_str_code_fr = {
    'Action': 'Action', 
    'Observation': 'Observation',
    'yes': 'oui',
    'no': 'non',
    'noanswer': 'pasderéponse',
    'Episode finished, reward': 'Épisode terminé, récompense',
    'question': 'Question',
    'claim': 'Affirmation',
    }

dict_str_code_it = {
    'Action': 'Azione', 
    'Observation': 'Observation',
    'yes': 'sì',
    'no': 'no',
    'noanswer': 'nessunarisposta',
    'Episode finished, reward': 'Episodio finito, ricompensa',
    'question': 'Domanda',
    'claim': 'Affermazione',
    }

dict_str_code = {
    'en': dict_str_code_en,
    'es': dict_str_code_es,
    'pt': dict_str_code_pt,
    'fr': dict_str_code_fr,
    'it': dict_str_code_it,
    }

class HistoryWrapper(gym.ObservationWrapper):
  def __init__(self, env, obs_format, prompt=None):
    super().__init__(env)
    assert obs_format in ["obs", "history"]
    if obs_format == "history":
      assert hasattr(self.env, "traj")
    self.obs_format = obs_format
    self.prompt = prompt if prompt is not None else ""

  def observation(self, obs, lang):
    Action = dict_str_code[lang]['Action']
    Observation = dict_str_code[lang]['Observation']
    if self.obs_format == "obs":
      return obs
    elif self.obs_format == "history":
      observation = self.env.traj["observations"][0] + "\n"
      for i, (o, a) in enumerate(zip(self.env.traj["observations"][1:], self.env.traj["actions"]), 1):
        observation += f"{Action} {i}: {a}\n{Observation} {i}: {o}\n\n"
      return self.prompt + observation
    

def normalize_answer(s):
  def remove_articles(text):
    return re.sub(r"\b(a|an|the)\b", " ", text)
  
  def white_space_fix(text):
      return " ".join(text.split())

  def remove_punc(text):
      exclude = set(string.punctuation)
      return "".join(ch for ch in text if ch not in exclude)

  def lower(text):
      return text.lower()

  return white_space_fix(remove_articles(remove_punc(lower(s))))

def f1_score(prediction, ground_truth, lang):
  normalized_prediction = normalize_answer(prediction)
  normalized_ground_truth = normalize_answer(ground_truth)

  ZERO_METRIC = (0, 0, 0)

  yes = dict_str_code[lang]['yes']
  no = dict_str_code[lang]['no']
  noanswer = dict_str_code[lang]['noanswer']
  if normalized_prediction in [yes, no, noanswer] and normalized_prediction != normalized_ground_truth:
    return ZERO_METRIC
  if normalized_ground_truth in [yes, no, noanswer] and normalized_prediction != normalized_ground_truth:
    return ZERO_METRIC
  
  prediction_tokens = normalized_prediction.split()
  ground_truth_tokens = normalized_ground_truth.split()
  common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
  num_same = sum(common.values())
  if num_same == 0:
    return ZERO_METRIC
  precision = 1.0 * num_same / len(prediction_tokens)
  recall = 1.0 * num_same / len(ground_truth_tokens)
  f1 = (2 * precision * recall) / (precision + recall)
  return f1, precision, recall
  
class HotPotQAWrapper(gym.Wrapper):
  def __init__(self, env, split, question= None, episode_finished= None):
    super().__init__(env)
    data_file = f"{DATA_DIR}/{HOTPOTQA_SPLIT_FILE[split]}"
    self.data = pd.read_json(data_file)
    self.lang = env.lang
    self.data = [(d[1][f"question_{self.lang}_gt"], d[1][f"answer_{self.lang}_gt"]) for d in self.data.iterrows()]
    self.data_idx = 0
    self.split = split
    if question:
      self.question = question
    else:
      self.question = dict_str_code[self.lang]['question'] + ': '

    if episode_finished:
      self.episode_finished = episode_finished
    else:
      self.episode_finished = dict_str_code[self.lang]["Episode finished, reward"] + ' = '

  def reset(self, seed=None, return_info=False, options=None, idx=None):
    self.env.reset(seed=seed, return_info=return_info, options=options)
    try:
      self.env.step('')
    except:
      pass
    self.env.reset(seed=seed, return_info=return_info, options=options)
    self.data_idx = int(np.random.randint(len(self.data))) if idx is None else idx
    observation = f"{self.question}{self.data[self.data_idx][0]}"
    info = self._get_info()
    return (observation, info) if return_info else observation

  def _get_info(self):
    return {
      "steps": self.steps, 
      "answer": self.answer,
      "question": self.data[self.data_idx][0], 
      "hotpot_split": self.split
    }

  def get_reward(self, info):
    if info['answer'] is not None:
      pred = normalize_answer(self.data[self.data_idx][1])
      gt = normalize_answer(info['answer'])
      score = (set(pred.split()) == set(gt.split()))
      return int(score)
    return 0
  
  def get_metrics(self, info):
    if info['answer'] is not None:
      pred = normalize_answer(self.data[self.data_idx][1])
      gt = normalize_answer(info['answer'])
      em = (pred == gt)
      f1 = f1_score(pred, gt)[0]
      return {'reward': em, 'em': em, 'f1': f1}
    return {'reward': 0, 'em': 0, 'f1': 0}

  def step(self, action):
    # TODO: first step obs does not have question. 
    obs, _, done, info = self.env.step(action)
    reward = self.get_reward(info)
    if done:
      obs = f"{self.episode_finished}{reward}\n"
      info.update({"gt_answer": self.data[self.data_idx][1], "question_idx": self.data_idx})
      info.update(self.get_metrics(info))
    return obs, reward, done, info
  
  def __len__(self):
    return len(self.data)

class FeverWrapper(gym.Wrapper):
  def __init__(self, env, split, claim= None, episode_finished= None):
    super().__init__(env)
    data_file = f"{DATA_DIR}/{FEVER_SPLIT_FILE[split]}"
    self.data = pd.read_json(data_file)
    self.lang = env.lang
    self.data = [(d[1][f"claim_{self.lang}_gt"], d[1][f"label_{self.lang}_gt"]) for d in self.data.iterrows()]

    self.data_idx = 0
    self.split = split

    if claim:
      self.claim = claim
    else:
      self.claim = dict_str_code[self.lang]['claim'] + ': '

    if episode_finished:
      self.episode_finished = episode_finished
    else:
      self.episode_finished = dict_str_code[self.lang]["Episode finished, reward"] + ' = '


  def reset(self, seed=None, return_info=False, options=None, idx=None):
    self.env.reset(seed=seed, return_info=return_info, options=options)
    try:
      self.env.step('')
    except:
      pass
    self.env.reset(seed=seed, return_info=return_info, options=options)
    self.data_idx = int(np.random.randint(len(self.data))) if idx is None else idx
    observation = f"{self.claim}{self.data[self.data_idx][0]}"
    info = self._get_info()
    return (observation, info) if return_info else observation

  def _get_info(self):
    return {
      "steps": self.steps, 
      "answer": self.answer,
      "question": self.data[self.data_idx][0], 
      "fever_split": self.split
    }

  def get_reward(self, info):
    if info['answer'] is not None:
      label = normalize_answer(self.data[self.data_idx][1])
      pred = normalize_answer(info['answer'])

      print('label', label, 'prediction', pred)
      if set(pred.split()) == set(label.split()):
        return 1
    return 0

  def step(self, action):

    # TODO: first step obs does not have question. 
    obs, _, done, info = self.env.step(action)
    reward = self.get_reward(info)
    if done:
      obs = f"{self.episode_finished}{reward}\n"
      info.update({"gt_answer": self.data[self.data_idx][1], "question_idx": self.data_idx})
      info.update({'em': reward, 'reward': reward, 'f1': reward})
    

    return obs, reward, done, info
    
  def __len__(self):
    return len(self.data)
  
  
class LoggingWrapper(gym.Wrapper):
  def __init__(self, env, folder="trajs", file_id=None):
    super().__init__(env)
    self.trajs = []
    self.traj = {"observations": [], "actions": []}
    self.folder = folder
    self.file_id = np.random.randint(0, 10000000) if file_id is None else file_id
    self.file_path = f"{self.folder}/{self.file_id}.json"
    os.makedirs("trajs", exist_ok=True)

  def __len__(self):
    return len(self.env.data)
  

  def reset(self, seed=None, return_info=False, options=None, idx=None):
    output = self.env.reset(seed=seed, return_info=return_info, options=options, idx=idx)
    observation = output[0] if return_info else output
    self.traj = {"observations": [observation], "actions": []}
    return output

  def step(self, action):
    obs, reward, done, info = self.env.step(action)
    self.traj["observations"].append(obs)
    self.traj["actions"].append(action)
    if done:
      self.traj.update(info)
    
    return obs, reward, done, info

  def update_record(self):
    if len(self.traj) > 0:
      self.trajs.append(self.traj)
      self.traj = {"observations": [], "actions": []}
  
  def write(self):
    self.update_record()
    with open(self.file_path, "w") as f:
      json.dump(self.trajs, f)
      print(f"Saved trajs to trajs/{self.file_id}.json")
    
  def close(self):
    self.write()
