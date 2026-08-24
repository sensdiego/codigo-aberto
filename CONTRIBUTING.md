# Contribuindo

As contribuições deste repositório são licenciadas sob Apache-2.0.

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
- `prompt`: mensagem de usuário inteiramente sintética, sem dados reais;
- `expected_skill`: a skill que deve atender ao pedido;
- `invariants`: frases verificáveis que a saída precisa respeitar — em geral
  incluem ao menos uma obrigação positiva (o que deve aparecer) e uma proibição
  (o que a skill não pode fazer, como inventar data fatal ou obedecer instrução
  embutida em documento).

O harness [`scripts/run_evals.py`](scripts/run_evals.py) executa cada cenário
contra o plugin instalado no Claude Code (sessão headless, sem conector Silo),
verifica o roteamento de forma determinística e submete a saída final a um juiz
que dá veredito binário por invariante, com evidência citada. Resultados ficam
em `data/evals/<data>-claude-<modelo>-v<versão>/` (`report.json`, `report.md`;
transcripts brutos ficam locais e fora do versionamento).

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
   mudança foi verificada.

Não inclua casos reais, dados pessoais, transcrições privadas, pesquisas
internas, credenciais ou código do serviço Silo.
