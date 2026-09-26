import json
import threading
import unittest
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer
from motor import BASE, inferir
from app import Handler

class MotorTests(unittest.TestCase):
    def test_cada_regra_de_primeiro_nivel(self):
        for regra in BASE['rules'][:10]:
            with self.subTest(regra=regra['id']):
                result=inferir(regra['conditions'])
                self.assertIn(regra['id'],[r['id'] for r in result['results']])
    def test_encadeamento_primeira_camada(self):
        r=inferir({'aderencia':'sim','mesa_suja':'sim','z_alto':'sim'})
        self.assertEqual([(x['id'],x['round']) for x in r['results']],[('R01',1),('R02',1),('R11',2)])
    def test_encadeamento_fios(self):
        r=inferir({'fios':'sim','retracao_desativada':'sim','temperatura_alta':'sim'})
        self.assertEqual([x['id'] for x in r['results']],['R05','R06','R12'])
    def test_desconhecido_nao_e_sim(self):
        self.assertEqual(inferir({'fios':'sim'})['status'],'inconclusivo')
    def test_todas_negativas(self):
        self.assertEqual(inferir({q['id']:'nao' for q in BASE['questions']})['results'],[])
    def test_todas_desconhecidas(self):
        self.assertEqual(inferir({})['unknown_count'],14)
    def test_invalidas(self):
        for value in ({'fios':'talvez'},{'inexistente':'sim'},[],{'fios':True},{'fios':[]}):
            with self.subTest(value=value),self.assertRaises(ValueError): inferir(value)
    def test_multiplas_hipoteses(self):
        self.assertEqual(len(inferir({q['id']:'sim' for q in BASE['questions']})['results']),12)
    def test_sem_vazamento_entre_consultas(self):
        inferir({'fios':'sim','retracao_desativada':'sim'})
        self.assertEqual(inferir({})['results'],[])
    def test_negativa_bloqueia_regra(self):
        self.assertEqual(inferir({'fios':'sim','retracao_desativada':'nao'})['results'],[])

class WebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()
        cls.url='http://127.0.0.1:'+str(cls.server.server_port)
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join()
    def test_formulario_e_base(self):
        for path,expected in [('/','Analisar respostas'),('/base','R12')]:
            with urlopen(self.url+path) as r: self.assertIn(expected,r.read().decode())
    def test_resultado_exportacao_edicao(self):
        data=urlencode({'fios':'sim','retracao_desativada':'sim'}).encode()
        with urlopen(self.url+'/diagnosticar',data) as r: self.assertIn('R05',r.read().decode())
        with urlopen(self.url+'/exportar',data) as r:
            self.assertIn('attachment',r.headers['Content-Disposition'])
            self.assertEqual(json.load(r)['results'][0]['id'],'R05')
        with urlopen(self.url+'/editar',data) as r: self.assertIn('value="sim" selected',r.read().decode())
    def test_http_invalido(self):
        with self.assertRaises(HTTPError) as ctx: urlopen(self.url+'/diagnosticar',b'fios=talvez')
        self.assertEqual(ctx.exception.code,400)
    def test_404(self):
        with self.assertRaises(HTTPError) as ctx: urlopen(self.url+'/ausente')
        self.assertEqual(ctx.exception.code,404)

if __name__=='__main__': unittest.main(verbosity=2)
