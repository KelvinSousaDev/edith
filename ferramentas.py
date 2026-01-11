import datetime
import subprocess
from langchain_core.tools import tool
from ddgs import DDGS
import psutil
import pyautogui
import os
import pywhatkit

@tool
def ver_hora():
  """
    Retorna o horário atual do sistema. Use isso quando o usuário perguntar as horas ou a data de hoje.
  """
  hora_atual = datetime.datetime.now()
  hora_formatada = hora_atual.strftime("%H:%M do dia %d/%m/%Y")
  return hora_formatada

@tool
def abrir_programa(nome_programa: str):
  """
    Abre um programa no computador.
    O argumento 'nome_programa' deve ser um destes: 'chrome', 'bloco de notas', 'calculadora', 'spotify'.
  """
  
  programas = {
    "chrome": "start chrome",
    "bloco de notas": "notepad",
    "calculadora": "calc",
    "spotify": "start spotify" # Funciona se estiver instalado na loja/caminho
    }
  
  chave = nome_programa.lower().strip()

  if chave in programas:
    subprocess.Popen(programas[chave], shell=True)
    return f"Abrindo {chave} para o senhor."
  else:
    return f"Desculpe, não sei como abrir '{nome_programa}' ainda."

@tool
def pesquisar_internet(pergunta: str):
  """
      Pesquisa informações na internet.
      Use isso para buscar fatos atuais, notícias, clima ou dados que você não sabe.
  """

  with DDGS() as ddgs:
    resultados = ddgs.text(pergunta, max_results=3)
    resposta = ""
    for resultado in resultados:
      titulo = resultado["title"]
      resumo = resultado["body"]
      frase = f"{titulo} - {resumo} \n"
      resposta += frase
    
    return resposta
  
@tool
def monitorar_sistema():
  """
    Verifica o uso atual do sistema (CPU, Memória RAM e Bateria).
    Use isso quando o usuário perguntar: 'Como está o PC?', 'Uso de CPU', 'Memória' ou 'Bateria'.
  """

  uso_cpu = psutil.cpu_percent(interval=1)
  uso_ram = psutil.virtual_memory().percent

  resposta = f"CPU em {uso_cpu}%. Memória RAM em {uso_ram}%."

  bateria = psutil.sensors_battery()
  if bateria:
    resposta += f"Bateria em {bateria.percent}%"
  else:
    resposta += " Ligado na tomada (Sem bateria)."
  return resposta

@tool
def controlar_midia(comando: str):
  """
    Controla o player de áudio/vídeo que JÁ ESTÁ ABERTO.
    Use APENAS para comandos de controle: 'pausar', 'retomar' (play), 'proxima', 'anterior', 'aumentar', 'diminuir', 'mudo'.
    NÃO use isso para buscar músicas novas.
  """

  teclas = {
    "pausar": "playpause",
    "tocar": "playpause",
    "proxima": "nexttrack",
    "anterior": "prevtrack",
    "aumentar": "volumeup",
    "diminuir": "volumedown",
    "mudo": "volumemute"
  }
  comando_limpo = comando.lower().strip()

  if comando_limpo in teclas:
    pyautogui.press(teclas[comando_limpo])
    return f"Comando de mídia '{comando_limpo}' executado."
  else:
    return f"Comando de mídia '{comando_limpo}' não reconhecido."
  
@tool
def salvar_memoria(texto: str):
  """
    Salva uma informação importante na memória de longo prazo.
    Use isso quando o usuário disser 'anote isso', 'lembre-se que', ou passar uma informação pessoal (senha, nome, gosto).
  """

  if not os.path.exists("memoria"):
    os.makedirs("memoria")

  caminho = "memoria/dados.txt"
  data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

  with open(caminho, "a", encoding="utf-8") as arquivo:
    arquivo.write(f"[{data_hora}] {texto}\n")
  return "Informação salva no banco de dados."

@tool
def ler_memoria():
  """
    Lê todas as anotações salvas na memória de longo prazo.
    Use isso quando o usuário perguntar 'o que eu te pedi para lembrar?', 'qual é a senha?', 'o que você sabe sobre mim?'.
  """

  caminho = "memoria/dados.txt"
  if not os.path.exists(caminho):
    return "Minha memória está vazia por enquanto."
  
  with open(caminho, "r", encoding="utf-8") as arquivo:
    conteudo = arquivo.read()
  return conteudo

@tool
def tocar_youtube(video: str):
  """
    Busca e toca um vídeo ou música NOVA no YouTube.
    Use isso quando o usuário disser: 'toque [nome]', 'ouvir [nome]', 'bota [nome]'.
  """

  pywhatkit.playonyt(video)
  return f"Tocando {video} no YouTube."