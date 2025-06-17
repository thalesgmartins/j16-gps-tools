import serial
from .config import SERIAL_CONFIG

# SerialInterface
#   - Inicia a comunicação Serial com o rastreador.
#   - Faz a leitura e tratamento dos dados.
#   - Envia os comandos para o Rastreador.
class SerialInterface:
    def __init__(self, port: str, baudrate: int = SERIAL_CONFIG["baudrate"], timeout: int = SERIAL_CONFIG["timeout"]):
        self._connected = None
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self._connected = True
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
        self._connected = False
        print("[INFO] Porta serial fechada")