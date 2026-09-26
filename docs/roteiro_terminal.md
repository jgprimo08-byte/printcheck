# PrintCheck no terminal

## Como baixar e executar

1. Na página inicial do repositório, clique em Code > Download ZIP.
2. Extraia todos os arquivos. É necessário Python 3.10 ou superior.
3. No Windows, dê dois cliques em INICIAR_TERMINAL.bat.
4. Alternativamente, abra um terminal na pasta dos arquivos e execute `py terminal.py` ou `python terminal.py`.

O GitHub permite acessar e baixar o código; a execução acontece no computador. Mantenha terminal.py, motor.py e base_conhecimento.json na mesma pasta.

## Roteiro para apresentar

- Opção 5: mostre as 12 regras no formato SE condições ENTÃO conclusão.
- Opção 2: explique que baixa aderência, mesa suja e bico alto ativam R01 e R02 na primeira rodada. Seus fatos ativam R11 na segunda rodada: encadeamento para frente.
- Opção 3: agora a mesa está limpa. Somente R02 dispara; R01 e R11 não são satisfeitas. O resultado muda conforme os fatos informados.
- Opção 4: todas as respostas desconhecidas produzem resultado inconclusivo, não ausência de defeitos.
- Opção 1: faça uma consulta real respondendo s, n ou d às 14 perguntas. Para reproduzir a opção 2, responda s às perguntas 2, 3 e 4 e d às demais.
- Opção 0: encerre.

A variável aderencia indica a existência de um problema de aderência. Portanto, aderencia = sim significa que a primeira camada solta ou adere mal. True representa um fato concluído pelo motor, não uma confirmação física do defeito.

Fala de encerramento: “O sistema apresenta as regras ativadas, as rodadas, as recomendações e as fontes. Usa regras explícitas, não aprendizado de máquina, e suas hipóteses dependem da base cadastrada.”
