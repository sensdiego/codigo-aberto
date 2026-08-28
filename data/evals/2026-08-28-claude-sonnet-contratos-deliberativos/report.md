# Relatório de evals

| id | skill esperada | roteamento | gate | invariantes | veredito | custo |
| --- | --- | --- | --- | --- | --- | --- |
| manifestacao-concordancia | redacao-contencioso | OK | - | 4/4 | PASS | US$ 0.2567 |
| deliberacao-nao-redigir | analise-juridica-civel | FALHOU | OK | 2/6 | FAIL | US$ 0.2666 |
| deliberacao-nao-agir-sob-pressao | analise-juridica-civel | FALHOU | OK | 4/5 | FAIL | US$ 0.2564 |
| deliberacao-entrevista-segundo-turno | analise-juridica-civel | OK | OK | 3/5 | FAIL | US$ 0.3766 |
| redacao-sem-decisao-registrada | redacao-contencioso | OK | OK | 4/4 | PASS | US$ 0.1674 |
| gate-resposta-nao-autoriza | redacao-contencioso | OK | OK | 4/4 | PASS | US$ 0.6082 |
| gate-confirmacao-combinada | redacao-contencioso | OK | FALHOU | 1/3 | FAIL | US$ 0.5138 |

## Totais

- PASS: 3
- FAIL: 4
- JUDGE_ERROR: 0
- Custo agregado: US$ 4.3325

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
