# Handoff de sessão

Atualizado em 2026-08-30 após a implementação integral da fila de módulos de
redação contenciosa aprovada pelo owner.

## Estado do produto

A versão publicada continua `v0.3.0`. O módulo de tutela provisória permanece
no PR #27, branch `codex/SEN-2413-tutela-urgencia-evidencia`, commit `86a28eb`.
A skill autônoma de deliberação continua pausada no PR #26 e não foi incorporada.

O trabalho posterior à tutela está no branch local empilhado
`codex/redacao-contencioso-cobertura-integral`. Não há PR remoto para este
branch, merge, release, publicação de bundle ou anúncio.

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
- Dez fixtures não executadas acrescentam cobertura futura para as famílias
  novas e o gate de confirmação.

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
- terceiro commit (HEAD deste branch) — checks, fixtures, documentação e este
  handoff.

## Verificação

- extração oficial: 235/235 artigos sem divergência;
- módulos: 37/37 com as seis seções contratuais;
- manifesto: 869 IDs únicos, nenhuma referência ausente;
- `make validate`: PASS;
- `make lint`: PASS;
- `make test`: PASS — 37 testes.

A rodada final deve repetir os comandos abaixo e incluir `make test-release` e
`git diff --check` depois do commit de documentação.

## Limites e recibos negativos

- Nenhuma fixture nova foi executada contra modelo; não houve dogfood nem custo
  de inferência.
- Não houve pesquisa jurisprudencial nova.
- Não houve criação de issue, PR, push, merge, tag, release ou anúncio.
- O plano de release calcula `v0.4.0` a partir dos dois fragmentos `minor`, mas
  nenhuma publicação está autorizada por este handoff.

## Próxima ação

Depois da validação final, encerrar a etapa e pedir novas instruções ao owner.
As escolhas ainda abertas são de integração: manter o branch empilhado, dividir
em PRs ou reorganizar commits; nenhuma delas deve ser tomada silenciosamente.

## Comandos de retomada

```bash
git switch codex/redacao-contencioso-cobertura-integral
git status --short --branch
git log --oneline --decorate -6
make validate
make lint
make test
make test-release
git diff --check
python3 scripts/release.py impact --ref-range origin/main...HEAD
python3 scripts/release.py plan
```
