# j16tracker/parser.py

import re

# ResponsParser
#   Responsável por interpretar as respostas brutas enviadas pelo rastreador J16,
#   extraindo informações úteis como IMEI, status do GPS e localização em formato estruturado.
class ResponseParser:
    @staticmethod
    def parse_imei(response: str) -> str:
        match = re.search(r'(\d{15})', response)
        return match.group(1) if match else "IMEI não encontrado"

    @staticmethod
    def parse_gps_status(response: str) -> str:
        if "Location 3D Fix" in response:
            return "GPS fixado"
        elif "Not Fix" in response:
            return "Sem sinal de GPS"
        return "Status desconhecido"

    @staticmethod
    def parse_location(response: str) -> dict:
        # Exemplo fictício: +CGPSINF: 0,22.5726,88.3639,...
        parts = response.split(',')
        try:
            return {"latitude": float(parts[1]), "longitude": float(parts[2])}
        except (IndexError, ValueError):
            return {"latitude": None, "longitude": None}
