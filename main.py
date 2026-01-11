import cerebro
from ouvidos import Ouvidos
import voz

WAKE_WORDS = ["jarvis", "alfred"]

def iniciar_jarvis():
  print("Inicializando...")

  jarvis_ouvidos = Ouvidos()

  voz.falar("Sistemas online. Ao seu dispor, mestre.")

  while True:
    print("Aguardando comando...", flush=True)

    texto_usuario = jarvis_ouvidos.ouvir()
    if texto_usuario:
      texto_lower = texto_usuario.lower().strip()

      ativou = False
      for palavra in WAKE_WORDS:
        if texto_lower.startswith(palavra):
          ativou = True
          break
      
      if ativou:
        print(f"✅ Comando aceito: {texto_usuario}")
        print("🧠 Processando...")
        texto_final = texto_usuario.replace("Jarvis", "").replace("Alfred", "").strip()

        resposta_jarvis = cerebro.pensar(texto_final)
        print(f"Jarvis: {resposta_jarvis}")
        voz.falar(resposta_jarvis)
      
      else:
        print(f"🔇 Ignorado (Sem wake word): {texto_usuario}")

if __name__ == "__main__":
  iniciar_jarvis()