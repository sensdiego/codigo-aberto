# Contribuindo

As contribuições deste repositório são licenciadas sob Apache-2.0.

## Estrutura de uma skill

- pasta `skills/<nome>/` com `SKILL.md`;
- frontmatter com `name` em kebab-case e `description` que explique o que a
  skill faz e quando usá-la;
- escopo, pré-requisitos e limites explícitos;
- referências carregadas progressivamente;
- fontes e localizadores para afirmações materiais;
- confirmação humana obrigatória antes de redação jurídica;
- seção `O que esta skill não faz`.

Toda referência `CPC:<id>` deve existir em
[`references/legislacao/cpc/manifest.json`](references/legislacao/cpc/manifest.json).

## Envio

1. Crie uma branch `feat/<nome>`.
2. Adicione ou altere apenas os arquivos necessários.
3. Execute:

   ```bash
   python3 scripts/validate_skills.py
   ```

4. Abra um pull request explicando o resultado, os gatilhos de uso e como a
   mudança foi verificada.

Não inclua casos reais, dados pessoais, transcrições privadas, pesquisas
internas, credenciais ou código do serviço Silo.
