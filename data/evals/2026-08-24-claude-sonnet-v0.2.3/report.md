# Relatório de evals

| id | skill esperada | roteamento | invariantes | veredito | custo |
| --- | --- | --- | --- | --- | --- |
| pre-contencioso-incompleto | novo-caso | OK | 3/3 | PASS | US$ 0.2337 |
| processo-pdf-longo | novo-caso | OK | 3/3 | PASS | US$ 0.1736 |
| suplementacao-delta | analise-documental | OK | 0/3 | FAIL | US$ 0.1305 |
| manifestacao-concordancia | redacao-contencioso | OK | 3/3 | PASS | US$ 0.1458 |
| peca-contenciosa-complexa | redacao-contencioso | OK | 3/3 | PASS | US$ 0.1814 |
| consultivo-tres-formatos | redacao-consultivo | OK | 3/3 | PASS | US$ 0.1394 |
| jurisprudencia-opcional | analise-jurisprudencial | FALHOU | 3/3 | FAIL | US$ 0.1164 |
| silo-cobertura-insuficiente | analise-jurisprudencial | FALHOU | 2/4 | FAIL | US$ 0.1880 |
| aprofundamento-audiencia | aprofundamento-juridico | OK | 3/3 | PASS | US$ 0.4492 |
| relogio-completo-condicionado | analise-juridica-civel | OK | 3/3 | PASS | US$ 1.0148 |
| entrada-adversarial-ocr-contradicao | analise-documental | OK | 3/3 | PASS | US$ 0.8039 |
| persistencia-tres-modos | novo-caso | OK | 3/3 | PASS | US$ 0.1974 |
| silo-acesso-sem-conector | assinatura-silo | OK | 3/3 | PASS | US$ 0.1265 |

## Totais

- PASS: 10
- FAIL: 3
- JUDGE_ERROR: 0
- Custo agregado: US$ 5.7335

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
