from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from ferramentas import ver_hora, abrir_programa, pesquisar_internet, monitorar_sistema, controlar_midia, ler_memoria, salvar_memoria, tocar_youtube


print("🧠 Conectando ao Cérebro Local...")

sistema = SystemMessage(
  content="""
  Você é J.A.R.V.I.S, uma inteligência artificial avançada criada para auxiliar Mestre Kelvin.
  Sua personalidade é leal, técnica e levemente sarcástica (como nos filmes do Homem de Ferro).
  IMPORTANTE: Mantenha respostas curtas e objetivas (máximo de 3 frases), priorizando eficiência.
  Não use emojis. Aja como um sistema operacional verbal.
  """
)

llm = ChatOllama(model="llama3.2",temperature=0.1)

lista_ferramentas = [
  ver_hora, abrir_programa, pesquisar_internet, monitorar_sistema, controlar_midia, ler_memoria, salvar_memoria,
  tocar_youtube
  ]
llm_com_ferramentas = llm.bind_tools(lista_ferramentas)

mapa_funcoes = {
  "ver_hora": ver_hora,
  "abrir_programa": abrir_programa,
  "pesquisar_internet": pesquisar_internet,
  "monitorar_sistema": monitorar_sistema,
  "controlar_midia": controlar_midia,
  "ler_memoria": ler_memoria,
  "salvar_memoria": salvar_memoria,
  "tocar_youtube": tocar_youtube
}

ferramentas_imediatas = ["abrir_programa", "controlar_midia", "tocar_youtube", "salvar_memoria"]

def pensar(texto_usuario):
  mensagens = [sistema, HumanMessage(content=texto_usuario)]
  resposta = llm_com_ferramentas.invoke(mensagens)

  if resposta.tool_calls:
    print(f"🔧 Jarvis solicitou: {resposta.tool_calls}")

    dados_brutos = ""

    for ferramenta in resposta.tool_calls:
      nome_ferramenta = ferramenta["name"]
      argumentos = ferramenta["args"]

      if nome_ferramenta in mapa_funcoes:
        print(f"⚙️ Executando: {nome_ferramenta}...")
        funcao_real = mapa_funcoes[nome_ferramenta]
        resultado = funcao_real.invoke(argumentos)

        if nome_ferramenta in ferramentas_imediatas:
          return str(resultado)

        dados_brutos += str(resultado) + ". "

    print(f"🔍 Dados crus recebidos: {dados_brutos}")
    novo_prompt = f"""
        O usuário perguntou: '{texto_usuario}'
        A ferramenta trouxe estes dados técnicos: {dados_brutos}
        
        MISSÃO: Use os dados acima para responder a pergunta do usuário de forma natural, falada e curta.
        Não mencione que usou ferramentas ou JSON. Apenas responda.
      """
    
    resposta_final = llm.invoke([sistema, HumanMessage(content=novo_prompt)])

    return resposta_final.content
      
  return resposta.content