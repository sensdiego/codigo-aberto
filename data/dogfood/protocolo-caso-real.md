# Protocolo de uso do plugin em caso real

Regra reutilizável para o owner usar o plugin `silo-legal` num caso real do
escritório e produzir um recibo de uso humano sem que nenhum dado real chegue a
este repositório nem identifique pessoas perante o fornecedor do modelo.

Estado: **proposto em 2026-09-05**, emendado no mesmo dia após parecer do
conselho. O protocolo não autoriza execução por si. Cada execução exige a
ficha da seção 7 preenchida e assinada pelo owner antes da primeira mensagem.
Ele complementa, sem substituir, a seção "Privacidade e segurança" da
[RFC-CA-001](../../RFC-CA-001-adaptacao-casos-reais.md), a regra do
[README](../../README.md) de que casos reais nunca entram no repositório e o
molde de condução do
[dogfood pareado](2026-08-31-pareado-deliberacao/protocolo.md).

Decisões do owner que moldaram esta primeira versão (2026-09-05):

- o caso é **encerrado**, com desfecho conhecido, e chega ao modelo em **cópia
  pseudonimizada**: nomes viram papéis, identificadores viram códigos opacos,
  datas, valores e fatos ficam intactos;
- a sessão roda no **aplicativo do Claude (Cowork)**, com o plugin instalado
  pelo marketplace, e não no Claude Code;
- o desfecho real do caso vira **gabarito** guardado fora da sessão, para
  julgar a deliberação do plugin sem que o modelo o conheça.

Calibração: este protocolo foi escrito para o aplicativo do Claude e a conta
do owner. Executá-lo com outro fornecedor, outro plano ou acesso por API exige
reconferir retenção, uso para treinamento e a existência real dos controles da
seção 3.5 antes de qualquer sessão.

## 1. Finalidade e fundamentos

### O que este uso é

Teste de produto conduzido pelo advogado que atuou no caso: o plugin recebe os
documentos como estavam no momento em que uma decisão estratégica real foi
tomada e conduz intake, análise e deliberação até uma decisão. O advogado
compara essa decisão com o que de fato aconteceu. O resultado é um recibo de
uso humano, o primeiro sobre material não sintético, e uma lista de defeitos
observados.

Uma execução completa fecha três pendências de uma vez: o protocolo de
privacidade que o HANDOFF mantinha estacionado, o recibo de uso humano do
plugin no aplicativo em caso que o owner não desenhou, e, se a instalação
limpa pelo marketplace for feita antes como pré-requisito, o item em andamento
da Fase 1 do ROADMAP. É esse encadeamento que justifica o tamanho deste
documento.

### O que este uso não é

Não é serviço ao cliente, não produz peça para protocolo, não reabre o caso e
não autoriza uso profissional de nada que o plugin gerar. A finalidade é
distinta do mandato que originou os documentos, e é essa distinção que
governa todo o desenho abaixo.

### Fundamentos operacionais

Os artigos abaixo foram confirmados nas páginas oficiais do Planalto em
2026-09-05 pelo conector Silo (`verify_legislation_in_planalto`). A
verificação prova a existência do texto na fonte oficial; não prova vigência
nem substitui a leitura do owner, que é o advogado responsável.

| Fundamento | O que o protocolo faz com ele |
|---|---|
| Lei 13.709/2018, art. 6, I a III (finalidade, adequação, necessidade) | A finalidade "teste de produto" é declarada na ficha; o tratamento se limita ao mínimo: um caso, uma cópia, documentos até o ponto de corte, nada de identificadores. |
| Lei 13.709/2018, art. 7, IX, e art. 10 (legítimo interesse) | **Base presumida deste protocolo.** A base do mandato (art. 7, V e VI) não é presumida como cobertura automática de um uso com finalidade distinta. O protocolo é o registro do balanceamento que o art. 10 exige: finalidade concreta de apoio à atividade do controlador (inciso I), dados estritamente necessários (§ 1), transparência por este documento público (§ 2), dado sensível inelegível, titular não exposto a identificação. O owner que se apoiar em base diversa declara e justifica na ficha. |
| Lei 13.709/2018, art. 12, caput e § 1 (anonimização e reversão por meios próprios) | A cópia é **pseudonimizada, não anonimizada**, e a identificabilidade é relativa a quem detém os meios. Para o owner, que guarda o mapa, a cópia continua sendo dado pessoal e a LGPD continua aplicável a ele como controlador. Para o fornecedor do modelo, sem o mapa, a identificação não se faz por esforço razoável. Isso reduz o risco; não o zera, porque fatos intactos podem identificar (seção 2.3). |
| Lei 8.906/1994, art. 34, VII (violar, sem justa causa, sigilo profissional) | O fornecedor do modelo não recebe a identidade do cliente, da parte contrária, de testemunhas, de advogados ou do juízo. O que sai do escritório são fatos sem titular identificável por esforço razoável. |
| CPC, art. 189 (segredo de justiça) | Processo em segredo de justiça é inelegível, sem exceção. |

