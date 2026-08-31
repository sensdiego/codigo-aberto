# Dossiê — Fábrica de datasets sintéticos da Harvey e equivalente jurídico brasileiro

| Campo | Valor |
|---|---|
| Status | **Lote de 12 assuntos/36 mundos aprovado estaticamente e no executor Codex skill-backed: 36/36 mundos e 252/252 invariantes** |
| Data de corte | 2026-08-31 |
| Escopo | BigLaw Bench, Harvey LAB, métodos públicos de geração sintética e desenho da investigação brasileira neste repositório |
| Decisão recomendada | **CONGELAR ESTE P0 COMO BENCHMARK DE REGRESSÃO E NÃO AMPLIAR A ESCALA ANTES DE ESCOLHER UMA SEGUNDA FAMÍLIA JURÍDICA** |
| Confiança | **Alta** na integridade mecânica, proveniência e recuperabilidade do lote; **moderada** na diversidade dos revisores dos oito assuntos e na generalização além de cumprimento de sentença |
| Destino possível | SEN-1746 — laboratório de benchmarks abertos; nenhuma ação externa foi executada |

## Decisão em uma frase

O ativo investigado não é o benchmark pronto, mas a capacidade de converter
uma especificação jurídica oculta em documentos interdependentes, problemas
plantados, proveniência, gabarito e rubrica. A prova mecânica local passou; a
revisão cega por Sonnet 5 e Opus 5 recuperou os três mundos e aprovou a
construção do P0. O lote foi então materializado em 12 assuntos, 36 mundos e
612 documentos. Um canário por agentes sobre quatro assuntos encontrou e
corrigiu um erro de harness e dois defeitos de realismo antes de aprovar 12/12
mundos. Dois pares cegos de subagentes Codex e dois adjudicadores aprovaram os
24 mundos restantes sem chamada externa. Os 12 assuntos aprovados foram
integrados ao executor local como 36 cenários, sem duplicar os 612 documentos.
O baseline funcional Codex encontrou uma omissão do art. 524. Ao receber a
skill-alvo no pacote cego, o agente corrigiu W-B; o lote integral encontrou a
mesma classe de falha em outro assunto, endureceu a skill por uma regra geral e
fechou 36/36 mundos. Um segundo incidente revelou JSON incompleto do juiz e
endureceu o runner sem reexecutar o agente. O P0 agora é um benchmark local
auditável; o próximo gate é escolher se existe valor em construir uma segunda
família jurídica, sem revisão manual do owner e sem contratação de revisor
jurídico externo.

## Nota de correção

A primeira versão deste dossiê descreveu adequadamente o artefato publicado,
mas errou o centro estratégico e uma contagem material:

- tratou o contrato de tarefa como o principal ativo, quando as fontes mais
  recentes mostram uma fábrica de mundos sintéticos usada para avaliação e
  treinamento;
- recomendou um assunto manual com três tarefas, que provaria o avaliador local,
  mas não a capacidade de gerar datasets;
- declarou como exata uma árvore Git para a qual a API retornou
  `truncated=true`;
- contou 504 documentos em Firm Knowledge, cujo acervo possui 9.288 arquivos.

A recontagem por subárvores individualmente não truncadas preservou as 2.010
tarefas, mas corrigiu o total para **60.979 documentos** e
**3.206.967.747 bytes documentais**. A decisão `EXPERIMENTAR` da versão
anterior está retirada; a pesquisa, sozinha, não autorizava implementação. A
execução standalone abaixo ocorreu por autorização posterior e não autoriza
integração com o produto.

## Nota de execução da investigação

Após autorização do owner, a investigação mínima foi executada localmente em
`data/research/2026-08-31-world-spec-p0/`, inicialmente sem integrar o harness
e sem executar modelo. Uma autoridade única gerou três pastas cegas opacas:

- `W-A`: 17 documentos;
- `W-B`: 16 documentos, diferindo do controle apenas pela retirada do
  comprovante de pagamento;
- `W-C`: 17 documentos, diferindo do controle apenas pela data da certidão de
  publicação.

O build e o check independentes passaram. Eles resolvem cinco fontes locais do
CPC, fatos, critérios e localizadores; verificam hashes, proveniência,
autoridades de rubrica, ausência de rótulos internos na view cega e isolamento
das duas mutações. A mutação cronológica também atravessa, de propósito, o
prazo de quinze dias numa contagem apenas de dias úteis: esse check prova que a
divergência é material, não que o prazo jurídico concreto esteja resolvido.

Na máquina da sessão, a regeneração levou 0,05 s e o check separado 0,03 s.
Esses tempos medem somente processamento local. Sonnet 5 e Opus 5 concluíram a
revisão cega da revisão 3 e o canário de quatro assuntos do lote. Os oito
assuntos restantes foram medidos em dois pacotes cegos por subagentes Codex:
24/24 mundos aprovados, sem chamada externa. Nenhum documento gerado foi
corrigido manualmente; as correções foram feitas na especificação ou no
renderer e o conjunto foi regenerado.

## Resumo executivo

A premissa inicial de que “o benchmark público da Harvey é o BigLaw Bench” está
desatualizada. Em 2026 existem dois artefatos públicos materialmente diferentes:

1. **BigLaw Bench**, de 2024, é uma amostra de um benchmark interno. O GitHub
   contém seis tarefas Core, dez acordos de compra e venda de ações e trinta
   consultas de recuperação. O conjunto completo permanece retido pela Harvey.
   O repositório não declara licença. Ele é útil para estudar taxonomia e
   rubricas, mas não é base segura para copiar, adaptar nem alegar
   reprodutibilidade.
2. **Harvey Legal Agent Benchmark (LAB)**, de 2026, é um dataset e harness sob
   licença MIT. A tag `v1.0` contém 1.760 tarefas; o `main` examinado contém
   2.010 `task.json`, 60.979 documentos e 3.206.967.747 bytes de documentos. A
   unidade é trabalho de agente de longa duração: receber um assunto sintético,
   localizar arquivos relevantes e produzir um artefato jurídico revisável.

O LAB é a referência técnica correta, mas não deve ser adotado sem correções.
Os resultados publicados pela Harvey não são reproduzíveis apenas com o
dataset aberto: eles usam um **holdout privado** que espelha a distribuição
pública. O `main` ainda muda, o perfil de juízes mudou depois da tag `v1.0`, a
documentação apresenta contagens incompatíveis com a árvore e há issues abertas
que demonstram critérios impossíveis, fatos errados, rubricas incompletas,
documentos de assuntos diferentes e falhas de infraestrutura transformadas em
notas aparentemente válidas.

Por isso, a recomendação não é “portar o LAB” nem escrever manualmente três
fixtures. A investigação corrente verifica se este workspace consegue
representar um assunto brasileiro numa especificação curta e, a partir dela,
derivar de forma rastreável documentos, variações, gabarito e rubrica. A parte
estática passou; o harness existente só entra depois da prova humana.

## 1. Pergunta, método e limite da prova

### 1.1 Pergunta

O que a Harvey publicou de fato, como ela transforma conhecimento jurídico em
datasets sintéticos para avaliar e treinar produtos e qual hipótese precisa ser
validada antes de construir um equivalente brasileiro aberto?

### 1.2 Método

A pesquisa usou somente fontes públicas e leitura local neste workspace:

- inventário ao vivo da organização `harveyai` e das árvores Git via API do
  GitHub;
- inspeção de README, licença, documentação, código do harness, tarefas de
  amostra, histórico, tag e issues;
- artigos metodológicos oficiais da Harvey sobre LAB, Diligence, Firm
  Knowledge, Review Table e Tenet;
- transcrição publicada pela Sequoia da palestra do cofundador Gabe Pereyra
  sobre geração de dados, post-training e produção;
- confronto com `scripts/run_evals.py`, os dois fixtures de workflow, os
  relatórios congelados e os contratos deste repositório.

Os números do LAB foram recalculados sem confiar no badge do README nem em
resposta recursiva truncada. As 25 famílias ordinárias foram enumeradas por
subárvore; os onze cenários de Diligence, o DMS de Firm Knowledge e suas 250
tarefas foram contados separadamente. Todas as árvores usadas no somatório
final retornaram `truncated=false`. Nenhum repositório externo foi clonado ou
alterado.

### 1.3 Snapshots examinados

