# SpellCaster — Sega Master System PT-BR

A **Newportgame** apresenta este projeto de tradução brasileira e restauração técnica de *SpellCaster* para Sega Master System.

Este repositório reúne a documentação técnica bilíngue e as ferramentas Python usadas na análise da ROM, investigação de textos e gráficos e validação do projeto. O material é voltado a romhackers, preservacionistas, pesquisadores e desenvolvedores interessados nos sistemas de 8 bits da Sega.

## Estrutura do repositório

- [`README.md`](README.md) — apresentação em inglês.
- [`docs/en/`](docs/en/) — documentação técnica em inglês.
- [`docs/pt-br/`](docs/pt-br/) — documentação técnica em português.
- [`tools/localization/`](tools/localization/) — ferramentas forenses e de localização em Python.

## Download

O pacote oficial do patch **SpellCaster PT-BR v1.0** está disponível na
[página da Release no GitHub](https://github.com/contatonewportgame-code/spellcaster-sms-ptbr/releases/tag/v1.0.0).
Ele contém o patch IPS, o `SpellCaster.tbl` e o `LEIA-ME.txt`. A ROM completa
não é distribuída.

## Documentação

O repositório reúne dois tipos de material técnico:

1. **Documentação específica do SpellCaster**, incluindo o Protocolo Mestre e o fluxo de localização e restauração.
2. **Documentação geral do Sega Master System**, incluindo o Compêndio Master System, que aborda Z80, VDP, VRAM, codificação de texto, ponteiros, Planar RLE e métodos relacionados de engenharia reversa.

## Ferramentas

As ferramentas são disponibilizadas como código-fonte para estudo e reprodutibilidade. Elas abrangem rastreamento de VRAM/tilemap, investigação do VDP Loader, análise Planar RLE, patching de fontes, localização de espaço livre, busca textual, investigação gráfica, diagnóstico de crashes, integridade narrativa, auditoria de bordas e verificações relacionadas.

Antes de executar qualquer ferramenta, leia o código-fonte e confirme os caminhos de entrada e saída esperados. Alguns scripts podem exigir uma imagem local da ROM ou arquivos específicos do projeto; ROMs completas não são incluídas intencionalmente neste repositório.

## Política de ROM e distribuição

Este repositório não inclui as imagens da ROM original ou traduzida. A distribuição da tradução deve utilizar um formato de patch e exigir uma ROM original obtida legalmente. Pacotes de lançamento, quando publicados, devem conter o patch, a tabela de caracteres e a documentação, e não uma ROM completa.

## Autor

Cristiano Mariano — Newportgame

## Idioma

A apresentação principal do repositório está em inglês. A documentação em português está disponível junto da documentação em inglês, e a visão geral em português está disponível neste arquivo.
