# Avaliação comportamental A01–A14 com subagentes Codex — R2

Data: 2026-08-30

Status: **válida**.

## Resultado

- Primeira passagem: **13 PASS / 1 FAIL**.
- Falha: **A03** usou a lente defensiva correta, mas não declarou que havia
  validado recibo, identidade, lente e elegibilidade do pacote.
- Correção: uma regra mínima em `skills/novo-caso/SKILL.md`, sem alterar fixture,
  invariantes ou input visível.
- Regressão A03: **PASS**, com executor e juiz novos.
- Estado efetivo: **14/14**, sem alegação de passagem única perfeita.
- Roteamento: **14/14**. Gate de redação: **14/14**.

## Cadeia auditável

1. `387c32f` congelou código, fixtures e
   [`input-manifest.json`](input-manifest.json), com hashes dos 14 inputs
   visíveis antes do despacho.
2. Três executores cegos receberam somente `prompt` e `setup_files`. Seus
   outputs e hashes foram congelados em `4f11742`, antes dos juízes, por meio de
   [`executor-manifest.json`](executor-manifest.json).
3. Três juízes novos aplicaram a fixture e registraram evidência por invariável.
   O resultado 13/14 foi congelado em `ff2a210` e
   [`judge-manifest.json`](judge-manifest.json).
4. `267bfc8` corrigiu somente a skill `novo-caso`; o input A03 permaneceu com o
   mesmo hash.
5. Um executor cego novo foi congelado em `de028ce`; um juiz novo registrou PASS
   em `252a917`.

Os manifests contêm nomes das tarefas, caminhos, SHA-256 e contagens. Os commits
separam inputs, execução, julgamento, correção e regressão, permitindo verificar
a ordem sem depender da narrativa desta sessão.

## Resultados por cenário

| Cenário | Primeira passagem | Efetivo |
|---|---:|---:|
| A01 | PASS | PASS |
| A02 | PASS | PASS |
| A03 | FAIL | PASS |
| A04 | PASS | PASS |
| A05 | PASS | PASS |
| A06 | PASS | PASS |
| A07 | PASS | PASS |
| A08 | PASS | PASS |
| A09 | PASS | PASS |
| A10 | PASS | PASS |
| A11 | PASS | PASS |
| A12 | PASS | PASS |
| A13 | PASS | PASS |
| A14 | PASS | PASS |

As evidências textuais completas estão em `judge-a01-a05.json`,
`judge-a06-a10.json`, `judge-a11-a14.json` e
`regression-a03-judge.json` neste diretório.

## Limites

- Executores e juízes pertencem à mesma família Codex. Tarefas distintas
  reduzem contaminação de contexto, mas não equivalem a validação cross-model.
- Cada agente recebeu um lote; pode haver efeito de contexto entre cenários do
  mesmo lote.
- Os pacotes são sintéticos e derivados de classes observadas. Nenhum documento
  privado foi entregue aos agentes ou incorporado ao repositório.
- A rodada valida os consumidores públicos, roteamento, invariantes e gate de
  redação. Não prova produtor, runtime, dogfood, uso humano ou adoção.
- Não houve rede, Claude CLI, API externa ou modelo pago por fora. O consumo da
  franquia Codex não foi medido em tokens ou dólares pelo harness.

## Rodada substituída

A rodada anterior em `../2026-08-30-codex-subagents-adaptacao/` foi preservada,
mas está formalmente invalidada: a associação posicional entre fatos, achados e
frentes corrompia parte dos pacotes materializados. Nenhum resultado daquela
rodada é usado no 14/14 acima.