| Artefato | Snapshot | Observação |
|---|---|---|
| BigLaw Bench | `138fd481b459a00bbd98eeb710f69ada1052bd47` | `main`, último commit em 2025-10-08 |
| LAB estável | tag anotada `v1.0`, commit `1da4750171bc5a534960b3d82d15ba7fd2cf653f` | 1.760 tarefas em 26 famílias de topo |
| LAB corrente | `a2b429eb6c9683c4fdeced3bc6b3af36edf239a6` | `main`, 2026-08-26; perfil dual de juízes como padrão |
| Workspace local | `main` em `50f6ee7` no início da análise | limpo e igual a `origin/main` |

### 1.4 O que esta pesquisa não prova

- Não audita juridicamente as 2.010 tarefas do LAB.
- Não reproduz os números da Harvey, porque o holdout oficial não é público.
- Não prova que uma nota de benchmark se correlaciona com uso profissional no
  Brasil.
- Não expõe o código, os prompts, os custos, as taxas de rejeição nem o manual
  interno completo da fábrica sintética da Harvey.
- Não prova que documentos sintéticos reproduzem a distribuição de pedidos do
  produto; o próprio cofundador identifica essa diferença como problema aberto.
- Não autoriza gasto com modelos, importação de dados, nova dependência,
  publicação, release, dogfood ou ação no SEN-1746.
- Não encontrou paper acadêmico, DOI ou protocolo de revisão por pares do LAB
  nas buscas dirigidas em arXiv, ACL Anthology e OpenReview. A especificação
  canônica disponível é o repositório mais os artigos da própria Harvey.

### 1.5 Matriz de confiança

| Conclusão | Confiança | Base |
|---|---|---|
| nomes, commits, contagens corrigidas e licença dos repositórios | **Alta** | inspeção direta e soma de subárvores não truncadas |
| distinção entre amostra BigLaw Bench e dataset+harness LAB | **Alta** | estrutura dos repositórios e documentação oficial convergem |
| arquitetura da fábrica sintética | **Alta** | palestra do cofundador e três implementações oficiais convergem |
| receita proprietária de autoria, geração e revisão | **Desconhecida** | código do gerador, prompts e protocolo integral não são públicos |
| validade dos resultados oficiais do LAB | **Moderada** | método e números são publicados, mas o holdout e as execuções não são reproduzíveis publicamente |
| correlação entre LAB e qualidade profissional brasileira | **Desconhecida** | nenhuma validação brasileira foi localizada ou executada |
| viabilidade de um gerador brasileiro | **Moderada como hipótese**, não como capacidade | o workspace possui consumidor e regras, mas não possui gerador nem QA do corpus |
| inexistência de paper acadêmico | **Moderada** | buscas dirigidas não encontraram resultado; ausência em índices não prova inexistência universal |

## 2. Inventário público da Harvey

### 2.1 Quadro consolidado

| Artefato | O que é | O que está público | Avaliação reproduzível? | Licença |
|---|---|---|---|---|
| BigLaw Bench Core | prompts e documentos para respostas jurídicas relativamente curtas | 6 registros e 14 PDFs | Não: é amostra, sem harness completo nem conjunto integral | Nenhuma detectada |
| BigLaw Bench Workflows — SPA | extração estruturada de 29 campos de contratos | 10 SPAs, CSV e schema JSON | Parcialmente: entradas e alvos existem, mas não o pipeline integral reportado | Nenhuma detectada |
| BigLaw Bench Retrieval | consultas sobre contratos e e-mails | 30 consultas e 30 PDFs de contratos; e-mails completos ficam em fonte externa | Parcialmente: faltam protocolo e respostas de referência públicas no CSV | Nenhuma detectada |
| BLB: Global | tarefas locais para Reino Unido, Austrália e Espanha | metodologia e exemplos em artigo | Não encontrei dataset correspondente no GitHub público da Harvey | Não aplicável ao artigo |
| BLB: Research | problemas difíceis de pesquisa jurisprudencial dos EUA | metodologia e exemplos em artigo | Não encontrei dataset correspondente no GitHub público da Harvey | Não aplicável ao artigo |
| BLB: Practice Areas | profundidade por área jurídica | anunciado para seis áreas | Não encontrei publicação própria ou dataset no GitHub até a data de corte | Não identificada |
| Harvey LAB | tarefas de agente, documentos sintéticos, rubricas e harness | dataset completo do repositório, código, docs e histórico | O conjunto público roda; o placar oficial não, pois usa holdout privado | MIT no repositório |

Conclusão: **“publicamente descrito” e “publicamente baixável” não são a mesma
coisa**. As expansões de 2026 do BigLaw Bench foram descritas como públicas,
mas não aparecem no único repositório `biglaw-bench` nem em outro repositório
de benchmark da organização examinado. O LAB, ao contrário, oferece arquivos e
código executável.

### 2.2 Linha evolutiva

| Data | Mudança |
|---|---|
| 2024-08-29 | lançamento do BigLaw Bench como versão pública de benchmark interno |
| 2026-02-09 | anúncio da expansão de BLB em Global, Practice Areas e Research |
| 2026-02-18 | descrição do BLB: Global |
| 2026-03-11 | descrição do BLB: Research |
| 2026-05-06 | abertura do Harvey LAB para trabalho jurídico de longa duração |
| 2026-05-26 | primeiros resultados do LAB, calculados em holdout privado |
| 2026-06-12 | extensão LAB Contracts anunciada como 500 tarefas |
| 2026-07-17 | LAB Diligence publica VDRs sintéticos com problemas plantados e rubricas derivadas |
| 2026-07-24 | tag `v1.0` do LAB |
| 2026-08-07 | Firm Knowledge publica especificação curta, renderização de 10–200 documentos e 250 tarefas |
| 2026-08-14 | Review Table descreve corpus público, queries sintéticas, agentes-oráculo e QA humano |
| 2026-08-20 | Tenet registra uso conjunto de dados sintéticos, públicos e de especialistas em post-training |
| 2026-08-26 | dois LLM-judges passam a ser o padrão do harness público |

## 3. BigLaw Bench em profundidade

### 3.1 Natureza do benchmark

O BigLaw Bench converte registros semelhantes a lançamentos de tempo de
advogados em pares de prompt e documentos. A intenção é medir tarefas que se
aproximem de trabalho faturável, em vez de questões de múltipla escolha. O
Core cobre raciocínio, análise e redação sem exigir workflow agente composto.

O artigo de lançamento declara que as tarefas foram concebidas pela equipe de
pesquisa jurídica da Harvey, composta por advogados com experiência em grandes
escritórios, e construídas com documentos públicos. Isso é uma declaração do
fornecedor; o conjunto completo, as instruções de anotação e as medidas de
acordo entre avaliadores não foram publicados.

### 3.2 Estrutura efetivamente publicada

#### Core

O arquivo `blb-core/core-samples.csv` possui sete colunas:

`Number`, `Category`, `Task Type`, `Task`, `Prompt`, `Document(s)` e `Rubric`.

Há seis registros:

1. alerta ao cliente sobre ordem judicial;
2. cronologia e inconsistências em documentos de julgamento;
3. memo sobre tratamento de equity awards em fusão;
4. consentimento do conselho sobre potencial conflito;
5. análise de cláusulas de reembolso em precedentes;
6. objeções a subpoena federal.

O diretório contém quatorze PDFs além do CSV e README. A rubrica é texto
embutido no CSV, com pontos afirmativos e negativos. Não há resposta-modelo.

#### Workflows — SPA Deal Points

O arquivo `spa-samples.csv` possui dez registros e 29 colunas de extração, como
partes, preço, capitalização, ajustes, indenização, condições de fechamento,
lei aplicável, foro, rescisão, impostos, despesas e notificações. Dez SPAs em
PDF acompanham o CSV. `schema.json` apresenta uma forma JSON equivalente, mas o
CSV é a resposta de referência publicada.

Esse componente é o mais reproduzível do BigLaw Bench: existe documento de
entrada e existe alvo estruturado. Ainda faltam normalização, regras de match,
tolerância, harness e licença.

#### Retrieval

O arquivo `samples.csv` contém trinta linhas com apenas `Query` e `Source`:

- dez consultas sobre e-mails de discovery;
- dez consultas sobre merger agreements;
- dez consultas sobre SPAs.

O diretório contém vinte merger agreements e dez SPAs em PDF. Para discovery,
o README aponta o corpus de e-mails Clinton publicado pelo Departamento de
Estado dos EUA. Não há no CSV uma resposta correta, conjunto de documentos
relevantes, métrica ou julgamento esperado por consulta.

