import os
import sys
from yt_dlp import YoutubeDL
import config
import downloaders

# Adiciona o diretório atual ao path para permitir importação dos módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Tela inicial

def init():
    print("{:=^100}".format(" DownTube ")+"\n")
    print("1 - Baixar música")
    print("2 - Baixar playlist")
    print("3 - Baixar Vídeo")
    print("0 - Sair\n")
    print("="*100+"\n")

# Função padrão para limpar a tela
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

# Loop para fazer o encaminhamento das funções
limpar_tela()
while True:
    
    init()
    
    opt = input("Digite a opção desejada: ")
    
    if opt == "1":
        downloaders.baixar_musica()
    elif opt == "2":
        downloaders.baixar_playlist()
    elif opt == "3":
        downloaders.baixar_video()
    elif opt == "0":
        break
    else:
        limpar_tela()
        print("Opção inválida.\n\n")