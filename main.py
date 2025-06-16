# main.py
#   Exemplo de uso da biblioteca para enviar comandos AT para um rastreador J16, printando respostas na Serial.

from j16tracker import SerialInterface, J16Commands

SERIAL_PORT = "/dev/ttyUSB2"

def main():

    serial = SerialInterface(SERIAL_PORT)

    try:
        serial.send_command(J16Commands.get_imei())

        resposta = serial.read_response()
        print("Resposta dos rastreador: ", resposta)
    finally:
        serial.close()


if __name__ == '__main__':
    main()