# Mapa visual de skills, módulos e modos

Este documento representa a infraestrutura disponível no branch atual. Ele é
um **mapa descritivo de capacidades, dependências, gates e taxonomias**. Não
simula casos, não atribui frequência, não encadeia módulos contenciosos e não
propõe workflows prováveis de utilização.

## Como ler

- `-->` indica pré-requisito ou consumo expressamente previsto no contrato;
- `-. condição .->` indica rota opcional ou condicional;
- `---` indica agrupamento taxonômico, sem ordem de execução;
- um módulo contencioso recebe no máximo um módulo-base; tutela provisória é o
  único complemento cumulativo previsto;
- “sem modo obrigatório” significa que o módulo não contém a seção
  `Modo obrigatório`; não significa ausência de escolhas no briefing.

Inventário da `v0.6.0`: **10 skills publicadas**, **37 módulos contenciosos**
(36 bases e 1 complemento), **24 módulos contenciosos com modo obrigatório** e
**13 sem modo obrigatório**.

## 1. Superfície pública: entrada e roteamento

O usuário pode entrar em qualquer ponto. As ligações abaixo significam apenas
que o roteador pode selecionar aquela capacidade pelo resultado pretendido.

```mermaid
flowchart TB
    U["Usuário<br/>entrada em qualquer ponto"] --> R["Roteamento pelo resultado pretendido<br/>e reparo apenas do pré-requisito ausente"]

    R --> NC["novo-caso"]
    R --> AD["analise-documental"]
    R --> AJ["analise-juridica-civel"]
    R --> AP["analise-jurisprudencial"]
    R --> PROF["aprofundamento-juridico"]
    R --> DEL["deliberacao-juridica"]
    R --> RC["redacao-contencioso"]
    R --> RCON["redacao-consultivo"]
    R --> PS["pesquisa-silo"]
    R --> AS["assinatura-silo"]
```

## 2. Compatibilidade entre artefatos e skills

Este é um grafo de **handoffs consumíveis**, não uma sequência que todo usuário
deva percorrer. Cada skill pode encerrar a tarefa depois de produzir seu próprio
resultado.

```mermaid
flowchart LR
    NC["novo-caso"] --> I["handoff: intake"]
    I --> AD["analise-documental"]
    AD --> D["handoff: análise documental"]
    D --> AJ["analise-juridica-civel"]
    AJ --> M["handoff: mapa jurídico"]

    M -. "pesquisa aceita" .-> AP["analise-jurisprudencial"]
    AP --> P["handoff: pesquisa"]

    D --> PROF["aprofundamento-juridico"]
    M --> PROF
    P -. "quando disponível" .-> PROF
    PROF --> A["handoff: aprofundamento"]

    M --> DEL["deliberacao-juridica"]
    A --> DEL
    DEL --> DEC["handoff: decisão"]

    D --> RCON["redacao-consultivo<br/>descritiva"]
    D --> RC["redacao-contencioso"]
    M --> RC
    M --> RCON2["redacao-consultivo<br/>com posição jurídica"]
    P -. "se usada e verificada" .-> RC
    P -. "se usada e verificada" .-> RCON2
    DEC --> RC
    DEC --> RCON2
```

## 3. Gates compartilhados antes da redação

O protocolo de deliberação continua sendo referência compartilhada. A skill
`deliberacao-juridica` o embrulha e produz o mesmo handoff `decisão`.

```mermaid
flowchart LR
    H["Handoffs maduros<br/>do mesmo caso e lente"] --> Q{"Decisão humana pendente<br/>que a redação pressupõe?"}
    Q -- "não" --> B["Briefing consolidado"]
    Q -- "sim" --> DEL["deliberacao-juridica"]
    DEL --> PROTO["Protocolo de deliberação"]
    PROTO --> DEC["handoff: decisão"]
    DEC --> B
    B --> C{"Confirmação humana explícita<br/>pela pergunta fechada?"}
    C -- "não ou com alteração" --> B
    C -- "sim, sem item aberto" --> RED["Redação"]
    RED --> LIM["Minuta produzida<br/>nenhum protocolo ou envio"]
```

```mermaid
flowchart LR
    BRUTO["Documento bruto,<br/>narrativa solta ou pesquisa não verificada"] -- "não satisfaz" --> GATE["Pré-requisito de redação"]
    ANALISE["Conteúdo interpretado,<br/>fontes, escopo e confirmação"] --> GATE
    GATE --> BRIEF["Briefing próprio"]
    DECISAO["Confirmação de análise<br/>ou handoff de decisão"] -- "não autoriza" --> MINUTA["Minuta"]
    BRIEF -- "confirmação específica" --> MINUTA
    MINUTA -- "não autoriza" --> EXTERNA["Protocolo, envio,<br/>assinatura ou contato"]
```

