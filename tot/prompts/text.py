dict_prompts_en = {

'standard_prompt': """
Write a coherent passage of 4 short paragraphs. The end sentence of each paragraph must be: {input}
""",

'cot_prompt': """
Write a coherent passage of 4 short paragraphs. The end sentence of each paragraph must be: {input}

Make a plan then write. Your output should be of the following format:

Plan:
Your plan here.

Passage:
Your passage here.
""",

'vote_prompt': """Given an instruction and several choices, decide which choice is most promising. Analyze each choice in detail, then conclude in the last line "The best choice is {s}", where s the integer id of the choice.
""",

'compare_prompt': """Briefly analyze the coherency of the following two passages. Conclude in the last line "The more coherent passage is 1", "The more coherent passage is 2", or "The two passages are similarly coherent".
""",

'score_prompt': """Analyze the following passage, then at the last line conclude "Thus the coherency score is {s}", where s is an integer from 1 to 10.
"""

}

dict_prompts_es = {

'standard_prompt': """
Escribir un pasaje coherente de 4 párrafos cortos. La oración final de cada párrafo debe ser: {input}
""",

'cot_prompt': """
Escribir un pasaje coherente de 4 párrafos cortos. La oración final de cada párrafo debe ser: {input}

Haz un plan y luego escribe. Su salida debe tener el siguiente formato:

Plan:
Tu plan aquí.

Pasaje:
Tu pasaje aquí.
""",

'vote_prompt': """Dada una instrucción y varias opciones, decida qué opción es la más prometedora. Analice cada opción en detalle, luego concluya en la última línea "La mejor opción es {s}", donde s es el id entero de la opción.
""",

'compare_prompt': """Analice brevemente la coherencia de los siguientes dos pasajes. Concluya en la última línea "El pasaje más coherente es 1", "El pasaje más coherente es 2" o "Los dos pasajes son igualmente coherentes".
""",

'score_prompt': """Analice el siguiente pasaje, luego, en la última línea, concluya "Así, la puntuación de coherencia es {s}", donde s es un número entero del 1 al 10.
"""

}

dict_prompts_pt = {

'standard_prompt': """
Escreva uma passagem coerente de 4 parágrafos curtos. A frase final de cada parágrafo deve ser: {input}
""",

'cot_prompt': """
Escreva uma passagem coerente de 4 parágrafos curtos. A frase final de cada parágrafo deve ser: {input}

Faça um plano e depois escreva. Sua saída deve ter o seguinte formato:

Plano:
Seu plano aqui.

Passagem:
Sua passagem aqui.
""",

'vote_prompt': """Dada uma instrução e várias opções, decida qual é a mais promissora. Analise cada escolha em detalhes e conclua na última linha "A melhor escolha é {s}", onde s é o id inteiro da escolha.
""",

'compare_prompt': """Analise brevemente a coerência das duas passagens seguintes. Conclua na última linha "A passagem mais coerente é 1", "A passagem mais coerente é 2" ou "As duas passagens são similarmente coerentes".
""",

'score_prompt': """Analise a seguinte passagem e, na última linha, conclua "Assim, a pontuação de coerência é {s}", onde s é um número inteiro de 1 a 10.
"""

}

dict_prompts_fr = {

'standard_prompt': """
Rédigez un passage cohérent de 4 courts paragraphes. La phrase de fin de chaque paragraphe doit être : {input}
""",

'cot_prompt': """
Rédigez un passage cohérent de 4 courts paragraphes. La phrase de fin de chaque paragraphe doit être : {input}

Faites un plan puis écrivez. Votre sortie doit être au format suivant :

Plan:
Votre plan ici.

Passage:
Votre passage ici.
""",

'vote_prompt': """Étant donné une instruction et plusieurs choix, décidez quel choix est le plus prometteur. Analysez chaque choix en détail, puis concluez à la dernière ligne "Le meilleur choix est {s}", où s l'identifiant entier du choix.
""",

'compare_prompt': """Analysez brièvement la cohérence des deux passages suivants. Concluez dans la dernière ligne "Le passage le plus cohérent est 1", "Le passage le plus cohérent est 2", ou "Les deux passages sont également cohérents".
""",

'score_prompt': """Analysez le passage suivant, puis à la dernière ligne concluez "Ainsi le score de cohérence est de {s}", où s est un entier de 1 à 10.
"""

}

dict_prompts_it = {

'standard_prompt': """
Scrivi un brano coerente di 4 brevi paragrafi. La frase finale di ogni paragrafo deve essere: {input}
""",

'cot_prompt': """
Scrivi un brano coerente di 4 brevi paragrafi. La frase finale di ogni paragrafo deve essere: {input}

Fai un piano e poi scrivi. Il tuo output dovrebbe essere nel seguente formato:

Piano:
Il tuo piano qui.

Passaggio:
Il tuo passaggio qui.
""",

'vote_prompt': """Date un'istruzione e diverse scelte, decidi quale è la più promettente. Analizza ogni scelta in dettaglio, quindi concludi nell'ultima riga "La scelta migliore è {s}", dove s è l'id intero della scelta.
""",

'compare_prompt': """Analizziamo brevemente la coerenza dei due passaggi seguenti. Concludi nell'ultima riga "Il passaggio più coerente è 1", "Il passaggio più coerente è 2", oppure "I due passaggi sono similmente coerenti".
""",

'score_prompt': """Analizza il seguente passaggio, quindi all'ultima riga concludi "Quindi il punteggio di coerenza è {s}", dove s è un numero intero compreso tra 1 e 10.
"""

}

dict_prompts = {
    'en': dict_prompts_en,
    'es': dict_prompts_es,
    'pt': dict_prompts_pt,
    'fr': dict_prompts_fr,
    'it': dict_prompts_it,
    }