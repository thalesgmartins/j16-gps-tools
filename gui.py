"""
gui.py

Interface gráfica para configurar e ler rastreadores J16.
- Importa as libs customizadas para conexão serial;
- Usar customtkinter para contruir o GUI;
"""

from j16tracker import SerialInterface, J16Commands, ResponseParser
import customtkinter as ctk
import serial.tools.list_ports
from PIL import Image

class J16GUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configs de aparência
        self.title("J16 GPS-Tool")
        self.geometry("600x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Cria as variáveis que serão usada pelo app
        self.interface = None

        # Inicialização do Aplicativo
        self.create_widgets()

    def create_widgets(self):
        """
        Cria os elementos do APP:
        - Define o conteúdo de cada elemento
        - Define o posicionamento de cada um dentro da janela;
        - Atribui funções para cada elemento; 
        """

        #
        # Seletor de portas seriais
        #
        # TODO Tratar erros como -> Não ter uma porta serial.
        # TODO Botão de atualizar itens da lista

        # Frame de conexão
        self.port_frame = ctk.CTkFrame(self)
        self.port_frame.pack(pady=10, fill="x", padx=10)

        # Frame interno para centralizar conteúdo (sem cor de fundo)
        self.inner_frame = ctk.CTkFrame(self.port_frame, fg_color="transparent")  
        self.inner_frame.pack(padx=20, pady=10)  # margem lateral para "empurrar" o conteúdo

        # Configura colunas no inner_frame
        for col in range(4):
            self.inner_frame.grid_columnconfigure(col, weight=1)

        self.port_label = ctk.CTkLabel(self.inner_frame, text="Porta serial:")
        self.port_label.grid(row=0, column=0, padx=5, pady=10)

        self.port_combobox = ctk.CTkComboBox(self.inner_frame, values=self.list_serial_ports(), width=180)
        self.port_combobox.grid(row=0, column=1, padx=5, pady=10)

        refresh_icon = ctk.CTkImage(Image.open("icons/refresh.png"), size=(24, 24))
        self.refresh_button = ctk.CTkButton(
            self.inner_frame,
            image=refresh_icon,
            text="",
            width=30,
            height=30,
            fg_color="#555555",
            hover_color="#777777",
            command=self.refresh_ports
        )
        self.refresh_button.grid(row=0, column=2, padx=5, pady=10)

        self.connect_button = ctk.CTkButton(self.inner_frame, text="Conectar", command=self.connect_serial)
        self.connect_button.grid(row=0, column=3, padx=5, pady=10)


        #
        # Botões de comandos rápidos
        #
        # TODO Validar se todos os comandos estão válidos.
        #self.command_frame = ctk.CTkFrame(self)
        #self.command_frame.pack(pady=10, fill="x", padx=10)

        #self.command_frame.grid_columnconfigure(0, weight=1)
        #self.command_frame.grid_columnconfigure(1, weight=1)
        #self.command_frame.grid_columnconfigure(2, weight=1)

        #self.command_label = ctk.CTkLabel(self.command_frame, text="Comandos rápidos:", font=ctk.CTkFont(weight="bold"))
        #self.command_label.grid(row=0, column=0, columnspan=3, pady=5)

        #self.command_get_imei = ctk.CTkButton(self.command_frame, text="Obter IMEI", command=self.get_imei)
        #self.command_get_imei.grid(row=1, column=0, padx=5, pady=5)

        #self.command_get_gps_status = ctk.CTkButton(self.command_frame, text="Status GPS", command=self.get_gps_status)
        #self.command_get_gps_status.grid(row=1, column=1, padx=5, pady=5)

        #self.command_get_device_info = ctk.CTkButton(self.command_frame, text="Info Dispositivo", command=self.get_device_info)
        #self.command_get_device_info.grid(row=1, column=2, padx=5, pady=5)


        #
        # Botões de comandos
        #
        #self.command_set_server = ctk.CTkButton(self.command_frame, text="Setar Servidor", command=self.set_server)
        #self.command_set_server.grid(row=2, column=0, padx=5, pady=5)

        #self.command_set_timezone = ctk.CTkButton(self.command_frame, text="Definir GMT", command=self.set_timezone)
        #self.command_set_timezone.grid(row=2, column=1, padx=5, pady=5)

        #self.command_enable_tracking = ctk.CTkButton(self.command_frame, text="Modo Rastreamento", command=self.enable_tracking)
        #self.command_enable_tracking.grid(row=2, column=2, padx=5, pady=5)

        # Comando personalizado

        self.custom_command_frame = ctk.CTkFrame(self)
        self.custom_command_frame.pack(pady=10, fill="x", padx=10)

        self.custom_command_frame.grid_columnconfigure(0, weight=1)  # Ocupa o máximo possível
        self.custom_command_frame.grid_columnconfigure(1, weight=0)  # Tamanho fixo pro botão

        self.command_entry = ctk.CTkEntry(self.custom_command_frame, placeholder_text="Digite um comando AT personalizado")
        self.command_entry.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        self.send_button = ctk.CTkButton(self.custom_command_frame, text="Enviar Comando", command=self.send_custom_command)
        self.send_button.grid(row=0, column=1, padx=5, pady=10)

        # Caixa de resposta
        self.response_box = ctk.CTkTextbox(self, height=150)
        self.response_box.pack(padx=10, pady=10, fill="both", expand=True)

    def list_serial_ports(self):
        """
        list_serial_ports():
         - Usa "list_ports.comports()" para descobrir todas as portas COM do dispositivo;
         - Cria uma instância temporária de serialInterface e tenta conectar;
         - Se conectar, envia "AT" e aguarda "OK";
         - Adiciona todos dispositivos válidos em um array;
         - Retorna o Array
        """

        # Pega todas as portas COM da máquina
        ports = serial.tools.list_ports.comports()

        # Filtrando apenas as portas que responderem a um comando AT
        valid_ports = []

        for port in ports:
            try:
                ser = SerialInterface(port=port.device, timeout=0.1)
                ser.send_command("AT")
                resposta = ser.read_response()
                ser.close()

                if "OK" in resposta:
                    valid_ports.append(port.device)
            except Exception:
                pass 

        return valid_ports
    
    def refresh_ports(self):
        ports = self.list_serial_ports()
        self.port_combobox.configure(values=ports)
        if ports:
            self.port_combobox.set(ports[0])  # Seleciona a primeira automaticamente
        else:
            self.port_combobox.set("")  # Limpa se não tiver nenhuma

    def connect_serial(self):
        if not self.interface:
            port = self.port_combobox.get()

            if port:
                try:
                    self.interface = SerialInterface(port)
                    self.response_box.insert("end", f"[OK] Conectado a {port}\n")

                    self.connect_button.configure(
                        text="Desconectar",
                        fg_color="#AA3333",
                        hover_color="#CC4444",
                        command=self.disconnect_serial
                    )

                except Exception as e:
                    self.response_box.insert("end", f"[ERRO] {e}\n")

    def disconnect_serial(self):
        if self.interface:
            self.interface.close()
            self.interface = None
            self.response_box.insert("end", "[INFO] Desconectado.\n")

            # Volta o botão ao estado original
            self.connect_button.configure(
                text="Conectar",
                fg_color="#2fa572",
                hover_color="#247f59",
                command=self.connect_serial
            )

    def get_imei(self):
        if self.interface:
            self.interface.send_command(J16Commands.get_imei())
            response = self.interface.read_response()
            imei = ResponseParser.parse_imei(response)
            self.response_box.insert("end", f"IMEI: {imei}\n")

    def get_gps_status(self):
        if self.interface:
            self.interface.send_command(J16Commands.get_gps_status())
            response = self.interface.read_response()
            status = ResponseParser.parse_gps_status(response)
            self.response_box.insert("end", f"GPS: {status}\n")

    def get_device_info(self):
        pass

    def set_server(self):
        pass

    def set_timezone(self):
        pass

    def enable_tracking(self):
        pass

    def send_custom_command(self):
        if not self.interface:
            self.response_box.insert("end", "[ERRO] Conecte a uma porta serial primeiro.\n")
            return

        command = self.command_entry.get().strip()
        if not command:
            self.response_box.insert("end", "[ERRO] Comando vazio.\n")
            return

        try:
            self.interface.send_command(command)
            response = self.interface.read_response()
            self.response_box.insert("end", f"> {command}\n{response.strip()}\n")
        except Exception as e:
            self.response_box.insert("end", f"[ERRO] Falha ao enviar comando: {e}\n")

if __name__ == "__main__":
    """
    Permite executar o arquivo diretamente, sem precisar ser chamado pela main.py
    """

    # Declara a classe do GUI e chama o loop do app.
    app = J16GUI()
    app.mainloop()