## 4. Infraestrutura compartilhada e Silo

Com acesso a 100% da infraestrutura, o conector autenticado fica disponível às
capacidades que expressamente o usam. O servidor, a base e a API do Silo
continuam sendo serviço separado deste repositório.

```mermaid
flowchart TB
    DISC["Disciplina compartilhada"] --> SK["10 skills publicadas"]
    HAND["Contrato comum de handoff"] --> SK
    CPC["Biblioteca versionada do CPC"] --> ADJ["analise-juridica-civel"]
    CPC --> APROF["aprofundamento-juridico"]
    CPC --> RCONT["redacao-contencioso"]

    SILO["Silo MCP autenticado"] --> AJUR["analise-jurisprudencial<br/>pesquisa estruturada"]
    SILO --> PESQ["pesquisa-silo<br/>consulta direta"]
    SILO -. "validação normativa quando disponível" .-> ADJ
    ASS["assinatura-silo"] -. "acesso ausente ou inativo" .-> SILO
```

## 5. Modos e módulos das skills não contenciosas

### 5.1 Novo caso

Os três eixos são independentes. O modo de persistência depende da capacidade
comprovada do ambiente.

```mermaid
flowchart TB
    NC["novo-caso"] --- CICLO["Eixo: ciclo"]
    CICLO --- AB["abertura"]
    CICLO --- SU["suplementação"]

    NC --- ESTADO["Eixo: estado"]
    ESTADO --- PRE["pré-contencioso"]
    ESTADO --- PROC["processo em andamento"]

    NC --- PERSIST["Eixo: persistência"]
    PERSIST --- COMP["completo"]
    PERSIST --- ASSIST["assistido"]
    PERSIST --- TEMP["temporário"]
```

### 5.2 Análise documental

Os módulos são carregados somente quando materiais ao pedido.

```mermaid
flowchart TB
    AD["analise-documental"] --- FAT["fatos"]
    AD --- ATOS["atos e efeitos"]
    AD --- CRONO["cronologia<br/>quando a sequência mudar a compreensão"]
    AD --- PROVA["avaliação probatória"]
    AD --- LAC["contradições e lacunas"]

    AD --- RODADA["Escopo da rodada"]
    RODADA --- PRI["primeira análise"]
    RODADA --- MOD["módulo específico"]
    RODADA --- ATU["atualização por documento novo"]
```

### 5.3 Análise jurídica cível

```mermaid
flowchart TB
    AJ["analise-juridica-civel"] --- MAT["questões de direito civil material"]
    AJ --- PROC["questões de processo civil"]
    AJ --> MAPA["mapa: norma → fato/prova<br/>→ aplicação → consequência"]
    AJ -. "evento temporal material" .-> REL["relógio processual"]
    AJ -. "Silo conectado" .-> VAL["validação Silo/Planalto"]
    AJ -. "questão delimitada e pesquisa aceita" .-> JUR["analise-jurisprudencial"]
    AJ -. "decisão estratégica pendente" .-> DEL["deliberacao-juridica"]
```

### 5.4 Análise jurisprudencial, pesquisa e acesso ao Silo

```mermaid
flowchart TB
    SILO["Silo MCP"] --> ESTR["analise-jurisprudencial<br/>pesquisa estruturada"]
    SILO --> DIRETA["pesquisa-silo<br/>consulta única e objetiva"]
    ESTR --- ESCOPO["questão + fatos comparáveis<br/>tribunais + período + finalidade"]
    ESTR --- DISP["pesquisa dispensada<br/>não bloqueia rota posterior"]
    DIRETA --- QUERY["tema + tribunal + tipo"]
    ACESSO["assinatura-silo"] -. "conector ausente" .-> SILO
    ACESSO --- STATUS["conectado | configurado-não-verificado | ausente"]
```

### 5.5 Aprofundamento jurídico

Escolhe-se um modo como eixo principal; artefatos podem ser combinados quando o
objetivo exigir.

```mermaid
flowchart TB
    A["aprofundamento-juridico"] --- M1["estressar tese ou posição"]
    A --- M2["explorar caso ou questão"]
    A --- M3["simular perspectivas"]
    A --- M4["preparar interação"]
    A --- M5["planejar investigação"]
    M4 -. "audiência civil" .-> AUD["referência específica de audiência"]
```

