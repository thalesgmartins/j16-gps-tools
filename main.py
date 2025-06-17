
"""
main.py

Função principal do código: 
- Usa a lib argparse para receber parâmetros;
- Permite rodar em modo CLI ou GUI (GUI por padrão);
- Usa TKinter para construir a GUI.
"""

import argparse

def run_cli():
    # TODO: Modo CLI não implementado ainda.
    print("Modo CLI ainda não implementado.")

def run_gui():
    # Importa a lib customizada
    from gui import J16GUI

    # Faz a instância do app e chama o loop do programa.
    app = J16GUI()
    app.mainloop()

if __name__ == "__main__":

    # Configurando os argumetnos esperados
    parser = argparse.ArgumentParser(description="J16 GPS-Tools - Ferramenta de comunicação com rastreador J16")
    parser.add_argument("--mode", choices=["cli", "gui"], default="gui", help="Modo de execução")
    args = parser.parse_args()

    # Executando o programa de acordo com o argumento passado.
    if args.mode == "gui":
        run_gui()
    else:
        run_cli()