dict_prompts_en = {
# 5-shot
'standard_prompt' : '''Use numbers and basic arithmetic operations (+ - * /) to obtain 24.
Input: 4 4 6 8
Answer: (4 + 8) * (6 - 4) = 24
Input: 2 9 10 12
Answer: 2 * 12 * (10 - 9) = 24
Input: 4 9 10 13
Answer: (13 - 9) * (10 - 4) = 24
Input: 1 4 8 8
Answer: (8 / 4 + 1) * 8 = 24
Input: 5 5 5 9
Answer: 5 + 5 + 5 + 9 = 24
Input: {input}
''',

# 5-shot
'cot_prompt' : '''Use numbers and basic arithmetic operations (+ - * /) to obtain 24. Each step, you are only allowed to choose two of the remaining numbers to obtain a new number.
Input: 4 4 6 8
Steps:
4 + 8 = 12 (left: 4 6 12)
6 - 4 = 2 (left: 2 12)
2 * 12 = 24 (left: 24)
Answer: (6 - 4) * (4 + 8) = 24
Input: 2 9 10 12
Steps:
12 * 2 = 24 (left: 9 10 24)
10 - 9 = 1 (left: 1 24)
24 * 1 = 24 (left: 24)
Answer: (12 * 2) * (10 - 9) = 24
Input: 4 9 10 13
Steps:
13 - 10 = 3 (left: 3 4 9)
9 - 3 = 6 (left: 4 6)
4 * 6 = 24 (left: 24)
Answer: 4 * (9 - (13 - 10)) = 24
Input: 1 4 8 8
Steps:
8 / 4 = 2 (left: 1 2 8)
1 + 2 = 3 (left: 3 8)
3 * 8 = 24 (left: 24)
Answer: (1 + 8 / 4) * 8 = 24
Input: 5 5 5 9
Steps:
5 + 5 = 10 (left: 5 9 10)
10 + 5 = 15 (left: 9 15)
15 + 9 = 24 (left: 24)
Answer: ((5 + 5) + 5) + 9 = 24
Input: {input}
''',

# 1-shot
'propose_prompt' : '''Input: 2 8 8 14
Possible next steps:
2 + 8 = 10 (left: 8 10 14)
8 / 2 = 4 (left: 4 8 14)
14 + 2 = 16 (left: 8 8 16)
2 * 8 = 16 (left: 8 14 16)
8 - 2 = 6 (left: 6 8 14)
14 - 8 = 6 (left: 2 6 8)
14 /  2 = 7 (left: 7 8 8)
14 - 2 = 12 (left: 8 8 12)
Input: {input}
Possible next steps:
''',

'value_prompt' : '''Evaluate if given numbers can reach 24 (sure/likely/impossible)
10 14
10 + 14 = 24
sure
11 12
11 + 12 = 23
12 - 11 = 1
11 * 12 = 132
11 / 12 = 0.91
impossible
4 4 10
4 + 4 + 10 = 8 + 10 = 18
4 * 10 - 4 = 40 - 4 = 36
(10 - 4) * 4 = 6 * 4 = 24
sure
4 9 11
9 + 11 + 4 = 20 + 4 = 24
sure
5 7 8
5 + 7 + 8 = 12 + 8 = 20
(8 - 5) * 7 = 3 * 7 = 21
I cannot obtain 24 now, but numbers are within a reasonable range
likely
5 6 6
5 + 6 + 6 = 17
(6 - 5) * 6 = 1 * 6 = 6
I cannot obtain 24 now, but numbers are within a reasonable range
likely
10 10 11
10 + 10 + 11 = 31
(11 - 10) * 10 = 10
10 10 10 are all too big
impossible
1 3 3
1 * 3 * 3 = 9
(1 + 3) * 3 = 12
1 3 3 are all too small
impossible
{input}
''',

'value_last_step_prompt' : '''Use numbers and basic arithmetic operations (+ - * /) to obtain 24. Given an input and an answer, give a judgement (sure/impossible) if the answer is correct, i.e. it uses each input exactly once and no other numbers, and reach 24.
Input: 4 4 6 8
Answer: (4 + 8) * (6 - 4) = 24
Judge: 
sure
Input: 2 9 10 12
Answer: 2 * 12 * (10 - 9) = 24
Judge: 
sure
Input: 4 9 10 13
Answer: (13 - 9) * (10 - 4) = 24
Judge: 
sure
Input: 4 4 6 8
Answer: (4 + 8) * (6 - 4) + 1 = 25
Judge: 
impossible
Input: 2 9 10 12
Answer: 2 * (12 - 10) = 24
Judge: 
impossible
Input: 4 9 10 13
Answer: (13 - 4) * (10 - 9) = 24
Judge: 
impossible
Input: {input}
Answer: {answer}
Judge:'''
}



