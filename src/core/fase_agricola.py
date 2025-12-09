"""
Módulo para cálculos da fase agrícola
Calcula emissões de GEE da produção/colheita de biomassa
"""

from typing import Dict, Any


class FaseAgricola:
    """Classe para cálculos da fase agrícola"""

    def __init__(self, fatores: Dict[str, Any]):
        """
        Inicializa com fatores de emissão.

        Args:
            fatores: Dicionário com fatores de emissão
        """
        self.fatores = fatores

    def calcular_emissoes(self, dados: Dict[str, Any]) -> Dict[str, float]:
        """
        Calcula as emissões da fase agrícola.

        Fórmula:
        Emissões = (Biomassa_kg × Fator_biomassa) +
                   (Fertilizantes_kg × Fator_fertilizante) +
                   (Pesticidas_kg × Fator_pesticida) +
                   (Distância_km × Fator_transporte_rodoviario × Biomassa_kg / 1000) +
                   LUC_dLUC_opcional

        Args:
            dados: Dicionário com dados de entrada:
                - quantidade_biomassa_kg: Quantidade de biomassa em kg
                - distancia_transporte_km: Distância de transporte em km
                - uso_fertilizantes_kg: Uso de fertilizantes em kg
                - uso_pesticidas_kg: Uso de pesticidas em kg
                - luc_dluc_opcional_kg_co2: LUC/dLUC opcional em kg CO2 (padrão: 0)
                - fator_biomassa_agricola: Fator de emissão da biomassa em gCO2/kg

        Returns:
            Dicionário com:
                - emissoes_kg_co2: Emissões totais em kg CO2
                - detalhamento: Detalhamento por componente
        """
        # Extrair dados de entrada
        biomassa_kg = dados.get('quantidade_biomassa_kg', 0)
        distancia_km = dados.get('distancia_transporte_km', 0)
        fertilizantes_kg = dados.get('uso_fertilizantes_kg', 0)
        pesticidas_kg = dados.get('uso_pesticidas_kg', 0)
        luc_dluc_kg_co2 = dados.get('luc_dluc_opcional_kg_co2', 0)
        fator_biomassa = dados.get('fator_biomassa_agricola', 100.0)  # gCO2/kg

        # Extrair fatores de emissão
        fator_fertilizante = self.fatores.get('fator_fertilizante_n', {}).get('valor', 6540.0)  # gCO2/kg
        fator_pesticida = self.fatores.get('fator_pesticida', {}).get('valor', 10000.0)  # gCO2/kg
        fator_transporte = self.fatores.get('fator_transporte_rodoviario', {}).get('valor', 62.0)  # gCO2/tkm

        # Cálculos de emissões (em kg CO2)
        emissoes_biomassa = (biomassa_kg * fator_biomassa) / 1000  # Converter gCO2 para kgCO2
        emissoes_fertilizantes = (fertilizantes_kg * fator_fertilizante) / 1000
        emissoes_pesticidas = (pesticidas_kg * fator_pesticida) / 1000

        # Transporte: gCO2/tkm × tkm = gCO2 → converter para kgCO2
        # tkm = (biomassa_kg / 1000) × distancia_km
        emissoes_transporte = (fator_transporte * distancia_km * biomassa_kg / 1000) / 1000

        emissoes_luc = luc_dluc_kg_co2

        # Total
        emissoes_totais = (
            emissoes_biomassa +
            emissoes_fertilizantes +
            emissoes_pesticidas +
            emissoes_transporte +
            emissoes_luc
        )

        return {
            'emissoes_kg_co2': emissoes_totais,
            'detalhamento': {
                'biomassa': emissoes_biomassa,
                'fertilizantes': emissoes_fertilizantes,
                'pesticidas': emissoes_pesticidas,
                'transporte': emissoes_transporte,
                'luc_dluc': emissoes_luc
            }
        }
