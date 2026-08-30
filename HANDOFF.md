# Handoff de sessão

Atualizado em 2026-08-30 durante a frente 3 da camada deliberativa. O
rastreamento é SEN-2408, sob SEN-2381; SEN-2384 registra o resultado da frente
2. A decisão e a cláusula de promoção originais vivem em
[#22](https://github.com/sensdiego/codigo-aberto/issues/22).

## Estado do produto e da branch

A versão publicada é `v0.3.0`: PR #25 integrado, release publicada e nove
skills públicas. A frente 3 está na branch
`codex/SEN-2408-deliberacao-juridica`, ainda sem merge, release ou publicação.
Ela adiciona a décima skill pública e o oitavo bundle de upload do ChatGPT.

O resultado ainda não está aceito. A medição dirigida comprovou a porta
decisória e consertou o incidente da confirmação combinada, mas reprovou dois
controles da ponte com redação. As correções de causa raiz feitas depois da
rodada ainda não foram re-medidas.

## Implementação da frente 3

- `skills/deliberacao-juridica/SKILL.md` embrulha o protocolo existente, exige
  análise madura, conduz opções/recomendação/entrevista e produz o handoff de
  tipo `decisão`; não pesquisa, aprofunda ou redige.
- As skills de análise e aprofundamento apenas oferecem a nova rota. As skills
  de redação a recebem quando uma escolha estratégica realmente impede um
  briefing coerente.
- `references/disciplina.md` explicita os estados `BLOQUEADA — item aberto`,
  `AGUARDANDO CONFIRMAÇÃO DO BRIEFING CONSOLIDADO` e `AUTORIZADA`. Resolver um
  item e dizer “pode redigir” na mesma mensagem não pula o estado intermediário.
- O roteamento foi estreitado após a medição: pedido de redação começa na skill
  de redação; uma escolha que cabe como campo aberto permanece no briefing
  bloqueado. A deliberação autônoma recebe pedido decisório direto ou
  encaminhamento de escolha estratégica.
- Validador, gerador de bundles, harness, documentação e as três fixtures
  `deliberacao-*` reconhecem a nova skill. O harness usa `--plugin-dir` para
  medir a árvore de trabalho, não o plugin instalado antigo.
- O fragmento `.changes/deliberacao-juridica.json` é `minor`; partindo da
  `v0.3.0`, uma publicação desta frente será `v0.4.0`.

## Evidência medida em 2026-08-30

Um smoke do Claude Code carregou o plugin inline `silo-legal@inline` na versão
`0.3.0` e listou `silo-legal:deliberacao-juridica`. O comando respondeu `OK`,
mas encerrou com `error_max_budget_usd`: custo observado de US$ 0,1265 para
limite nominal de US$ 0,05. Isso prova carregamento, não qualidade.

A primeira execução dirigida foi interrompida após dois FAIL e não gerou
relatório consolidado:

- `manifestacao-concordancia`: roteou para `redacao-contencioso`, mas exigiu
  handoff deliberativo e recusou briefing proporcional;
- `deliberacao-nao-redigir`: roteou corretamente para
  `deliberacao-juridica`, mas agrupou quatro perguntas na primeira resposta.

A continuação persistida em
`data/evals/2026-08-30-claude-sonnet-deliberacao-autonoma-continuacao/` terminou
com 3 PASS, 2 FAIL, 0 erro de juiz e US$ 2,6675:

- PASS: `deliberacao-nao-agir-sob-pressao`;
- PASS: `deliberacao-entrevista-segundo-turno`;
- PASS: `gate-confirmacao-combinada` — nenhum módulo ou rascunho antes de uma
  confirmação distinta do briefing consolidado;
- FAIL: `redacao-sem-decisao-registrada` — conteúdo 4/4, mas roteamento inicial
  precoce para `deliberacao-juridica`;
- FAIL: `gate-resposta-nao-autoriza` — gate mecânico aprovado, mas a redação
  enviou um item resolvível no briefing para deliberação e não chegou à minuta
  esperada no terceiro turno.

Depois da rodada, a primeira pergunta passou a ser singular e o gatilho
compartilhado foi estreitado para separar escolha estratégica de item aberto de
briefing. Essas duas correções não têm recibo comportamental posterior.

O custo conhecido mínimo do lote é US$ 3,2877: smoke, dois executores da rodada
interrompida e a continuação. O custo exato é maior porque os dois juízes da
rodada interrompida não foram persistidos. Como não é possível provar margem
sob o teto de US$ 5, não houve nova chamada paga. A condição para a regressão
completa também não foi satisfeita; portanto, os 19 cenários não rodaram.

## Próximo passo seguro

1. Com novo orçamento explícito, reexecutar somente os sete cenários dirigidos
   em diretório novo. O mínimo é 7/7, roteamento correto nos três
   `deliberacao-*`, `manifestacao-concordancia` preservado e os dois gates de
   redação aprovados.
2. Só depois do 7/7, rodar os 19 cenários. Qualquer falha direta de roteamento
   deliberativo ou do gate combinado volta a bloquear merge e publicação.
3. Com a regressão completa verde, revisar e integrar a frente, publicar a
   release `v0.4.0` e conferir separadamente release, assets, instalação limpa
   e smoke funcional.
4. Manter anúncio e piloto externo bloqueados até o dogfood pareado previsto no
   roadmap.

## Comandos de retomada

```bash
git switch codex/SEN-2408-deliberacao-juridica
git status --short
make validate
make lint
make test
make test-release
python3 scripts/release.py impact --ref-range origin/main...HEAD
```

O plugin instalado globalmente pode continuar na `v0.3.0`; o harness desta
branch precisa manter `--plugin-dir` para carregar a árvore de trabalho. Os
transcripts permanecem ignorados por `.gitignore`; `report.json` e `report.md`
são os recibos versionáveis.