### 5.6 Deliberação jurídica

A skill usa o protocolo compartilhado e não pesquisa, aprofunda ou
redige. A saída é sempre um handoff de decisão ou uma rota explícita de retorno.

```mermaid
flowchart TB
    DEL["deliberacao-juridica"] --> PROTO["protocolo compartilhado"]
    PROTO --- OPT["até quatro opções materiais"]
    PROTO --- REC["recomendação + confiança<br/>+ melhor objeção"]
    PROTO --- ENT["entrevista decisória<br/>uma pergunta de maior valor por vez"]
    PROTO --> DEC["handoff: decisão"]
    DEL -. "lacuna impede decidir" .-> PROF["aprofundamento-juridico"]
    DEC -. "briefing próprio confirmado" .-> RED["redação"]
```

### 5.7 Redação consultiva

Tipo e profundidade são eixos independentes. O diagrama não gera combinações
prováveis entre eles.

```mermaid
flowchart TB
    RC["redacao-consultivo"] --- TIPO["Eixo: tipo"]
    TIPO --- COM["comunicação jurídica"]
    TIPO --- REL["relatório"]
    TIPO --- PAR["parecer"]

    RC --- PROF["Eixo: profundidade"]
    PROF --- BREVE["breve"]
    PROF --- PAD["padrão"]
    PROF --- APROF["aprofundado"]
```

## 6. Redação contenciosa: regra de composição

```mermaid
flowchart LR
    RC["redacao-contencioso"] --> BASE["1 módulo-base confirmado"]
    BASE --> MODO["1 modo confirmado<br/>quando o módulo exigir"]
    MODO --> PECA["estrutura e checklist do ato"]
    TUT["tutela-urgencia-evidencia"] -. "somente se o briefing confirmar" .-> PECA
    OUTRO["segundo módulo-base"] -- "não previsto" --> BLOQ["voltar ao mapa jurídico<br/>e confirmar o ato"]
```

As conexões nas subseções seguintes são apenas de pertencimento ao grupo do
[índice de módulos](../skills/redacao-contencioso/references/indice-modulos.md).
Não há arestas entre atos processuais.

### 6.1 Procedimento comum e prova

```mermaid
flowchart LR
    G["Procedimento comum e prova"] --- PI["peticao-inicial<br/>sem modo obrigatório"]
    G --- TUT["tutela-urgencia-evidencia<br/>complemento; seleção no briefing:<br/>urgência | evidência<br/>antecipada | cautelar<br/>antecedente | incidental"]
    G --- CON["contestacao<br/>sem modo obrigatório"]
    G --- REP["replica<br/>sem modo obrigatório"]
    G --- ESP["especificacao-provas<br/>sem modo obrigatório"]
    G --- PP["prova-pericial<br/>quesitos_assistente | proposta_honorarios<br/>manifestacao_laudo | esclarecimentos"]
    G --- EX["exibicao-documento-coisa<br/>requerer_parte | requerer_terceiro | exibir<br/>responder | justificar_recusa"]
    G --- PAP["producao-antecipada-prova<br/>sem modo obrigatório"]
    G --- AF["alegacoes-finais<br/>sem modo obrigatório"]
    G --- MG["manifestacao-generica<br/>sem modo obrigatório"]
```

### 6.2 Incidentes, composição, liquidação e satisfação

```mermaid
flowchart LR
    G["Incidentes e composição"] --- IDPJ["incidente-desconsideracao-personalidade-juridica<br/>requerer | responder | manifestar_prova<br/>hipótese: direta ou inversa"]
    G --- AC["acordo-homologacao<br/>homologar | suspender_para_cumprimento<br/>noticiar_cumprimento | noticiar_inadimplemento"]
    G --- HC["habilitacao-impugnacao-credito<br/>habilitacao_sucessor | responder_habilitacao<br/>habilitar_credito_inventario | impugnar_credito_inventario"]

    S["Liquidação e satisfação"] --- LIQ["liquidacao-sentenca<br/>arbitramento | procedimento_comum<br/>responder | impugnar_calculo"]
    S --- CS["cumprimento-sentenca<br/>promover | impugnar | responder_impugnacao<br/>obrigação: quantia | alimentos | Fazenda Pública<br/>fazer | não fazer | entregar<br/>caráter: provisório | definitivo"]
    S --- EXT["execucao-titulo-extrajudicial<br/>promover | embargar | responder_embargos<br/>+ espécie do título e natureza da obrigação"]
    S --- EPE["excecao-pre-executividade<br/>sem modo obrigatório<br/>gate: prova pré-constituída + pesquisa atual"]
```

