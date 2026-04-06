
import yfinance as yf
import requests
from datetime import datetime

# --- CONFIGURAÇÕES DO SEU BOT ---
TOKEN = "8219204816:AAGKg2m5rCTPdPVwAS_rckbxR7nvzEQovaM"
CHAT_ID = "6784773008"

# Ativos que o Roger pediu: Dólar, Ethereum e Bitcoin
ativos = {
    "Dólar (USD/BRL)": "USDBRL=X",
    "Ethereum (ETH)": "ETH-USD",
    "Bitcoin (BTC)": "BTC-USD"
}

def enviar_resumo():
    # Pega o horário atual do Rio de Janeiro (aproximado pelo servidor)
    agora = datetime.now().strftime('%d/%m/%Y %H:%M')
    mensagem = f"📊 *Relatório do Mercado ({agora})*\n\n"
    
    for nome, ticker in ativos.items():
        try:
            # Busca o preço atual no Yahoo Finance
            dados = yf.Ticker(ticker).history(period="1d")
            if not dados.empty:
                preco = dados['Close'].iloc[-1]
                
                # Formatação: Dólar em R$, Criptos em US$
                if "Dólar" in nome:
                    mensagem += f"💵 *{nome}:* R$ {preco:.2f}\n"
                else:
                    mensagem += f"🪙 *{nome}:* US$ {preco:,.2f}\n"
        except Exception as e:
            print(f"Erro ao buscar {nome}: {e}")
            continue
    
    # Envia a mensagem final para o seu Telegram
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    
    try:
        requests.post(url, data=payload)
        print(f"✅ Relatório enviado com sucesso às {agora}!")
    except Exception as e:
        print(f"Erro ao conectar com o Telegram: {e}")

if __name__ == "__main__":
    enviar_resumo()
