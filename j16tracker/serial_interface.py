import serial
from .config import SERIAL_CONFIG

# SerialInterface
#   - Inicia a comunicação Serial com o rastreador.
#   - Faz a leitura e tratamento dos dados.
#   - Envia os comandos para o Rastreador.
class SerialInterface:
    def __init__(self, port: str, baudrate: int = SERIAL_CONFIG["baudrate"]):
        self.ser = serial.Serial(port, baudrate, timeout=SERIAL_CONFIG["timeout"])
        print(f"[INFO] Conectado à porta {port} @ {baudrate}bps")

    def send_command(self, command: str):
        if not command.endswith('\r'):
            command += '\r'
        self.ser.write(command.encode())
        print(f"[TX] {command.strip()}")

    def read_response(self) -> str:
        response = self.ser.read_until(b'OK\r\n').decode(errors='ignore')
        print(f"[RX] {response.strip()}")
        return response

    def close(self):
        self.ser.close()
        print("[INFO] Porta serial fechada")