### 3.3 Taxonomia Core

O artigo reporta a seguinte distribuição do conjunto completo, não da amostra
de seis linhas:

| Transacional | Fração |
|---|---:|
| Estratégia corporativa e aconselhamento | 28,3% |
| Redação | 24,5% |
| Pesquisa jurídica | 13,2% |
| Due diligence | 11,3% |
| Risco e compliance | 9,4% |
| Estratégia de negociação | 5,7% |
| Gestão do negócio | 3,8% |
| Estruturação da transação | 3,8% |

| Contencioso | Fração |
|---|---:|
| Análise de peças | 25,5% |
| Gestão do caso | 23,4% |
| Redação | 14,9% |
| Pesquisa jurisprudencial | 8,5% |
| Análise de transcrição | 8,5% |
| Revisão e análise documental | 6,4% |
| Regulação e aconselhamento | 6,4% |
| Preparação para julgamento e sustentação | 6,4% |

A utilidade dessa taxonomia está no eixo **tipo de trabalho**, não nos rótulos
“litigioso/transacional”. Um equivalente brasileiro deve cruzar tipo de
trabalho com jurisdição, ramo, fase, ato e papel processual.

### 3.4 Avaliação original

Cada tarefa usa uma rubrica própria com:

- pontos positivos ponderados pela importância do requisito;
- pontos negativos para erros e falhas como alucinação, tom ou extensão
  inadequados;
- `answer score` igual à soma de pontos positivos e negativos dividida pelo
  total de pontos positivos disponíveis;
- `source score` separado, que mede a proporção de afirmações corretas
  sustentadas por fonte verificável.

Essa separação entre qualidade e rastreabilidade é melhor que um único placar.
Também admite utilidade parcial. Sua fraqueza é a falta de protocolo público
completo: não estão disponíveis todos os itens, o harness, a amostragem, a
calibração dos avaliadores nem o conjunto integral de rubricas.

### 3.5 Expansões de 2026

O BLB: Global acrescenta seis tipos de tarefa — redação, análise de documento
longo, comparação, pesquisa pública, análise multidocumental e extração — em
Reino Unido, Austrália e Espanha. A Harvey relata colaboração de mais de duas
dezenas de especialistas locais e revisão cruzada por sua equipe de pesquisa.

O BLB: Research une busca e resposta. O modelo deve pesquisar jurisprudência
dos EUA e entregar resposta citada. A construção partiu de problemas úteis e
depois procurou empiricamente os que ainda separavam modelos de fronteira,
evitando dificuldade meramente esotérica.

A expansão por Practice Areas foi anunciada para Capital Markets, M&A, Fund
Formation, Litigation, Arbitration e Intellectual Property. Até a data de
corte, não foi localizada uma publicação metodológica própria equivalente às
duas anteriores.

Nenhuma dessas expansões aparece como dados novos no snapshot público do
`biglaw-bench`. Elas informam desenho, mas não fornecem material reproduzível.

### 3.6 Licença e decisão de reuso

O repositório não contém `LICENSE`, e a API do GitHub retorna licença nula.
Repositório público não equivale a obra sob licença aberta.

Decisão:

- **pode ser referenciado e estudado**;
- **não deve ser copiado, traduzido, redistribuído nem usado como base de
  tarefas derivadas** sem uma licença ou autorização adicional;
- sua taxonomia e ideias abstratas podem informar o desenho brasileiro;
- seus números não devem ser chamados de reproduzidos por terceiros.

## 4. Harvey LAB em profundidade

### 4.1 A mudança de unidade

O LAB deixa de perguntar “quanto de uma resposta o modelo completou?” e passa a
perguntar “o agente entregou todo o trabalho revisável?”. Cada tarefa contém:

1. uma instrução curta, formulada como pedido de sócio a associado;
2. um assunto fechado com documentos relevantes e periféricos;
3. um ou mais entregáveis;
4. critérios binários atômicos que representam a revisão do trabalho.

O artigo informa instruções com média aproximada de cinquenta palavras. A
contribuição ao repositório exige pessoas, empresas, escritórios, endereços e
fatos sintéticos e veda material real confidencial.

### 4.2 Versões e contagem independente

| Snapshot | Tarefas | Famílias de topo | Observação |
|---|---:|---:|---|
| artigo de lançamento | “mais de 1.200”; também chama uma tarefa de uma entre 1.250 | 24 | número editorial |
| tag `v1.0` | **1.760** | 26 | 24 áreas + Contracts + Diligence |
| `main` em 2026-08-26 | **2.010** | 27 | inclui Firm Knowledge |

O `main` contém exatamente 60.979 arquivos documentais, com
3.206.967.747 bytes. A contagem corrigida foi composta sem usar a árvore
recursiva global truncada:

| Grupo contado | Tarefas | Documentos | Bytes documentais |
|---|---:|---:|---:|
| 25 famílias ordinárias, incluindo Contracts | 1.749 | 14.068 | 638.450.228 |
| Diligence, somando onze VDRs | 11 | 37.623 | 2.047.920.250 |
| Firm Knowledge, somando DMS e tarefas | 250 | 9.288 | 520.597.269 |
| **Total** | **2.010** | **60.979** | **3.206.967.747** |

A distribuição de tarefas é:

| Família | Tarefas |
|---|---:|
| Antitrust & Competition | 33 |
| Arbitration & International Dispute Resolution | 37 |
| Banking & Finance | 37 |
| Bankruptcy & Restructuring | 36 |
| Capital Markets | 35 |
| Contracts | 498 |
| Corporate Governance | 97 |
| Corporate M&A | 161 |
| Data Privacy & Cybersecurity | 44 |
| Diligence | 11 |
| Emerging Companies & Venture Capital | 43 |
| Employment & Labor | 39 |
| Energy & Natural Resources | 31 |
| Environmental & ESG | 44 |
| Firm Knowledge | 250 |
| Funds & Asset Management | 66 |
| Healthcare & Life Sciences | 43 |
| Immigration | 27 |
| Insurance | 31 |
| Intellectual Property | 147 |
| International Trade & Sanctions | 41 |
| Litigation & Dispute Resolution | 52 |
| Real Estate | 44 |
| Structured Finance & Securitization | 31 |
| Tax | 34 |
| Trusts, Estates & Private Client | 77 |
| White Collar Defense & Investigations | 21 |
| **Total** | **2.010** |

As 24 áreas originais somam 1.251 tarefas, embora o artigo diga 1.250. A suíte
Contracts contém 498, embora o anúncio diga 500. O badge do README corrente diz
1.671. Essas divergências não invalidam os dados, mas provam que documentação e
árvore não têm uma única versão canônica de contagem.

Três suítes distorcem a escala:

- **Contracts:** 498 tarefas e 5.128 documentos;
- **Firm Knowledge:** 250 tarefas sobre um acervo compartilhado de 9.288
  documentos;
- **Diligence:** só onze tarefas, mas 37.623 documentos e 2.047.920.250 bytes.

“Quantidade de tarefas” e “carga documental” precisam, portanto, ser métricas
separadas.

### 4.3 Contrato de dados

O formato padrão de `task.json` é:

```json
{
  "title": "título legível",
  "work_type": "analyze | draft | review | research",
  "tags": ["área", "tema"],
  "instructions": "pedido enviado ao agente",
  "deliverables": {
    "arquivo-esperado.docx": "arquivo-esperado.docx"
  },
  "criteria": [
    {
      "id": "C-001",
      "title": "requisito atômico",
      "match_criteria": "PASS if ... FAIL if ...",
      "deliverables": ["arquivo-esperado.docx"],
      "sources": ["documento-fonte.docx"]
    }
  ]
}
```

Não existe resposta-modelo separada. `match_criteria` é simultaneamente
gabarito e instrução do juiz.

O schema real não é uniforme:

- uma tarefa ordinária de case assessment possui 55 critérios e o contrato
  padrão completo;
- uma tarefa legada de Contracts possui 48 critérios, mas não tem
  `deliverables`, `work_type`, `tags` nem escopo de entregável por critério;
- uma tarefa de Firm Knowledge usa `docs_dir` para um acervo compartilhado;
- uma tarefa de Diligence examinada tem 555 critérios para um único relatório.

Os testes reconhecem explicitamente tarefas legadas e aplicam validação mais
relaxada a elas. Logo, “há schema documentado” não significa “todas as tarefas
obedecem ao mesmo schema”.

### 4.4 A fábrica de datasets sintéticos

