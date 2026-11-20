#!/usr/bin/env python3
"""Mede o consumo dos subagentes nos registros locais do Claude Code.

Uso:
    python3 scripts/medir.py                 # projeto da pasta atual
    python3 scripts/medir.py /caminho/do/projeto
    python3 scripts/medir.py --desde 2026-11-01

Só lê arquivos. Nada sai da máquina.

O custo é relativo, em "unidades de entrada": entrada 1, escrita de cache 1,25,
leitura de cache 0,1, saída 5. Serve para comparar antes e depois no mesmo
projeto, não para prever a fatura.
"""
import collections
import glob
import json
import os
import re
import sys

PESO = {"entrada": 1.0, "escrita": 1.25, "leitura": 0.1, "saida": 5.0}

PAPEIS = [
    ("mapeador", r"mape|mapa\b|explor"),
    ("painel de testes", r"painel|especialista|lente|cat[aá]logo"),
    ("auditor", r"audit"),
    ("analista de premissa", r"premissa"),
    ("revisor", r"revis|review"),
    ("autor de testes", r"autor|escrev\w* testes?|test author"),
    ("implementador", r"implement|corrig|corre[cç]|fix"),
]
BUSCA = re.compile(r"\b(grep|rg|find|ls|cat|sed|head|tail|wc)\b")
TESTE = re.compile(r"phpunit|pytest|artisan test|jest|vitest|ng test|go test|cargo test|rspec|pest")


def pasta_dos_registros(projeto):
    slug = re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(projeto))
    return os.path.join(os.path.expanduser("~/.claude/projects"), slug)


def papel(descricao):
    d = (descricao or "").lower()
    for nome, padrao in PAPEIS:
        if re.search(padrao, d):
            return nome
    return "outros"


def ler_agente(caminho):
    mensagens, acoes, inicio = {}, collections.Counter(), None
    with open(caminho, errors="ignore") as f:
        for linha in f:
            try:
                d = json.loads(linha)
            except ValueError:
                continue
            inicio = inicio or d.get("timestamp")
            m = d.get("message") or {}
            if d.get("type") != "assistant" or not isinstance(m, dict):
                continue
            u = m.get("usage")
            if u:
                mensagens[m.get("id") or d.get("uuid")] = (
                    u.get("input_tokens", 0),
                    u.get("cache_creation_input_tokens", 0),
                    u.get("cache_read_input_tokens", 0),
                    u.get("output_tokens", 0),
                )
            for bloco in m.get("content") or []:
                if isinstance(bloco, dict) and bloco.get("type") == "tool_use":
                    nome = bloco.get("name", "")
                    comando = (bloco.get("input") or {}).get("command", "")
                    if nome in ("Read", "Grep", "Glob") or (nome == "Bash" and BUSCA.search(comando) and not TESTE.search(comando)):
                        acoes["procurar e ler"] += 1
                    elif nome == "Bash" and TESTE.search(comando):
                        acoes["rodar testes"] += 1
                    elif nome in ("Edit", "Write", "NotebookEdit"):
                        acoes["escrever"] += 1
                    else:
                        acoes["outras"] += 1
    t = [sum(v[i] for v in mensagens.values()) for i in range(4)]
    custo = t[0] * PESO["entrada"] + t[1] * PESO["escrita"] + t[2] * PESO["leitura"] + t[3] * PESO["saida"]
    return {"passos": len(mensagens), "custo": custo, "acoes": acoes, "inicio": inicio or ""}


def main():
    args = sys.argv[1:]
    desde = ""
    if "--desde" in args:
        i = args.index("--desde")
        desde = args[i + 1]
        del args[i:i + 2]
    pasta = pasta_dos_registros(args[0] if args else os.getcwd())
    arquivos = glob.glob(os.path.join(pasta, "*", "subagents", "agent-*.jsonl"))
    if not arquivos:
        sys.exit(f"Nenhum registro de subagente em {pasta}")

    agentes = []
    for a in arquivos:
        r = ler_agente(a)
        if r["inicio"][:10] < desde:
            continue
        try:
            meta = json.load(open(a[:-6] + ".meta.json"))
        except (OSError, ValueError):
            meta = {}
        r["papel"] = papel(meta.get("description", ""))
        agentes.append(r)
    if not agentes:
        sys.exit("Nenhum agente no período.")

    total = sum(r["custo"] for r in agentes) or 1
    datas = sorted(r["inicio"][:10] for r in agentes if r["inicio"])
    print(f"{len(agentes)} agentes, de {datas[0]} a {datas[-1]}")
    print(f"custo relativo total: {total / 1e6:.0f}M\n")

    print(f"{'papel':<22}{'agentes':>8}{'% custo':>9}{'passos/ag':>11}{'custo/ag':>10}")
    por_papel = collections.defaultdict(list)
    for r in agentes:
        por_papel[r["papel"]].append(r)
    for nome, lista in sorted(por_papel.items(), key=lambda kv: -sum(r["custo"] for r in kv[1])):
        c = sum(r["custo"] for r in lista)
        n = len(lista)
        print(f"{nome:<22}{n:>8}{100 * c / total:>8.1f}%{sum(r['passos'] for r in lista) / n:>11.1f}{c / n / 1e6:>9.2f}M")

    print("\nagentes por número de passos")
    faixas = [("até 20", 0, 20), ("21 a 50", 21, 50), ("51 a 100", 51, 100), ("mais de 100", 101, 10 ** 9)]
    for nome, lo, hi in faixas:
        lista = [r for r in agentes if lo <= r["passos"] <= hi]
        print(f"  {nome:<12}{len(lista):>6} agentes{100 * sum(r['custo'] for r in lista) / total:>7.1f}% do custo")

    acoes = collections.Counter()
    for r in agentes:
        acoes.update(r["acoes"])
    n = sum(acoes.values()) or 1
    print("\no que os agentes fazem (ações)")
    for nome, v in acoes.most_common():
        print(f"  {nome:<16}{100 * v / n:>5.0f}%")


if __name__ == "__main__":
    main()
