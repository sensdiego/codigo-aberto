# Regressão integral R3

Resultado observado após corrigir os dois invariantes ambíguos: **22 PASS / 8
FAIL / 0 JUDGE_ERROR** em 30 cenários. As 30 primeiras rotas foram corretas e
nenhum dos sete gates mecânicos de redação falhou.

O número bruto não é um diagnóstico de dez defeitos. A triagem independente
dos dez FAILs originais encontrou:

- 7 conflitos entre fixture e contrato; 2 foram corrigidos e rejulgados;
- 1 limitação do ambiente, sem conector Silo autenticado;
- 2 defeitos reais da baseline: o briefing de agravo interno omite efeito e
  risco de multa, e o briefing de interdição omite intervenção institucional
  obrigatória.

Excluídas cinco fixtures materialmente inelegíveis e o cenário condicionado ao
Silo, a leitura comparável é **22 PASS / 2 FAIL em 24 elegíveis**. Nenhum dos
dois defeitos foi introduzido pela PR #26, mas a regressão integral da baseline
não deve ser descrita como verde.

Não houve chamada de modelo externo, custo medido em dólares, dogfood ou uso
humano. Houve consumo não medido da franquia Codex.
