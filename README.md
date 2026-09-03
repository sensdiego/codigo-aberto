# Código Aberto

Skills abertas, em português brasileiro, para organizar, analisar, pesquisar,
aprofundar, decidir e redigir trabalho jurídico cível.

## Skills

| Skill | Resultado |
|---|---|
| [`novo-caso`](skills/novo-caso/SKILL.md) | Intake de acervo novo, limitado ou de processo em andamento |
| [`analise-documental`](skills/analise-documental/SKILL.md) | Fatos, atos, provas, contradições e lacunas com localizadores |
| [`analise-juridica-civel`](skills/analise-juridica-civel/SKILL.md) | Mapa normativo e processual aplicado aos fatos interpretados |
| [`analise-jurisprudencial`](skills/analise-jurisprudencial/SKILL.md) | Pesquisa opcional de precedentes pelo Silo |
| [`aprofundamento-juridico`](skills/aprofundamento-juridico/SKILL.md) | Investigação dinâmica de teses, riscos e preparação para audiência |
| [`deliberacao-juridica`](skills/deliberacao-juridica/SKILL.md) | Opções, recomendação, entrevista e registro da decisão do advogado |
| [`redacao-contencioso`](skills/redacao-contencioso/SKILL.md) | Peças, execuções, procedimentos especiais, manifestações e recursos cíveis |
| [`redacao-consultivo`](skills/redacao-consultivo/SKILL.md) | Pareceres, relatórios, e-mails e outros documentos consultivos |
| [`pesquisa-silo`](skills/pesquisa-silo/SKILL.md) | Consulta jurídica rápida pelo conector Silo |
| [`assinatura-silo`](skills/assinatura-silo/SKILL.md) | Orientação para a lista de espera e conexão ao Silo |

Fluxo sugerido:

`novo-caso → analise-documental → analise-juridica-civel → [jurisprudência ou aprofundamento] → [deliberação] → [redação]`

Para a topologia completa, sem simulação de jornadas, consulte o
[mapa visual de skills, módulos e modos](references/mapa-visual-skills-modulos.md).
O estado de prontidão contra situações documentadas está na
[validação estrutural anonimizada com casos reais](references/validacao-casos-reais.md).
A arquitetura adotada para fechar as lacunas está na
[RFC-CA-001 de adaptação segura de casos reais](RFC-CA-001-adaptacao-casos-reais.md).
As quatro skills consumidoras aceitam o pacote v1 sem tornar esse formato
obrigatório para handoffs comuns.

O usuário pode começar em qualquer etapa. A skill deve identificar e reparar
somente os pré-requisitos ausentes. Pesquisa jurisprudencial e aprofundamento
são opcionais.

Antes de redigir, a IA precisa ter interpretado os fatos e materiais relevantes
e, quando houver escolha estratégica pendente, registrar a decisão do advogado.
A redação ainda apresenta um briefing para confirmação humana explícita.
Confirmar uma minuta não autoriza protocolo, envio ou contato externo.

## Estrutura pública

```text
skills/                 produto utilizável
references/             disciplina, handoff e recorte legislativo necessário
.claude-plugin/          manifestos de distribuição (plugin e marketplace)
scripts/                 validação, avaliação, geração de bundles e release
tests/fixtures/          cenários sintéticos de roteamento e avaliação
data/                    relatórios de avaliação, pesquisa e dogfood, todos sintéticos
```

Os documentos de engenharia ([roadmap](ROADMAP.md), [handoff](HANDOFF.md),
[RFC](RFC-CA-001-adaptacao-casos-reais.md)) e a pasta `data/` registram o
desenvolvimento e as avaliações; não são guia de uso. Casos reais, documentos
de clientes, dados pessoais e configurações pessoais nunca entram neste
repositório: toda evidência publicada é sintética ou agregada e anonimizada.

## Origem e primeiro uso

Usuário inicial: **Diego Sens**, em dogfood jurídico interno. Primeira entrega
comprovada nos dois caminhos suportados: **24 de agosto de 2026**, no Claude
Code e no ChatGPT.

Certidão do antecessor:

1. **Antecessor:** distribuição fragmentada de skills jurídicas mantidas para
   uso interno e por aplicativo.
2. **O que morre:** cópias públicas soltas, sem um pacote, versão e régua de
   qualidade comuns.
3. **O que é herdado:** disciplina jurídica, fluxo cível, handoffs e fontes,
   reescritos sem dados ou dependências internas.
4. **Por que sucessor:** um repositório único permite validar e distribuir a
   mesma capacidade sem corrigir cada cópia separadamente.
5. **Limite da sucessão:** serviço, base, pesquisa interna e casos reais do
   Silo permanecem fora deste projeto.

## Uso

Três caminhos de instalação, detalhados no [guia rápido](QUICKSTART.md#instalação):

- **Aplicativo do Claude (Cowork):** Customize → Plugins → Add marketplace →
  `sensdiego/codigo-aberto` → Install. Instala o plugin completo, com as dez
  skills, e atualiza com um clique.
- **Claude Code:** `claude plugin marketplace add sensdiego/codigo-aberto` e
  `claude plugin install silo-legal@codigo-aberto`.
- **ChatGPT:** oito ZIPs autossuficientes publicados em cada
  [release](https://github.com/sensdiego/codigo-aberto/releases/latest),
  montados pelo modelo dentro da conversa ou de um projeto.

As skills também podem ser lidas diretamente em [`skills/`](skills/) ou
carregadas em qualquer aplicativo compatível com Agent Skills.

O corpus local contém o recorte do CPC necessário ao workflow. Pesquisa
jurisprudencial e validações externas usam o conector autenticado do Silo quando
disponível; a base, a API e o servidor do Silo não integram este repositório.
O acesso externo está em validação privada e pode ser solicitado pela
[lista de espera oficial](https://silo.legal/#waitlist).

Skills e código estão sob a licença [Apache-2.0](LICENSE). Para contribuir,
consulte [CONTRIBUTING.md](CONTRIBUTING.md); relatos sensíveis seguem a
[política de segurança](SECURITY.md). Versões publicadas ficam no
[changelog](CHANGELOG.md), o protocolo está em [RELEASING.md](RELEASING.md) e
as próximas fases estão no [roadmap](ROADMAP.md).