Referências não verificáveis pelo conector, a conferir na fonte da OAB antes
da execução: Código de Ética e Disciplina da OAB, capítulo do sigilo
profissional; recomendações do Conselho Federal da OAB sobre uso de
inteligência artificial generativa na advocacia.

## 2. Elegibilidade do caso

### 2.1 Inclusão (todos obrigatórios)

1. Caso cível dentro do escopo das skills publicadas: procedimento comum,
   tutela, cumprimento de sentença, execução, monitória, exibição, inventário
   ou procedimento especial coberto pelos módulos de `redacao-contencioso`.
2. Encerrado: arquivado, com trânsito em julgado, acordo cumprido ou
   desistência homologada. Nenhuma decisão pendente, nenhum prazo aberto,
   nenhuma possibilidade prática de desdobramento que a sessão pudesse afetar.
3. Houve pelo menos uma **bifurcação estratégica real** com registro
   datado: negociar ou executar, recorrer ou cumprir, produzir prova ou
   aguardar, contestar em bloco ou reconvir. O momento dessa bifurcação é o
   **ponto de corte** da sessão.
4. O desfecho posterior à bifurcação é conhecido e documentado, e serve de
   gabarito.
5. O owner foi o advogado do caso ou detém o mandato, com acesso legítimo aos
   autos e aos documentos internos.
6. Os documentos existem em texto extraível. Imagens de assinaturas,
   documentos pessoais escaneados e fotos são excluídos ou substituídos por
   descrição neutra.
7. Existem fontes contemporâneas ao ponto de corte (e-mails, atas, petições)
   suficientes para escrever a folha do advogado da seção 3.4 sem depender só
   de memória.

### 2.2 Exclusão (qualquer um basta)

- segredo de justiça, confidencialidade arbitral ou sigilo imposto por decisão
  judicial;
- parte menor de idade, incapaz ou em situação de vulnerabilidade;
- dados sensíveis materiais para o caso: saúde, orientação sexual, religião,
  origem racial, biometria, filiação sindical ou política;
- matéria fora do contrato cível vigente: trabalhista, criminal, fiscal,
  tributário especial, fiduciário, precatório;
- cliente que vedou uso de inteligência artificial ou cujo contrato tem
  cláusula de confidencialidade que o owner entenda alcançar este uso;
- caso reprovado no teste de reidentificação da seção 2.3;
- caso já usado como fonte de um dos 14 cenários anonimizados de
  `references/validacao-casos-reais.md`, para não medir a skill sobre
  material cuja classe de falha já orientou o contrato.

### 2.3 Teste de reidentificação (mecânico)

Datas, valores e cláusulas ficam intactos por decisão do owner, e são
justamente o vetor pelo qual quem conhece o foro reconheceria o caso. Antes
da preparação, o owner faz uma busca pública (busca na web e consulta
processual pública do tribunal) com a combinação: tribunal, ano, comarca,
valor aproximado da causa e objeto descrito em dez palavras. Se o caso real
aparecer entre os dez primeiros resultados, o caso é **inelegível**.

Alternativa registrada, não presumida: o owner pode, anotando na ficha,
rebaixar datas para mês e ano e valores para faixas, e repetir o teste. Isso
altera a decisão de manter datas e valores intactos e por isso exige
declaração expressa; sem ela, vale a inelegibilidade.

## 3. Preparação

Tudo nesta seção acontece antes da primeira mensagem ao modelo e fica fora do
repositório.

### 3.1 Diretórios

