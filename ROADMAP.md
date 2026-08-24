# Roadmap

Plano de desenvolvimento do plugin `silo-legal`. O roadmap é vivo: itens mudam
de estado conforme o trabalho avança, mas decisões registradas aqui não são
apagadas — itens descartados movem-se para [Fora de escopo](#fora-de-escopo).

Estado dos itens:

- `[ ]` pendente;
- `[~]` em andamento;
- `[x]` concluído.

## Estado atual (2026-08-24, v0.2.3)

- Nove skills publicadas, com disciplina compartilhada, contrato de handoff e
  recorte versionado do CPC.
- Protocolo de release validado ponta a ponta: fragmentos, semver, tag imutável,
  GitHub Release e publicação idempotente de assets (`v0.2.3`, workflow verde).
- Sete bundles ChatGPT e o manifesto de checksums publicados na
  [release v0.2.3](https://github.com/sensdiego/codigo-aberto/releases/tag/v0.2.3).
- Smoke completo do Claude Code aprovado em 2026-08-24
  ([#9](https://github.com/sensdiego/codigo-aberto/issues/9)): instalação limpa
  da `v0.2.3` via marketplace, nove skills carregadas, roteamento correto e
  leitura das referências compartilhadas sem negação de permissão.
- Sete bundles ChatGPT comprovados no aplicativo: três smokes in-app de
  2026-08-22 e os quatro restantes aprovados in-app em 2026-08-24 com os ZIPs
  exatos da release v0.2.3 (checksum conferido dentro do app), 12/12
  invariantes, além do proxy CLI com `gpt-5.6`
  ([#11](https://github.com/sensdiego/codigo-aberto/issues/11)).
- Mecânica real do ChatGPT documentada: não há instalação de skills de
  terceiros no runtime; o modelo monta o ZIP anexado à conversa e segue o
  `SKILL.md` ([QUICKSTART](QUICKSTART.md) corrigido).
- Treze cenários de roteamento definidos em
  [`tests/fixtures/workflows.json`](tests/fixtures/workflows.json), sem
  execução automatizada.

## Princípios de ordenação

1. Provar o caminho do usuário antes de anunciar; release não comprova
   instalação.
2. Medir qualidade antes de expandir conteúdo; editar skill sem régua é no
   escuro.
3. Toda fase entrega valor isoladamente; nada depende de fase posterior.
4. Mudanças de produto seguem o [protocolo de release](RELEASING.md) com
   fragmento por PR.

## Fase 0 — Higiene e papercuts

Objetivo: eliminar atrito local que já demonstrou quebrar o fluxo de trabalho.

- [x] Tratar arquivos de sistema operacional no validador: `validate_skills.py`
      deve ignorar `.DS_Store`, `Thumbs.db` e equivalentes em qualquer pasta,
      em vez de falhar com "entrada não prevista". O gerador de bundles também
      os exclui, em vez de empacotá-los silenciosamente.
      Critério atendido: `make validate` passa com arquivos de sistema
      plantados; cobertura em `tests/test_validate_skills.py`.
- [x] Remover o `.DS_Store` existente na raiz do workspace local.
- [x] Adicionar target `make lint` executando `ruff check scripts tests`.
      Critério atendido: o CI de qualidade roda lint antes da validação, e
      `make test` executa toda a suíte local.

## Fase 1 — Provar o caminho do usuário

Objetivo: fechar o ciclo aberto pela v0.2.0 — garantir que um usuário real
consegue instalar e usar as skills nos aplicativos suportados.

- [x] Smoke test no Claude Code: instalar via marketplace
      (`/plugin marketplace add sensdiego/codigo-aberto`) e confirmar que as
      nove skills carregam, roteiam e leem as referências compartilhadas.
      Critério atendido em 2026-08-24 com o cenário
      `relogio-completo-condicionado`: roteamento correto, seis leituras de
      referência sem negação de permissão e os três invariantes respeitados.
      Resultado registrado em
      [#9](https://github.com/sensdiego/codigo-aberto/issues/9).
- [x] Smoke test no ChatGPT Work: subir os sete bundles de `dist/` e repetir
      dois ou três cenários de `workflows.json` manualmente.
      Critério atendido em 2026-08-24: os quatro bundles restantes rodaram
      in-app com os ZIPs da release v0.2.3 (SHA-256 conferido pelo próprio
      modelo contra o manifesto), 12/12 invariantes, somando-se aos três
      smokes de 2026-08-22. Achado registrado: o runtime não tem instalação
      de skills de terceiros; o fluxo comprovado é montar o ZIP anexado à
      conversa ([#11](https://github.com/sensdiego/codigo-aberto/issues/11)).
- [~] Reescrever a seção de instalação do [`QUICKSTART.md`](QUICKSTART.md) com
      passos concretos por aplicativo (Claude Code, Claude Cowork, ChatGPT
      Work), testados na prática. Claude Code e ChatGPT estão documentados com
      caminho comprovado (a seção do ChatGPT foi corrigida em 2026-08-24 para o
      fluxo real de montagem do ZIP anexado); Claude Cowork permanece sem
      caminho comprovado.
- [x] Anexar os bundles como artefatos da GitHub Release no
      [`software-release.yml`](.github/workflows/software-release.yml).
      Critério atendido: `gh release view v0.2.3` lista os sete ZIPs e o
      manifesto de checksums.

## Fase 2 — Avaliação de qualidade

Objetivo: transformar os cenários sintéticos em régua objetiva para qualquer
edição futura de skills.

- [ ] Criar `scripts/run_evals.py`: executa cada cenário de
      `workflows.json` contra um modelo e verifica os invariantes declarados.
- [ ] Relatório por cenário: passos observados, invariantes atendidos/violados
      e veredito binário; saída em `data/evals/` com data, modelo e versão.
- [ ] Execução manual apenas (`workflow_dispatch` ou comando local), sem gate
      automático no CI, controlando custo.
- [ ] Baseline registrado para as nove skills na versão corrente.
      Critério: rodar o harness duas vezes produz resultados comparáveis.
- [ ] Documentar como interpretar e estender os cenários em
      [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Fase 3 — Expansão de conteúdo

Objetivo: cobrir as lacunas do workflow cível identificadas na análise,
usando o eval harness como pré-condição de qualidade.

Pré-requisito: Fase 2 concluída.

- [ ] Módulo `tutela-urgencia-evidencia` em `redacao-contencioso`
      (CPC arts. 300–310); ampliar recorte legislativo se necessário.
- [ ] Módulo `cumprimento-sentença` (CPC arts. 523–541), incluindo
      impugnação.
- [ ] Módulo `execucao` (CPC Livre II, arts. 771+), avaliando escopo mínimo
      viável antes de redigir.
- [ ] Revisar cobertura do `manifest.json` do CPC contra os novos módulos;
      o validador garante consistência de IDs.
- [ ] Avaliar skills candidatas fora do fluxo atual: cálculo e atualização
      monetária; relógio processual autônomo. Decidir entrar ou registrar em
      Fora de escopo.
- [ ] Cada módulo entra por PR próprio com fragmento `minor`.

## Fase 4 — Adoção e comunidade

Objetivo: preparar o repositório para público externo e só então divulgar.

Pré-requisito: Fases 1 e 2 concluídas.

- [ ] `SECURITY.md` com política de reporte, escopo (conteúdo de skills,
      scripts, protocolo) e expectativa de resposta.
- [ ] Templates de issue (bug, sugestão de skill, problema de conteúdo
      jurídico) e template de pull request alinhado ao CONTRIBUTING.
- [ ] Material de apresentação: exemplo ponta a ponta (prompt → handoff →
      peça) com caso sintético, sem dados reais.
- [ ] Anúncio público somente após smoke tests verdes e baseline de evals
      registrado.

## Fora de escopo

Decisões explícitas de não fazer, com motivação; revisáveis, mas não
silenciosas.

- Telemetria ou coleta de uso: produto jurídico; privacidade vira passivo
  maior que o aprendizado obtido.
- Código do serviço Silo neste repositório: o Silo permanece dependência
  opcional externa, conforme o README.
- Casos reais, dados de clientes ou pesquisas internas como conteúdo:
  proibido pelo CONTRIBUTING.
- Suporte a jurisdições não cíveis (trabalhista, criminal): manter o foco até
  o fluxo cível estar completo e validado.
