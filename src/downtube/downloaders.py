import os
import sys
from yt_dlp import YoutubeDL
import config


# Função padrão para limpar a tela
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

# Função que executa o download de vídeos
def baixar_video():
    while True:
        limpar_tela()

        # Define o link do vídeo a ser baixado
        print("{:=^100}".format(" Baixar Vídeo ")+"\n")
        link_video = input("Qual o link do vídeo a ser baixado?: ")

        # Cópia temporária das configs pra extração das informações do vídeo
        opcoes_extracao = config.opcoes_base_video.copy()

        # Coleta as informações do vídeo e lista as resoluções disponíveis para o usuário escolher
        try:
            with YoutubeDL(opcoes_extracao) as ydl:
                infos = ydl.extract_info(link_video, download=False)
            
            formatos = infos.get("formats", [])
            opcoes_video = []

            resolucoes_vistas = set()

            # Checa se o vídeo tem formatos válidos e registra suas resoluções
            for  f in formatos:
                if f.get('vcodec') != 'none' and f.get('height'):
                    res_height = f.get('height')
                    ext = f.get('ext', 'mp4')
                    format_id = f.get('format_id')
                    note = f.get('format_note', '')

                    if res_height not in resolucoes_vistas:
                        resolucoes_vistas.add(res_height)
                        opcoes_video.append({
                            'id': format_id,
                            'res': f"{res_height}p",
                            'ext': ext,
                            'note': note
                        })

            # Organiza as resoluões em ordem da menor pra maior
            opcoes_video = sorted(opcoes_video, key=lambda x: int(x['res'].replace('p', '')))

            if not opcoes_video:
                print("Nenhuma resolução de vídeo encontrada!")
                input("Pressione ENTER para tentar novamente...")
                continue

            # Exibe as resoluções encontradas e pede a escolha de uma delas
            limpar_tela()
            print("{:=^100}".format(f" Resolução "))
            for i, opt in enumerate(opcoes_video, start=1):
                print(f"[{i}] {opt['res']} ({opt['ext']}) - {opt['note']}")
            print("[0] Cancelar\n")

            escolha = input("Qual a resolução desejada?: ")

            if escolha == "0":
                limpar_tela()
                return
            idx = int(escolha)-1
            if idx < 0 or idx >= len(opcoes_video):
                print("Opção inválida.")
                input("\nPressione ENTER para continuar...")
                continue

            # Define a opção escolhida pelo usuário
            formato_escolhido = opcoes_video[idx]['id']

            # Faz uma cópia das opções padrão para download de vídeos
            opcoes_download = config.opcoes_base_video.copy()

            # Define o download do formato/resolução escolhido + o melhor áudio e juntar no final
            opcoes_download["format"] = f"{formato_escolhido}+bestaudio/best"

            limpar_tela()
            print(f"Baixando em {opcoes_video[idx]['res']}...\n")
            with YoutubeDL(opcoes_download) as ydl:
                ydl.download([link_video])

        # Caso ocorra algum erro no processo, informa o erro e da continuidade
        except Exception as e:
            print(f"Ocorreu um erro ao processar o vídeo: {e}")
            input("\nPressione ENTER para continuar...")
            continue

        limpar_tela()

        # Tela de encerramento para download de vídeos
        while True:
            print("{:=^100}".format(" Baixar Vídeo ")+"\n")
            print("Vídeo baixado com sucesso!\n")
            print("="*100+"\n")
            print("1 - Voltar")
            print("2 - Baixar outro vídeo\n")
            finish_opt = input("Escolha uma opção: ")
            if finish_opt == "2":
                break
            elif finish_opt == "1":
                limpar_tela()
                return
            else:
                limpar_tela()
                print("opção inválida\n")

# Função que executa o download de músicas
def baixar_musica():
    while True:
        limpar_tela()

        # Define o link da música a ser baixado
        print("{:=^100}".format(" Baixar Música ")+"\n")
        link_musica = input("Qual o link da música a ser baixada?: ")

        # Faz uma cópia das configurações para música padrão 
        opcoes = config.opcoes_base_audio.copy()

        # Chama o yt_dlp e baixa o vídeo
        with YoutubeDL(opcoes) as ydl:
            ydl.download([link_musica])
        limpar_tela()

        # Tela de encerramento para download de músicas
        while True:
            print("{:=^100}".format(" Baixar Música ")+"\n")
            print("Música baixada com sucesso!\n")
            print("="*100+"\n")
            print("1 - Voltar")
            print("2 - Baixar outra música\n")
            finish_opt = input("Escolha uma opção: ")
            if finish_opt == "2":
                break
            elif finish_opt == "1":
                limpar_tela()
                return
            else:
                limpar_tela()
                print("opção inválida\n")

# Função que executa o download de playlists
def baixar_playlist():
    while True:
        limpar_tela()

        # Define o link da playlist a ser baixada
        print("{:=^100}".format(" Baixar Playlist ")+"\n")
        link_playlist = input("Qual o link da playlist a ser baixada?: ")

        # Faz uma cópia das configurações padrão de download de música (playlist usa as mesmas, apenas com uma modificação do caminho)
        opcoes = config.opcoes_base_audio.copy()
        opcoes["outtmpl"] = os.path.join(
            config.pastaMusica,
            "%(playlist_title)s",
            "%(playlist_index)02d - %(title)s.%(ext)s"
        )
        opcoes["ignoreerrors"] = True
        
        # Chama o yt_dlp e baixa a playlist
        with YoutubeDL(opcoes) as ydl:
            ydl.download([link_playlist])
        limpar_tela()

        # Tela final do download de playlists
        while True:
            print("{:=^100}".format(" Baixar Playlist ")+"\n")
            print("Playlist baixada com sucesso!\n")
            print("="*100+"\n")
            print("1 - Voltar")
            print("2 - Baixar outra playlist\n")
            finish_opt = input("Escolha uma opção: ")

            if finish_opt == "2":
                break
            elif finish_opt == "1":
                limpar_tela()
                return
            else:
                limpar_tela()
                print("opção inválida\n")