```
~/Dev/Habilidades/dogfood-caso-real-<AAAA-MM-DD>/
  sessao/            ← única pasta que o aplicativo do Claude enxerga
    documentos/      ← cópia pseudonimizada, só até o ponto de corte
    LEIA-ME.md       ← inventário dos documentos, sem conteúdo
  privado/           ← nunca aberto pelo aplicativo
    ficha.md         ← seção 7 preenchida
    mapa.md          ← correspondência real ↔ pseudônimo
    folha-do-advogado.md
    gabarito.md      ← o que aconteceu depois do ponto de corte
    registro.md      ← preenchido durante e após a sessão
    transcript.md    ← conversa copiada ao final
```

A pasta raiz fica fora de qualquer diretório sincronizado (Drive, iCloud,
Dropbox) e fora de qualquer repositório Git. Antes de copiar o primeiro
documento, a pasta é excluída do Time Machine (`tmutil addexclusion` sobre a
raiz) e o resultado é anotado na ficha. Alternativa mais forte, recomendada:
criar a pasta dentro de uma imagem de disco cifrada, cuja senha é destruída no
descarte; assim, qualquer cópia de segurança que sobreviva fica inútil.

### 3.2 Ponto de corte

Só entram em `sessao/documentos/` documentos datados até o ponto de corte,
inclusive. Petições, decisões, e-mails e atas posteriores ficam em
`privado/gabarito.md`, resumidos pelo owner em até vinte linhas: o que foi
decidido, por quem, quando, e o que resultou. O modelo não vê o gabarito em
nenhuma hipótese.

### 3.3 Pseudonimização

Regras de substituição, aplicadas com consistência em todos os documentos:

| Elemento | Substituição |
|---|---|
| Pessoas naturais (partes, sócios, testemunhas, peritos) | Papel + índice: `Autor`, `Sócio 1`, `Testemunha 2`, `Perito` |
| Pessoas jurídicas | Papel + ramo genérico: `Fornecedora`, `Construtora`, `Banco` |
| Advogados e escritórios | `advogado do Autor`, `advogada da Ré` |
| Juízo, juiz, relator, servidor | `Juízo da N.ª Vara Cível de <cidade>`, `Relator` |
| Número CNJ | Mantém tribunal e ano; zera o sequencial: `0000000-00.AAAA.8.16.0000` |
| CPF, CNPJ, RG, OAB, matrícula, placa, conta bancária | Removidos: `[id removido]` |
| Endereços | Cidade e UF apenas |
| E-mails, telefones, URLs pessoais | Removidos |
| Assinaturas, fotos, documentos pessoais escaneados | Removidos ou descritos: `[assinatura]` |
| Datas, valores, prazos, índices, percentuais | **Intactos** (salvo rebaixamento declarado na seção 2.3) |
| Fatos, cláusulas, teses, pedidos, fundamentos | **Intactos** |

O mapa de correspondência (`privado/mapa.md`) lista cada substituição, com as
variantes conhecidas de cada nome (abreviações, siglas, sobrenome isolado,
razão social e nome fantasia).

A conferência antes da sessão tem três camadas, e as duas últimas não
dependem de o owner ter percebido o dado:

1. **busca literal** de cada cadeia da coluna "real" do mapa em `sessao/`:
   zero ocorrências;
2. **busca normalizada**: sem acentos, caixa baixa, dígitos sem separadores
   (`1.000.000,00` e `1000000` são a mesma coisa), sobre o mapa e sobre os
   números de identificação por padrão (CPF, CNPJ, CNJ, OAB, telefone,
   e-mail): zero ocorrências;
3. **listagem de sequências com inicial maiúscula** em todo o `sessao/`
   (candidatas a nome próprio residual), revisadas uma a uma pelo owner e
   arquivadas em `privado/`.

O teste de reidentificação da seção 2.3 cobre o quarto vetor, os fatos
intactos. Os quatro resultados entram na ficha. A leitura integral da cópia
pelo owner, documento a documento, continua obrigatória; ela é a última
barreira, não a única.

### 3.4 Folha do advogado

`privado/folha-do-advogado.md` fixa, **antes da sessão**, o que o cliente
priorizava no ponto de corte: objetivo, apetite a risco, restrições de mesa,
prazo, caixa, relação com a outra parte. É o único material de que o operador
se serve para responder às perguntas do plugin.

