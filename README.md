# PrintCheck

Sistema especialista acadêmico para triagem de problemas em impressão 3D FDM/FFF.
Utiliza 14 perguntas, 12 regras de produção e encadeamento para frente.
Não usa aprendizado de máquina. As conclusões são hipóteses explicáveis.

## Executar

Requisito: Python 3.10 ou superior. Sem bibliotecas externas.

1. Baixe em **Code > Download ZIP** e extraia os arquivos.
2. Abra um terminal nessa pasta.
3. Execute `python app.py` (no Windows, também pode usar `py app.py`).
4. Abra http://127.0.0.1:8000 no navegador.
5. Para encerrar, pressione Ctrl+C no terminal.

Se a porta estiver ocupada: `python app.py --port 8001`.
O servidor aceita conexões apenas do próprio computador.

## Demonstração

Clique em **Exemplo: primeira camada** e depois em **Analisar respostas**.
R01 e R02 disparam na primeira rodada e R11 na segunda.
No exemplo **fios**, o resultado contém R05, R06 e R12.
Uma consulta com todas as respostas em Não sei é inconclusiva.
O botão **Revisar respostas** mantém os valores. **Nova consulta** limpa o formulário.
**Baixar consulta JSON** exporta respostas, regras, recomendações e fatos.
Não há cadastro nem histórico persistente.

## Arquivos

- `app.py`: interface e servidor HTTP local.
- `motor.py`: inferência e validação de respostas.
- `base_conhecimento.json`: perguntas, regras e fontes.
- `test_printcheck.py`: testes do motor e da interface HTTP.
- `docs/prototipo.html`: protótipo navegável de três telas, aberto por duplo clique.
- `docs/diagramas.md`: diagramas editáveis em Mermaid.

## Testar

Execute `python -m unittest -v`.
Os testes validam cada regra inicial, encadeamento, entradas inválidas, respostas desconhecidas, múltiplas conclusões, exportação e navegação HTTP.
Esses testes verificam o software, não a precisão de diagnósticos em impressoras reais.

## Decisões do motor

Todas as condições de cada regra devem ser satisfeitas. Não sei não equivale a Não.
Cada regra dispara uma vez por consulta. Fatos derivados alimentam a rodada seguinte.
As regras aparecem em ordem de identificador dentro de cada rodada e não possuem pesos probabilísticos.
Quando há mais de uma hipótese, o sistema preserva todas. Quando nenhuma regra dispara, informa resultado inconclusivo. R11 e R12 combinam recomendações anteriores.

## Fontes

As regras são uma modelagem didática própria, inspirada nos guias da Prusa Research.
As URLs constam em `base_conhecimento.json`. Procedimentos variam por impressora e material. Não foram realizados testes físicos ou validação com especialistas.

## Repositório e documentação

Repositório público: https://github.com/jgprimo08-byte/printcheck

- [Roteiro de apresentação](docs/roteiro_apresentacao.md)
- [Diagramas](docs/diagramas.md)
- [Protótipo navegável](docs/prototipo.html): baixe o arquivo e abra no navegador.

O GitHub hospeda os arquivos. O programa Python executa localmente.
O relatório acadêmico e a apresentação personalizados integram o pacote de entrega do grupo.