dict_prompts_es = {
# 5-intentos
'standard_prompt' : '''Usa números y operaciones aritméticas básicas (+ - * /) para obtener 24.
Entrada: 4 4 6 8
Respuesta: (4 + 8) * (6 - 4) = 24
Entrada: 2 9 10 12
Respuesta: 2 * 12 * (10 - 9) = 24
Entrada: 4 9 10 13
Respuesta: (13 - 9) * (10 - 4) = 24
Entrada: 1 4 8 8
Respuesta: (8 / 4 + 1) * 8 = 24
Entrada: 5 5 5 9
Respuesta: 5 + 5 + 5 + 9 = 24
Entrada: {input}
''',

# 5-intentos
'cot_prompt' : '''Usa números y operaciones aritméticas básicas (+ - * /) para obtener 24. En cada paso, solo puede elegir dos de los números que quedan para obtener un nuevo número.
Entrada: 4 4 6 8
Pasos:
4 + 8 = 12 (quedan: 4 6 12)
6 - 4 = 2 (quedan: 2 12)
2 * 12 = 24 (quedan: 24)
Respuesta: (6 - 4) * (4 + 8) = 24
Entrada: 2 9 10 12
Pasos:
12 * 2 = 24 (quedan: 9 10 24)
10 - 9 = 1 (quedan: 1 24)
24 * 1 = 24 (quedan: 24)
Respuesta: (12 * 2) * (10 - 9) = 24
Entrada: 4 9 10 13
Pasos:
13 - 10 = 3 (quedan: 3 4 9)
9 - 3 = 6 (quedan: 4 6)
4 * 6 = 24 (quedan: 24)
Respuesta: 4 * (9 - (13 - 10)) = 24
Entrada: 1 4 8 8
Pasos:
8 / 4 = 2 (quedan: 1 2 8)
1 + 2 = 3 (quedan: 3 8)
3 * 8 = 24 (quedan: 24)
Respuesta: (1 + 8 / 4) * 8 = 24
Entrada: 5 5 5 9
Pasos:
5 + 5 = 10 (quedan: 5 9 10)
10 + 5 = 15 (quedan: 9 15)
15 + 9 = 24 (quedan: 24)
Respuesta: ((5 + 5) + 5) + 9 = 24
Entrada: {input}
''',

# 1-intento
'propose_prompt' : '''Entrada: 2 8 8 14
Posibles próximos pasos:
2 + 8 = 10 (quedan: 8 10 14)
8 / 2 = 4 (quedan: 4 8 14)
14 + 2 = 16 (quedan: 8 8 16)
2 * 8 = 16 (quedan: 8 14 16)
8 - 2 = 6 (quedan: 6 8 14)
14 - 8 = 6 (quedan: 2 6 8)
14 /  2 = 7 (quedan: 7 8 8)
14 - 2 = 12 (quedan: 8 8 12)
Entrada: {input}
Posibles próximos pasos:
''',

'value_prompt' : '''Evaluar si los números dados pueden llegar a 24 (seguro/probable/imposible)
10 14
10 + 14 = 24
seguro
11 12
11 + 12 = 23
12 - 11 = 1
11 * 12 = 132
11 / 12 = 0.91
imposible
4 4 10
4 + 4 + 10 = 8 + 10 = 18
4 * 10 - 4 = 40 - 4 = 36
(10 - 4) * 4 = 6 * 4 = 24
seguro
4 9 11
9 + 11 + 4 = 20 + 4 = 24
seguro
5 7 8
5 + 7 + 8 = 12 + 8 = 20
(8 - 5) * 7 = 3 * 7 = 21
No puedo obtener 24 ahora, pero los números están dentro de un rango razonable
probable
5 6 6
5 + 6 + 6 = 17
(6 - 5) * 6 = 1 * 6 = 6
No puedo obtener 24 ahora, pero los números están dentro de un rango razonable
probable
10 10 11
10 + 10 + 11 = 31
(11 - 10) * 10 = 10
10 10 10 son todos demasiado grandes
imposible
1 3 3
1 * 3 * 3 = 9
(1 + 3) * 3 = 12
1 3 3 son todos demasiado pequeños
imposible
{input}
''',

'value_last_step_prompt' : '''Usa números y operaciones aritméticas básicas (+ - * /) para obtener 24. Dada una entrada y una respuesta, emita un juicio (seguro/imposible) si la respuesta es correcta, i.e. utiliza cada entrada exactamente una vez y ningún otro número, y llega a 24.
Entrada: 4 4 6 8
Respuesta: (4 + 8) * (6 - 4) = 24
Juicio: 
seguro
Entrada: 2 9 10 12
Respuesta: 2 * 12 * (10 - 9) = 24
Juicio: 
seguro
Entrada: 4 9 10 13
Respuesta: (13 - 9) * (10 - 4) = 24
Juicio: 
seguro
Entrada: 4 4 6 8
Respuesta: (4 + 8) * (6 - 4) + 1 = 25
Juicio: 
imposible
Entrada: 2 9 10 12
Respuesta: 2 * (12 - 10) = 24
Juicio: 
imposible
Entrada: 4 9 10 13
Respuesta: (13 - 4) * (10 - 9) = 24
Juicio: 
imposible
Entrada: {input}
Respuesta: {answer}
Juicio:'''
}



