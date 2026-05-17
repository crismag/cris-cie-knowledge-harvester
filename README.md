# cris-cie-knowledge-harvester

Standalone Python utility for harvesting external repositories and exporting validated CRIS-CIE capability packs.

## CLI

- `cie-harvest init`
- `cie-harvest list-sources`
- `cie-harvest add-source --name ... --repo ... --domain ... --license ...`
- `cie-harvest fetch --source ...`
- `cie-harvest scan --source ...`
- `cie-harvest extract --source ...`
- `cie-harvest build-pack --domain ... --pack-id ...`
- `cie-harvest validate-pack --pack ...`
- `cie-harvest export-pack --pack ... --target ...`

## Purpose

The harvester stays outside the CRIS-CIE runtime. It scans source repos, normalizes reusable patterns, and exports validated packs for later runtime use.
