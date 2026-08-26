# Handoff de sessão

Atualizado em 2026-08-26, após o estudo da camada deliberativa entre análise e
redação, a revisão independente por dois modelos e a decisão registrada no
[ROADMAP](ROADMAP.md) e em
[#22](https://github.com/sensdiego/codigo-aberto/issues/22).

## Onde o produto está

A versão corrente continua sendo a `v0.2.4`, publicada e auditada. As nove
skills, o recorte do CPC, os sete bundles ChatGPT e a régua de treze cenários
permanecem inalterados nesta sessão. Nenhuma skill foi criada ou editada e
nenhuma versão foi publicada.

Claude Code e ChatGPT têm caminhos de uso comprovados. No Claude Cowork há
dogfood interno em projeto já montado, sem prova de instalação limpa.

## Decisão fixada nesta sessão

A hipótese de 2026-08-25 foi estudada e decidida: **adaptar os contratos
existentes, sem skill nova**. Foram comparadas quatro alternativas (skill
autônoma; protocolo compartilhado; ajuste só das skills; adiar ou rejeitar)
contra os critérios fixados no roadmap, e a posição foi submetida a duas
revisões independentes — uma às cegas e uma com a posição — que convergiram na
direção e corrigiram a especificação. O registro completo, com a especificação
aprovada, está em [#22](https://github.com/sensdiego/codigo-aberto/issues/22);
o resumo vive na seção "Camada deliberativa" do roadmap.

Pontos que a próxima sessão não deve reabrir sem motivo novo:

- gatilho enumerável: pedido explícito do advogado; decisão humana pendente
  que a minuta consome; ato inferido fora das opções do mapa;
- handoff de tipo `decisão` exigido só quando o gatilho dispara; decisão
  registrada nunca autoriza redação;
- gate como máquina de estados: pergunta fechada ao fim do briefing; só
  autoriza a afirmativa a essa pergunta, sobre o briefing consolidado, sem
  itens abertos e sem alteração material; todo o resto reapresenta compacto;
- protocolo em `references/deliberacao.md`, carregado sob demanda; regras
  curtas e universais (gatilho e gate) em `disciplina.md`;
- até quatro opções materialmente distintas, sem fabricar pluralidade;
  recomendação pode ser "não decidir ainda"; perguntas independentes juntas;
- fronteira com `aprofundamento-juridico` mantida: ele informa a decisão; a
  deliberação a registra.

## Próxima tarefa com maior impacto: frente 1 — a régua antes das skills

A implementação começa pela medição, não pelos contratos. Sem esta frente, a
frente 2 não tem contra o que ser comparada.

1. Dar a `scripts/run_evals.py` suporte a cenários multi-turno (sequência de
   prompts na mesma sessão, transcript persistido por turno antes do
   julgamento) e uma verificação mecânica: nenhum módulo de redação
   (`skills/redacao-contencioso/references/modulos/*.md`) lido antes da fala
   autorizadora, derivada das referências lidas que o harness já registra.
2. Escrever os seis cenários novos em `tests/fixtures/workflows.json`
   (`deliberacao-nao-redigir`, `deliberacao-nao-agir-sob-pressao`,
   `deliberacao-entrevista-segundo-turno`, `redacao-sem-decisao-registrada`,
   `gate-resposta-nao-autoriza`, `gate-confirmacao-combinada`) com invariantes
   granulares por passo do protocolo, e acrescentar a
   `manifestacao-concordancia` o invariante "não dispara deliberação nem exige
   decisão registrada; um único turno de confirmação".
3. Cobrir o multi-turno e a verificação mecânica em `tests/test_run_evals.py`.
4. Rodar a rodada contra a v0.2.4 e registrar em `data/evals/`: a falha
   esperada é o baseline da lacuna.
5. Abrir PR próprio; a frente 2 (contratos, fragmento `minor` → v0.3.0) só
   começa depois.

Regra do CONTRIBUTING que se aplica: não alterar skill e régua no mesmo pull
request sem justificativa.

## Pendências secundárias

- Documentar e testar a preparação limpa de um projeto no Claude Cowork.
- Revisar, em frente separada, lacunas do recorte legislativo do CPC percebidas
  durante a redação.
- `pesquisa-silo` continua sem cenário próprio na régua.
- Classificar `data/**` explicitamente no `.release-policy.toml` na próxima
  mudança que tocar a policy (observação de #15).
- Não iniciar piloto externo ou anúncio público; o dogfood pareado (salto
  direto × protocolo) é pré-condição de anúncio.

## Avisos operacionais

- O plugin local do Claude Code está na `v0.2.4`; re-medições futuras devem
  conferir a versão instalada antes de rodar (`claude plugin list`).
- O projeto "Silo Legal Skills — Smoke" no ChatGPT usa instruções permanentes e
  o acervo foi atualizado com os ZIPs da v0.2.4 em 2026-08-24.
- A rodada completa de evals custa aproximadamente US$ 6 e é sempre manual:
  `python3 scripts/run_evals.py`. Os sete cenários da frente 1 devem custar
  cerca de US$ 2 por rodada.
- Rastreamento externo: o repositório passou a ter issue guarda-chuva e frentes
  filhas no Linear a partir de 2026-08-26.
