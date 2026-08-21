# Changelog e releases

O Código Aberto usa o mesmo contrato básico adotado por `fs.brain` e Valter:
uma fonte única de versão, fragmentos por mudança, changelog gerado, tag imutável
e GitHub Release vinculada ao commit exato.

## Fonte da versão

A versão canônica está em [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json).
Não altere esse número manualmente. O workflow de release atualiza o manifesto e
o changelog juntos.

## Mudança normal

Toda alteração que afete o produto inclui um fragmento:

```bash
python3 scripts/release.py fragment-add \
  --name correcao-links \
  --kind patch \
  --category Fixed \
  --summary "Corrige links das referências compartilhadas."
```

Depois, valide:

```bash
make validate
make test-release
python3 scripts/release.py impact --ref-range origin/main...HEAD
```

O fragmento entra no mesmo pull request da mudança. O `CHANGELOG.md` não deve ser
editado manualmente para trabalho ainda não publicado.

## Incrementos

| Tipo | Quando usar |
|---|---|
| `patch` | Correção compatível |
| `minor` | Nova capacidade compatível |
| `major` | Mudança incompatível; exige descrição `breaking` |
| `none` | Mudança consumida sem publicar versão |

As categorias `Added`, `Changed`, `Fixed`, `Security` e `Removed` controlam a
seção do changelog, independentemente do incremento semântico.

## O que acontece depois do merge

Em um push elegível para `main`, o workflow
[`software-release.yml`](.github/workflows/software-release.yml):

1. valida que a mudança declarou intenção por fragmento;
2. calcula a próxima versão;
3. consome os fragmentos e gera a seção do changelog;
4. valida skills, referências, bundles e o próprio protocolo;
5. cria e envia `chore(release): vX.Y.Z`;
6. cria a tag anotada `vX.Y.Z` no SHA exato;
7. publica o GitHub Release com as notas extraídas do changelog.

A primeira publicação mantém a versão já declarada no manifesto (`0.2.0`). As
seguintes aplicam o maior incremento existente nos fragmentos do lote.

## Garantias

- uma tag existente nunca é movida;
- fragmentos alterados depois do planejamento invalidam a operação;
- caminhos desconhecidos exigem decisão explícita, em vez de serem ignorados;
- o commit automático só chega a `main` depois dos checks locais do workflow;
- release não comprova instalação no aplicativo, funcionamento do Silo ou uso
  humano das skills;
- uma execução interrompida pode ser repetida: se a tag existir sem GitHub
  Release, o workflow publica a release a partir do commit já marcado.

Comandos de inspeção:

```bash
python3 scripts/release.py plan
python3 scripts/release.py audit
python3 scripts/release.py notes --version 0.2.0
```
