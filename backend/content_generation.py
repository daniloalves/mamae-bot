import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

PROMPT_TEXTO = os.path.join(os.path.dirname(__file__), 'prompts', 'texto.txt')
PROMPT_HASHTAGS = os.path.join(os.path.dirname(__file__), 'prompts', 'hashtags.txt')

def ler_prompt(path, **kwargs):
    with open(path, 'r') as f:
        prompt = f.read()
    return prompt.format(**kwargs)

def gerar_texto(tema):
    prompt = ler_prompt(PROMPT_TEXTO, tema=tema)
    resposta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300
    )
    return resposta.choices[0].text.strip()

def gerar_hashtags(texto):
    prompt = ler_prompt(PROMPT_HASHTAGS, texto=texto)
    resposta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=30
    )
    return resposta.choices[0].text.strip().replace('\n', ' ')

def gerar_imagem(descricao):
    response = openai.Image.create(
        prompt=descricao,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']