### 6.3 Recursos e impugnação autônoma

```mermaid
flowchart LR
    G["Recursos e impugnação autônoma"] --- APE["apelacao<br/>sem modo obrigatório"]
    G --- AGI["agravo-instrumento<br/>sem modo obrigatório"]
    G --- AGINT["agravo-interno<br/>agravar | responder"]
    G --- ED["embargos-declaracao<br/>sem modo obrigatório"]
    G --- RSE["recurso-especial-extraordinario<br/>recurso_especial | recurso_extraordinario<br/>contrarrazoes | agravo_recurso_especial_extraordinario<br/>resposta_agravo"]
    G --- AR["acao-rescisoria<br/>ajuizar | contestar | manifestar"]
```

### 6.4 Procedimentos especiais contenciosos

```mermaid
flowchart LR
    G["Procedimentos especiais<br/>painel A — agrupamento apenas"] --- CP["consignacao-pagamento<br/>extrajudicial_quantia | ajuizar | contestar<br/>complementar | levantar<br/>+ prestação: dinheiro ou coisa"]
    G --- EC["exigir-contas<br/>exigir | contestar_dever | prestar | impugnar_contas<br/>+ primeira ou segunda fase"]
    G --- POS["acoes-possessorias<br/>manutencao | reintegracao | interdito<br/>contestar | responder_pedido_contraposto<br/>+ força nova ou velha quando relevante"]
    G --- DD["demarcacao-divisao<br/>demarcacao | divisao | cumular | contestar<br/>fase_pericial | fase_material"]
    G --- DPS["dissolucao-parcial-sociedade<br/>exclusao | retirada_recesso | falecimento<br/>apuracao_haveres | contestar | manifestar_pericia"]
    G --- INV["inventario-partilha<br/>abertura | primeiras_declaracoes | impugnacao<br/>avaliacao | dividas | colacao | partilha<br/>arrolamento | sobrepartilha | responder"]
    G --- ET["embargos-terceiro<br/>embargar | contestar"]
```

```mermaid
flowchart LR
    G["Procedimentos especiais<br/>painel B — agrupamento apenas"] --- OPO["oposicao<br/>opor | contestar"]
    G --- FAM["acoes-familia<br/>ajuizar | contestar | manifestar_acordo<br/>manifestar_audiencia"]
    G --- MON["acao-monitoria<br/>ajuizar | embargar | responder_embargos<br/>+ pagar | entregar | fazer | não fazer"]
    G --- HPL["homologacao-penhor-legal<br/>sem modo obrigatório"]
    G --- AVG["regulacao-avaria-grossa<br/>requerer | indicar_regulador | apresentar_documentos<br/>impugnar_regulamento | responder_impugnacao"]
    G --- RA["restauracao-autos<br/>requerer | contestar | fornecer_copias<br/>manifestar_restauracao"]
```

### 6.5 Jurisdição voluntária

O módulo-base é único e exige exatamente um dos treze modos abaixo.

```mermaid
flowchart LR
    JV["jurisdicao-voluntaria"] --- G["geral"]
    JV --- NI["notificacao_interpelacao"]
    JV --- AJ["alienacao_judicial"]
    JV --- FC["familia_consensual"]
    JV --- ARB["alteracao_regime_bens"]
    JV --- TC["testamento_codicilo"]
    JV --- HJ["heranca_jacente"]
    JV --- BA["bens_ausente"]
    JV --- CV["coisa_vaga"]
    JV --- INT["interdicao"]
    JV --- OTC["organizacao_tutela_curatela"]
    JV --- FUN["fundacao"]
    JV --- PM["protesto_maritimo"]
```

## 7. Fronteiras preservadas pelo mapa

```mermaid
flowchart TB
    MAPA["Mapa atual"] --- IN["Inclui<br/>skills, módulos, modos, handoffs,<br/>gates e dependências documentadas"]
    MAPA --- OUT["Não inclui nesta etapa<br/>personas, casos sintéticos, frequência,<br/>combinações prováveis ou jornadas simuladas"]
    MAPA --- DEL["Inclui deliberacao-juridica<br/>publicada e validada de forma dirigida"]
    MAPA --- EXT["Não representa como local<br/>servidor, base ou API externos do Silo"]
```