O owner conhece o desfecho, e nenhuma declaração de boa-fé remove isso. A
proteção é documental: cada afirmação da folha cita fonte datada anterior ao
ponto de corte (e-mail, ata, petição, anotação da época). Item sem fonte
contemporânea é marcado `[memória]`. Resposta ao plugin sustentada apenas em
item `[memória]` invalida a comparação com o gabarito naquele ponto; não
invalida a sessão nem o recibo comportamental. A folha registra a data em
que foi escrita.

### 3.5 Ambiente

Conferências obrigatórias, cada uma com resposta registrada na ficha. A ficha
registra a declaração do owner; o aplicativo não oferece verificação
auditável por sessão, e o recibo declara esse limite.

1. **Pré-requisito bloqueante:** plugin `silo-legal` instalado no aplicativo
   do Claude pelo marketplace `sensdiego/codigo-aberto`, com o recibo de
   instalação limpa da Fase 1 do ROADMAP já registrado. Sem esse recibo, a
   execução não começa. Versão anotada na ficha.
2. Configuração de privacidade da conta do Claude conferida na data: uso das
   conversas para treinamento de modelo desligado. A resposta na ficha é
   "conferido, desligado" ou a execução não começa.
3. Sessão aberta com acesso de arquivos restrito à pasta `sessao/`.
4. Conectores desligados na conta ou no seletor da conversa, exceto o
   conector do Silo. Em especial, Google Drive, Gmail e qualquer conector que
   alcance os autos reais ficam fora, para que o modelo não possa buscar o
   caso original.
5. Conector do Silo: permitido, sob a regra de condução da seção 4, item 5.
   O owner sabe que o serviço guarda os termos consultados, desacoplados de
   quem perguntou; por isso termo distintivo do caso nunca pode virar
   consulta.
6. Nenhum outro projeto, instrução permanente ou memória do aplicativo
   contendo material do escritório ativo na sessão.
7. Registro de chamadas: o aplicativo não exporta a conversa com chamadas de
   ferramenta. O operador conta, durante a sessão, as consultas ao Silo e as
   leituras de arquivo que o aplicativo exibir, e anota no registro.

### 3.6 Critérios pré-registrados de falseabilidade

O desenho detecta defeito com força e virtude com fraqueza: o operador é o
autor do plugin, conhece a rota esperada e conhece o desfecho. Para que
"mantém" não seja confirmação retroativa, a ficha fixa, antes da sessão:

- que divergência entre a decisão do plugin e o gabarito contaria como
  `diverge sem razão sustentável` (ex.: recomendar executar quando a folha
  registra restrição expressa do cliente à execução);
- que opção ausente do mapa contaria como `a opção real não apareceu`;
- que comportamento nas fases de intake e análise contaria como defeito
  (ex.: fato promovido a provado sem documento; localizador inexistente).

O veredito é julgado contra esses critérios, não contra a impressão do dia.

## 4. Condução

1. **Operador:** o próprio owner, digitando. Isso fecha a ressalva do dogfood
   pareado, em que um agente aplicou a folha.
2. **Prompt inicial fixo**, sem citar nenhuma skill:

   > Recebi este caso. Os documentos estão na pasta `documentos/` e o
   > inventário em `LEIA-ME.md`. Preciso entender o que temos e decidir o que
   > fazer agora. Se consultar o Silo, use só institutos e teses jurídicas;
   > nunca fatos, cláusulas, nomes ou valores deste caso.

   Rota esperada: `novo-caso`, seguida de `analise-documental`,
   `analise-juridica-civel` e `deliberacao-juridica`. Rota diferente é achado,
   não falha automática.
3. **Respostas do operador:** somente a partir da folha do advogado, como
   responderia no ponto de corte. Pergunta do plugin que a folha não cobre é
   respondida como o advogado responderia à época e anotada como "resposta
   improvisada" no registro, com a marca `[memória]`.
4. **Nunca digitar nome, número ou dado real.** Se escapar, a mensagem é
   anotada no registro como incidente de nível 1, a conversa é excluída do
   aplicativo ao fim da sessão e o recibo estrutural declara o incidente. O
   recibo comportamental continua válido; o recibo de identificabilidade não.
5. **Silo só com institutos e teses.** Se o modelo, por iniciativa própria,
   consultar o Silo com cláusula, valor, nome ou fato íntegro do caso, o
   operador anota como incidente de nível 1: o termo ficou persistido fora
   da conversa e fora do alcance do descarte da seção 6.