dict_prompts_pt = {
# 5-testados
'standard_prompt' : '''Use números e operações aritméticas básicas (+ - * /) para obter 24.
Entrada: 4 4 6 8
Resposta: (4 + 8) * (6 - 4) = 24
Entrada: 2 9 10 12
Resposta: 2 * 12 * (10 - 9) = 24
Entrada: 4 9 10 13
Resposta: (13 - 9) * (10 - 4) = 24
Entrada: 1 4 8 8
Resposta: (8 / 4 + 1) * 8 = 24
Entrada: 5 5 5 9
Resposta: 5 + 5 + 5 + 9 = 24
Entrada: {input}
''',

# 5-testados
'cot_prompt' : '''Use números e operações aritméticas básicas (+ - * /) para obter 24. A cada passo, você só pode escolher dois dos números restantes para obter um novo número.
Entrada: 4 4 6 8
Entrada: 4 4 6 8
Passos:
4 + 8 = 12 (restantes: 4 6 12)
6 - 4 = 2 (restantes: 2 12)
2 * 12 = 24 (restantes: 24)
Resposta: (6 - 4) * (4 + 8) = 24
Entrada: 2 9 10 12
Passos:
12 * 2 = 24 (restantes: 9 10 24)
10 - 9 = 1 (restantes: 1 24)
24 * 1 = 24 (restantes: 24)
Resposta: (12 * 2) * (10 - 9) = 24
Entrada: 4 9 10 13
Passos:
13 - 10 = 3 (restantes: 3 4 9)
9 - 3 = 6 (restantes: 4 6)
4 * 6 = 24 (restantes: 24)
Resposta: 4 * (9 - (13 - 10)) = 24
Entrada: 1 4 8 8
Passos:
8 / 4 = 2 (restantes: 1 2 8)
1 + 2 = 3 (restantes: 3 8)
3 * 8 = 24 (restantes: 24)
Resposta: (1 + 8 / 4) * 8 = 24
Entrada: 5 5 5 9
Passos:
5 + 5 = 10 (restantes: 5 9 10)
10 + 5 = 15 (restantes: 9 15)
15 + 9 = 24 (restantes: 24)
Resposta: ((5 + 5) + 5) + 9 = 24
Entrada: {input}
''',

# 1-testado
'propose_prompt' : '''Entrada: 2 8 8 14
Possíveis próximos passos:
2 + 8 = 10 (restantes: 8 10 14)
8 / 2 = 4 (restantes: 4 8 14)
14 + 2 = 16 (restantes: 8 8 16)
2 * 8 = 16 (restantes: 8 14 16)
8 - 2 = 6 (restantes: 6 8 14)
14 - 8 = 6 (restantes: 2 6 8)
14 /  2 = 7 (restantes: 7 8 8)
14 - 2 = 12 (restantes: 8 8 12)
Entrada: {input}
Possíveis próximos passos:
''',

'value_prompt' : '''Avalie se os números dados podem chegar a 24 (certo/provável/impossível)
10 14
10 + 14 = 24
certo
11 12
11 + 12 = 23
12 - 11 = 1
11 * 12 = 132
11 / 12 = 0.91
impossível
4 4 10
4 + 4 + 10 = 8 + 10 = 18
4 * 10 - 4 = 40 - 4 = 36
(10 - 4) * 4 = 6 * 4 = 24
certo
4 9 11
9 + 11 + 4 = 20 + 4 = 24
certo
5 7 8
5 + 7 + 8 = 12 + 8 = 20
(8 - 5) * 7 = 3 * 7 = 21
Não consigo obter 24 agora, mas os números estão dentro de um intervalo razoável
provável
5 6 6
5 + 6 + 6 = 17
(6 - 5) * 6 = 1 * 6 = 6
Não consigo obter 24 agora, mas os números estão dentro de um intervalo razoável
provável
10 10 11
10 + 10 + 11 = 31
(11 - 10) * 10 = 10
10 10 10 são todos muito grandes
impossível
1 3 3
1 * 3 * 3 = 9
(1 + 3) * 3 = 12
1 3 3 são todos muito pequenos
impossível
{input}
''',

'value_last_step_prompt' : '''Use números e operações aritméticas básicas (+ - * /) para obter 24. Dado um entrada e uma resposta, faça um julgamento (certo/impossível) se a resposta estiver correta, ou seja, usa cada entrada exatamente uma vez e nenhum outro número, e chega a 24.
Resposta: (4 + 8) * (6 - 4) = 24
Julgamento: 
certo
Entrada: 2 9 10 12
Resposta: 2 * 12 * (10 - 9) = 24
Julgamento: 
certo
Entrada: 4 9 10 13
Resposta: (13 - 9) * (10 - 4) = 24
Julgamento: 
certo
Entrada: 4 4 6 8
Resposta: (4 + 8) * (6 - 4) + 1 = 25
Julgamento: 
impossível
Entrada: 2 9 10 12
Resposta: 2 * (12 - 10) = 24
Julgamento: 
impossível
Entrada: 4 9 10 13
Resposta: (13 - 4) * (10 - 9) = 24
Julgamento: 
impossível
Entrada: {input}
Resposta: {answer}
Julgamento:'''
}




