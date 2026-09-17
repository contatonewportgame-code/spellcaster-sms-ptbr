# SpellCaster — Sega Master System PT-BR

**Newportgame** presents a Brazilian Portuguese translation and technical restoration project for *SpellCaster* on the Sega Master System.

This repository contains the project's bilingual technical documentation and the Python tools used for ROM analysis, text/graphic investigation, and validation. It is intended for romhackers, preservationists, researchers, and developers studying Sega 8-bit systems.

## Repository layout

- [`README_PTBR.md`](README_PTBR.md) — Portuguese presentation.
- [`docs/en/`](docs/en/) — English technical documentation.
- [`docs/pt-br/`](docs/pt-br/) — Portuguese technical documentation.
- [`tools/localization/`](tools/localization/) — Python forensic and localization tools.

## Documentation

The repository includes two kinds of technical material:

1. **SpellCaster-specific documentation**, including the Master Protocol and the restoration/localization workflow.
2. **General Sega Master System documentation**, including the Master System Compendium, which discusses Z80, VDP, VRAM, text encoding, pointers, Planar RLE, and related reverse-engineering methods.

## Tools

The tools are provided as source code for research and reproducibility. They cover VRAM/tilemap tracing, VDP loader investigation, Planar RLE analysis, font patching, free-space detection, text searches, graphic hunting, crash diagnostics, narrative integrity, border auditing, and related checks.

Before running a tool, read its source and verify its expected input/output paths. The scripts may require a local ROM image or project-specific files; complete ROM images are intentionally not included in this repository.

## ROM and distribution policy

This repository does not include the original or translated ROM images. Distribution of a translation should use a patch format and require a legally obtained original ROM. Release packages, when published, should contain the patch, table file, and documentation rather than a full ROM.

## Author

Cristiano Mariano — Newportgame

## Language

The canonical repository presentation is in English. Portuguese documentation is available alongside the English material, and the Portuguese repository overview is available in [`README_PTBR.md`](README_PTBR.md).