6. **Sem gabarito, sem hindsight.** O operador não corrige o plugin com o que
   sabe do desfecho. Se o plugin errar um fato que está nos documentos, o
   operador aponta o documento, como faria com um associado, e anota.
7. **Skills pelo nome só como último recurso.** Se o roteamento falhar duas
   vezes, o operador cita a skill e anota o turno.
8. **Confirmações:** o operador confirma handoffs como advogado confirmaria,
   lendo. Confirmação de fatos não autoriza redação; a deliberação tem gate
   próprio; qualquer autorização implícita observada é registrada como
   violação de invariante.
9. **Parada por desenho:** a sessão termina na decisão registrada pelo plugin
   (handoff de tipo `decisão`) ou no briefing de redação aceito. Minuta é
   opcional e, se produzida, não sai da pasta `privado/`.
10. **Parada por risco**, distinta da anterior e registrada como tal: o
    modelo pede documento posterior ao ponto de corte, tenta alcançar
    `privado/` ou outro caminho fora de `sessao/`, produz texto que
    identifica alguém, ou o operador percebe identificador que escapou ao
    mapa. A sessão para no ato; o registro anota turno e causa; a conversa é
    excluída; a ficha recebe a decisão do owner sobre repetir ou encerrar.
11. **Orçamento:** até três horas, com uma pausa permitida. Turnos e horário
    de início e fim vão para o registro. O aplicativo não expõe custo por
    sessão; o recibo declara "custo não medido".
12. **Ao final:** copiar a conversa para `privado/transcript.md` (cópia
    manual; chamadas de ferramenta vêm da contagem do operador), excluir a
    conversa do histórico do aplicativo e preencher o registro no mesmo dia.

## 5. O que sai da sessão

### 5.1 Registro (privado)

`privado/registro.md` segue o molde de
`2026-08-31-pareado-deliberacao/registro-sessao-b.md`, acrescido de uma
seção por fase:

- **intake:** elegibilidade declarada? fontes inventariadas com localizador?
  o que faltou?
- **análise documental:** achados com fonte e localizador? contradições e
  lacunas nomeadas? algum fato inventado ou promovido indevidamente a
  provado?
- **análise jurídica:** mapa de opções com premissa, consequência,
  reversibilidade e urgência? a opção que o escritório de fato escolheu
  apareceu no mapa?
- **deliberação:** as sete métricas do dogfood pareado (decisão final,
  trade-off exposto, lacunas descobertas, turnos e tempo, abandono, gate,
  protocolo de entrevista);
- **comparação com o gabarito:** classificada em uma de quatro classes,
  contra os critérios pré-registrados da seção 3.6: `coincide`, `diverge com
  razão que a folha sustenta`, `diverge sem razão sustentável`, `a opção real
  não apareceu`. A última é o sinal de produto mais valioso do desenho, porque
  mede cobertura do mapa de opções e não concordância; ela ganha destaque no
  recibo. Divergência sustentada pela folha não é falha; divergência
  sustentada só por endosso posterior do owner é classificada como `sem razão
  sustentável`, porque o gabarito registra o que se fez, não o que se devia
  fazer, e o endosso retroativo não é evidência.

### 5.2 Veredito (entra no repositório)

Cinco linhas do owner: o que ajudou, o que atrapalhou, o que faltou, como a
decisão do plugin se compara com o desfecho real, e a conclusão `mantém`,
`redesenha` ou `não usar em caso real ainda`. Entra no ROADMAP e em
`data/dogfood/<AAAA-MM-DD>-caso-real-<NN>/veredito.md`.

### 5.3 Recibo estrutural (entra no repositório)

`data/dogfood/<AAAA-MM-DD>-caso-real-<NN>/recibo.md`, no espírito da seção
"Observabilidade e recibos" da RFC-CA-001: estrutura e resultado, nunca
conteúdo. Campos:

- versão do plugin, aplicativo, data, duração, turnos do operador;
- classe processual em termo genérico (ex.: "cumprimento de sentença") e fase
  em termo genérico (ex.: "antes de constrição"), sem juízo, comarca, ano do
  processo ou valor;
- skills acionadas, em ordem; roteamento por nome forçado (sim/não, turno);
- tipos de handoff produzidos e contagens: documentos fornecidos, achados,
  contradições, lacunas, opções no mapa;
