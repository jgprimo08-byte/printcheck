"""Interface web local. Execução: python app.py. Sem dependências externas."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import argparse
import html
import json
from motor import BASE, inferir

ROOT = Path(__file__).parent
LABELS = {'sim':'Sim', 'nao':'Não', 'desconhecido':'Não sei'}
EXEMPLOS = {
 'aderencia': {'aderencia':'sim','mesa_suja':'sim','z_alto':'sim'},
 'fios': {'fios':'sim','retracao_desativada':'sim','temperatura_alta':'sim'},
 'inconclusivo': {},
}
CSS = """
:root{font-family:Arial,sans-serif;color:#152e3b;background:#f3f6f7;line-height:1.55}
*{box-sizing:border-box}body{margin:0}header{background:#103642;color:white;padding:22px max(5%,calc((100% - 1100px)/2))}
header a{color:white;text-decoration:none}header strong{font-size:27px}header span{display:block;color:#bce3df}
main{max-width:1100px;margin:32px auto;padding:0 24px}h1{font-size:38px;line-height:1.15;margin-bottom:14px}h2{font-size:24px}
.intro{max-width:780px;font-size:18px}.muted,small{color:#536b76}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.card{background:white;padding:23px;border:1px solid #dce5e8;border-radius:12px;margin-bottom:18px}
label{display:block;font-weight:bold;margin-bottom:7px}select{display:block;width:100%;padding:12px;border:1px solid #809ba5;border-radius:6px;background:white;font-size:16px;margin-top:13px}
button,.button{display:inline-block;background:#087c76;color:white;padding:12px 20px;border:0;border-radius:7px;text-decoration:none;font-size:16px;cursor:pointer;margin:6px 8px 6px 0}
.secondary{background:#e4eef0;color:#153642}a{color:#086f6b}.tag{font-size:13px;font-weight:bold;color:#087c76;text-transform:uppercase;letter-spacing:1px}
.notice{border-left:4px solid #087c76;background:#e8f4f2;padding:18px;margin:24px 0}details{margin-top:16px}summary{cursor:pointer;font-weight:bold}
nav{margin:18px 0}table{width:100%;border-collapse:collapse}td,th{text-align:left;border-bottom:1px solid #ddd;padding:10px}footer{margin:36px 0;color:#536b76;font-size:14px}
@media(max-width:650px){.grid{grid-template-columns:1fr}h1{font-size:30px}main{padding:0 16px}}
"""

def pagina(titulo, conteudo):
    return f"""<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(titulo)} | PrintCheck</title><style>{CSS}</style><header><a href="/"><strong>PrintCheck</strong></a><span>Assistente de diagnóstico de impressão 3D</span></header><main>{conteudo}<footer>Projeto acadêmico A1. Triagem de impressão FDM/FFF. As conclusões são hipóteses, não garantias de reparo.</footer></main></html>"""

def formulario(respostas=None):
    respostas = respostas or {}
    campos = []
    for q in BASE['questions']:
        options = ''.join(f'<option value="{v}" {"selected" if respostas.get(q["id"],"desconhecido")==v else ""}>{t}</option>' for v,t in LABELS.items())
        campos.append(f'<div class="card"><label for="{q["id"]}">{q["label"]}</label><small>{q["help"]}</small><select id="{q["id"]}" name="{q["id"]}">{options}</select></div>')
    return pagina('Nova consulta', '<p class="tag">Nova consulta</p><h1>O que aconteceu com a peça?</h1><p class="intro">Informe o que observou. Se não verificou um item, mantenha “Não sei”. O sistema explica quais regras sustentam cada hipótese.</p><nav><a class="button secondary" href="/?exemplo=aderencia">Exemplo: primeira camada</a><a class="button secondary" href="/?exemplo=fios">Exemplo: fios</a><a class="button secondary" href="/base">Ver base de conhecimento</a></nav><form action="/diagnosticar" method="post"><div class="grid">'+''.join(campos)+'</div><button type="submit">Analisar respostas</button></form>')

def resultado(dados):
    resultados = dados['results']
    title = 'Hipóteses e recomendações' if resultados else 'Resultado inconclusivo'
    blocos = []
    for r in resultados:
        evidencias = ', '.join(f'{k} = {LABELS.get(v, "verdadeiro")}' for k,v in r['conditions'].items())
        fonte = BASE['sources'][r['source']]
        blocos.append(f'<section class="card"><p class="tag">{r["id"]} · Rodada {r["round"]}</p><h2>{r["title"]}</h2><p>{r["action"]}</p><details><summary>Por que o sistema sugeriu isso?</summary><p>{evidencias}</p><p>Fato derivado: {r["fact"]}</p><a href="{fonte["url"]}" target="_blank" rel="noopener">Fonte técnica: {fonte["title"]}</a></details></section>')
    if not resultados:
        blocos.append('<div class="notice">Nenhuma regra teve todas as condições satisfeitas. Isso não comprova ausência de defeito. Revise as observações e, se necessário, consulte um técnico.</div>')
    respostas = ''.join(f'<tr><td>{q["label"]}</td><td>{LABELS[dados["answers"][q["id"]]]}</td></tr>' for q in BASE['questions'])
    hidden = ''.join(f'<input type="hidden" name="{k}" value="{v}">' for k,v in dados['answers'].items())
    return pagina(title, f'<p class="tag">Resultado da consulta</p><h1>{title}</h1><p>{len(resultados)} regra(s) aplicada(s). {dados["unknown_count"]} resposta(s) “Não sei”. Não há classificação por probabilidade.</p>'+''.join(blocos)+f'<form method="post"><span><button formaction="/editar" class="secondary">Revisar respostas</button><button formaction="/exportar">Baixar consulta JSON</button></span>{hidden}</form><a class="button secondary" href="/">Nova consulta</a><details><summary>Respostas utilizadas</summary><table>{respostas}</table></details>')

def base_page():
    blocos=[]
    for r in BASE['rules']:
        cond=' E '.join(k+' = '+str(v) for k,v in r['conditions'].items())
        blocos.append(f'<section class="card"><h2>{r["id"]}: {r["title"]}</h2><p>SE {cond}, ENTÃO {r["fact"]}.</p><p>{r["action"]}</p></section>')
    return pagina('Base de conhecimento','<h1>Base de conhecimento</h1><p>12 regras de produção. A ordem define apenas a apresentação dos resultados.</p><a href="/">Voltar à consulta</a>'+''.join(blocos))

class Handler(BaseHTTPRequestHandler):
    def responder(self, body, status=200, tipo='text/html; charset=utf-8', download=False):
        raw=body.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type',tipo)
        self.send_header('Content-Length',str(len(raw)))
        self.send_header('Cache-Control','no-store')
        if download:
            self.send_header('Content-Disposition','attachment; filename="consulta-printcheck.json"')
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        url=urlparse(self.path)
        if url.path=='/':
            exemplo=parse_qs(url.query).get('exemplo',[''])[0]
            self.responder(formulario(EXEMPLOS.get(exemplo)))
        elif url.path=='/base':
            self.responder(base_page())
        else:
            self.responder(pagina('Não encontrado','<h1>Página não encontrada</h1><a href="/">Início</a>'),404)

    def do_POST(self):
        if self.path not in {'/diagnosticar','/editar','/exportar'}:
            self.responder('Rota inexistente',404)
            return
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0 < size <= 16000:
                raise ValueError('Tamanho da requisição inválido.')
            parsed=parse_qs(self.rfile.read(size).decode('utf-8'),keep_blank_values=True)
            if any(len(v)!=1 for v in parsed.values()):
                raise ValueError('Respostas duplicadas.')
            respostas={k:v[0] for k,v in parsed.items()}
            dados=inferir(respostas)
            if self.path=='/editar':
                self.responder(formulario(dados['answers']))
            elif self.path=='/exportar':
                self.responder(json.dumps(dados,ensure_ascii=False,indent=2),tipo='application/json; charset=utf-8',download=True)
            else:
                self.responder(resultado(dados))
        except (ValueError,UnicodeError) as error:
            self.responder(pagina('Entrada inválida','<h1>Entrada inválida</h1><p>'+html.escape(str(error))+'</p><a href="/">Recomeçar</a>'),400)

    def log_message(self, *args):
        pass

def main():
    parser=argparse.ArgumentParser(description='PrintCheck: servidor local')
    parser.add_argument('--port',type=int,default=8000)
    args=parser.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    print(f'PrintCheck em http://127.0.0.1:{args.port} - Ctrl+C para encerrar.',flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__=='__main__':
    main()
