dict_prompts_en = {
# 5-provato
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

# 5-provato
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