A leitura conjunta das publicações recentes muda a unidade de análise. A
Harvey não está apenas escrevendo tarefas e anexando documentos fictícios. Ela
mantém um processo que transforma conhecimento de especialistas em ambientes
jurídicos controlados, com verdade oculta suficiente para avaliar e treinar
agentes sem usar dados confidenciais de clientes.

Na palestra publicada pela Sequoia, Gabe Pereyra descreve o desbloqueio de
Diligence: Julio Pereyra começou pela rubrica e pelo cenário, plantou os
problemas que deveriam existir na sala de dados e então gerou os contratos e
demais arquivos. Como a equipe conhece os problemas plantados, consegue
conferir se o agente os encontrou. Especialistas e fornecedores como Mercor e
Snorkel entram para aumentar realismo e escala. Gabe afirma que os datasets são
usados tanto para treinamento quanto para avaliação do produto.

O padrão público possui pelo menos três receitas complementares.

#### Receita A — rubrica primeiro, para Diligence

1. definir cenário, riscos, omissões, inconsistências e recomendações esperadas;
2. plantar esses problemas numa especificação controlada;
3. gerar milhares de documentos interdependentes que expressem os problemas;
4. acrescentar material periférico e tornar os artefatos realistas;
5. pedir ao agente um memorando de diligência;
6. avaliar o resultado contra os problemas conhecidos e seus critérios.

Isso permite representar problemas diretos, arquivos deliberadamente ausentes
e riscos que só aparecem ao combinar documentos. O snapshot examinado contém
onze VDRs, 37.623 documentos e centenas de critérios numa tarefa individual; a
palestra relata mais de mil verificações no conjunto de Diligence.

#### Receita B — especificação primeiro, para Firm Knowledge

Cada assunto nasce de uma especificação compacta, em torno de mil tokens, que
define cliente, forma do projeto e características substantivas relevantes. O
pipeline renderiza a especificação em 10–200 documentos realistas. Cada
característica é vinculada a documentos determinados, permitindo rastreá-la no
nível do assunto e do arquivo.

As tarefas são enumeradas contra as especificações ocultas. O gabarito é
calculado pela combinação das características; o agente recebe somente o DMS
não estruturado. A rubrica expande esse gabarito em critérios atômicos. Essa
separação entre `world specification` e `agent view` é o componente que torna
a geração auditável.

#### Receita C — distribuição do produto primeiro, para Review Table

1. formar corpus offline a partir de contratos, filings, e-mails e outros dados
   jurídicos públicos;
2. registrar proveniência, tipo, extensão, conteúdo e embeddings;
3. filtrar, deduplicar e selecionar uma mistura que aproxime o produto;
4. usar modelos de fronteira representando perfis de usuário para gerar
   perguntas diversas;
5. usar agentes-oráculo com acesso integral para produzir respostas corretas,
   inclusive a decisão de abster-se;
6. comparar respostas entre agentes e executar rodadas de QA com especialistas;
7. avaliar separadamente localização da fonte, correção, schema, valor e
   citação.

Essa receita não fabrica necessariamente todo o mundo documental. Ela sintetiza
a distribuição de tarefas e respostas sobre corpus público controlado. Logo,
“dataset sintético” abrange mais de uma técnica.

#### O ciclo completo

```text
trabalho e distribuição do produto
        ↓
conhecimento de especialista
        ↓
especificação oculta + problemas plantados
        ↓
documentos, consultas e material periférico
        ↓
proveniência + gabarito + rubrica
        ↓
benchmark e ambiente de treinamento
        ↓
QA humano + sinais do produto
        ↓
próxima geração do dataset
```

O Tenet demonstra a reutilização desses ambientes em post-training: o corpus
combina dados sintéticos, dados jurídicos públicos e dados de especialistas; os
especialistas também revisam e corrigem material sintético. Ambientes de
treinamento preservam instrução, assunto documental e rubrica de especialista.

O lançamento atribui à primeira versão mais de 75.000 critérios escritos por
especialistas. Esse número descreve o corpus inicial anunciado; não foi
recalculado para o `main`. As rubricas cobrem fatos, conclusões, citações,
estrutura, severidade, recomendações, prazos, valores e formato.

#### O que permanece privado ou não comprovado

O repositório público distribui os mundos renderizados, tarefas, rubricas e
harness. Em Firm Knowledge, por exemplo, a pasta pública contém apenas `dms/`
e `tasks/`; as especificações latentes e o gerador não são distribuídos.
Continuam desconhecidos:

- prompts, código e modelos usados em cada etapa de geração;
- custo e tempo de autoria por assunto ou documento;
- taxa de rejeição, correção e regeneração;
- número, independência e acordo dos revisores;
- protocolo integral de auditoria jurídica e documental;
- composição do holdout oficial;
- grau em que o dataset sintético coincide com a distribuição real do produto.

O próprio Gabe afirma que dados sintéticos sozinhos não bastam e que um modelo
pode passar no benchmark e falhar fora da distribuição. Portanto, a vantagem
não é automação documental isolada: é o ciclo entre especialistas, geração,
avaliação, produto e feedback.

### 4.5 Harness de execução

O LAB é filesystem-first e possui três fases: executar, avaliar e reportar.

Cada execução recebe um workspace com documentos somente para leitura e pasta
de saída gravável. O agente dispõe de ferramentas de shell, leitura, escrita,
edição, glob e grep. Parsers cobrem DOCX, XLSX, PPTX, PDF e texto. O harness
registra configuração, transcript, métricas e entregáveis.

A documentação corrente descreve execução em sandbox Podman por tarefa, sem
rede, com capabilities removidas e documentos montados como read-only. Isso é
um controle de segurança relevante para arquivos não confiáveis, mas adiciona
uma superfície operacional que a investigação brasileira ainda não precisa.

O harness possui adaptadores para Anthropic, OpenAI, Google, Mistral e modelos
servidos pela Fireworks. Relatórios agregam cobertura documental, uso de
tokens, latência e custo estimado, além dos escores.

### 4.6 Avaliação atual

Cada critério recebe `pass` ou `fail` de um LLM-judge. O juiz recebe:

- título da tarefa;
- conteúdo dos entregáveis associados ao critério;
- título do critério;
- `match_criteria`.

Ele **não recebe os documentos-fonte** nem a instrução completa da tarefa no
prompt corrente. O campo opcional `sources` não é usado por `score_rubric()`
para reabrir e conferir a fonte. Portanto, o LAB verifica semanticamente a
saída contra fatos codificados na rubrica; não executa uma segunda prova
independente de que a citação realmente corresponda ao documento.

O score de tarefa é:

```text
1.0 se todos os critérios passarem; caso contrário, 0.0
```

O harness também reporta taxa de critérios aprovados como diagnóstico. No
`main` corrente, dois juízes avaliam independentemente por padrão:

- `claude-sonnet-4-6`;
- `gpt-5.5`.

A taxa dual é a média dos dois resultados. Para uma única tarefa ela pode ser
`0`, `0,5` ou `1`. O campo agregado estrito exige que ambos aprovem tudo. O
perfil recebe a etiqueta `lab-standard-dual-v1`.

Essa mudança entrou em 2026-08-26, depois da tag `v1.0`. Resultado comparável
exige fixar pelo menos commit do dataset, commit do harness, perfil dos juízes,
modelos executores, limite de turnos, ferramentas, parsers e versão dos
prompts.

### 4.7 O problema matemático do all-pass

`All-pass` responde a uma pergunta operacional legítima: “o trabalho passou
inteiro?”. Ele não produz, sozinho, uma comparação justa entre tarefas com
rubricas de tamanhos muito diferentes.

Exemplo puramente ilustrativo: se cada critério tivesse chance independente de
99% de aprovação, uma tarefa com sete critérios teria aproximadamente 93,2% de
chance de `all-pass`; com 55, 57,5%; com 555, apenas 0,38%. O LAB observado
possui exatamente tarefas nessa ordem de grandeza.

Consequências:

- a composição e a granularidade da rubrica alteram o placar;
- um critério irrelevante ou defeituoso pode zerar toda a tarefa;
- comparar áreas exige controlar a distribuição de quantidade e severidade de
  critérios;
- taxa de critérios, taxa estrita de tarefas e severidade do erro devem ser
  apresentadas juntas;
- `all-pass` deve ser gate de revisão, não único índice científico.

### 4.8 Resultados publicados e reprodutibilidade

