import time
import schedule
import uuid
from content_generation import gerar_texto, gerar_imagem, gerar_hashtags
from telegram_bot import enviar_para_aprovacao, iniciar_bot

# Temas podem ser dinâmicos, aqui um exemplo fixo
TEMAS = [
    "Desafios da maternidade moderna",
    "Tendências de educação positiva",
    "Polêmicas sobre licença maternidade",
    "Saúde mental das mães em 2025",
    "Redes sociais e maternidade"
]

def rotina():
    tema = TEMAS[int(time.time()) % len(TEMAS)]
    texto = gerar_texto(tema)
    imagem = gerar_imagem(tema)
    hashtags = gerar_hashtags(texto)
    post_id = str(uuid.uuid4())
    enviar_para_aprovacao(texto, imagem, hashtags, post_id)

if __name__ == "__main__":
    schedule.every().day.at("09:00").do(rotina)
    schedule.every().day.at("18:00").do(rotina)
    iniciar_bot()
    while True:
        schedule.run_pending()
        time.sleep(1)
