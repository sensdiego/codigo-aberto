# Handoff de sessão

Atualizado em 2026-08-30 durante a implementação do módulo de tutela
provisória, rastreado em SEN-2413 sob a guarda-chuva SEN-2381.

## Estado do produto

A versão publicada é `v0.3.0`, com nove skills e sete bundles. O PR #25 está
integrado. A skill autônoma de deliberação permanece fora da `main`, no PR #26
em rascunho; por decisão do owner, aquela frente foi pausada sem nova medição,
merge ou publicação.

Esta frente parte diretamente da `main` na branch
`codex/SEN-2413-tutela-urgencia-evidencia`. Ela não depende do PR #26 e não o
incorpora.

## O que a frente SEN-2413 entrega

- `tutela-urgencia-evidencia.md`: módulo complementar de
  `redacao-contencioso`, carregado junto de um único módulo-base somente quando
  o briefing confirmar tutela provisória dos arts. 294–311.
- O módulo separa tutela de urgência e tutela da evidência; exige medida exata,
  fatos e provas, reversibilidade, caução, risco adverso e consequências do
  procedimento antecedente. Efeito suspensivo e tutela recursal permanecem no
  módulo do recurso.
- `indice-modulos.md`, `redacao-contencioso/SKILL.md` e `peticao-inicial.md`
  agora admitem um módulo-base mais o complemento de tutela, sem liberar outros
  módulos cumulativos.
- O recorte versionado do CPC foi completado com os arts. 295–299 e 302–310;
  os arts. 294, 300, 301 e 311 já existiam. Texto e ordem foram conferidos em
  2026-08-30 contra o HTML compilado oficial do Planalto.
- `manifest.json` recebeu os IDs de artigo correspondentes e data de revisão
  `2026-08-30`.
- A fixture `tutela-urgencia-complementar` acrescenta o vigésimo cenário:
  petição inicial mais tutela de urgência em dois turnos, com leitura de módulo
  proibida antes da confirmação do briefing (`authorizing_turn: 2`).
- O teste de bundle comprova que o ZIP de `redacao-contencioso` contém tanto o
  novo módulo quanto o recorte do procedimento comum.
- O fragmento `.changes/tutela-urgencia-evidencia.json` é `minor`; partindo da
  v0.3.0, o plano de release deve calcular v0.4.0.

## Verificação executada

- `make validate`: PASS — nove skills, sete bundles e fragmento válido;
- `make lint`: PASS;
- `make test`: PASS — 36 testes;
- `make test-release`: PASS — 13 testes;
- `git diff --check`: PASS.

O cenário novo não foi executado contra modelo. Isso seria uma chamada paga e
não recebeu orçamento específico nesta frente. A régua foi adicionada porque o
módulo não tinha cobertura anterior; nenhum cenário ou veredito histórico foi
alterado.

## Limites

- Não há pesquisa jurisprudencial nem afirmação de entendimento de tribunal.
- Não há suporte novo a tutela recursal, execução, cumprimento de sentença ou
  procedimento especial.
- Não houve merge, release, publicação de bundle ou anúncio.
- A conferência do texto do CPC não equivale, isoladamente, a certidão de
  vigência ou análise de regra especial aplicável a um caso.

## Próxima ação

Finalizar o diff, conferir o plano de release, abrir PR próprio ligado a
SEN-2413 e manter a issue em andamento até o check remoto. Se houver decisão de
medir comportamento, executar somente `tutela-urgencia-complementar` com teto
de custo explícito; isso não é pré-autorizado por este handoff.

Depois desta frente, os próximos módulos do roadmap são cumprimento de sentença
com impugnação e execução, cada um em PR próprio.

## Comandos de retomada

```bash
git switch codex/SEN-2413-tutela-urgencia-evidencia
git status --short
make validate
make lint
make test
make test-release
python3 scripts/release.py impact --ref-range origin/main...HEAD
python3 scripts/release.py plan
```