Em 2026-05-26, a Harvey reportou em holdout:

| Modelo | All-pass publicado |
|---|---:|
| Claude Opus 4.7 | 7,1% |
| Claude Sonnet 4.6 | 5,4% |
| Claude Opus 4.6 | 4,2% |
| GPT-5.5 | 2,1% |
| Gemini 3.5 Flash | 0,8% |

O melhor perfil custava aproximadamente US$ 50,90 por tarefa e levava cerca de
22 minutos. Esses números são relevantes como ordem de grandeza, mas não são
resultados do conjunto público: a própria Harvey declara um holdout que espelha
a distribuição do LAB e múltiplas avaliações entre famílias de modelos.

O artigo de 2026-08-20 registra que execuções internas, Vals e Artificial
Analysis divergem em harness e judge. A execução interna acrescentou um
`finish tool` ao harness padrão; outros parceiros usam abstrações e prompts de
juiz diferentes. Isso confirma que “mesma tarefa e mesmo modelo” não basta para
comparabilidade.

Além disso, a distribuição pública expõe instruções, documentos e rubricas e é
explicitamente indicada para treinamento e reward signals. Ela é excelente
para desenvolvimento, mas deixa de ser um teste cego para modelos ou agentes
que a consumiram. Um benchmark brasileiro aberto também precisa de:

- conjunto público de desenvolvimento;
- holdout versionado e inacessível aos executores;
- protocolo para abertura tardia de holdouts aposentados;
- declaração de possível contaminação do modelo;
- resultados nunca misturados entre public e holdout.

### 4.9 Falhas atuais que precisam influenciar o desenho brasileiro

Issues abertas no snapshot examinado documentam pelo menos cinco classes de
defeito:

| Classe | Evidência |
|---|---|
| Fato exigido só existe na rubrica | #152 exige escrow de US$ 31 milhões ausente das nove fontes; #149 exige data de reunião ausente dos treze documentos |
| Rubrica incompleta | #147 permite `1.0` sem responder ao cálculo percentual pedido |
| Contradição interna | #146 fixa contagens e listas incompatíveis em sete tarefas de Firm Knowledge |
| Direito ou entidade errados | #115 mistura thresholds de HHI de 2010 e 2023; #129 exige comprador diferente do documento operativo |
| Dataset contaminado | #79 mistura documentos de dois incidentes; #80 referencia fatos e arquivos ausentes |
| Erro de infraestrutura convertido em nota | #145 transforma falha de leitura por `pandoc` ausente em conteúdo julgado; #114 relata comportamento diferente conforme o provider disponível |

Esses não são detalhes periféricos. Em um regime `all-pass`, a qualidade da
rubrica e a legibilidade do arquivo são parte do sistema de medição. Um único
critério impossível pode tornar uma tarefa impossível; uma falha silenciosa do
parser pode produzir uma nota falsa.

O LAB deve ser tratado como projeto ativo e valioso, não como padrão-ouro
pronto.

### 4.10 Licença e decisão de reuso

O repositório possui `LICENSE` MIT com copyright de 2026 da Harvey AI e não
apresenta carve-out visível para as tarefas. O guia de contribuição declara os
documentos como sintéticos.

Decisão:

- o código e o contrato de dados podem ser estudados, usados, modificados e
  redistribuídos com preservação do aviso de copyright e licença;
- qualquer cópia material deve carregar o texto MIT;
- ainda é prudente manter inventário de direitos de documentos e assets, pois
  uma licença de repositório não cura direito de terceiro incorporado por erro;
- **não há razão técnica para copiar as tarefas**: a jurisdição, idioma,
  processo, fontes e atos brasileiros exigem dados novos;
- a melhor reutilização é conceitual e pequena: formato de tarefa, separação
  run/eval/report e rubricas escopadas por entregável.

## 5. Comparação com este workspace

### 5.1 O que já existe

O harness local não começa do zero:

| Capacidade | Evidência local |
|---|---|
| Executor de cenários | `scripts/run_evals.py` chama o plugin em sessão headless |
| Universo fechado | cada cenário roda em diretório temporário com arquivos semeados |
| Restrição de ferramentas | executor permite `Skill`, `Read`, `Glob` e `Grep`; MCPs são removidos |
| Multi-turno real | o mesmo `session_id` é retomado entre falas |
| Roteamento mecânico | primeira skill invocada deve coincidir com a esperada |
| Gate temporal | leitura de módulo de redação antes do turno autorizador reprova sem LLM-judge |
| Rubrica semântica | invariantes enumerados, veredito binário e citação curta de evidência |
| Auditabilidade | transcripts e relatórios persistem antes/depois do julgamento |
| Custo | relatórios nativos capturam custo do executor e do juiz quando disponível |
| Casos adaptados | pacote sintético com fatos ligados a achados e frentes |

O corpus corrente contém:

- `workflows.json`: 30 cenários, 35 turnos, 103 invariantes e quatro cenários
  multi-turno;
- `adaptacao-workflows.json`: 14 cenários, 55 invariantes;
- nove skills esperadas no fixture geral e quatro no fixture de adaptação.

As provas armazenadas não devem ser achatadas:

- a adaptação tem 14/14 efetivos após correção e regressão de A03, mas não uma
  passagem única perfeita;
- a regressão integral observou 22/30; cinco fixtures eram materialmente
  inelegíveis e uma dependia de conector autenticado;
- duas falhas de baseline foram corrigidas e passaram em rodada dirigida;
- a leitura agregada de 24/24 cenários elegíveis combina rodadas, não constitui
  uma única execução integral verde;
- tudo é sintético; não houve prova de uso profissional.

### 5.2 O que falta para um benchmark de trabalho

| Lacuna | Impacto |
|---|---|
| Especificação oculta do mundo | hoje fatos, arquivos e invariantes são escritos diretamente na fixture; não existe uma autoridade separada que gere todos eles |
| Gerador de documentos e variações | o runner materializa conteúdo já escrito, mas não transforma fatos e relações em acervos coerentes |
| Compilador de gabarito e rubrica | invariantes são autorados manualmente e podem divergir do corpus sem uma prova de derivabilidade |
| Grafo de proveniência | não há ligação mecânica `fato → documento → localizador → critério` |
| Protocolo de realismo e consistência | não existe revisão cega do mundo gerado nem medida de retrabalho humano |
| Entregável como arquivo | o harness atual julga texto final, não DOCX/XLSX/PDF gerado |
| Inventário documental por tarefa | não há contrato uniforme de `documents`, papel, hash e proveniência |
| Separação dev/holdout | fixtures e invariantes ficam públicos no mesmo repositório |
| Juiz independente padrão | executor e juiz nativos usam o mesmo modelo selecionado; rodadas por subagente ainda foram da mesma família |
| Conferência de fonte | o juiz vê o output e o invariante, não reabre a fonte para validar a citação |
| Falha de parser fail-closed | ainda não existe porque a investigação não lê binários, mas será obrigatória ao adicioná-los |
| Perfil de execução congelado | relatórios guardam modelo e versão do plugin, mas não um contrato completo comparável ao LAB |
| Adjudicação humana | não há protocolo formal de revisão de divergências e de aprovação de rubricas |
| Medidas de cobertura | não há cobertura de documentos, esforço, latência e severidade numa visão única |

### 5.3 O que não deve ser importado agora

- o harness inteiro do LAB;
- Podman, pandas, matplotlib, seaborn e cinco SDKs de provider;
- geração de DOCX, XLSX e PPTX antes de provar a coerência em texto simples;
- dashboard HTML;
- 24 áreas de prática;
- centenas de tarefas de contrato;
- fuzzy matching de nomes de entregável por outro LLM.

Esses componentes resolvem escala e formatos que a investigação ainda não
demonstrou precisar. O primeiro gargalo é epistemológico: provar que uma
especificação brasileira consegue gerar fontes e rubricas coerentes. Importar
infraestrutura antes disso criaria uma segunda plataforma de eval ao lado de
`scripts/run_evals.py` sem criar a capacidade estratégica.

## 6. O que se traduz, muda e deve ser rejeitado

### 6.1 Traduzir diretamente

1. **Autoridade latente separada:** a especificação do mundo é a fonte da
   verdade e nunca é mostrada ao executor.
2. **Renderização derivada:** documentos, consultas e tarefas nascem da
   especificação; não são escritos como universos independentes.
3. **Problemas plantados:** omissões, contradições e riscos são deliberados,
   identificados e verificáveis.
