"""
Módulo para cálculos da fase de distribuição
Calcula emissões de GEE do transporte da biomassa processada até o consumidor final
"""

from typing import Dict, Any


class FaseDistribuicao:
    """Classe para cálculos da fase de distribuição"""

    def __init__(self, fatores: Dict[str, Any]):
        """
        Inicializa com fatores de emissão.

        Args:
            fatores: Dicionário com fatores de emissão
        """
        self.fatores = fatores

    def calcular_emissoes(self, dados: Dict[str, Any]) -> Dict[str, float]:
        """
        Calcula as emissões da fase de distribuição.

        Fórmula:
        Emissões = Distância_km × Fator_modal_transporte × Biomassa_kg / 1000

        Args:
            dados: Dicionário com dados de entrada:
                - modal_transporte: Modal de transporte (rodoviario, maritimo, ferroviario)
                - distancia_km: Distância de transporte em km
                - quantidade_biomassa_kg: Quantidade de biomassa em kg

        Returns:
            Dicionário com:
                - emissoes_kg_co2: Emissões totais em kg CO2
                - detalhamento: Detalhamento por componente
        """
        # Extrair dados de entrada
        modal = dados.get('modal_transporte', 'rodoviario')
        distancia = dados.get('distancia_km', 0)
        biomassa_kg = dados.get('quantidade_biomassa_kg', 0)

        # Mapear modal para fator de emissão
        fatores_modal = {
            'rodoviario': self.fatores.get('fator_transporte_rodoviario', {}).get('valor', 62.0),  # gCO2/tkm
            'maritimo': self.fatores.get('fator_transporte_maritimo', {}).get('valor', 8.5),  # gCO2/tkm
            'ferroviario': self.fatores.get('fator_transporte_ferroviario', {}).get('valor', 22.0)  # gCO2/tkm
        }

        fator_transporte = fatores_modal.get(modal, 62.0)

        # Cálculo de emissões
        # tkm = (biomassa_kg / 1000) × distancia_km
        # emissoes_gCO2 = tkm × fator_transporte
        # emissoes_kgCO2 = emissoes_gCO2 / 1000
        emissoes_transporte = (fator_transporte * distancia * biomassa_kg / 1000) / 1000

        return {
            'emissoes_kg_co2': emissoes_transporte,
            'detalhamento': {
                'transporte': emissoes_transporte,
                'modal': modal,
                'distancia_km': distancia
            }
        }
