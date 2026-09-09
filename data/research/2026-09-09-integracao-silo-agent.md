# Exploração — integração das skills com o Silo Agent

Data: 2026-09-09
Natureza: documento de exploração. **Não é decisão, não é RFC, não altera contrato.**
Registra uma sessão de estudo sobre como o trabalho deste repo se conecta ao
Silo Agent (workspace `silo-mcp`) e ao acervo de skills do escritório
(`fs.archive`). Issues de execução: SEN-2463, SEN-2464 (contexto: SEN-2452,
SEN-2444; guarda: SEN-2462).

## 1. O que foi mapeado

Três frentes, via leitura exploratória dos três workspaces:

- **Este repo (codigo-aberto):** 10 skills 100% Markdown, sem código executável;
  única dependência de runtime é o conector Silo MCP (jurisprudência), com
  degradação honesta. Contratos centrais: handoff de dez campos
  (`references/handoff.md`), pacote adaptado `case-adaptation-v1`
  (RFC-CA-001), gates mecânicos (redação, deliberação, limite de ação externa)
  e grafo de orquestração (`references/mapa-visual-skills-modulos.md`).
  Distribuição já existente em três formatos: plugin Claude Code, ZIPs
  standalone (`dist/chatgpt-work-smoke/`), harness `--codex-skill-backed`.
- **Silo Agent (`silo-mcp`):** skill runtime ~80% construído e deliberadamente
  desligado — registry completo em `agent/native/server/orgSkills.mjs`, injeção
  `# Skill ativa` no loop (`workspace.mjs`), tool `consultar_catalogo_skills`,
  gate em `agent/worker.mjs` (`CAPABILITY_NOT_VERIFIED`,
  `getCapability: () => null`). Padrão de transplante comprovado:
  `agent/procedures/ledger-v1/` (SOURCE.json com hash, validação estrita de
  saída, recibos). RFC-002 §4.1 já cita `codigo-aberto/skills/*` e
  `fs.archive/skills/org/*` como origens. Governança: prova A→B→C.
- **fs.archive:** 14 skills CLI + bundle org (25 skills); camada de
  capabilities (SEN-1654) com contratos congelados em
  `src/fs_archive_mcp/capabilities.py`; `prepare_invocation` serve o corpo vivo
  da skill do disco. A `/audit` existe nos três mundos: SKILL.md org v1.1
  (canônica), contrato MCP congelado (2026-06-17, dessincronizado) e capability
  declarada no bundle do Agent.

## 2. Conclusão da sessão: piloto /audit

A `/audit` (fs.archive `skills/org/audit/SKILL.md` v1.1) é a skill piloto por
perfil de custo/risco: `instruction_package` puro, read-only,
`requires.valter: never`, `human_gate: false`, Passo 6 documental com
análogos 1:1 nas tools do Agent, e gabaritos red/green + golden set prontos
para a prova A→B→C. Execução no workspace `silo-mcp`; pré-requisito de
contrato no fs.archive (re-freeze do `_AUDIT_METADATA` para v1.1 — enum com
`nao_verificavel`, sem side-effect de memória pós-SEN-2273).

## 3. Tese registrada (brainstorm do Diego, sem decisão)

> Transformar as skills deste repo em capabilities executadas nativamente pelo
> Silo Agent, e posicionar o repo público como distribuição multi-plataforma
> (Claude, ChatGPT, etc.) — "sentir o que o Silo pode fazer" fora, execução
> completa dentro. Possível rebrand: "silo aberto".

Leitura da sessão: a tese **confirma a arquitetura já desenhada** (RFC-CA-001:
skills plataforma-neutras, adaptador pertence ao ambiente externo). Os pontos
fixados para quando virar decisão:

1. **"Execução completa" precisa de definição precisa e honesta.** Não está nas
   skills (markdown idêntico); está no que só a plataforma tem: ambiente de
   caso (AgentStore, memória, ledger), conector de jurisprudência incluído,
   pacote adaptado `case-adaptation-v1` (Fase 2 da RFC — hoje inexistente) e
   gates mecânicos com recibo. Nunca degradar artificialmente a experiência
   externa.
2. **Custo de conversão por skill é desconhecido.** O piloto /audit precifica
   a unidade (contrato de I/O + mapeamento de tools + prova A→B→C). Não
   comprometer "todas as skills" antes desse número.
3. **Sequência antes de marca.** Piloto /audit → 2-3 skills como capabilities →
   adaptador de caso → multiusuário → só então funil/rebrand. Inverter gera
   waitlist, não funil.
4. **Neutralidade do repo é ativo.** O validador hoje proíbe claims comerciais
   sobre o Silo (`check_silo_access_copy`); rebrand implica reverter isso
   deliberadamente. Repo genuinamente útil standalone atrai contribuição
   externa; isca de marketing, não.
5. **Colisão de nomes:** "Silo" já denota MCP server, Juris e Agent no
   ecossistema; "silo aberto" adicionaria uma quarta acepção.

## 4. Próximos passos formais

- SEN-2464 (fs.archive): re-freeze do contrato MCP da /audit para v1.1.
- SEN-2463 (silo-mcp): piloto /audit com prova A→B→C e gate cirúrgico —
  executado já com a consciência de que constrói a referência de "execução
  completa" desta tese.
- Esta tese vira RFC própria (ou do silo-mcp) quando o piloto trouxer o custo
  unitário e o Agent tiver multiusuário no horizonte.