4. **Proveniência de ponta a ponta:** cada verdade exigida liga-se ao documento,
   localizador e critério correspondente.
5. **Gabarito e rubrica compilados:** o que será avaliado deriva da mesma
   autoridade que produziu os documentos.
6. **Material periférico controlado:** o mundo inclui ruído realista sem
   contaminar assuntos ou inventar fatos exigidos apenas pela rubrica.
7. **Views separadas:** autor, executor, juiz e revisor humano recebem apenas a
   informação necessária ao seu papel.
8. **Separação run/eval/report:** output e trajetória são congelados antes de
   qualquer julgamento.
9. **Dev e holdout distintos:** mundos públicos de desenvolvimento não podem
   sustentar sozinhos alegação de generalização.
10. **Especialista no ciclo:** geração automática não substitui autoria,
    revisão, remediação e feedback de advogados.

### 6.2 Adaptar ao direito brasileiro

1. **Jurisdição e corte temporal obrigatórios.** Toda tarefa declara país,
   ramo, tribunal quando aplicável e data até a qual o direito deve ser lido.
2. **Fonte de autoridade por proposição.** Lei, decisão, petição, contrato,
   prova e memória derivada não são intercambiáveis.
3. **Papel e lente.** Autor/réu, credor/devedor, consulente e frente ativa
   controlam relevância e estratégia.
4. **Fase e ato atual.** Classe processual histórica não substitui o ato
   efetivamente devido.
5. **Estados epistêmicos.** Informado, extraído, inferido, confirmado,
   controvertido e ausente devem produzir exigências diferentes.
6. **Precedentes.** Citação precisa incluir tribunal, órgão, processo, data e
   localizador verificável quando a fonte estiver no universo da tarefa.
7. **Direito superveniente.** Mudança de lei ou precedente após o corte deve
   aparecer como limite, não ser silenciosamente absorvida.
8. **Gates humanos.** Análise confirmada não é decisão; decisão não é
   autorização para redigir; minuta não é protocolo.
9. **Resultado “não agir”.** Uma tarefa de deliberação pode passar ao concluir
   que não redigir ou não agir é a opção correta.
10. **Português jurídico brasileiro.** Precisão, registro e estrutura devem ser
    julgados no idioma de uso, sem traduzir taxonomia anglo-americana de forma
    literal.
11. **Causalidade processual.** Evento, documento, prazo, ato e consequência
    devem respeitar dependências; uma certidão não pode anteceder o ato que
    certifica e uma intimação não pode produzir efeito sem o evento definido.
12. **Variação controlada.** Alterar um fato deve mudar somente documentos,
    gabaritos e critérios dependentes desse fato.

### 6.3 Rejeitar

1. Chamar de gerador um conjunto de fixtures escrito manualmente.
2. Gerar documentos primeiro e escrever retrospectivamente uma rubrica que
   combine com eles.
3. Escalar documentos ou tarefas antes de provar derivabilidade e consistência.
4. Tratar `all-pass` como único número de qualidade.
5. Considerar `match_criteria` suficiente sem auditoria das fontes.
6. Esconder toda resposta e todo holdout indefinidamente.
7. Aceitar falha de parser, arquivo ausente ou output ilegível como `fail`
   jurídico; deve ser `INFRA_ERROR`.
8. Permitir que um LLM renomeie silenciosamente o entregável para fazê-lo
   parecer presente.
9. Comparar resultados obtidos em commits, ferramentas ou juízes diferentes.
10. Reaproveitar material do BigLaw Bench sem licença.
11. Confundir conclusão de benchmark com prontidão para protocolo ou uso
   profissional.
12. Usar aparência estilística como substituto de coerência jurídica ou
    correspondência com a distribuição real do produto.

## 7. Contrato mínimo da investigação brasileira

O objeto primário deixa de ser a fixture e passa a ser uma especificação
oculta de mundo. O exemplo abaixo orientou a investigação. Ela materializou um
schema local `1`, ainda restrito a pesquisa; ele não é contrato público nem
autoriza integração com o harness.

```json
{
  "schema_version": "br-legal-world-v0",
  "world_id": "br-civ-exec-001",
  "seed": "variante-controlada",
  "jurisdiction": {
    "country": "BR",
    "branch": "civil",
    "procedure": "cumprimento-de-sentenca"
  },
  "law_as_of": "2026-08-31",
  "actors": ["partes e papéis inteiramente fictícios"],
  "facts": ["F-001: valor, estado epistêmico e dependências"],
  "events": ["E-001: data, tipo e evento anterior"],
  "document_plan": ["D-001: tipo, fatos expressos e fatos omitidos"],
  "planted_issues": ["I-001: evidência, severidade e achado esperado"],
  "tasks": ["T-001: pedido profissional e entregável"],
  "expected_trace": ["F-001 -> D-001#localizador -> I-001 -> C-001"]
}
```

Cinco componentes formam a menor arquitetura que merece ser chamada de
fábrica:

1. **`world_spec`:** autoridade oculta com fatos, relações, eventos e problemas.
2. **Renderer:** produz arquivos visíveis sem expor IDs, gabarito ou instruções
   internas.
3. **Compiler:** deriva prompts, respostas esperadas, rubricas e mapas de
   evidência.
4. **Validator:** prova integridade referencial, causalidade, cobertura e
   ausência de vazamento.
5. **Adapter:** converte a view do executor em `setup_files`, `prompt`,
   `expected_skill`, `invariants` e `authorizing_turn`, que o runner atual já
   entende.

Não é necessário banco, serviço, interface, pacote externo ou formato Office
para testar essa arquitetura. Texto simples, JSON e os validadores existentes
são suficientes até que o modelo seja aprovado.

## 8. Investigação estática antes do protótipo

### 8.1 Hipótese

Uma especificação curta de cumprimento de sentença consegue produzir múltiplos
mundos documentais brasileiros coerentes e um gabarito rastreável sem exigir
que um advogado reescreva manualmente cada arquivo e cada critério.

O P0 da investigação definiu um único `world_spec` e três mutações controladas:

| Mundo | Mutação | Efeito esperado |
|---|---|---|
| Controle | documentos e cronologia completos | o achado confirma a situação sem inventar lacuna |
| Prova ausente | remove-se um documento necessário | documentos dependentes, gabarito e rubrica passam a exigir cautela ou diligência |
| Cronologia controvertida | dois eventos ou documentos divergem de modo plantado | o achado registra contradição e não escolhe silenciosamente uma versão |

Cada mundo deve conter uma ordem de grandeza de 10–20 arquivos textuais entre
fontes relevantes e periféricas. O número não é meta de produto; serve apenas
para impedir que um único documento disfarce a ausência de geração
multidocumental.

O tema do caso em `data/dogfood/2026-08-31-pareado-deliberacao/` pode orientar a
taxonomia, mas seus arquivos não são entrada do gerador. Em especial,
`contexto-advogado.md` continua privado ao operador e não pode vazar para
especificação, documentos ou executor.

### 8.2 Produtos da investigação

A investigação, sem executar modelos, produziu:

1. `world_spec.json` como autoridade única;
2. dependências entre fatos, documentos, observações e critérios no spec e na
   proveniência compilada;
3. três corpora demonstrativos gerados pelo mesmo contrato;
4. manifestos de proveniência com SHA-256 e localizadores `arquivo:linha`;
5. a mesma tarefa de análise compilada para cada mundo opaco;
6. rubricas derivadas com classe, severidade e autoridade explícitas;
7. relatório de QA estático `PASS` e pacote de revisão cega concluído por
   Sonnet 5 e Opus 5;
8. tempo local de geração e validação, sem inventar custo de autoria ou
   correção humana ainda não observados.

Uma única tarefa de análise é suficiente nessa fase. Deliberação e redação
devem permanecer fora até que o mundo documental prove coerência; adicioná-las
agora confundiria falha do gerador com falha de roteamento ou gate.

### 8.3 Rubrica compilada

Cada critério deve pertencer a uma classe, apontar para a autoridade que o
originou e ter severidade explícita:

| Classe | Origem obrigatória | Exemplo de gate |
|---|---|---|
| Fato | `facts` + documento/localizador | identifica valor e estado sem promover controvérsia a fato |
| Relação | dependência entre fatos ou eventos | conecta pagamento, intimação e prazo na ordem correta |
| Ausência | `document_plan` ou `planted_issues` | reconhece que uma conclusão não está documentalmente provada |
| Contradição | duas expressões plantadas incompatíveis | preserva ambas e pede resolução em vez de escolher uma |
| Direito | jurisdição + `law_as_of` + fonte pública | aplica apenas o regime carregado e declara limite temporal |
| Processo | evento, papel, fase e ato atual | não confunde classe histórica com providência atual |
| Proibição | risco explicitamente modelado | não inventa precedente, prazo, protocolo ou confirmação |