- eventos de gate: autorizações implícitas observadas (esperado: zero);
- consultas ao Silo, pela contagem do operador: quantidade, se alguma usou
  termo distintivo (incidente) e se alguma resultou em precedente usado;
- conferência de pseudonimização: resultado das três camadas e do teste de
  reidentificação; incidentes de nível 1: quantidade; parada por risco:
  sim/não;
- classe da comparação com o gabarito (uma das quatro), com a classe `a
  opção real não apareceu` em destaque quando ocorrer;
- custo: "não medido no aplicativo";
- limites declarados: um caso, operador que conhece o desfecho, cópia
  reversível pelo owner, transcript por cópia manual, controles de ambiente
  declarados e não verificados, retenção do fornecedor não verificável.

### 5.4 Barreira de publicação

Antes de qualquer commit com `veredito.md` e `recibo.md`:

1. conferência mecânica dos dois arquivos, literal e normalizada, contra a
   coluna "real" do mapa: zero ocorrências;
2. leitura dos dois arquivos pelo owner com duas perguntas: "alguém do foro
   reconheceria o caso por isto?" e "o próprio cliente se reconheceria por
   isto, sabendo quem é o escritório e a data do commit?"; resposta "sim" ou
   "talvez" a qualquer uma reescreve até ser "não";
3. nada mais da pasta da sessão é copiado: nem documentos, nem mapa, nem
   folha, nem gabarito, nem transcript, nem minuta;
4. fragmento de release `none`, como nos dogfoods anteriores.

**Incidente de nível 2:** dado real que chegue ao repositório, em qualquer
commit, mesmo em branch. Resposta: remover o conteúdo do histórico (reescrita
e envio forçado), solicitar ao GitHub a limpeza de caches e forks, anotar o
incidente no registro privado e no ROADMAP em uma linha sem conteúdo, e
avaliação pelo owner, como advogado responsável, sobre comunicação ao cliente
e demais consequências. É a única hipótese em que a regra de não reescrever
histórico deste repositório cede.

## 6. Retenção e descarte

- **Pasta da sessão:** mantida localmente, fora de sincronização e excluída
  do Time Machine desde a criação, por até 30 dias após o commit do recibo,
  para permitir releitura ou contestação do veredito. Depois, excluída
  integralmente. A exclusão é anotada no ROADMAP em uma linha, sem reabrir o
  diretório no repositório.
- **Cópias de segurança:** o descarte aos 30 dias cobre a pasta de trabalho.
  Snapshots locais do sistema podem reter a pasta por algum tempo depois da
  exclusão; o owner os apaga com `tmutil` ou espera sua expiração antes de
  declarar o descarte completo. Se a pasta esteve dentro de imagem cifrada, a
  destruição da senha equivale ao descarte, e os snapshots deixam de importar.
  Descarte que não puder ser completado é declarado **parcial** no recibo,
  com a causa.
- **Mapa de correspondência:** excluído no mesmo prazo e pelas mesmas regras.
  Sem o mapa e sem cópia recuperável, a cópia pseudonimizada deixa de ser
  reversível por meios próprios do owner.
- **Conversa no aplicativo:** excluída do histórico ao fim da sessão, depois
  da cópia. A retenção do lado do fornecedor segue a política vigente na
  data, que o owner confere e anota na ficha; este protocolo não a verifica e
  o recibo declara esse limite.
- **Incidente de identificabilidade:** dado real detectado após a sessão, no
  transcript ou no recibo, dispara exclusão imediata da conversa, anotação no
  registro e avaliação pelo owner, como advogado responsável, sobre
  comunicação ao cliente e demais consequências. O protocolo não decide isso.

## 7. Ficha de execução

Copiar para `privado/ficha.md` e preencher antes da primeira mensagem. Ficha
incompleta significa execução não autorizada.

