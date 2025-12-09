"""
Módulo para exportação de resultados
Exporta resultados para CSV
"""

from typing import Dict, Any
import pandas as pd
from datetime import datetime


class Exportador:
    """Classe para exportação de resultados"""

    @staticmethod
    def exportar_csv(resultados: Dict[str, Any], nome_arquivo: str = None) -> str:
        """
        Exporta resultados para arquivo CSV.

        Args:
            resultados: Dicionário com resultados do cálculo
            nome_arquivo: Nome do arquivo (opcional, gera automático se None)

        Returns:
            Caminho do arquivo gerado
        """
        # Gerar nome de arquivo se não fornecido
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            biomassa = resultados.get('biomassa', 'unknown')
            nome_arquivo = f"resultados_biocalc_{biomassa}_{timestamp}.csv"

        # Preparar dados para exportação
        dados_export = []

        # Informações gerais
        dados_export.append({
            'Categoria': 'Informacoes Gerais',
            'Item': 'Biomassa',
            'Valor': resultados.get('biomassa', ''),
            'Unidade': ''
        })

        dados_export.append({
            'Categoria': 'Informacoes Gerais',
            'Item': 'PCI',
            'Valor': resultados.get('biomassa_info', {}).get('pci', 0),
            'Unidade': 'MJ/kg'
        })

        dados_export.append({
            'Categoria': 'Informacoes Gerais',
            'Item': 'Energia Total',
            'Valor': round(resultados.get('energia_total_mj', 0), 2),
            'Unidade': 'MJ'
        })

        # Resultados por fase
        for fase, dados_fase in resultados.get('resultados_por_fase', {}).items():
            dados_export.append({
                'Categoria': f'Fase {fase.capitalize()}',
                'Item': 'Emissoes',
                'Valor': round(dados_fase.get('emissoes_kg_co2', 0), 2),
                'Unidade': 'kg CO2'
            })

            dados_export.append({
                'Categoria': f'Fase {fase.capitalize()}',
                'Item': 'Percentual',
                'Valor': round(dados_fase.get('percentual', 0), 1),
                'Unidade': '%'
            })

        # Totais
        dados_export.append({
            'Categoria': 'Totais',
            'Item': 'Emissoes Totais',
            'Valor': round(resultados.get('emissoes_totais_kg_co2', 0), 2),
            'Unidade': 'kg CO2'
        })

        dados_export.append({
            'Categoria': 'Totais',
            'Item': 'Intensidade de Carbono',
            'Valor': round(resultados.get('intensidade_carbono_g_co2_mj', 0), 2),
            'Unidade': 'gCO2/MJ'
        })

        dados_export.append({
            'Categoria': 'Totais',
            'Item': 'NEEA',
            'Valor': round(resultados.get('neea', 0), 2),
            'Unidade': 'gCO2/MJ'
        })

        # Comparação com fóssil
        comparacao = resultados.get('comparacao_fossil', {})
        dados_export.append({
            'Categoria': 'Comparacao com Fossil',
            'Item': 'CI Fossil Referencia',
            'Valor': round(comparacao.get('ci_fossil_referencia_g_co2_mj', 0), 2),
            'Unidade': 'gCO2/MJ'
        })

        dados_export.append({
            'Categoria': 'Comparacao com Fossil',
            'Item': 'Reducao',
            'Valor': round(comparacao.get('reducao_g_co2_mj', 0), 2),
            'Unidade': 'gCO2/MJ'
        })

        dados_export.append({
            'Categoria': 'Comparacao com Fossil',
            'Item': 'Reducao Percentual',
            'Valor': round(comparacao.get('reducao_percentual', 0), 1),
            'Unidade': '%'
        })

        # Criar DataFrame e salvar
        df = pd.DataFrame(dados_export)
        df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')

        return nome_arquivo

    @staticmethod
    def exportar_detalhado_csv(resultados: Dict[str, Any], nome_arquivo: str = None) -> str:
        """
        Exporta resultados detalhados (incluindo detalhamento de cada fase) para CSV.

        Args:
            resultados: Dicionário com resultados do cálculo
            nome_arquivo: Nome do arquivo (opcional)

        Returns:
            Caminho do arquivo gerado
        """
        # Gerar nome de arquivo se não fornecido
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            biomassa = resultados.get('biomassa', 'unknown')
            nome_arquivo = f"resultados_biocalc_detalhado_{biomassa}_{timestamp}.csv"

        dados_export = []

        # Adicionar informações gerais
        dados_export.append({
            'Secao': 'Informacoes Gerais',
            'Fase': '',
            'Componente': 'Biomassa',
            'Valor': resultados.get('biomassa', ''),
            'Unidade': ''
        })

        # Adicionar detalhamento de cada fase
        for fase, dados_fase in resultados.get('resultados_por_fase', {}).items():
            detalhamento = dados_fase.get('detalhamento', {})

            # Total da fase
            dados_export.append({
                'Secao': 'Emissoes por Fase',
                'Fase': fase.capitalize(),
                'Componente': 'Total',
                'Valor': round(dados_fase.get('emissoes_kg_co2', 0), 4),
                'Unidade': 'kg CO2'
            })

            # Detalhamento de cada componente
            for componente, valor in detalhamento.items():
                if isinstance(valor, (int, float)):
                    dados_export.append({
                        'Secao': 'Detalhamento',
                        'Fase': fase.capitalize(),
                        'Componente': componente.capitalize(),
                        'Valor': round(valor, 4),
                        'Unidade': 'kg CO2'
                    })

        # Adicionar totais
        dados_export.append({
            'Secao': 'Totais',
            'Fase': '',
            'Componente': 'Emissoes Totais',
            'Valor': round(resultados.get('emissoes_totais_kg_co2', 0), 4),
            'Unidade': 'kg CO2'
        })

        dados_export.append({
            'Secao': 'Totais',
            'Fase': '',
            'Componente': 'Intensidade de Carbono',
            'Valor': round(resultados.get('intensidade_carbono_g_co2_mj', 0), 4),
            'Unidade': 'gCO2/MJ'
        })

        dados_export.append({
            'Secao': 'Totais',
            'Fase': '',
            'Componente': 'NEEA',
            'Valor': round(resultados.get('neea', 0), 4),
            'Unidade': 'gCO2/MJ'
        })

        # Criar DataFrame e salvar
        df = pd.DataFrame(dados_export)
        df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')

        return nome_arquivo
