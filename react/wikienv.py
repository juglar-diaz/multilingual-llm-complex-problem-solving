import ast
import json
import time
import gym
import requests
from bs4 import BeautifulSoup
import sys
sys.path.append("..")

# import wikipedia

dict_str_code_en = {
    'Could not find': 'Could not find', 
    'Similar': 'Similar',
    'may refer to': 'may refer to',
    'No more results': 'No more results',
    'search': 'search',
    'lookup': 'find',
    'Result': 'Result',
    'finish': 'finish',
    'Episode finished, reward': 'Episode finished, reward',
    'think': 'think',
    'Invalid action': 'Invalid action',
    'Nice thought': 'Nice thought',
    'Thought': 'Thought',
    'and': 'and',
    'Interact with Wikipedia using': 'Interact with Wikipedia using',
    }

dict_str_code_es = {
    'Could not find': 'No pudo encontrar', 
    'Similar': 'Similar',
    'may refer to': 'puede referirse a',
    'No more results': 'No hay más resultados',
    'search': 'buscar',
    'lookup': 'encontrar',
    'Result': 'Resultado',
    'finish': 'finalizar',
    'Episode finished, reward': 'Episodio terminado, recompensa',
    'think': 'pensar',
    'Invalid action': 'Acción no válida',
    'Nice thought': 'Buena idea',
    'Thought': 'Idea',
    'and': 'y',
    'Interact with Wikipedia using': 'Interactuar con Wikipedia usando',
    }



dict_str_code_pt = {
    'Could not find': 'Não consegui encontrar', 
    'Similar': 'Semelhante',
    'may refer to': 'pode se referir a',
    'No more results': 'Sem mais resultados',
    'search': 'pesquisar',
    'lookup': 'encontre',
    'Result': 'Resultado',
    'finish': 'concluir',
    'Episode finished, reward': 'Episódio finalizado, recompensa',
    'think': 'pensar',
    'Invalid action': 'Ação inválida',
    'Nice thought': 'Belo pensamento',
    'Thought': 'Pensamento',
    'and': 'e',
    'Interact with Wikipedia using': 'Interaja com a Wikipédia usando',
    }

dict_str_code_fr = {
    'Could not find': "N'a pas pu trouver", 
    'Similar': 'Similaire',
    'may refer to': "peut faire référence à",
    'No more results': 'Plus de résultats',
    'search': 'rechercher',
    'lookup': 'chercher',
    'Result': 'Résultat',
    'finish': 'terminer',
    'Episode finished, reward': 'Épisode terminé, récompense',
    'think': 'penser',
    'Invalid action': 'Action invalide',
    'Nice thought': 'Bonne idée',
    'Thought': 'Idée',
    'and': 'et',
    'Interact with Wikipedia using': 'Interagissez avec Wikipédia en utilisant',
    }

dict_str_code_it = {
    'Could not find': 'Non ho potuto trovare', 
    'Similar': 'Simile',
    'may refer to': 'può fare riferimento a',
    'No more results': 'Niente più risultati',
    'search': 'ricerca',
    'lookup': 'trova',
    'Result': 'Risultato',
    'finish': 'termina',
    'Episode finished, reward': 'Episodio finito, ricompensa',
    'think': 'pensare',
    'Invalid action': 'Azione non valida',
    'Nice thought': 'Bel pensiero',
    'Thought': 'Pensiero',
    'and': 'e',
    'Interact with Wikipedia using': 'Interagisci con Wikipedia utilizzando',
    }

dict_str_code = {
    'en': dict_str_code_en,
    'es': dict_str_code_es,
    'pt': dict_str_code_pt,
    'fr': dict_str_code_fr,
    'it': dict_str_code_it,
    }


def clean_str(p):
  return p.encode().decode("unicode-escape").encode("latin1").decode("utf-8")


class textSpace(gym.spaces.Space):
  def contains(self, x) -> bool:
    """Return boolean specifying if x is a valid member of this space."""
    return isinstance(x, str)


