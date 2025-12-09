"""
Motor de cálculo principal da BioCalc
Orquestra as 4 fases e calcula intensidade de carbono total e NEEA
"""

from typing import Dict, Any
import pandas as pd
import json
import sys
import os

# Adicionar o diretório pai ao path para permitir imports
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from src.core.fase_agricola import FaseAgricola
    from src.core.fase_industrial import FaseIndustrial
    from src.core.fase_distribuicao import FaseDistribuicao
    from src.core.fase_uso import FaseUso
else:
    from .fase_agricola import FaseAgricola
    from .fase_industrial import FaseIndustrial
    from .fase_distribuicao import FaseDistribuicao
    from .fase_uso import FaseUso


class CalculadoraBioCalc:
    """Calculadora principal para intensidade de carbono de biocombustíveis sólidos"""

    def __init__(self, caminho_fatores: str = "data/fatores.csv",
                 caminho_biomassas: str = "data/biomasses_preset.json"):
        """
        Inicializa a calculadora.

        Args:
            caminho_fatores: Caminho para o arquivo CSV de fatores de emissão
            caminho_biomassas: Caminho para o arquivo JSON de biomassas preset
        """
        # Carregar fatores de emissão
        self.fatores = self._carregar_fatores(caminho_fatores)

        # Carregar biomassas preset
        self.biomassas = self._carregar_biomassas(caminho_biomassas)

        # Inicializar calculadoras de cada fase
        self.fase_agricola = FaseAgricola(self.fatores)
        self.fase_industrial = FaseIndustrial(self.fatores)
        self.fase_distribuicao = FaseDistribuicao(self.fatores)
        self.fase_uso = FaseUso(self.fatores)

    def _carregar_fatores(self, caminho: str) -> Dict[str, Any]:
        """Carrega fatores de emissão do arquivo CSV"""
        df = pd.read_csv(caminho)
        fatores = {}
        for _, row in df.iterrows():
            fatores[row['parametro']] = {
                'valor': row['valor'],
                'unidade': row['unidade'],
                'fonte': row['fonte']
            }
        return fatores

    def _carregar_biomassas(self, caminho: str) -> Dict[str, Any]:
        """Carrega dados de biomassas preset do arquivo JSON"""
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_biomassa_info(self, nome_biomassa: str) -> Dict[str, Any]:
        """
        Retorna informações sobre uma biomassa preset.

        Args:
            nome_biomassa: Nome da biomassa (amendoim, pinus, eucalipto)

        Returns:
            Dicionário com informações da biomassa
        """
        if nome_biomassa not in self.biomassas:
            raise ValueError(f"Biomassa '{nome_biomassa}' não encontrada. "
                           f"Opções disponíveis: {list(self.biomassas.keys())}")
        return self.biomassas[nome_biomassa]

    def calcular_intensidade_carbono(self, dados_entrada: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula a intensidade de carbono total do biocombustível.

        Args:
            dados_entrada: Dicionário com todos os dados de entrada:
                - biomassa: Nome da biomassa (amendoim, pinus, eucalipto)
                - fase_agricola: Dados da fase agrícola
                - fase_industrial: Dados da fase industrial
                - fase_distribuicao: Dados da fase distribuição
                - fase_uso: Dados da fase uso

        Returns:
            Dicionário com resultados completos:
                - resultados_por_fase: Emissões por fase
                - emissoes_totais_kg_co2: Emissões totais em kg CO2
                - energia_total_mj: Energia total produzida em MJ
                - intensidade_carbono_g_co2_mj: Intensidade de carbono em gCO2/MJ
                - neea: NEEA (Eficiência Energético-Ambiental)
                - comparacao_fossil: Comparação com combustível fóssil
        """
        # Obter informações da biomassa
        nome_biomassa = dados_entrada.get('biomassa')
        if not nome_biomassa:
            raise ValueError("Nome da biomassa não fornecido")

        biomassa_info = self.get_biomassa_info(nome_biomassa)

        # Preparar dados para cada fase
        dados_agricola = dados_entrada.get('fase_agricola', {})
        dados_agricola['fator_biomassa_agricola'] = biomassa_info['fator_biomassa_agricola']

        dados_industrial = dados_entrada.get('fase_industrial', {})

        dados_distribuicao = dados_entrada.get('fase_distribuicao', {})
        dados_distribuicao['quantidade_biomassa_kg'] = dados_agricola.get('quantidade_biomassa_kg', 0)

        dados_uso = dados_entrada.get('fase_uso', {})
        dados_uso['quantidade_biomassa_kg'] = dados_agricola.get('quantidade_biomassa_kg', 0)
        dados_uso['pci'] = biomassa_info['pci']

        # Calcular emissões de cada fase
        resultado_agricola = self.fase_agricola.calcular_emissoes(dados_agricola)
        resultado_industrial = self.fase_industrial.calcular_emissoes(dados_industrial)
        resultado_distribuicao = self.fase_distribuicao.calcular_emissoes(dados_distribuicao)
        resultado_uso = self.fase_uso.calcular_emissoes(dados_uso)

        # Calcular emissões totais
        emissoes_totais = (
            resultado_agricola['emissoes_kg_co2'] +
            resultado_industrial['emissoes_kg_co2'] +
            resultado_distribuicao['emissoes_kg_co2'] +
            resultado_uso['emissoes_kg_co2']
        )

        # Calcular energia total produzida
        energia_total_mj = dados_uso['quantidade_biomassa_kg'] * biomassa_info['pci']

        # Calcular intensidade de carbono (gCO2/MJ)
        if energia_total_mj > 0:
            intensidade_carbono = (emissoes_totais * 1000) / energia_total_mj  # Converter kgCO2 para gCO2
        else:
            intensidade_carbono = 0

        # Calcular NEEA (Eficiência Energético-Ambiental)
        ci_fossil = self.fatores.get('ci_fossil_referencia', {}).get('valor', 85.0)  # gCO2/MJ
        neea = ci_fossil - intensidade_carbono

        # Calcular percentuais por fase
        percentuais = {}
        if emissoes_totais > 0:
            percentuais = {
                'agricola': (resultado_agricola['emissoes_kg_co2'] / emissoes_totais) * 100,
                'industrial': (resultado_industrial['emissoes_kg_co2'] / emissoes_totais) * 100,
                'distribuicao': (resultado_distribuicao['emissoes_kg_co2'] / emissoes_totais) * 100,
                'uso': (resultado_uso['emissoes_kg_co2'] / emissoes_totais) * 100
            }
        else:
            percentuais = {
                'agricola': 0,
                'industrial': 0,
                'distribuicao': 0,
                'uso': 0
            }

        # Calcular redução percentual em relação ao fóssil
        if ci_fossil > 0:
            reducao_percentual = (neea / ci_fossil) * 100
        else:
            reducao_percentual = 0

        return {
            'biomassa': nome_biomassa,
            'biomassa_info': biomassa_info,
            'resultados_por_fase': {
                'agricola': {
                    'emissoes_kg_co2': resultado_agricola['emissoes_kg_co2'],
                    'percentual': percentuais['agricola'],
                    'detalhamento': resultado_agricola['detalhamento']
                },
                'industrial': {
                    'emissoes_kg_co2': resultado_industrial['emissoes_kg_co2'],
                    'percentual': percentuais['industrial'],
                    'detalhamento': resultado_industrial['detalhamento']
                },
                'distribuicao': {
                    'emissoes_kg_co2': resultado_distribuicao['emissoes_kg_co2'],
                    'percentual': percentuais['distribuicao'],
                    'detalhamento': resultado_distribuicao['detalhamento']
                },
                'uso': {
                    'emissoes_kg_co2': resultado_uso['emissoes_kg_co2'],
                    'percentual': percentuais['uso'],
                    'detalhamento': resultado_uso['detalhamento'],
                    'emissoes_biogenicas_kg_co2': resultado_uso.get('emissoes_biogenicas_kg_co2', 0)
                }
            },
            'emissoes_totais_kg_co2': emissoes_totais,
            'energia_total_mj': energia_total_mj,
            'intensidade_carbono_g_co2_mj': intensidade_carbono,
            'neea': neea,
            'comparacao_fossil': {
                'ci_fossil_referencia_g_co2_mj': ci_fossil,
                'ci_biocombustivel_g_co2_mj': intensidade_carbono,
                'reducao_g_co2_mj': neea,
                'reducao_percentual': reducao_percentual
            }
        }


def exemplo_uso():
    """Exemplo de uso da calculadora"""
    # Inicializar calculadora
    calc = CalculadoraBioCalc()

    # Dados de entrada de exemplo
    dados = {
        'biomassa': 'pinus',
        'fase_agricola': {
            'quantidade_biomassa_kg': 1000,
            'distancia_transporte_km': 50,
            'uso_fertilizantes_kg': 10,
            'uso_pesticidas_kg': 2,
            'luc_dluc_opcional_kg_co2': 0
        },
        'fase_industrial': {
            'energia_eletrica_kwh': 150,
            'energia_termica_mj': 500,
            'agua_m3': 5
        },
        'fase_distribuicao': {
            'modal_transporte': 'rodoviario',
            'distancia_km': 200
        },
        'fase_uso': {
            'tipo_combustao': 'caldeira'
        }
    }

    # Calcular
    resultado = calc.calcular_intensidade_carbono(dados)

    # Exibir resultados
    print("\n" + "="*60)
    print("RESULTADOS DA CALCULADORA BIOCALC")
    print("="*60)
    print(f"\nBiomassa: {resultado['biomassa'].upper()}")
    print(f"PCI: {resultado['biomassa_info']['pci']} MJ/kg")
    print(f"\nEmissoes totais: {resultado['emissoes_totais_kg_co2']:.2f} kg CO2")
    print(f"Energia total: {resultado['energia_total_mj']:.2f} MJ")
    print(f"\nIntensidade de carbono: {resultado['intensidade_carbono_g_co2_mj']:.2f} gCO2/MJ")
    print(f"NEEA: {resultado['neea']:.2f} gCO2/MJ")
    print(f"Reducao vs. fossil: {resultado['comparacao_fossil']['reducao_percentual']:.1f}%")

    print("\n" + "-"*60)
    print("EMISSOES POR FASE:")
    print("-"*60)
    for fase, dados_fase in resultado['resultados_por_fase'].items():
        print(f"{fase.capitalize():15s}: {dados_fase['emissoes_kg_co2']:8.2f} kg CO2 ({dados_fase['percentual']:5.1f}%)")


if __name__ == "__main__":
    exemplo_uso()
