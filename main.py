import yfinance as yf
import requests
from datetime import datetime

# --- CONFIGURAÇÕES DO SEU BOT ---
TOKEN = "8219204816:AAGKg2m5rCTPdPVwAS_rckbxR7nvzEQovaM"
CHAT_ID = "6784773008"

# Lista de ativos atualizada (Dólar, Crypto, Ações e FIIs)
ativos = {
    "Dólar (USD/BRL)": "USDBRL=X",
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Binance Coin (BNB)": "BNB-USD",
    "Shiba Inu (SHIB)": "SHIB-USD",
    "Petrobras (PETR4)": "PETR4.SA",
    "FII MGHT11": "MGHT11.SA",
    "FII SNEL11": "SNEL11.SA"
}

def enviar_resumo():
    # Pega o horário atual
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    mensagem = f"📊 *Relatório do Mercado ({agora})*\n\n"
    
    for nome, ticker in ativos.items():
        try:
            # Busca o preço atual no Yahoo Finance
            dados = yf.Ticker(ticker).history(period="1d")
            if not dados.empty:
                preco = dados['Close'].iloc[-1]
                
                # Formatação: Se for Crypto ou Dólar mostra mais casas decimais
                if "USD" in ticker or "SHIB" in ticker:
                    mensagem += f"🔹 *{nome}:* $ {preco:.4f}\n"
                else:
                    mensagem += f"🔹 *{nome}:* R$ {preco:.22f}\n"
            else:
                mensagem += f"❌ *{nome}:* Erro ao buscar\n"
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
    except Exception as e:
        print(f"Erro ao conectar com o Telegram: {e}")

if __name__ == "__main__":
    enviar_resumo()
