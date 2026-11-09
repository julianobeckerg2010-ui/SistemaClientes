import os
import tempfile
from pathlib import Path

arquivo = tempfile.TemporaryDirectory()
os.environ['DATABASE_PATH'] = str(Path(arquivo.name) / 'teste.db')
from app import app, validar_cliente

app.config['TESTING'] = True


def test_pagina_inicial():
    assert app.test_client().get('/').status_code == 200


def test_pagina_cadastro():
    assert app.test_client().get('/cadastro').status_code == 200


def test_pagina_clientes():
    assert app.test_client().get('/clientes').status_code == 200


def test_validacao_nome_vazio():
    assert validar_cliente('', 'teste@email.com', '51999999999') is not None


def test_validacao_email_invalido():
    assert validar_cliente('Joao', 'invalido', '51999999999') is not None


def test_validacao_correta():
    assert validar_cliente('Joao', 'joao@email.com', '51999999999') is None


def test_cadastro_vazio():
    assert app.test_client().post('/cadastro', data={'nome':'', 'email':'', 'telefone':''}).status_code == 400


def test_cadastrar_e_consultar():
    cliente = app.test_client()
    resposta = cliente.post('/cadastro', data={'nome':'Maria Teste', 'email':'maria@email.com', 'telefone':'51999999999'}, follow_redirects=True)
    assert resposta.status_code == 200
    assert b'Maria Teste' in resposta.data


def test_busca():
    assert b'Maria Teste' in app.test_client().get('/clientes?busca=Maria').data


def test_editar():
    cliente = app.test_client()
    resposta = cliente.post('/clientes/1/editar', data={'nome':'Maria Atualizada', 'email':'maria@email.com', 'telefone':'51999999999'}, follow_redirects=True)
    assert b'Maria Atualizada' in resposta.data


def test_excluir():
    cliente = app.test_client()
    resposta = cliente.post('/clientes/1/excluir', follow_redirects=True)
    assert b'Maria Atualizada' not in resposta.data


def test_health():
    assert app.test_client().get('/health').json == {'status':'ok'}
