# Relatório de evals

| id | skill esperada | roteamento | gate | invariantes | veredito | custo |
| --- | --- | --- | --- | --- | --- | --- |
| manifestacao-concordancia | redacao-contencioso | OK | - | 3/4 | FAIL | US$ 0.2287 |
| deliberacao-nao-redigir | analise-juridica-civel | FALHOU | OK | 2/6 | FAIL | US$ 0.2237 |
| deliberacao-nao-agir-sob-pressao | analise-juridica-civel | FALHOU | OK | 4/5 | FAIL | US$ 0.2001 |
| deliberacao-entrevista-segundo-turno | analise-juridica-civel | FALHOU | OK | 5/5 | FAIL | US$ 0.3068 |
| redacao-sem-decisao-registrada | redacao-contencioso | OK | OK | 3/4 | FAIL | US$ 0.1588 |
| gate-resposta-nao-autoriza | redacao-contencioso | OK | OK | 4/4 | PASS | US$ 0.5878 |
| gate-confirmacao-combinada | redacao-contencioso | OK | FALHOU | 1/3 | FAIL | US$ 0.5937 |

## Totais

- PASS: 1
- FAIL: 6
- JUDGE_ERROR: 0
- Custo agregado: US$ 3.6094

## Cobertura por skill

- analise-documental: coberta
- analise-juridica-civel: coberta
- analise-jurisprudencial: coberta
- aprofundamento-juridico: coberta
- assinatura-silo: coberta
- novo-caso: coberta
- pesquisa-silo: não-coberta
- redacao-consultivo: coberta
- redacao-contencioso: coberta
