# adam-ops

<!-- adam-badges:start -->
[![commits](https://img.shields.io/github/commit-activity/t/Adam-Blf/adam-ops?color=001329&label=commits&style=flat-square)](https://github.com/Adam-Blf/adam-ops/commits)
[![visites](https://hits.sh/github.com/Adam-Blf/adam-ops.svg?style=flat-square&label=visites&color=001329)](https://hits.sh/github.com/Adam-Blf/adam-ops/)
[![last commit](https://img.shields.io/github/last-commit/Adam-Blf/adam-ops?color=D4A437&style=flat-square&label=dernier%20push)](https://github.com/Adam-Blf/adam-ops/commits)
[![top language](https://img.shields.io/github/languages/top/Adam-Blf/adam-ops?style=flat-square)](https://github.com/Adam-Blf/adam-ops)
[![license](https://img.shields.io/github/license/Adam-Blf/adam-ops?style=flat-square&color=D4A437)](LICENSE)
<!-- adam-badges:end -->

![version](https://img.shields.io/badge/version-1.0.0-D4A437?style=flat-square)

Garde-fous automatiques des repos Adam-Blf. Applique les regles
d'exploitation du proprietaire (typographie, qualite) en CI, sans
intervention manuelle.

## Features

- [x] Audit typographique quotidien de tous les repos publics (README +
  description) : echec + issue si tiret cadratin, demi-cadratin,
  mediopoint ou puce detecte

## Architecture

```mermaid
flowchart TB
    CRON["GitHub Actions cron<br/>06:23 UTC quotidien"]
    SCRIPT["scripts/typo_audit.py<br/>stdlib, GITHUB_TOKEN"]
    API["API GitHub<br/>repos publics Adam-Blf"]
    OK["Run vert"]
    ISSUE["Issue ouverte sur adam-ops<br/>liste des fichiers fautifs"]
    CRON --> SCRIPT --> API
    SCRIPT -->|aucun caractere interdit| OK
    SCRIPT -->|detection| ISSUE
```

## Regles verifiees

Caracteres interdits dans les README et descriptions : `U+2014` (tiret
cadratin), `U+2013` (demi-cadratin), `U+00B7` (mediopoint), `U+2022`
(puce). Remplacement attendu : tiret court, virgule ou point.

## Lancer en local

```bash
GITHUB_TOKEN=$(gh auth token) python scripts/typo_audit.py
```

## Limites

Les repos prives ne sont pas audites (GITHUB_TOKEN du workflow limite
aux repos publics de l'utilisateur).

## Licence

MIT, voir [LICENSE](LICENSE).
