# Indexação semântica de processo

Use esta referência para íntegra processual, especialmente PDF longo.

## Autoridade e endereçamento

O arquivo original permanece autoritativo. Registre seu hash quando a plataforma
permitir, sem alterar o original.

Use três níveis de endereço:

- `F-01`: fonte original;
- `F-01/U-014`: unidade processual natural;
- `F-01/U-014/C-003`: segmento semântico criado apenas quando a unidade for
  extensa ou combinar assuntos diferentes.

Todo endereço preserva páginas inicial e final no PDF original. Índice, OCR e
chunks são derivados e nunca substituem a fonte.

## Unidade processual

Prefira limites já existentes no processo:

- petição ou manifestação;
- decisão, despacho, sentença ou acórdão;
- certidão, intimação ou ato ordinatório;
- documento anexado ou conjunto documental coerente;
- audiência, laudo ou prova produzida;
- movimentação com seus arquivos.

Não crie uma unidade a cada página. Não una atos independentes apenas porque
estão próximos no PDF.

## Chunk semântico

Subdivida uma unidade somente quando isso melhorar recuperação e citação. Use
seções como fatos, preliminares, mérito, pedidos, fundamentação, dispositivo ou
bloco documental coerente. Cada chunk registra:

- ID da unidade mãe;
- título descritivo;
- páginas;
- começo e fim reconhecíveis;
- qualidade do texto ou OCR;
- indicação de imagem, tabela, assinatura ou carimbo relevante.

Chunking não interpreta se a alegação é verdadeira, se a tese procede ou se a
prova é suficiente.

## INDICE_PROCESSO.md

Uma linha por unidade:

| ID | Evento ou data | Tipo | Autor ou órgão | Páginas | Qualidade | Observação estrutural |
|---|---|---|---|---|---|---|

Registre páginas ausentes, repetidas, fora de ordem e unidades bloqueadas. Não
afirme completude sem conferir o início, o fim e a sequência da íntegra.

## CORPUS_PROCESSO.md

Para cada unidade e chunk, registre:

- endereço estável;
- páginas do original;
- texto extraído ou resumo estrutural não substantivo;
- marcadores de baixa confiança;
- ponteiro de reabertura do original.

Reabra o PDF quando houver OCR inseguro, imagem material, tabela, assinatura,
carimbo, necessidade de citação literal, conflito com o índice ou suspeita de
página ausente.

## Atualização

Ao receber nova íntegra ou movimentação:

1. não renumere IDs antigos;
2. verifique sobreposição e versão;
3. acrescente novas unidades na sequência apropriada;
4. marque unidades substituídas sem apagá-las;
5. encaminhe somente conteúdo novo ou alterado para análise documental.
