dict_prompts_en = {
# 5-essayé
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

# 5-essayé
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