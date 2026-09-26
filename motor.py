"""Motor determinístico de encadeamento para frente, separado da interface."""
import json
from pathlib import Path

BASE = json.loads(Path(__file__).with_name("base_conhecimento.json").read_text(encoding="utf-8"))
VALORES = {"sim", "nao", "desconhecido"}

def inferir(respostas):
    if not isinstance(respostas, dict):
        raise ValueError("As respostas devem formar um objeto.")
    ids = {q["id"] for q in BASE["questions"]}
    if set(respostas) - ids:
        raise ValueError("Pergunta desconhecida.")
    if any(not isinstance(v, str) or v not in VALORES for v in respostas.values()):
        raise ValueError("Resposta inválida. Use sim, nao ou desconhecido.")
    fatos = {key: respostas.get(key, "desconhecido") for key in ids}
    trilha = []
    disparadas = set()
    rodada = 0
    while True:
        rodada += 1
        agenda = [r for r in BASE["rules"] if r["id"] not in disparadas
                  and all(fatos.get(k) == v for k, v in r["conditions"].items())]
        if not agenda:
            break
        for regra in agenda:
            fatos[regra["fact"]] = True
            disparadas.add(regra["id"])
            trilha.append({**regra, "round": rodada})
    return {"status": "conclusoes" if trilha else "inconclusivo",
            "answers": {q["id"]: fatos[q["id"]] for q in BASE["questions"]},
            "results": trilha, "facts": fatos,
            "unknown_count": sum(fatos[k] == "desconhecido" for k in ids)}
