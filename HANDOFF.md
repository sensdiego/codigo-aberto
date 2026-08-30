# Handoff de sessão

Atualizado em 2026-08-30 após a implementação integral da fila de módulos de
redação contenciosa, a elaboração do mapa visual, a validação estrutural
anonimizada contra situações documentadas em casos reais e a adoção da
arquitetura de adaptação, seus consumidores públicos locais e a avaliação
comportamental A01–A14 com subagentes Codex, além da correção dirigida dos
gates de briefing do agravo interno e da interdição.

## Estado do produto

A versão publicada é `v0.5.1`. O PR #27 foi integrado a `main` pelo merge commit
`0d9c04c`, preservando o commit `86a28eb`; o PR #28 foi integrado pelo merge
commit `7b6ecf0`, preservando toda a cadeia de avaliação; o PR #30 foi integrado
pelo merge commit `da41883`. O workflow `Software release` criou o commit
`f2e99ba`, a tag e o GitHub Release `v0.5.1`. A skill autônoma de deliberação
continua pausada no PR #26 e não foi incorporada.

O trabalho posterior à tutela está integrado e publicado. A release contém os
sete bundles de skills e o manifesto produzidos pelo workflow; publicação,
instalação e uso humano continuam sendo recibos distintos.

## O que este branch entrega

- 27 módulos novos em `redacao-contencioso`; o catálogo passa de 10 para 37
  módulos.
- Família prioritária: cumprimento de sentença, execução de título
  extrajudicial, liquidação, prova pericial, exibição, produção antecipada,
  IDPJ, agravo interno e acordo/homologação.
- Fila posterior: monitória, embargos de terceiro, ação rescisória, REsp/RE,
  exceção de pré-executividade, habilitação e crédito, inventário, consignação,
  exigir contas, possessórias, demarcação/divisão, dissolução parcial,
  oposição, ações de família, penhor legal, avaria grossa e restauração.
- Procedimentos de jurisdição voluntária dos arts. 719–770 cobertos em módulo
  único com treze modos obrigatórios: geral, notificação/interpelação,
  alienação, família consensual, alteração de regime, testamento/codicilo,
  herança jacente, ausência, coisa vaga, interdição, tutela/curatela, fundação
  e protesto marítimo.
- `indice-modulos.md` organiza o roteamento por fase e preserva um único
  módulo-base; tutela continua sendo o único complemento cumulativo.
- Dez fixtures acrescentam cobertura para as famílias novas e o gate de
  confirmação. Agravo interno e interdição foram executados com subagentes
  Codex depois de expor no índice seus controles pré-briefing: 2/2 cenários,
  6/6 invariantes e zero leitura prematura de módulo. Essa avaliação sintética
  não equivale a dogfood; as oito restantes não foram reexecutadas nesta frente.
- `references/mapa-visual-skills-modulos.md` representa as nove skills, seus
  handoffs e gates, os modos não contenciosos e os 37 módulos contenciosos. O
  mapa é estritamente descritivo e não simula workflows prováveis.
- `references/validacao-casos-reais.md` confronta os contratos públicos com 14
  cenários reais anonimizados, registra a fronteira da prova e prioriza as
  lacunas sem incorporar dado identificador do corpus privado.
- `RFC-CA-001-adaptacao-casos-reais.md` adota adaptador versionado, intake
  obrigatório, análise documental condicionada, perfil de frentes, precedência
  temporal, despachante de escopo e critérios sintéticos A01–A14. A RFC foi
  aceita; as Fases 1 e 3 e a validação local da Fase 5 foram concluídas. A
  comparação externa, as Fases 2 e 4 e o dogfood não foram autorizados.
- `novo-caso`, `analise-documental`, `analise-juridica-civel` e
  `redacao-contencioso` consomem o pacote v1 conforme sua etapa. O estado de
  escopo agora pertence a cada frente; handoffs comuns continuam compatíveis.
- `adaptacao-workflows.json` referencia A01–A14 sem duplicar as 20 frentes. O
  runner materializa pacotes sintéticos completos, cobre os quatro consumidores
  e mantém A01–A04 como canário separado da rodada integral.
- A rodada comportamental R2 teve primeira passagem 13/14. A03 usou a lente
  defensiva correta, mas não declarou a validação do pacote; `novo-caso` foi
  corrigida sem mudar fixture, invariantes ou input, e a regressão com executor
  e juiz novos passou. O estado efetivo é 14/14, sem alegação de passagem única
  perfeita. A rodada anterior foi invalidada por associação posicional de
  fatos, achados e frentes.

## Resultado da validação com casos reais

A infraestrutura não sustenta ainda uma promessa de cobertura integral. O
núcleo de redação cível tem encaixe material forte, mas nenhum cenário provou o
fluxo completo desde a fonte real até uma minuta confirmada.

A amostra estratificada produziu quatro cenários válidos com extensão, dois
inconsistentes na integração, dois não validáveis por falta de evento atual e
seis fora do escopo end-to-end. Esses números não são taxa de sucesso: a
amostra foi escolhida por variedade e dificuldade, não por frequência.

As causas prioritárias são:

1. ausência de adaptador do estado do caso para o handoff público;
2. ausência de roteador explícito de frente e ato atual;
3. falta de precedência temporal e resolução de conflito entre artefatos;
4. ausência de recibo end-to-end;
5. regimes tributário/público especial, fiscal, trabalhista, criminal,
   fiduciário e de precatórios fora do contrato cível vigente.

As Fases 1 e 3 implementaram contrato, régua e consumidores locais:
`references/handoff.md` recebeu elegibilidade e perfil opcional de frentes;
`adaptacao-casos-reais.json` contém A01–A14 sintéticos com escopo por frente; o
validador reprova promoções, remoção das cláusulas consumidoras e roteamentos
inseguros. Não existe produtor neste repositório e nenhum outro workspace foi
alterado.

