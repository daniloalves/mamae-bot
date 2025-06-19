# Mamae Bot

Automação de geração, aprovação e publicação de posts diários sobre mães, com IA, Telegram, Instagram e página estática (Hugo + Netlify).

## Como funciona

1. Geração automática de texto, imagem e hashtags via IA.
2. Envio para aprovação no Telegram.
3. Após aprovação, publicação no Instagram e na página web estática.

## Estrutura

- `backend/`: scripts Python para geração, aprovação e publicação.
- `site/`: site estático Hugo.
- `.github/workflows/`: automação com GitHub Actions.
- `netlify.toml`: configuração do Netlify.

## Configuração

- Adicione suas chaves de API como secrets no GitHub.
- Configure o Telegram Bot, Instagram API e Netlify.

## Rodando localmente

```bash
pip install -r backend/requirements.txt
python backend/scheduler.py
```
