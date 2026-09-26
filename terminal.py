"""Interface de terminal do PrintCheck. Execute: py terminal.py."""
from motor import BASE, inferir


def mostrar_resultado(respostas):
    resultado = inferir(respostas)
    print('\n=== RESULTADO E EXPLICACAO ===')
    if not resultado['results']:
        print('Inconclusivo: nenhum conjunto de condições foi satisfeito.')
        print('Isso não significa que a impressora esteja sem defeitos.')
    for regra in resultado['results']:
        condicoes = ' E '.join(f'{k} = {v}' for k, v in regra['conditions'].items())
        print(f"\nRodada {regra['round']} | {regra['id']} | {regra['title']}")
        print(f"SE {condicoes} ENTÃO {regra['fact']} = True")
        print('Recomendação:', regra['action'])
        print('Fonte:', BASE['sources'][regra['source']]['url'])
    print('\nRespostas desconhecidas:', resultado['unknown_count'])


def consultar():
    respostas = {}
    valores = {'s': 'sim', 'n': 'nao', 'd': 'desconhecido'}
    for pergunta in BASE['questions']:
        print('\n' + pergunta['label'])
        print(pergunta['help'])
        while True:
            entrada = input('[s] Sim | [n] Não | [d] Não sei: ').strip().lower()
            if entrada in valores:
                respostas[pergunta['id']] = valores[entrada]
                break
            print('Entrada inválida. Digite s, n ou d.')
    mostrar_resultado(respostas)


def main():
    while True:
        print('\n=== PRINTCHECK — SISTEMA ESPECIALISTA ===')
        print('1 - Nova consulta (responder às 14 perguntas)')
        print('2 - Demonstração: primeira camada')
        print('3 - Demonstração: primeira camada com mesa limpa')
        print('4 - Demonstração: todas as respostas desconhecidas')
        print('5 - Exibir base de regras')
        print('0 - Sair')
        opcao = input('Escolha: ').strip()
        if opcao == '0':
            break
        if opcao == '1':
            consultar()
        elif opcao in {'2', '3', '4'}:
            respostas = {} if opcao == '4' else {
                'aderencia': 'sim', 'mesa_suja': 'nao' if opcao == '3' else 'sim',
                'z_alto': 'sim'}
            print('\nExemplo predefinido. Demais respostas: desconhecido.')
            for chave, valor in respostas.items():
                print(f'{chave}: {valor}')
            mostrar_resultado(respostas)
        elif opcao == '5':
            for regra in BASE['rules']:
                condicoes = ' E '.join(f'{k} = {v}' for k, v in regra['conditions'].items())
                print(f"{regra['id']}: SE {condicoes} ENTÃO {regra['fact']} = True")
        else:
            print('Opção inválida. Escolha de 0 a 5.')


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\nPrintCheck encerrado.')
