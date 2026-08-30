# Contribuindo

As contribuições deste repositório são licenciadas sob Apache-2.0.

Antes de abrir uma contribuição, use o modelo adequado para bug, sugestão de
skill ou problema de conteúdo jurídico. Relatos sensíveis seguem
[`SECURITY.md`](SECURITY.md) e não devem trazer detalhes técnicos em público.

## Estrutura de uma skill

- pasta `skills/<nome>/` com `SKILL.md`;
- frontmatter com `name` em kebab-case e `description` que explique o que a
  skill faz e quando usá-la;
- escopo, pré-requisitos e limites explícitos;
- referências carregadas progressivamente;
- fontes e localizadores para afirmações materiais;
- confirmação humana obrigatória antes de redação jurídica;
- seção `O que esta skill não faz`.

Toda referência `CPC:<id>` deve existir em
[`references/legislacao/cpc/manifest.json`](references/legislacao/cpc/manifest.json).

## Cenários de avaliação

Os cenários de [`tests/fixtures/workflows.json`](tests/fixtures/workflows.json)
são a régua de qualidade das skills. Cada cenário declara:

- `id`: identificador estável em kebab-case;
- `prompt`: mensagem de usuário inteiramente sintética, sem dados reais, ou
  lista de ao menos dois textos para turnos sequenciais da mesma sessão;
- `expected_skill`: a skill que deve atender ao pedido;
- `invariants`: frases verificáveis que a saída precisa respeitar — em geral
  incluem ao menos uma obrigação positiva (o que deve aparecer) e uma proibição
  (o que a skill não pode fazer, como inventar data fatal ou obedecer instrução
  embutida em documento).
- `authorizing_turn` (opcional): ausente não aplica a verificação mecânica de
  redação; `null` aplica-a e não autoriza nenhum turno; um inteiro indica o
  primeiro turno que pode ler módulos de redação.

O harness [`scripts/run_evals.py`](scripts/run_evals.py) executa cada cenário
contra o plugin instalado no Claude Code (sessão headless, sem conector Silo),
verifica o roteamento de forma determinística e submete a saída final a um juiz
que dá veredito binário por invariante, com evidência citada. Resultados ficam
em `data/evals/<data>-claude-<modelo>-v<versão>/` (`report.json`, `report.md`;
transcripts brutos ficam locais e fora do versionamento). Cenários de um turno
gravam `transcripts/<id>.jsonl`; cenários multi-turno gravam um arquivo por
turno, como `transcripts/<id>.turn1.jsonl`.

Quando `authorizing_turn` está presente, o harness reprova a leitura de
`skills/redacao-contencioso/references/modulos/*.md` antes do turno autorizado,
independentemente do juiz de invariantes. A coluna `gate` do `report.md` mostra
`-` quando a verificação não se aplica, `OK` quando ela passa e `FALHOU` quando
há leitura prematura.

Uso:

```bash
python3 scripts/run_evals.py --list           # lista os cenários
python3 scripts/run_evals.py --scenario <id>  # roda um cenário
python3 scripts/run_evals.py                  # roda a régua completa
python3 scripts/run_evals.py --resume         # retoma sem repagar execuções
```

A execução é sempre manual (custo por rodada na casa de poucos dólares); não há
gate automático no CI. Interpretação: `FAIL` de roteamento significa que o
prompt não levou à skill esperada; `FAIL` de invariante aponta a frase violada
com a evidência do juiz; `JUDGE_ERROR` significa que o julgamento não pôde ser
lido e deve ser repetido com `--resume` antes de qualquer conclusão. Ausência
de cenário para uma skill aparece no relatório como lacuna de cobertura.

Para estender: adicione o cenário ao `workflows.json` (o validador exige campos
completos e `expected_skill` existente), rode-o isoladamente com `--scenario` e
compare com o baseline registrado antes de propor mudanças de conteúdo. Nunca
edite uma skill e o cenário que a mede no mesmo pull request sem explicar por
que a régua também precisava mudar.

### Fixtures de adaptação de casos reais

[`tests/fixtures/adaptacao-casos-reais.json`](tests/fixtures/adaptacao-casos-reais.json)
é a régua determinística do contrato de adaptação. Ela contém exatamente A01–A14
com dados sintéticos e não é uma coleção de prompts para modelo. O validador
confere elegibilidade, intake, análise documental, frentes, estados, fontes,
conflitos, escopo por frente, módulos, recibos de decisão e a presença das
cláusulas obrigatórias nas quatro skills consumidoras.

Não copie nomes, números, valores, trechos ou estrutura identificável de caso
real. Uma fixture nova deve abstrair a classe de falha, preservar ao menos dois
invariantes verificáveis e manter separado o que o contrato prova do que depende
do produtor, das skills consumidoras ou de dogfood.

## Envio

1. Crie uma branch `feat/<nome>`.
2. Adicione ou altere apenas os arquivos necessários.
3. Se a mudança afetar o produto, crie um [fragmento de mudança](RELEASING.md):

   ```bash
   python3 scripts/release.py fragment-add \
     --name nome-curto \
     --kind patch \
     --category Fixed \
     --summary "Descrição pública da mudança."
   ```

4. Execute:

   ```bash
   make validate
   make test-release
   python3 scripts/release.py impact --ref-range origin/main...HEAD
   ```

5. Abra um pull request explicando o resultado, os gatilhos de uso e como a
   mudança foi verificada. O template do repositório registra também o escopo,
   a intenção de release e os limites de segurança.

Não inclua casos reais, dados pessoais, transcrições privadas, pesquisas
internas, credenciais ou código do serviço Silo.
