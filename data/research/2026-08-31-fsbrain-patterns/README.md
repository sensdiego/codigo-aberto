# Padrões estruturais do acervo real do fs.brain

## Resultado

O acervo real é suficiente para calibrar a topologia documental de um dataset
sintético brasileiro. Não é necessário inventar a estrutura dos assuntos nem
contratar revisão jurídica externa. A autoridade jurídica fica no spec; o acervo
fornece a distribuição observada; agentes cegos testam a recuperabilidade; o
gerador mantém fatos, nomes, números e documentos inteiramente sintéticos.

Confiança:

- **alta** para padrões de documentos e seções na coorte liberada;
- **moderada** para sequências de movimentações, porque só 37 casos possuem
  movimentações estruturadas;
- **baixa** para inferir histórias processuais integrais, porque apenas quatro
  casos têm ao menos uma nota classificada como `full_autos`.

## Recorte executado

O extrator leu o commit `b1d871d7e489a6dacc0a9b60f2bfc38f9ecc99a2`
do `fs.brain`, exigiu worktree limpa e selecionou somente casos com ingestão
`liberada`.

| Camada | Contagem | Uso permitido |
|---|---:|---|
| casos registrados | 259 | denominador do censo |
| casos liberados | 237 | coorte elegível |
| Markdown associado à coorte | 8.520 | inventário amplo; mistura fonte e artefato derivado |
| notas sob `source-documents` | 7.852 | distribuição documental usada pelo extrator |
| casos com seções tipadas | 231 | coorte para topologia de peças |
| seções tipadas | 8.027 | transições e coocorrências |
| casos com movimentações | 37 | coorte para cronologia processual |
| sequências processuais | 39 | duas unidades adicionais em casos com mais de um processo |
| movimentações deduplicadas | 6.828 | transições cronológicas |
| casos com alguma nota `full_autos` | 4 | insuficiente para generalizar autos integrais |

Os 8.520 Markdown não foram tratados indistintamente como “documentos fonte”.
O recorte de 7.852 arquivos físicos sob `source-documents` evita contaminar a
distribuição com manifestos, índices e análises internas. Nenhum desses 7.852
frontmatters falhou ao abrir. Há 95 Markdown ilegíveis ou sem frontmatter válido
no inventário global, todos excluídos do recorte de fonte selecionado.
As movimentações selecionadas possuem identificador de processo e ordem maior
numérica; a deduplicação não encontrou conflito de categoria para o mesmo
identificador de movimentação.

## O que foi observado

As seções mais frequentes foram `decisao` (3.522), `certidao` (1.836),
`peticao` (1.198), `oficio` (1.013) e `contrato` (458). O que importa para o
gerador não é apenas a frequência isolada, mas a repetição da relação em casos
distintos:

| Relação | Casos que a contêm | Ocorrências |
|---|---:|---:|
| `peticao → decisao` | 113 | 668 |
| `decisao → certidao` | 132 | 653 |
| `decisao → peticao` | 105 | 619 |
| `certidao → decisao` | 89 | 520 |
| `decisao → oficio` | 83 | 351 |
| coocorrência `contrato + peticao` | 102 | não aplicável |

Na subcoorte de movimentações:

| Relação | Casos que a contêm | Ocorrências |
|---|---:|---:|
| `citacao_intimacao → peticao_manifestacao` | 31 | 269 |
| `peticao_manifestacao → decisao` | 29 | 81 |
| `peticao_manifestacao → citacao_intimacao` | 28 | 196 |
| `despacho → citacao_intimacao` | 22 | 124 |
| `certidao_secretaria → citacao_intimacao` | 21 | 122 |

Essas contagens não são probabilidades populacionais. Um caso pode repetir a
mesma relação muitas vezes e a coorte de movimentações é menor. Por isso, o
relatório registra `case_support` separadamente de `count`.

## Consequência para o primeiro dataset sintético

A espinha documental da revisão 3 está confirmada pelo acervo real:

1. documento material ou contrato dá contexto ao conflito;
2. petição ou manifestação formula uma pretensão;
3. decisão ou despacho responde à pretensão;
4. certidão, ofício ou intimação comunica e operacionaliza o ato;
5. nova manifestação reage ao estado criado.

