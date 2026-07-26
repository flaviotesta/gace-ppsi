#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Coleta métricas do repositório do GACE-PPSI e as arquiva em CSVs na pasta metrics/.

Executado pela GitHub Action .github/workflows/metricas.yml. Não coleta nenhum dado
de usuários: apenas os agregados que o próprio GitHub disponibiliza (visitas e clones
dos últimos 14 dias, downloads acumulados das releases, estrelas e forks).

Arquivos gerados:
  metrics/trafego_visitas.csv     data, total, unicos          (série diária, mesclada)
  metrics/trafego_clones.csv      data, total, unicos          (série diária, mesclada)
  metrics/downloads_releases.csv  data_coleta, release, arquivo, downloads_acumulados
  metrics/estrelas_forks.csv      data_coleta, estrelas, forks
"""
import csv
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

TOKEN = os.environ.get('GH_TOKEN', '')
REPO = os.environ.get('GITHUB_REPOSITORY', 'flaviotesta/gace-ppsi')
HOJE = datetime.now(timezone.utc).strftime('%Y-%m-%d')
API = 'https://api.github.com'


def consultar(caminho, com_token=True):
    req = urllib.request.Request(API + caminho)
    req.add_header('Accept', 'application/vnd.github+json')
    req.add_header('X-GitHub-Api-Version', '2022-11-28')
    if com_token and TOKEN:
        req.add_header('Authorization', 'Bearer ' + TOKEN)
    with urllib.request.urlopen(req, timeout=30) as resposta:
        return json.load(resposta)


def mesclar_trafego(chave, arquivo):
    """Mescla a janela de 14 dias da API com o histórico já gravado.

    Para cada dia, mantém o maior valor observado (os números dos dias mais
    recentes ainda podem se consolidar entre uma coleta e outra)."""
    try:
        dados = consultar(f'/repos/{REPO}/traffic/{chave}')
    except Exception as erro:
        print(f'AVISO: sem acesso a traffic/{chave} ({erro}). '
              f'Confira o secret TRAFEGO_TOKEN (permissão Administration: read).',
              file=sys.stderr)
        return
    serie = {item['timestamp'][:10]: (int(item['count']), int(item['uniques']))
             for item in dados.get(chave, [])}
    historico = {}
    if os.path.exists(arquivo):
        with open(arquivo, newline='', encoding='utf-8') as f:
            for linha in list(csv.reader(f))[1:]:
                if linha:
                    historico[linha[0]] = (int(linha[1]), int(linha[2]))
    for dia, (total, unicos) in serie.items():
        anterior = historico.get(dia)
        if anterior is None or total >= anterior[0]:
            historico[dia] = (total, unicos)
    with open(arquivo, 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        escritor.writerow(['data', 'total', 'unicos'])
        for dia in sorted(historico):
            escritor.writerow([dia, historico[dia][0], historico[dia][1]])
    print(f'{arquivo}: {len(serie)} dias mesclados; {len(historico)} dias no histórico.')


def ja_coletado_hoje(arquivo):
    """Evita fotografias duplicadas quando o fluxo roda mais de uma vez no dia."""
    if not os.path.exists(arquivo):
        return False
    with open(arquivo, newline='', encoding='utf-8') as f:
        return any(linha and linha[0] == HOJE for linha in list(csv.reader(f))[1:])


os.makedirs('metrics', exist_ok=True)

# 1) Tráfego (exige o token com Administration: read)
mesclar_trafego('views', 'metrics/trafego_visitas.csv')
mesclar_trafego('clones', 'metrics/trafego_clones.csv')

# 2) Downloads acumulados por arquivo de release (fotografia da data)
#    Endpoint público, mas o token é enviado quando disponível para evitar limites de taxa.
try:
    arquivo = 'metrics/downloads_releases.csv'
    if ja_coletado_hoje(arquivo):
        print(f'{arquivo}: fotografia de {HOJE} já existia; nada a fazer.')
    else:
        releases = consultar(f'/repos/{REPO}/releases?per_page=100')
        novo = not os.path.exists(arquivo)
        with open(arquivo, 'a', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            if novo:
                escritor.writerow(['data_coleta', 'release', 'arquivo', 'downloads_acumulados'])
            for release in releases:
                for anexo in release.get('assets', []):
                    escritor.writerow([HOJE, release.get('tag_name', ''),
                                       anexo.get('name', ''), anexo.get('download_count', 0)])
        print(f'{arquivo}: fotografia de {HOJE} registrada.')
except Exception as erro:
    print(f'AVISO: falha ao ler as releases ({erro}).', file=sys.stderr)

# 3) Estrelas e forks (fotografia da data; mesmo critério de token do item 2)
try:
    arquivo = 'metrics/estrelas_forks.csv'
    if ja_coletado_hoje(arquivo):
        print(f'{arquivo}: fotografia de {HOJE} já existia; nada a fazer.')
    else:
        repositorio = consultar(f'/repos/{REPO}')
        novo = not os.path.exists(arquivo)
        with open(arquivo, 'a', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            if novo:
                escritor.writerow(['data_coleta', 'estrelas', 'forks'])
            escritor.writerow([HOJE, repositorio.get('stargazers_count', 0),
                               repositorio.get('forks_count', 0)])
        print(f'{arquivo}: fotografia de {HOJE} registrada.')
except Exception as erro:
    print(f'AVISO: falha ao ler os dados do repositório ({erro}).', file=sys.stderr)
