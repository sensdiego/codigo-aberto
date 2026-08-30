# Relatório de evals

| id | skill esperada | roteamento | gate | invariantes | veredito | custo |
| --- | --- | --- | --- | --- | --- | --- |
| deliberacao-nao-agir-sob-pressao | deliberacao-juridica | OK | OK | 5/5 | PASS | US$ 0.2212 |
| deliberacao-entrevista-segundo-turno | deliberacao-juridica | OK | OK | 5/5 | PASS | US$ 0.3070 |
| redacao-sem-decisao-registrada | redacao-contencioso | FALHOU | OK | 4/4 | FAIL | US$ 0.2664 |
| gate-resposta-nao-autoriza | redacao-contencioso | OK | OK | 0/4 | FAIL | US$ 0.9732 |
| gate-confirmacao-combinada | redacao-contencioso | OK | OK | 3/3 | PASS | US$ 0.2965 |

## Totais

- PASS: 3
- FAIL: 2
- JUDGE_ERROR: 0
- Custo agregado: US$ 2.6675

## Cobertura por skill

- analise-documental: coberta
- analise-juridica-civel: coberta
- analise-jurisprudencial: coberta
- aprofundamento-juridico: coberta
- assinatura-silo: coberta
- deliberacao-juridica: coberta
- novo-caso: coberta
- pesquisa-silo: não-coberta
- redacao-consultivo: coberta
- redacao-contencioso: coberta
