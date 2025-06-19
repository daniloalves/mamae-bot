import os
import requests
from dotenv import load_dotenv

load_dotenv()
IG_ACCESS_TOKEN = os.getenv('IG_ACCESS_TOKEN')
IG_BUSINESS_ID = os.getenv('IG_BUSINESS_ID')

SITE_POSTS_PATH = os.path.join(os.path.dirname(__file__), '../site/content/posts')

def publicar_instagram(imagem_url, legenda):
    url = f"https://graph.facebook.com/v19.0/{IG_BUSINESS_ID}/media"
    payload = {
        'image_url': imagem_url,
        'caption': legenda,
        'access_token': IG_ACCESS_TOKEN
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        creation_id = response.json()['id']
        publish_url = f"https://graph.facebook.com/v19.0/{IG_BUSINESS_ID}/media_publish"
        publish_payload = {
            'creation_id': creation_id,
            'access_token': IG_ACCESS_TOKEN
        }
        requests.post(publish_url, data=publish_payload)
    else:
        print('Erro ao publicar no Instagram:', response.text)

def criar_post_markdown(titulo, texto, imagem_url, hashtags):
    filename = os.path.join(SITE_POSTS_PATH, f"{titulo.replace(' ', '_')}.md")
    with open(filename, "w") as f:
        f.write(f"---\ntitle: '{titulo}'\ntags: {hashtags}\nimage: {imagem_url}\n---\n\n{texto}\n")

def publicar_fluxo(texto, imagem_url, hashtags):
    titulo = texto.split('.')[0][:40]
    publicar_instagram(imagem_url, f"{texto}\n\n{hashtags}")
    criar_post_markdown(titulo, texto, imagem_url, hashtags)
