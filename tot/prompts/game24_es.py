dict_prompts_es = {
# 5-intento
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

# 5-intento
'cot_prompt' : '''Usa números y operaciones aritméticas básicas (+ - * /) para obtener 24. En cada paso, solo puede elegir dos de los números restantes para obtener un nuevo número.
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