dict_prompts_fr = {
# 5-essayés
'standard_prompt' : '''Utilisez des nombres et des opérations arithmétiques de base (+ - * /) pour obtenir 24.
Entrée: 4 4 6 8
Réponse: (4 + 8) * (6 - 4) = 24
Entrée: 2 9 10 12
Réponse: 2 * 12 * (10 - 9) = 24
Entrée: 4 9 10 13
Réponse: (13 - 9) * (10 - 4) = 24
Entrée: 1 4 8 8
Réponse: (8 / 4 + 1) * 8 = 24
Entrée: 5 5 5 9
Réponse: 5 + 5 + 5 + 9 = 24
Entrée: {input}
''',

# 5-essayés
'cot_prompt' : '''Utilisez des nombres et des opérations arithmétiques de base (+ - * /) pour obtenir 24. A chaque étape, vous n'êtes autorisé à choisir que deux des numéros restants pour obtenir un nouveau numéro.
Entrée: 4 4 6 8
Étapes:
4 + 8 = 12 (rester: 4 6 12)
6 - 4 = 2 (rester: 2 12)
2 * 12 = 24 (rester: 24)
Réponse: (6 - 4) * (4 + 8) = 24
Entrée: 2 9 10 12
Étapes:
12 * 2 = 24 (rester: 9 10 24)
10 - 9 = 1 (rester: 1 24)
24 * 1 = 24 (rester: 24)
Réponse: (12 * 2) * (10 - 9) = 24
Entrée: 4 9 10 13
Étapes:
13 - 10 = 3 (rester: 3 4 9)
9 - 3 = 6 (rester: 4 6)
4 * 6 = 24 (rester: 24)
Réponse: 4 * (9 - (13 - 10)) = 24
Entrée: 1 4 8 8
Étapes:
8 / 4 = 2 (rester: 1 2 8)
1 + 2 = 3 (rester: 3 8)
3 * 8 = 24 (rester: 24)
Réponse: (1 + 8 / 4) * 8 = 24
Entrée: 5 5 5 9
Étapes:
5 + 5 = 10 (rester: 5 9 10)
10 + 5 = 15 (rester: 9 15)
15 + 9 = 24 (rester: 24)
Réponse: ((5 + 5) + 5) + 9 = 24
Entrée: {input}
''',

# 1-essayé
'propose_prompt' : '''Entrée: 2 8 8 14
Prochaines étapes possibles:
2 + 8 = 10 (rester: 8 10 14)
8 / 2 = 4 (rester: 4 8 14)
14 + 2 = 16 (rester: 8 8 16)
2 * 8 = 16 (rester: 8 14 16)
8 - 2 = 6 (rester: 6 8 14)
14 - 8 = 6 (rester: 2 6 8)
14 /  2 = 7 (rester: 7 8 8)
14 - 2 = 12 (rester: 8 8 12)
Entrée: {input}
Prochaines étapes possibles:
''',

'value_prompt' : '''Évaluer si les nombres donnés peuvent atteindre 24 (sûr/probable/impossible)
10 14
10 + 14 = 24
sûr
11 12
11 + 12 = 23
12 - 11 = 1
11 * 12 = 132
11 / 12 = 0.91
impossible
4 4 10
4 + 4 + 10 = 8 + 10 = 18
4 * 10 - 4 = 40 - 4 = 36
(10 - 4) * 4 = 6 * 4 = 24
sûr
4 9 11
9 + 11 + 4 = 20 + 4 = 24
sûr
5 7 8
5 + 7 + 8 = 12 + 8 = 20
(8 - 5) * 7 = 3 * 7 = 21
Je ne peux pas obtenir 24 maintenant, mais les chiffres sont dans une fourchette raisonnable
probable
5 6 6
5 + 6 + 6 = 17
(6 - 5) * 6 = 1 * 6 = 6
Je ne peux pas obtenir 24 maintenant, mais les chiffres sont dans une fourchette raisonnable
probable
10 10 11
10 + 10 + 11 = 31
(11 - 10) * 10 = 10
10 10 10 sont tous trop grands
impossible
1 3 3
1 * 3 * 3 = 9
(1 + 3) * 3 = 12
1 3 3 sont tous trop petits
impossible
{input}
''',

'value_last_step_prompt' : '''Utilisez des nombres et des opérations arithmétiques de base (+ - * /) pour obtenir 24. Étant donné une entrée et une réponse, donnez un jugement (sûr/impossible) si la réponse est correcte, c'est-à-dire qu'elle utilise chaque entrée exactement une fois et aucun autre nombre, et atteignez 24.
Entrée: 4 4 6 8
Réponse: (4 + 8) * (6 - 4) = 24
Jugement: 
sûr
Entrée: 2 9 10 12
Réponse: 2 * 12 * (10 - 9) = 24
Jugement: 
sûr
Entrée: 4 9 10 13
Réponse: (13 - 9) * (10 - 4) = 24
Jugement: 
sûr
Entrée: 4 4 6 8
Réponse: (4 + 8) * (6 - 4) + 1 = 25
Jugement: 
impossible
Entrée: 2 9 10 12
Réponse: 2 * (12 - 10) = 24
Jugement: 
impossible
Entrée: 4 9 10 13
Réponse: (13 - 4) * (10 - 9) = 24
Jugement: 
impossible
Entrée: {input}
Réponse: {answer}
Jugement:'''
}


