# j16tracker/commands.py

# J16Commands
#   Comandos AT utilizados para configurar e consultar informações do rastreador J16,
#   como IMEI, APN, status do GPS e localização.
class J16Commands:
    @staticmethod
    def get_imei():
        return "AT+GSN"

    @staticmethod
    def set_apn(apn: str):
        return f'AT+CGDCONT=1,"IP","{apn}"'

    @staticmethod
    def reboot():
        return "AT+RESET"

    @staticmethod
    def get_gps_status():
        return "AT+CGPSSTATUS?"

    @staticmethod
    def get_location():
        return "AT+CGPSINF=0"