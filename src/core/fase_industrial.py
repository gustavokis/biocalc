"""
Módulo para cálculos da fase industrial
Calcula emissões de GEE do processamento da biomassa em pellets/briquetes
"""

from typing import Dict, Any


class FaseIndustrial:
    """Classe para cálculos da fase industrial"""

    def __init__(self, fatores: Dict[str, Any]):
        """
        Inicializa com fatores de emissão.

        Args:
            fatores: Dicionário com fatores de emissão
        """
        self.fatores = fatores

    def calcular_emissoes(self, dados: Dict[str, Any]) -> Dict[str, float]:
        """
        Calcula as emissões da fase industrial.

        Fórmula:
        Emissões = (Energia_elétrica_kWh × Fator_eletricidade) +
                   (Energia_térmica_MJ × Fator_energia_termica) +
                   (Água_m3 × Fator_agua)

        Args:
            dados: Dicionário com dados de entrada:
                - energia_eletrica_kwh: Consumo de energia elétrica em kWh
                - energia_termica_mj: Consumo de energia térmica em MJ
                - agua_m3: Consumo de água em m³

        Returns:
            Dicionário com:
                - emissoes_kg_co2: Emissões totais em kg CO2
                - detalhamento: Detalhamento por componente
        """
        # Extrair dados de entrada
        energia_eletrica = dados.get('energia_eletrica_kwh', 0)
        energia_termica = dados.get('energia_termica_mj', 0)
        agua = dados.get('agua_m3', 0)

        # Extrair fatores de emissão
        fator_eletricidade = self.fatores.get('fator_eletricidade_br', {}).get('valor', 95.0)  # gCO2/kWh
        fator_energia_termica = self.fatores.get('fator_diesel', {}).get('valor', 2680.0) / 38.0  # gCO2/MJ (diesel ~38 MJ/L)
        fator_agua = self.fatores.get('fator_agua', {}).get('valor', 0.36)  # gCO2/m3

        # Cálculos de emissões (converter gCO2 para kgCO2)
        emissoes_eletricidade = (energia_eletrica * fator_eletricidade) / 1000
        emissoes_termica = (energia_termica * fator_energia_termica) / 1000
        emissoes_agua = (agua * fator_agua) / 1000

        # Total
        emissoes_totais = (
            emissoes_eletricidade +
            emissoes_termica +
            emissoes_agua
        )

        return {
            'emissoes_kg_co2': emissoes_totais,
            'detalhamento': {
                'energia_eletrica': emissoes_eletricidade,
                'energia_termica': emissoes_termica,
                'agua': emissoes_agua
            }
        }
