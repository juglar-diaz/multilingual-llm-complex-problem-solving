dict_prompts_en = {
# 5-testado
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

# 5-testado
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