Se um critério não puder ser derivado de uma dessas autoridades, ele não entra
na rubrica. Texto livre escrito apenas porque “parece uma boa resposta” é
diagnóstico editorial, não ground truth.

### 8.4 QA antes de qualquer execução de agente

Cada mundo precisa passar mecanicamente por estas verificações:

1. IDs e dependências são únicos e resolvíveis;
2. todo documento declarado existe, abre e tem hash;
3. todo fato expresso aponta para pelo menos um localizador visível;
4. toda omissão ou contradição exigida está plantada, não acidental;
5. todo critério deriva de fato, relação, ausência, contradição ou regra
   declarada;
6. fatos não afetados por uma mutação permanecem idênticos;
7. documentos dependentes mudam quando sua autoridade muda;
8. nenhum ID interno, rótulo de problema ou gabarito vaza para a view do
   executor;
9. instrução, documentos, gabarito e rubrica pertencem à mesma versão e seed;
10. falha de geração ou leitura produz erro de infraestrutura, nunca nota
    jurídica.

O red-team automatizado é executado por agentes independentes quando isso trouxer
informação nova: cada braço recebe o corpus sem `world_spec`, gabarito ou rubrica, registra quais
fatos, lacunas e contradições recupera e, depois do congelamento, compara com a
especificação para apontar:

- fatos sem suporte documental;
- documentos impossíveis, incoerentes ou artificialmente reveladores;
- problema plantado que não pode ser encontrado;
- problema encontrado que não estava plantado;
- correções manuais necessárias e seu custo.

Esse red-team mede a qualidade documental sem exigir análise manual do owner. A
autoridade jurídica fica no spec; os dois revisores-modelo cegos e o adjudicador
fornecem o teste adversarial automatizado.

### 8.5 Gate de decisão da investigação

| Veredito | Condição |
|---|---|
| **CONSTRUIR P0** | os três mundos derivam do mesmo contrato, passam nos checks, preservam mutações localizadas, o revisor recupera os problemas plantados e a correção humana não equivale a reescrever o corpus |
| **REDESENHAR** | a especificação representa o caso, mas renderer, proveniência ou compiler produzem incoerência sistemática corrigível |
| **REMOVER** | gabarito e documentos não podem ser derivados da mesma autoridade, a maioria dos artefatos exige reescrita humana ou o mundo não parece trabalho jurídico brasileiro plausível |

O gate não usa percentual agregado com apenas três mundos. O relatório deve
mostrar contagens brutas de fatos, dependências, documentos, problemas,
critérios, falhas estáticas e correções humanas.

**Estado em 2026-08-31:** checks mecânicos passaram; Sonnet 5 e Opus 5 revisaram
a revisão 3 de forma cega, recuperaram os problemas plantados e propuseram
`CONSTRUIR P0`. O status é `STATIC_PASS / MODEL_BLIND_COMPLETE /
CONSENSUS_CONSTRUIR_P0 / OWNER_DIRECTED_BUILD`. O owner é advogado e decidiu
que revisão por terceiro não bloqueia a construção.

### 8.6 Calibração no acervo real

O `fs.brain` foi usado exclusivamente como fonte read-only no commit
`b1d871d7e489a6dacc0a9b60f2bfc38f9ecc99a2`. Dos 259 casos registrados, 237
estavam com ingestão liberada. O censo encontrou 8.520 Markdown associados à
coorte, mas o extrator restringiu a distribuição documental a 7.852 notas sob
`source-documents`, evitando misturar fonte com manifesto, índice ou análise
derivada.

A cobertura não é homogênea:

| Unidade | Cobertura |
|---|---:|
| casos com notas de fonte | 237 |
| casos com seções tipadas | 231 |
| seções tipadas | 8.027 |
| casos com movimentações estruturadas | 37 |
| sequências processuais distintas | 39 |
| movimentações deduplicadas | 6.828 |
| casos com alguma nota `full_autos` | 4 |

As relações de maior suporte confirmam a espinha já usada na revisão 3:
`peticao → decisao` apareceu em 113 casos; `decisao → certidao`, em 132;
`contrato + peticao`, em 102. Na subcoorte de movimentações,
`peticao_manifestacao → decisao` apareceu em 29 dos 37 casos e
`despacho → citacao_intimacao`, em 22.

Esses números sustentam topologia documental, não uma inferência de autos
integrais nem probabilidades nacionais. O P0 agora possui um
`empirical-basis.json`; seu check compara commit, cobertura e suportes com o
relatório agregado. Nenhum slug, nome, número de processo, data, valor, texto
de documento ou descrição literal de movimentação foi gravado neste workspace.

## 9. Lote P0 construído e próximo gate

O `batch-spec.json` parametriza doze assuntos inteiramente sintéticos. O
`build_batch.py` gerou três mundos por assunto — controle, prova ausente e
conflito cronológico — mantendo 17 documentos por mundo. O resultado contém 36
tarefas, 612 documentos e 805 arquivos totais. O check reconstruiu tudo em
diretório temporário e confirmou igualdade determinística da árvore.

O lote distribui quatro motivos: quatro assuntos em
`peticao → decisao → certidao`, três em `peticao → decisao → peticao`, três em
`decisao → oficio → certidao` e dois em `contrato → peticao → decisao`. Cada
assunto possui partes, objeto, valor, juízo e identificador próprios. Doze
deslocamentos semanais distintos variam a cronologia entre março e agosto de
2026 sem alterar a relação de tempestividade aprovada no seed. O validador
recusa janelas que atravessem os fechamentos forenses de 2026 relevantes ao
intervalo gerado.

O canário selecionou um assunto por motivo (`M-101`, `M-105`, `M-108` e
`M-111`). Sonnet 5 e Opus 5 receberam o mesmo prompt com 216 arquivos, sem
tools, `authority/`, parecer anterior ou resposta do outro braço. A primeira
rodada válida expôs uma contradição no harness; a segunda recuperou toda a
semântica, mas Opus reprovou feriados brasileiros dentro das janelas de M-105 e
M-108 e um ofício híbrido. O spec foi corrigido e regenerado. Na v3, ambos
deram `CONSTRUIR` ao lote e aos quatro assuntos.

Estado: `STATIC_PASS / AGENT_FULL_BATCH_PASS / 36_OF_36_WORLDS /
CODEX_SKILL_BACKED_FULL_PASS`. O canário
registrou 16/16 observações críticas e 8/8 relevantes por modelo. Nos dois
pacotes restantes, cada revisor Codex recuperou 16/16 críticas e 8/8 relevantes,
sem parcial, omissão ou falso positivo crítico.

O fixture `tests/fixtures/world-spec-p0-workflows.json` congela o hash do
manifesto e dos três recibos de aprovação. `run_evals.py` recusa drift, recibo
reprovado, cobertura incompleta ou caminho fora do repositório; depois
materializa, em diretório temporário, 36 cenários com `task.md`, 17 documentos
cegos e sete invariantes derivados da rubrica de cada mundo. `--list` confirmou
36/36 cenários destinados a `analise-juridica-civel`.

O backend Codex foi executado em chamadas efêmeras, separadas e somente leitura,
sem roteamento automático do plugin. O baseline bruto omitiu o art. 524 em
`M-101/W-B`; o modo skill-backed passou os três mundos de M-101. A execução
integral encontrou uma omissão real da mesma classe em `M-105/W-A`. A skill foi
corrigida por uma regra geral: todo dispositivo material trazido pela fonte
normativa autorizada deve ser aplicado ou declarado não incidente. A reexecução
isolada passou. Em `M-110/W-C`, o memorando estava correto, mas o juiz retornou
apenas três dos sete itens; o runner passou a classificar veredito incompleto
como `JUDGE_ERROR`, e o transcript congelado passou no rejulgamento.

O relatório canônico consolidou somente os resultados finais válidos: 36/36
mundos e 252/252 invariantes, custo externo US$ 0. Os dois incidentes permanecem
preservados e vinculados como tentativas supersedidas. A franquia Codex consumiu
4.150.622 tokens de entrada dos executores e 666.345 dos juízes, com 3.416.320
tokens de entrada em cache. A auditoria dos comandos não encontrou acesso a
`authority/`, rubrica, gabarito ou rede. Próxima ordem:

1. congelar o P0 e seu relatório canônico como baseline local de regressão;
2. não afrouxar rubricas nem editar documentos derivados para obter PASS;
3. decidir separadamente se uma segunda família jurídica merece P1;
4. manter autorização própria para publicação, SEN-1746, release ou anúncio.

Nenhum novo pacote Python é necessário para esse P0. Nenhum código do LAB
precisa ser copiado. Formatos Office, sandbox adicional, dashboard, geração em
escala e treinamento permanecem fora até haver necessidade observada.

## 10. Veredito final

### Opções consideradas

| Opção | Avaliação |
|---|---|
| Construir agora um equivalente amplo | **Rejeitada.** Escala sem QA repetiria os defeitos observados e duplicaria o harness local. |
| Importar Harvey LAB e traduzir tarefas | **Rejeitada.** A licença permite código, mas a jurisdição e o desenho local tornam a tradução materialmente errada; também aumentaria risco de contaminação. |
| Usar somente BigLaw Bench | **Rejeitada.** Amostra incompleta, sem licença e sem reprodutibilidade integral. |
| Escrever manualmente um assunto e três tarefas | **Rejeitada como prova do gerador.** Pode testar o harness depois, mas não demonstra criação repetível de datasets. |
| Publicar imediatamente um gerador como produto | **Rejeitada.** O mecanismo foi aprovado no primeiro assunto, mas ainda não generalizou para outras famílias. |
| Investigar `world_spec → documentos → gabarito → rubrica` | **Adotada e executada na camada estática.** É a menor unidade que testa a capacidade estratégica sem confundi-la com execução de agentes. |

### Recomendação

**CONGELAR ESTE P0 COMO BENCHMARK DE REGRESSÃO. Confiança alta na integridade,
recuperabilidade e capacidade discriminatória desta família; moderada na
generalização para outras áreas e configurações de agente.**

A Harvey demonstra que a vantagem vem da conversão repetível de conhecimento
especialista em ambientes com verdade controlada. Este workspace já possui um
consumidor adequado — executor, invariantes, multi-turno e gates — e agora tem
uma fábrica standalone que passou nos checks mecânicos, na revisão cega do seed
por dois modelos e na geração determinística do primeiro lote. A topologia
deixou de ser hipótese manual: está ancorada em padrões agregados do acervo real
e materializada em múltiplas especificações parametrizadas. Isso ainda é uma
única família substantiva; não prova generalização jurídica ampla. A autoridade
está no spec e o lote é testado por agentes; nenhum advogado externo nem revisão
manual do owner é necessário.
Dataset público, nova família, treinamento, release e anúncio continuam sem
autorização separada.

## 11. Fontes primárias

### BigLaw Bench

- [Repositório BigLaw Bench no snapshot examinado](https://github.com/harveyai/biglaw-bench/tree/138fd481b459a00bbd98eeb710f69ada1052bd47)
- [Artigo de lançamento de 2024](https://www.harvey.ai/blog/introducing-biglaw-bench)
- [Expansão anunciada em 2026](https://www.harvey.ai/blog/expanding-big-law-bench)
- [BigLaw Bench: Global](https://www.harvey.ai/blog/introducing-big-law-bench-global)
- [BigLaw Bench: Research](https://www.harvey.ai/blog/introducing-big-law-bench-research)

### Harvey LAB

- [Tag LAB v1.0](https://github.com/harveyai/harvey-labs/tree/v1.0)
- [LAB no commit corrente examinado](https://github.com/harveyai/harvey-labs/tree/a2b429eb6c9683c4fdeced3bc6b3af36edf239a6)
- [Arquitetura do harness](https://github.com/harveyai/harvey-labs/blob/a2b429eb6c9683c4fdeced3bc6b3af36edf239a6/docs/architecture.md)
- [Metodologia de avaliação](https://github.com/harveyai/harvey-labs/blob/a2b429eb6c9683c4fdeced3bc6b3af36edf239a6/docs/eval-strategies.md)
- [Guia de contribuição e regra de dados sintéticos](https://github.com/harveyai/harvey-labs/blob/a2b429eb6c9683c4fdeced3bc6b3af36edf239a6/CONTRIBUTING.md)
- [Licença MIT](https://github.com/harveyai/harvey-labs/blob/a2b429eb6c9683c4fdeced3bc6b3af36edf239a6/LICENSE)
- [Artigo de abertura do LAB](https://www.harvey.ai/blog/introducing-harveys-legal-agent-benchmark)
- [Resultados iniciais e holdout](https://www.harvey.ai/blog/legal-agent-benchmark-initial-results)
- [Extensão LAB Contracts](https://www.harvey.ai/blog/legal-agent-benchmark-in-house-contracting)

### Fábrica de dados, produto e treinamento

- [Palestra de Gabe Pereyra — Building Frontier AI at the Application Layer](https://sequoiacap.com/podcast/building-frontier-ai-at-the-application-layer-harvey-s-playbook)
- [LAB M&A Due Diligence — problemas plantados e VDRs sintéticos](https://www.harvey.ai/blog/legal-agent-bench-m-and-a-due-diligence)
- [LAB Firm Knowledge — especificação, renderer e proveniência](https://www.harvey.ai/blog/legal-agent-bench-law-firm-knowledge)
- [Review Table — corpus público, queries sintéticas, oráculos e QA](https://www.harvey.ai/blog/training-frontier-review-table-models-with-applied-compute)
- [Harvey Tenet — dados sintéticos, especialistas e post-training](https://www.harvey.ai/blog/post-training-update-harvey-tenet)

### Issues de qualidade citadas

- [#152 — escrow ausente das fontes](https://github.com/harveyai/harvey-labs/issues/152)
- [#149 — data disponível somente na rubrica](https://github.com/harveyai/harvey-labs/issues/149)
- [#147 — rubrica permite nota máxima sem responder ao cálculo](https://github.com/harveyai/harvey-labs/issues/147)
- [#146 — contagens incompatíveis](https://github.com/harveyai/harvey-labs/issues/146)
- [#145 — falha de leitura vira nota](https://github.com/harveyai/harvey-labs/issues/145)
- [#129 — comprador divergente](https://github.com/harveyai/harvey-labs/issues/129)
- [#115 — thresholds de HHI incorretos](https://github.com/harveyai/harvey-labs/issues/115)
- [#114 — scoring depende do provider](https://github.com/harveyai/harvey-labs/issues/114)
- [#80 — critérios apontam fontes ausentes](https://github.com/harveyai/harvey-labs/issues/80)
- [#79 — documentos de dois assuntos misturados](https://github.com/harveyai/harvey-labs/issues/79)

## 12. Recibo de escopo

Produzido:

- inventário dos benchmarks e expansões públicas;
- estrutura de dados e exemplos;
- reconstrução da metodologia e da avaliação;
- análise de licença e reprodutibilidade;
- crítica de qualidade com issues atuais;
- confronto com os ativos e limites deste workspace;
- correção auditável da contagem truncada;
- reconstrução de três receitas públicas de geração sintética;
- execução standalone da investigação com um spec, três mundos opacos,
  proveniência, rubricas e QA estático;
- revisão cega concluída por Sonnet 5 e Opus 5;
- censo read-only de 259 casos e extrator agregado sobre 237 casos liberados;
- relatório não identificável com padrões de documentos, seções e
  movimentações;
- base empírica validada ligada à revisão 3;
- contrato de lote com 12 assuntos, quatro motivos e 12 cronologias;
- geração determinística de 36 mundos, 612 documentos e 805 arquivos;
- canário cego por agentes com 12/12 mundos aprovados e recibos de isolamento;
- extensão cega aos oito assuntos restantes, com 24/24 mundos aprovados por
  pares Codex e custo externo zero;
- fixture do `run_evals.py` com 36 cenários, 18 arquivos cegos e sete
  invariantes por mundo, vinculado por hash aos recibos aprovados;
- manifestos, fatos resolvidos, proveniência e rubricas para cada mundo.

Não produzido:

- dataset brasileiro publicável, representativo ou integrado ao benchmark;
- execução por modelo ou relatório funcional dos 36 cenários integrados;
- execução paga além das revisões registradas nos recibos;
- clone ou importação do LAB;
- ação no SEN-1746;
- release, deploy, dogfood ou anúncio.