class WikiEnv(gym.Env):

  def __init__(self, lang):
    """
      Initialize the environment.
    """
    super().__init__()
    self.page = None  # current Wikipedia page
    self.obs = None  # current observation
    self.lookup_keyword = None  # current lookup keyword
    self.lookup_list = None  # list of paragraphs containing current lookup keyword
    self.lookup_cnt = None  # current lookup index
    self.steps = 0  # current number of steps
    self.answer = None  # current answer from the agent
    self.observation_space = self.action_space = textSpace()
    self.search_time = 0
    self.num_searches = 0
    self.lang = lang
  def _get_obs(self):
    return self.obs

  def _get_info(self):
    return {"steps": self.steps, "answer": self.answer}

  def reset(self, seed=None, return_info=False, options=None):
    # We need the following line to seed self.np_random
    # super().reset(seed=seed)
    search = dict_str_code[self.lang]['search']
    lookup = dict_str_code[self.lang]['lookup']
    and_ = dict_str_code[self.lang]['and']
    finish = dict_str_code[self.lang]['finish']

    Interact_with_Wikipedia_using = dict_str_code[self.lang]['Interact with Wikipedia using']
      
    self.obs = (f"{Interact_with_Wikipedia_using} {search}[], {lookup}[], {and_} {finish}[].\n")
    self.page = None
    self.lookup_keyword = None
    self.lookup_list = None
    self.lookup_cnt = None
    self.steps = 0
    self.answer = None
    observation = self._get_obs()
    info = self._get_info()
    return (observation, info) if return_info else observation

  def construct_lookup_list(self, keyword):
    # find all paragraphs
    if self.page is None:
      return []
    paragraphs = self.page.split("\n")
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    # find all sentence
    sentences = []
    for p in paragraphs:
      sentences += p.split('. ')
    sentences = [s.strip() + '.' for s in sentences if s.strip()]

    parts = sentences
    parts = [p for p in parts if keyword.lower() in p.lower()]
    return parts

  @staticmethod
  def get_page_obs(page):
    # find all paragraphs
    paragraphs = page.split("\n")
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    # find all sentence
    sentences = []
    for p in paragraphs:
      sentences += p.split('. ')
    sentences = [s.strip() + '.' for s in sentences if s.strip()]
    return ' '.join(sentences[:5])

    # ps = page.split("\n")
    # ret = ps[0]
    # for i in range(1, len(ps)):
    #   if len((ret + ps[i]).split(" ")) <= 50:
    #     ret += ps[i]
    #   else:
    #     break
    # return ret

  def search_step(self, entity):
    #entity = translate_text(target='en', text=entity)

    entity_ = entity.replace(" ", "+")
    search_url = f"https://en.wikipedia.org/w/index.php?search={entity_}"
    search_url = f"https://{self.lang}.wikipedia.org/w/index.php?search={entity_}"

    old_time = time.time()
    response_text = requests.get(search_url).text
    self.search_time += time.time() - old_time
    self.num_searches += 1
    soup = BeautifulSoup(response_text, features="html.parser")
    result_divs = soup.find_all("div", {"class": "mw-search-result-heading"})
    if result_divs:  # mismatch

      self.result_titles = [clean_str(div.get_text().strip()) for div in result_divs]
      Could_not_find = dict_str_code[self.lang]['Could not find']
      Similar = dict_str_code[self.lang]['Similar']
      self.obs = f"{Could_not_find} {entity}. {Similar}: {self.result_titles[:5]}."

    else:

      page = [p.get_text().strip() for p in soup.find_all("p") + soup.find_all("ul")]
      may_refer_to = dict_str_code['en']['may refer to']
      if any(f"{may_refer_to}:" in p for p in page):
        self.search_step("[" + entity + "]")
      else:
        self.page = ""
        for p in page:
          if len(p.split(" ")) > 2:
            self.page += clean_str(p)
            if not p.endswith("\n"):
              self.page += "\n"
        #self.obs = translate_text(target=self.lang, text=self.get_page_obs(self.page))
        self.obs = self.get_page_obs(self.page)
        self.lookup_keyword = self.lookup_list = self.lookup_cnt = None
  
  def step(self, action):
    reward = 0
    done = False
    action = action.strip()
    if self.answer is not None:  # already finished
      done = True
      return self.obs, reward, done, self._get_info()
    
    search = dict_str_code[self.lang]['search']
    lookup = dict_str_code[self.lang]['lookup']
    no_more_results = dict_str_code[self.lang]['No more results']
    Result = dict_str_code[self.lang]['Result']
    finish = dict_str_code[self.lang]['finish']
    Episode_finished_reward = dict_str_code[self.lang]['Episode finished, reward']
    think = dict_str_code[self.lang]['think']
    Invalid_action = dict_str_code[self.lang]['Invalid action']
    Nice_thought = dict_str_code[self.lang]['Nice thought']

    if action.startswith(f"{search}[") and action.endswith("]"):

      entity = action[len(f"{search}["):-1]
      # entity_ = entity.replace(" ", "_")
      # search_url = f"https://en.wikipedia.org/wiki/{entity_}"
      self.search_step(entity)
    elif action.startswith(f"{lookup}[") and action.endswith("]"):

      keyword = action[len(f"{lookup}["):-1]
      if self.lookup_keyword != keyword:  # reset lookup
        self.lookup_keyword = keyword
        self.lookup_list = self.construct_lookup_list(keyword)
        self.lookup_cnt = 0
      if self.lookup_cnt >= len(self.lookup_list):
        self.obs = f"{no_more_results}.\n"
      else:
        self.obs = f"({Result} {self.lookup_cnt + 1} / {len(self.lookup_list)}) " + self.lookup_list[self.lookup_cnt]
        self.lookup_cnt += 1
    elif action.startswith(f"{finish}[") and action.endswith("]"):

      answer = action[len(f"{finish}["):-1]
      self.answer = answer
      done = True
      self.obs = f"{Episode_finished_reward} = {reward}\n"
    elif action.startswith(f"{think}[") and action.endswith("]"):
      
      self.obs = f"{Nice_thought}."
    else:
      self.obs = f"{Invalid_action}: {action}"

    self.steps += 1

    return self.obs, reward, done, self._get_info()
  
  def get_time_info(self):
    speed = self.search_time / self.num_searches if self.num_searches else 0
    return {
        "call_speed": speed,
        "call_time": self.search_time,
        "num_calls": self.num_searches,
    }