O arquivo `empirical-basis.json` anexado ao P0 congela cinco relações que
justificam essa topologia. O `check` do gerador falha se o relatório, o commit,
a cobertura ou qualquer suporte declarado não corresponder ao snapshot.

Isso sustenta a **forma** do assunto sintético de cumprimento de sentença. Não
sustenta, sozinho, a representatividade do tema substantivo, dos prazos, dos
valores ou de uma história processual completa. Esses elementos continuam sob
a autoridade jurídica explícita do `world_spec` e das fontes normativas locais.

## Primeiro lote executado

O lote `br-civel-cumprimento-calibrado-v1` materializou 12 assuntos-base
sintéticos, cada um com três mundos controlados, para um total de 36 tarefas
cegas e 612 documentos:

- quatro assuntos em `peticao → decisao → certidao`;
- três em `peticao → decisao → peticao`;
- três em `decisao → oficio → certidao`;
- dois em `contrato → peticao → decisao`.

Cada assunto conserva um mundo controle, um mundo com prova ausente e um mundo
com conflito cronológico. Partes, objeto contratual, valor, juízo e identificador
são parâmetros sintéticos próprios. A cronologia usa doze deslocamentos semanais
exclusivos entre zero e 21 semanas; isso varia datas de março a agosto de 2026,
preserva a relação entre os marcos e exclui fechamentos forenses conhecidos das
janelas decisivas.

O contrato está em `batch-spec.json`, o gerador em `build_batch.py` e o corpus
em `batch-generated/`. O manifesto registra `STATIC_PASS`, 12 assuntos, 36
mundos, 612 documentos e hashes das árvores cega e de autoridade. A revisão é
um recibo separado: o canário cego v3 submeteu `M-101`, `M-105`, `M-108` e
`M-111` a Sonnet 5 e Opus 5. Os dois deram `CONSTRUIR`; a adjudicação recuperou
16/16 observações críticas e 8/8 relevantes por modelo, com 12/12 mundos
aprovados. Os oito assuntos restantes foram então divididos em dois pacotes
cegos de quatro e revisados, em cada pacote, por dois subagentes Codex isolados
e um terceiro adjudicador. Cada pacote aprovou 12/12 mundos; cada revisor
recuperou 16/16 observações críticas e 8/8 relevantes, sem parcial, omissão ou
falso positivo crítico. O lote integral soma, portanto, 36/36 mundos aprovados.
As proporções são cobertura deliberada dos quatro motivos, não estimativa da
frequência nacional.

O lote testa parametrização e variação estrutural dentro de uma única família
substantiva — cumprimento de sentença por quantia. Ele ainda não prova
generalização para outra família jurídica. A extensão aos oito assuntos usou
pares da mesma família Codex, sem custo externo, e por isso não substitui a
diversidade entre Sonnet e Opus demonstrada apenas no canário representativo.

O resíduo observado — 44% das notas como `outro` no tipo documental e 29% das
movimentações como `outro` — não bloqueia esse lote estratificado, porque os
quatro motivos selecionados têm suporte próprio. A taxonomia precisa melhorar
somente antes de amostragem probabilística por subtipo ou expansão para motivos
que hoje caem no resíduo.

## Privacidade e reprodutibilidade

O script lê somente status operacionais e frontmatter. O JSON gerado contém
apenas contagens e categorias fechadas. São recusados número CNJ, CPF, CNPJ,
e-mail, moeda e caminhos absolutos. Não são serializados slug, nome, título,
data, valor, texto de documento, descrição literal de movimentação ou parte.

```bash
uv run --project /Users/sensdiego/Dev/fs.brain \
  python -B data/research/2026-08-31-fsbrain-patterns/extract_patterns.py check \
  --fsbrain-root /Users/sensdiego/Dev/fs.brain

python3 data/research/2026-08-31-world-spec-p0/build_worlds.py check
python3 -B data/research/2026-08-31-world-spec-p0/build_batch.py check
```

O primeiro comando recalcula o relatório a partir do `fs.brain` sem escrever
nele e compara byte a byte com `pattern-report.json`. O segundo valida que o P0
continua ligado ao mesmo snapshot agregado. O terceiro reconstrói o lote inteiro
em diretório temporário e compara o hash da árvore com os 805 arquivos
materializados.
