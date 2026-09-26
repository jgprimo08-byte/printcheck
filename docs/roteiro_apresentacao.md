# Roteiro de apresentação

Duração sugerida: aproximadamente 8 minutos, incluindo demonstração.

## Slide 1: PrintCheck
Apresente o tema: um sistema especialista para triagem de defeitos em impressão 3D com filamento. O objetivo é produzir hipóteses justificadas. Tempo: 30 segundos.

## Slide 2: Minimundo
A oficina é um cenário proposto. O usuário iniciante informa observações da peça e da impressora. O sistema orienta verificações e não controla o equipamento. Tempo: 40 segundos.

## Slide 3: Base de conhecimento
São 14 perguntas, 12 regras e cinco fontes técnicas. Sim, não e não sei são valores distintos. Fatos derivados são booleanos. As fontes estão no arquivo base_conhecimento.json. Tempo: 45 segundos.

## Slide 4: Regras de produção
R01: baixa aderência e resíduos geram a hipótese de contaminação. R02: baixa aderência e bico alto geram a hipótese de altura inadequada. R11 combina essas hipóteses. Tempo: 50 segundos.

## Slide 5: Encadeamento para frente
A memória começa com as respostas. A agenda usa os fatos existentes no início de cada rodada. R01 e R02 disparam na primeira rodada e R11 na segunda. Cada regra dispara no máximo uma vez. Tempo: 50 segundos.

## Slide 6: Fluxograma
Explique validar, montar agenda, disparar regras e repetir. Agenda vazia encerra a inferência. Sem conclusões, o resultado é inconclusivo. A memória preserva os fatos derivados. Tempo: 45 segundos.

## Slide 7: Casos de uso
O ator é o usuário da oficina. Ele responde, obtém hipóteses, revisa, exporta, consulta a base e inicia nova consulta. O diagrama de estados fica apenas no relatório. Tempo: 40 segundos.

## Slide 8: Protótipo de telas
Abra docs/prototipo.html. Há três telas com exemplo fixo. A aplicação Python é a versão funcional. Tempo: 35 segundos.

## Slide 9: Implementação e demonstração
Execute python app.py e abra http://127.0.0.1:8000. Clique em Exemplo: primeira camada e Analisar respostas. Abra uma justificativa e mostre R11 na segunda rodada. Revise uma resposta e compare. Tempo: 1 minuto e 20 segundos.

## Slide 10: Testes e limites
Foram executados 14 métodos de teste, incluindo subtestes das dez regras iniciais. O sucesso verifica o software, não a acurácia em impressoras reais. Não há probabilidades nem aprendizado de máquina. Tempo: 40 segundos.

## Slide 11: Conclusão
O sistema torna explícito o raciocínio por regras. A evolução proposta é validar com um técnico e casos reais. Repositório: https://github.com/jgprimo08-byte/printcheck. Tempo: 30 segundos.
