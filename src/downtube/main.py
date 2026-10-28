import downloaders


def init():
    print("{:=^100}".format(" DownTube ") + "\n")
    print("1 - Baixar música")
    print("2 - Baixar playlist")
    print("3 - Baixar Vídeo")
    print("0 - Sair\n")
    print("=" * 100 + "\n")


def main():
    acoes = {
        "1": downloaders.baixar_musica,
        "2": downloaders.baixar_playlist,
        "3": downloaders.baixar_video,
    }

    downloaders.limpar_tela()
    while True:
        init()
        opt = input("Digite a opção desejada: ").strip()

        if opt == "0":
            break
        elif opt in acoes:
            acoes[opt]()
            downloaders.limpar_tela()
        else:
            print("Opção inválida.\n\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nSaindo...")