```
Execução: caso-real-<NN>          Data prevista:
Identificador opaco do caso: CR-<NN>
Classe processual / fase no ponto de corte:
Ponto de corte (data e evento):
Bifurcação estratégica real (uma frase):
Desfecho conhecido (sim/não; resumido em gabarito.md):

Elegibilidade
  Inclusão 1 a 7 conferidas:            [ ] sim
  Exclusões conferidas, nenhuma aplica: [ ] sim
  Cliente vedou IA ou cláusula alcança este uso? [ ] não
  Caso usado em validacao-casos-reais? [ ] não
  Teste de reidentificação (2.3): [ ] caso não aparece nos dez primeiros
    Rebaixamento de datas/valores declarado? [ ] não  [ ] sim, porque:

Fundamentos
  Finalidade declarada: teste de produto, distinta do mandato
  Base legal: [ ] legítimo interesse (art. 7, IX; art. 10), balanceamento
    registrado neste protocolo   [ ] outra, justificada:
  Leitura integral da cópia, documento a documento: [ ] feita em <data>
  Conferência literal do mapa: [ ] zero ocorrências
  Conferência normalizada (mapa + padrões de identificação): [ ] zero
  Listagem de iniciais maiúsculas revisada: [ ] feita, arquivada em privado/

Ambiente
  Fornecedor / plano / aplicativo:
  Plugin instalado pelo marketplace, versão:
  Recibo de instalação limpa (Fase 1) registrado em: [ ] <data e local>
  Privacidade da conta (treinamento): [ ] conferido, desligado em <data>
  Acesso de arquivos restrito a sessao/: [ ] sim
  Conectores desligados, exceto Silo: [ ] sim (declaração, não verificação)
  Projetos, instruções e memórias do escritório inativos: [ ] sim
  Política de retenção do fornecedor conferida em <data>:
  Pasta excluída do Time Machine (tmutil addexclusion): [ ] sim
  Imagem de disco cifrada: [ ] sim  [ ] não

Preparação
  folha-do-advogado.md escrita em <data>; itens [memória]: <n> de <total>
  gabarito.md escrito em <data>

Critérios pré-registrados (3.6)
  Divergência que conta como "sem razão sustentável":
  Opção cuja ausência conta como "a opção real não apareceu":
  Defeito de intake/análise que conta como falha:

Assinatura do owner e data:
```

## 8. Limites deste protocolo

- Um caso não é estatística; o recibo prova uso humano em material real, não
  eficácia geral.
- O desenho é assimétrico: detecta defeito com força e virtude com fraqueza.
  O operador é o autor do plugin, conhece a rota esperada e conhece o
  desfecho. Os critérios pré-registrados e a folha com fontes datadas reduzem
  o viés; não o eliminam.
- A cópia é reversível pelo owner enquanto o mapa ou qualquer cópia de
  segurança existir; para ele, continua sendo dado pessoal.
- Os controles de ambiente da seção 3.5 são declarações do owner; o
  aplicativo não os verifica por sessão.
- O protocolo não verifica o que o fornecedor do modelo retém nem por quanto
  tempo.
- O protocolo foi calibrado para o aplicativo do Claude e a conta do owner;
  outro fornecedor, plano ou API exige reconferência.
- O protocolo não autoriza serviço ao cliente, protocolo de peça, anúncio
  público ou uso em caso vivo. Caso vivo exige revisão própria deste
  documento, com base legal e consentimento tratados de forma diferente.
- O protocolo não é parecer jurídico. O owner é o advogado responsável e
  decide, caso a caso, se os fundamentos da seção 1 sustentam a execução.

## Proveniência

- Escrito em 2026-09-05 a partir das decisões do owner na mesma data (caso
  encerrado pseudonimizado; aplicativo do Claude; desenho em seis partes
  aprovado) e do item estacionado do HANDOFF "execução de skills sobre autos
  reais (exige protocolo de privacidade próprio)".
- Emendado em 2026-09-05 após parecer do conselho (K3, contribuição
  material; Sol indisponível por franquia): base legal presumida em vez de
  delegada; teste mecânico de reidentificação; conferência em três camadas;
  folha do advogado com fontes datadas; critérios pré-registrados de
  falseabilidade; regra de condução para o Silo; parada por risco; incidente
  de nível 2; retenção honesta quanto a cópias de segurança; pré-requisito
  bloqueante de instalação limpa; pergunta do cliente na barreira de
  publicação; remoção da analogia com o art. 13 da LGPD.
- Artigos verificados em 2026-09-05 pelo conector Silo nas páginas oficiais:
  Lei 13.709/2018, arts. 6, 7, 10 e 12
  (`https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm`);
  Lei 8.906/1994, art. 34
  (`https://www.planalto.gov.br/ccivil_03/leis/l8906.htm`);
  CPC, art. 189
  (`https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm`).
  A verificação não avalia vigência.
- Nenhum caso real foi lido, copiado ou pseudonimizado para escrever este
  documento.
