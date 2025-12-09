"""
Módulo para cálculos da fase de uso
Calcula emissões de GEE da combustão da biomassa para geração de energia
"""

from typing import Dict, Any


class FaseUso:
    """Classe para cálculos da fase de uso"""

    def __init__(self, fatores: Dict[str, Any]):
        """
        Inicializa com fatores de emissão.

        Args:
            fatores: Dicionário com fatores de emissão
        """
        self.fatores = fatores

    def calcular_emissoes(self, dados: Dict[str, Any]) -> Dict[str, float]:
        """
        Calcula as emissões da fase de uso (combustão).

        Fórmula:
        Emissões = Biomassa_kg × PCI × Fator_combustao

        IMPORTANTE: Seguindo a metodologia RenovaCalc e IPCC, as emissões biogênicas
        de CO2 da combustão são consideradas neutras (CF = 0) sob condições de
        regeneração em estado estacionário.

        Args:
            dados: Dicionário com dados de entrada:
                - quantidade_biomassa_kg: Quantidade de biomassa em kg
                - pci: Poder Calorífico Inferior em MJ/kg
                - tipo_combustao: Tipo de combustão (caldeira, fornalha, outro)

        Returns:
            Dicionário com:
                - emissoes_kg_co2: Emissões totais em kg CO2 (normalmente 0 para biomassa)
                - detalhamento: Detalhamento por componente
                - emissoes_biogenicas_kg_co2: Emissões biogênicas (reportadas separadamente)
        """
        # Extrair dados de entrada
        biomassa_kg = dados.get('quantidade_biomassa_kg', 0)
        pci = dados.get('pci', 18.0)  # MJ/kg
        tipo_combustao = dados.get('tipo_combustao', 'caldeira')

        # Fator de combustão (CF = 0 para biomassa, conforme metodologia)
        fator_combustao = self.fatores.get('fator_combustao', {}).get('valor', 0.0)  # gCO2/MJ

        # Emissões calculadas (normalmente 0 para biomassa)
        emissoes_combustao = (biomassa_kg * pci * fator_combustao) / 1000

        # Emissões biogênicas (reportadas separadamente, mas não contabilizadas no total)
        # Assumindo ~1840 gCO2/kg de biomassa (baseado em composição média de biomassa)
        emissoes_biogenicas = biomassa_kg * 1.84  # kg CO2

        return {
            'emissoes_kg_co2': emissoes_combustao,  # Normalmente 0
            'detalhamento': {
                'combustao': emissoes_combustao,
                'tipo_combustao': tipo_combustao,
                'energia_gerada_mj': biomassa_kg * pci
            },
            'emissoes_biogenicas_kg_co2': emissoes_biogenicas  # Reportadas separadamente
        }