## Biblioteca legislativa

Seis recortes novos armazenam 235 artigos integrais selecionados:

- `incidentes-e-provas.md`;
- `cumprimento-e-execucao.md`;
- `procedimentos-especiais.md`;
- `inventario-partilha.md`;
- `jurisdicao-voluntaria.md`;
- `recursos-avancados.md`.

Os 235 artigos foram comparados mecanicamente, sem divergência, com nova leitura
do HTML compilado oficial do Planalto em 2026-08-30, excluindo notas editoriais
e redações revogadas conforme a regra declarada do corpus. O manifesto agora
contém 869 IDs únicos; todas as 378 referências usadas pelas skills resolvem.
Essa conferência não equivale, isoladamente, a certidão de vigência nem substitui
lei material, regimento ou jurisprudência exigidos pelo caso.

## Decisões de escopo

- Cumprimento cobre os arts. 513–538; o recorte anterior 523–541 foi corrigido,
  pois o art. 539 inicia consignação em pagamento.
- Credor e devedor começam como modos rígidos dentro das famílias de
  cumprimento e execução. Extração futura para módulos separados depende de
  falha observada, não de antecipação arquitetural.
- Jurisdição voluntária usa um módulo com modos, evitando onze arquivos com o
  mesmo contrato-base.
- Cálculo/atualização monetária e relógio processual não foram disfarçados como
  redação: permanecem fora de escopo até existir mecanismo reproduzível próprio.
- Exceção de pré-executividade bloqueia redação sem prova pré-constituída e
  pesquisa jurisprudencial atual do tribunal competente.
- Procedimentos sujeitos a legislação material ou extravagante exigem que essa
  fonte seja carregada antes de qualquer minuta; o novo corpus é apenas CPC.

## Histórico local

- `3c753a0` — base normativa e módulos prioritários;
- `d7ce8ab` — procedimentos especiais e roteamento completo;
- `d21c7b9` — checks, fixtures e fechamento da cobertura de redação;
- `9168d63` — mapa visual de skills, módulos e modos;
- `8c255e5` — checkpoint local das Fases 1 e 3 da adaptação;
- `10d7337` — primeira avaliação comportamental, depois invalidada pela revisão;
- `387c32f` — correções do materializador, gates e manifesto de inputs;
- `4f11742` — outputs cegos A01–A14 congelados antes do julgamento;
- `ff2a210` — julgamento independente da primeira passagem, 13/14;
- `267bfc8` — validação do pacote tornada explícita em `novo-caso`;
- `de028ce` — output cego da regressão A03;
- `252a917` — julgamento independente da regressão A03, PASS;
- `3f2265a` — relatório R2 e documentação de fechamento.
- `babdfba` — sincronização com `main` após o landing e a release automática da
  tutela, sem reescrita da cadeia.
- `7b6ecf0` — merge do PR #28, sem rebase ou squash;
- `632fa21` — release `v0.5.0` e consumo dos sete fragmentos.
- `da41883` — merge do PR #30, com os gates de briefing corrigidos;
- `f2e99ba` — release `v0.5.1` e consumo do fragmento `patch`.

## Verificação

- extração oficial: 235/235 artigos sem divergência;
- módulos: 37/37 com as seis seções contratuais;
- manifesto: 869 IDs únicos, nenhuma referência ausente;
- `make validate`: PASS;
- `make lint`: PASS;
- `make test`: PASS — 61 testes.
- `make test-release`: PASS — 13 testes.
- `git diff --check`: PASS.

Os comandos foram repetidos antes do landing do PR #30. O workflow de release
passou e publicou sete ZIPs e `manifest.json` a partir de `f2e99ba`.

## Limites e recibos negativos

- A01–A14 e a regressão A03 foram executados com subagentes Codex; não houve
  chamada de modelo externo, dogfood ou recibo de custo em dólares. Houve
  consumo não medido da franquia Codex.
- Custo medido nos quatro relatórios anteriores: medianas por cenário entre
  US$ 0,28 e US$ 0,65; máximo de US$ 1,19. Estimativa não executada no executor
  externo: US$ 2–5 para A01–A04 e US$ 8–17 para A01–A14.
- Esta etapa não escreveu em outro workspace. A análise anterior do corpus
  privado permaneceu somente como evidência de origem anonimizada.
- Nenhum nome, número processual, valor, documento ou trecho identificador de
  caso real foi incorporado ao `codigo-aberto`.
- Não houve pesquisa jurisprudencial nova.
- Os PRs #27, #28 e #30 foram integrados; seus workflows publicaram `v0.4.0`,
  `v0.5.0` e `v0.5.1`, respectivamente.
- A publicação `v0.5.1` contém sete bundles ZIP e um manifesto. Não houve
  instalação das skills, dogfood, uso humano ou anúncio externo.
- A rodada dirigida dos dois gates usou subagentes Codex e cenários sintéticos;
  não houve modelo externo, dogfood, uso humano ou custo medido em dólares.

## Próxima ação

Sincronizar o PR #26 com a baseline `v0.5.1` e repetir seus gates proporcionais.
Comparação externa, Fases 2 e 4, instalação, dogfood e anúncio continuam fora
do escopo concluído.

## Comandos de retomada

```bash
git switch codex/SEN-2408-deliberacao-juridica
git fetch origin main
git status --short --branch
git log --oneline --decorate -6
make validate
make lint
make test
make test-release
git diff --check
python3 scripts/release.py impact --ref-range origin/main...HEAD
python3 scripts/release.py plan
python3 scripts/run_evals.py --fixture tests/fixtures/adaptacao-workflows.json --list
```