dict_prompts_it = {
# 5-provatos
'standard_prompt' : '''Usa i numeri e le operazioni aritmetiche di base (+ - * /) per ottenere 24.
Input: 4 4 6 8
Risposta: (4 + 8) * (6 - 4) = 24
Ingresso: 2 9 10 12
Risposta: 2 * 12 * (10 - 9) = 24
Ingresso: 4 9 10 13
Risposta: (13 - 9) * (10 - 4) = 24
Ingresso: 1 4 8 8
Risposta: (8 / 4 + 1) * 8 = 24
Ingresso: 5 5 5 9
Risposta: 5 + 5 + 5 + 9 = 24
Ingresso: {input}
''',

# 5-provatos
'cot_prompt' : '''Usa i numeri e le operazioni aritmetiche di base (+ - * /) per ottenere 24. Ad ogni passaggio, puoi solo scegliere due dei numeri rimanenti per ottenere un nuovo numero.
Ingresso: 4 4 6 8
Passi:
4 + 8 = 12 (rimanere: 4 6 12)
6 - 4 = 2 (rimanere: 2 12)
2 * 12 = 24 (rimanere: 24)
Risposta: (6 - 4) * (4 + 8) = 24
Ingresso: 2 9 10 12
Passi:
12 * 2 = 24 (rimanere: 9 10 24)
10 - 9 = 1 (rimanere: 1 24)
24 * 1 = 24 (rimanere: 24)
Risposta: (12 * 2) * (10 - 9) = 24
Ingresso: 4 9 10 13
Passi:
13 - 10 = 3 (rimanere: 3 4 9)
9 - 3 = 6 (rimanere: 4 6)
4 * 6 = 24 (rimanere: 24)
Risposta: 4 * (9 - (13 - 10)) = 24
Ingresso: 1 4 8 8
Passi:
8 / 4 = 2 (rimanere: 1 2 8)
1 + 2 = 3 (rimanere: 3 8)
3 * 8 = 24 (rimanere: 24)
Risposta: (1 + 8 / 4) * 8 = 24
Ingresso: 5 5 5 9
Passi:
5 + 5 = 10 (rimanere: 5 9 10)
10 + 5 = 15 (rimanere: 9 15)
15 + 9 = 24 (rimanere: 24)
Risposta: ((5 + 5) + 5) + 9 = 24
Ingresso: {input}
''',

# 1-provato
'propose_prompt' : '''Ingresso: 2 8 8 14
Possibili passi successivi:
2 + 8 = 10 (rimanere: 8 10 14)
8 / 2 = 4 (rimanere: 4 8 14)
14 + 2 = 16 (rimanere: 8 8 16)
2 * 8 = 16 (rimanere: 8 14 16)
8 - 2 = 6 (rimanere: 6 8 14)
14 - 8 = 6 (rimanere: 2 6 8)
14 /  2 = 7 (rimanere: 7 8 8)
14 - 2 = 12 (rimanere: 8 8 12)
Ingresso: {input}
Possibili passi successivi:
''',

'value_prompt' : '''Valutare se i numeri dati possono raggiungere 24 (sicuro/probabile/impossibile)
10 14
10 + 14 = 24
sicuro
11 12
11 + 12 = 23
12 - 11 = 1
11 * 12 = 132
11 / 12 = 0.91
impossibile
4 4 10
4 + 4 + 10 = 8 + 10 = 18
4 * 10 - 4 = 40 - 4 = 36
(10 - 4) * 4 = 6 * 4 = 24
sicuro
4 9 11
9 + 11 + 4 = 20 + 4 = 24
sicuro
5 7 8
5 + 7 + 8 = 12 + 8 = 20
(8 - 5) * 7 = 3 * 7 = 21
Non posso ottenere 24 ora, ma i numeri sono in un intervallo ragionevole
probabile
5 6 6
5 + 6 + 6 = 17
(6 - 5) * 6 = 1 * 6 = 6
Non posso ottenere 24 ora, ma i numeri sono in un intervallo ragionevole
probabile
10 10 11
10 + 10 + 11 = 31
(11 - 10) * 10 = 10
10 10 10 are all too big
impossibile
1 3 3
1 * 3 * 3 = 9
(1 + 3) * 3 = 12
1 3 3 are all too small
impossibile
{input}
''',

'value_last_step_prompt' : '''Usa i numeri e le operazioni aritmetiche di base (+ - * /) per ottenere 24. Dato un input e una risposta, dai un giudizio (sicuro/impossibile) se la risposta è corretta, cioè usa ogni input esattamente una volta e nessun altro numero, e arriva a 24.
Ingresso: 4 4 6 8
Risposta: (4 + 8) * (6 - 4) = 24
Giudizio: 
sicuro
Ingresso: 2 9 10 12
Risposta: 2 * 12 * (10 - 9) = 24
Giudizio: 
sicuro
Ingresso: 4 9 10 13
Risposta: (13 - 9) * (10 - 4) = 24
Giudizio: 
sicuro
Ingresso: 4 4 6 8
Risposta: (4 + 8) * (6 - 4) + 1 = 25
Giudizio: 
impossibile
Ingresso: 2 9 10 12
Risposta: 2 * (12 - 10) = 24
Giudizio: 
impossibile
Ingresso: 4 9 10 13
Risposta: (13 - 4) * (10 - 9) = 24
Giudizio: 
impossibile
Ingresso: {input}
Risposta: {answer}
Giudizio:'''
}


dict_prompts = {
    'en': dict_prompts_en,
    'es': dict_prompts_es,
    'pt': dict_prompts_pt,
    'fr': dict_prompts_fr,
    'it': dict_prompts_it,
}