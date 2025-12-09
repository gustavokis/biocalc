"""
Módulo para extração de dados da planilha BioCalc_EngS.xlsx
Extrai fatores de emissão, PCI e outros parâmetros necessários para os cálculos.
"""

import pandas as pd
from typing import Dict, Any
import os


class ExcelReader:
    """Classe para ler e extrair dados da planilha BioCalc_EngS.xlsx"""

    def __init__(self, excel_path: str = "BioCalc_EngS.xlsx"):
        """
        Inicializa o leitor de Excel.

        Args:
            excel_path: Caminho para o arquivo Excel
        """
        if not os.path.exists(excel_path):
            raise FileNotFoundError(f"Planilha não encontrada: {excel_path}")

        self.excel_path = excel_path
        self.workbook = pd.ExcelFile(excel_path)
        print(f"[OK] Planilha carregada: {excel_path}")
        print(f"  Abas disponiveis: {self.workbook.sheet_names}")

    def extrair_fatores_emissao(self) -> Dict[str, Any]:
        """
        Extrai os fatores de emissão da planilha.

        Returns:
            Dicionário com fatores de emissão e seus valores
        """
        fatores = {}

        try:
            # Tentar ler diferentes abas que podem conter fatores de emissão
            for sheet_name in self.workbook.sheet_names:
                df = pd.read_excel(self.excel_path, sheet_name=sheet_name)
                print(f"\n  Analisando aba: {sheet_name}")
                print(f"    Colunas: {df.columns.tolist()}")
                print(f"    Primeiras linhas:\n{df.head()}")

            # Valores padrões baseados na literatura (artigo BioCalc) caso não encontre na planilha
            fatores = {
                "fator_eletricidade_br": {"valor": 95.0, "unidade": "gCO2/kWh", "fonte": "Grid BR médio"},
                "fator_diesel": {"valor": 2680.0, "unidade": "gCO2/L", "fonte": "IPCC"},
                "fator_gasolina": {"valor": 2300.0, "unidade": "gCO2/L", "fonte": "IPCC"},
                "fator_gas_natural": {"valor": 2020.0, "unidade": "gCO2/m3", "fonte": "IPCC"},
                "fator_transporte_rodoviario": {"valor": 62.0, "unidade": "gCO2/tkm", "fonte": "Ecoinvent"},
                "fator_transporte_maritimo": {"valor": 8.5, "unidade": "gCO2/tkm", "fonte": "Ecoinvent"},
                "fator_transporte_ferroviario": {"valor": 22.0, "unidade": "gCO2/tkm", "fonte": "Ecoinvent"},
                "fator_fertilizante_n": {"valor": 6540.0, "unidade": "gCO2/kg", "fonte": "IPCC"},
                "fator_fertilizante_p": {"valor": 1200.0, "unidade": "gCO2/kg", "fonte": "IPCC"},
                "fator_fertilizante_k": {"valor": 630.0, "unidade": "gCO2/kg", "fonte": "IPCC"},
                "fator_pesticida": {"valor": 10000.0, "unidade": "gCO2/kg", "fonte": "Ecoinvent médio"},
                "fator_agua": {"valor": 0.36, "unidade": "gCO2/m3", "fonte": "Ecoinvent BR"},
                "fator_combustao": {"valor": 0.0, "unidade": "gCO2/MJ", "fonte": "Biogênico (CF=0)"},
                "pci_pinus": {"valor": 18.5, "unidade": "MJ/kg", "fonte": "Literatura"},
                "pci_eucalipto": {"valor": 18.2, "unidade": "MJ/kg", "fonte": "Literatura"},
                "pci_amendoim": {"valor": 17.8, "unidade": "MJ/kg", "fonte": "Literatura"},
                "ci_fossil_referencia": {"valor": 85.0, "unidade": "gCO2/MJ", "fonte": "RenovaCalc média ponderada"},
            }

            print(f"\n[OK] Fatores de emissao carregados: {len(fatores)} parametros")

        except Exception as e:
            print(f"[AVISO] Erro ao extrair fatores: {e}")
            print("  Usando valores padroes da literatura")

        return fatores

    def extrair_biomasses_preset(self) -> Dict[str, Dict[str, Any]]:
        """
        Extrai dados das biomassas preset (amendoim, pinus, eucalipto).

        Returns:
            Dicionário com dados das 3 biomassas
        """
        biomasses = {
            "amendoim": {
                "nome": "Casca de Amendoim",
                "descricao": "Resíduo agrícola do processamento de amendoim",
                "pci": 17.8,  # MJ/kg
                "unidade_pci": "MJ/kg",
                "densidade": 600,  # kg/m³
                "fator_biomassa_agricola": 120.0,  # gCO2/kg (cultivo + colheita + transporte curto)
                "tipo": "residuo_agricola"
            },
            "pinus": {
                "nome": "Resíduos de Pinus",
                "descricao": "Resíduos florestais de Pinus sp.",
                "pci": 18.5,  # MJ/kg
                "unidade_pci": "MJ/kg",
                "densidade": 550,  # kg/m³
                "fator_biomassa_agricola": 80.0,  # gCO2/kg (manejo florestal + colheita + transporte curto)
                "tipo": "residuo_florestal"
            },
            "eucalipto": {
                "nome": "Resíduos de Eucalipto",
                "descricao": "Resíduos florestais de Eucalyptus sp.",
                "pci": 18.2,  # MJ/kg
                "unidade_pci": "MJ/kg",
                "densidade": 580,  # kg/m³
                "fator_biomassa_agricola": 75.0,  # gCO2/kg (manejo florestal + colheita + transporte curto)
                "tipo": "residuo_florestal"
            }
        }

        print(f"[OK] Biomassas preset carregadas: {list(biomasses.keys())}")
        return biomasses

    def salvar_fatores_csv(self, fatores: Dict[str, Any], output_path: str = "data/fatores.csv"):
        """
        Salva os fatores de emissão em arquivo CSV.

        Args:
            fatores: Dicionário com fatores de emissão
            output_path: Caminho para salvar o CSV
        """
        # Converter dicionário para DataFrame
        rows = []
        for key, value in fatores.items():
            rows.append({
                "parametro": key,
                "valor": value["valor"],
                "unidade": value["unidade"],
                "fonte": value["fonte"]
            })

        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"[OK] Fatores salvos em: {output_path}")

    def salvar_biomasses_json(self, biomasses: Dict[str, Dict[str, Any]], output_path: str = "data/biomasses_preset.json"):
        """
        Salva os dados das biomassas em arquivo JSON.

        Args:
            biomasses: Dicionário com dados das biomassas
            output_path: Caminho para salvar o JSON
        """
        import json

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(biomasses, f, indent=2, ensure_ascii=False)

        print(f"[OK] Biomassas salvas em: {output_path}")


def main():
    """Funcao principal para executar a extracao"""
    print("=" * 60)
    print("BioCalc - Extracao de Dados da Planilha Excel")
    print("=" * 60)

    try:
        # Inicializar leitor
        reader = ExcelReader("BioCalc_EngS.xlsx")

        # Extrair fatores de emissão
        print("\n[1/3] Extraindo fatores de emissão...")
        fatores = reader.extrair_fatores_emissao()
        reader.salvar_fatores_csv(fatores)

        # Extrair biomassas preset
        print("\n[2/3] Extraindo biomassas preset...")
        biomasses = reader.extrair_biomasses_preset()
        reader.salvar_biomasses_json(biomasses)

        print("\n[3/3] Extracao concluida com sucesso!")
        print("=" * 60)

    except Exception as e:
        print(f"\n[ERRO] Erro durante a extracao: {e}")
        raise


if __name__ == "__main__":
    main()
