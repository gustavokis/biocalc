"""
Testes unitários para o motor de cálculo principal
"""

import pytest
import sys
import os

# Adicionar diretório raiz ao path para imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.calculo import CalculadoraBioCalc


class TestCalculadoraBioCalc:
    """Testes para o motor principal de cálculo"""

    def test_inicializacao(self):
        """Teste de inicialização da calculadora"""
        calc = CalculadoraBioCalc()

        # Verificar que foi inicializada
        assert calc is not None

        # Verificar que fatores foram carregados
        assert hasattr(calc, 'fatores')
        assert len(calc.fatores) > 0

        # Verificar que biomassas foram carregadas
        assert hasattr(calc, 'biomassas')
        assert len(calc.biomassas) == 3  # amendoim, pinus, eucalipto

    def test_calculo_completo_basico(self):
        """Teste de cálculo completo com dados básicos"""
        calc = CalculadoraBioCalc()

        dados_entrada = {
            'biomassa': 'pinus',
            'fase_agricola': {
                'quantidade_biomassa_kg': 1000,
                'distancia_transporte_km': 50,
                'uso_fertilizantes_kg': 100,
                'uso_pesticidas_kg': 10,
                'luc_dluc_opcional_kg_co2': 0
            },
            'fase_industrial': {
                'energia_eletrica_kwh': 500,
                'energia_termica_mj': 2000,
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

        resultado = calc.calcular_intensidade_carbono(dados_entrada)

        # Verificar estrutura do resultado
        assert isinstance(resultado, dict)
        assert 'biomassa' in resultado
        assert 'biomassa_info' in resultado
        assert 'resultados_por_fase' in resultado
        assert 'emissoes_totais_kg_co2' in resultado
        assert 'energia_total_mj' in resultado
        assert 'intensidade_carbono_g_co2_mj' in resultado
        assert 'neea' in resultado
        assert 'comparacao_fossil' in resultado

        # Verificar que todas as 4 fases estão presentes
        assert 'agricola' in resultado['resultados_por_fase']
        assert 'industrial' in resultado['resultados_por_fase']
        assert 'distribuicao' in resultado['resultados_por_fase']
        assert 'uso' in resultado['resultados_por_fase']

        # Verificar que valores são razoáveis
        assert resultado['emissoes_totais_kg_co2'] > 0
        assert resultado['energia_total_mj'] > 0
        assert resultado['intensidade_carbono_g_co2_mj'] > 0

        # Intensidade de carbono deve ser menor que fóssil (85 gCO2/MJ)
        assert resultado['intensidade_carbono_g_co2_mj'] < 85.0

        # NEEA deve ser positivo (redução vs fóssil)
        assert resultado['neea'] > 0

    def test_calculo_com_cada_biomassa(self):
        """Teste de cálculo com cada tipo de biomassa"""
        calc = CalculadoraBioCalc()

        biomassas = ['amendoim', 'pinus', 'eucalipto']

        for biomassa in biomassas:
            dados_entrada = {
                'biomassa': biomassa,
                'fase_agricola': {
                    'quantidade_biomassa_kg': 1000,
                    'distancia_transporte_km': 50,
                    'uso_fertilizantes_kg': 50,
                    'uso_pesticidas_kg': 5,
                    'luc_dluc_opcional_kg_co2': 0
                },
                'fase_industrial': {
                    'energia_eletrica_kwh': 300,
                    'energia_termica_mj': 1000,
                    'agua_m3': 3
                },
                'fase_distribuicao': {
                    'modal_transporte': 'rodoviario',
                    'distancia_km': 100
                },
                'fase_uso': {
                    'tipo_combustao': 'caldeira'
                }
            }

            resultado = calc.calcular_intensidade_carbono(dados_entrada)

            # Verificar que o cálculo foi bem-sucedido
            assert resultado['biomassa'] == biomassa
            assert resultado['intensidade_carbono_g_co2_mj'] > 0
            assert resultado['neea'] > 0

    def test_percentuais_somam_100(self):
        """Teste que os percentuais por fase somam 100%"""
        calc = CalculadoraBioCalc()

        dados_entrada = {
            'biomassa': 'eucalipto',
            'fase_agricola': {
                'quantidade_biomassa_kg': 1000,
                'distancia_transporte_km': 50,
                'uso_fertilizantes_kg': 100,
                'uso_pesticidas_kg': 10,
                'luc_dluc_opcional_kg_co2': 0
            },
            'fase_industrial': {
                'energia_eletrica_kwh': 500,
                'energia_termica_mj': 2000,
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

        resultado = calc.calcular_intensidade_carbono(dados_entrada)

        # Somar percentuais
        total_percentual = sum(
            resultado['resultados_por_fase'][fase]['percentual']
            for fase in ['agricola', 'industrial', 'distribuicao', 'uso']
        )

        # Deve somar 100% (com tolerância para arredondamento)
        assert total_percentual == pytest.approx(100.0, abs=0.1)

    def test_energia_total_correta(self):
        """Teste que a energia total é calculada corretamente"""
        calc = CalculadoraBioCalc()

        quantidade_biomassa = 1000  # kg

        dados_entrada = {
            'biomassa': 'pinus',  # PCI = 18.5 MJ/kg
            'fase_agricola': {
                'quantidade_biomassa_kg': quantidade_biomassa,
                'distancia_transporte_km': 0,
                'uso_fertilizantes_kg': 0,
                'uso_pesticidas_kg': 0,
                'luc_dluc_opcional_kg_co2': 0
            },
            'fase_industrial': {
                'energia_eletrica_kwh': 0,
                'energia_termica_mj': 0,
                'agua_m3': 0
            },
            'fase_distribuicao': {
                'modal_transporte': 'rodoviario',
                'distancia_km': 0
            },
            'fase_uso': {
                'tipo_combustao': 'caldeira'
            }
        }

        resultado = calc.calcular_intensidade_carbono(dados_entrada)

        # Energia total = quantidade × PCI
        # 1000 kg × 18.5 MJ/kg = 18500 MJ
        assert resultado['energia_total_mj'] == pytest.approx(18500.0, rel=0.01)

    def test_comparacao_fossil(self):
        """Teste da comparação com combustível fóssil"""
        calc = CalculadoraBioCalc()

        dados_entrada = {
            'biomassa': 'pinus',
            'fase_agricola': {
                'quantidade_biomassa_kg': 1000,
                'distancia_transporte_km': 50,
                'uso_fertilizantes_kg': 50,
                'uso_pesticidas_kg': 5,
                'luc_dluc_opcional_kg_co2': 0
            },
            'fase_industrial': {
                'energia_eletrica_kwh': 300,
                'energia_termica_mj': 1000,
                'agua_m3': 3
            },
            'fase_distribuicao': {
                'modal_transporte': 'rodoviario',
                'distancia_km': 100
            },
            'fase_uso': {
                'tipo_combustao': 'caldeira'
            }
        }

        resultado = calc.calcular_intensidade_carbono(dados_entrada)

        comparacao = resultado['comparacao_fossil']

        # Verificar estrutura
        assert 'ci_fossil_referencia_g_co2_mj' in comparacao
        assert 'reducao_g_co2_mj' in comparacao
        assert 'reducao_percentual' in comparacao

        # CI fóssil de referência deve ser 85 gCO2/MJ
        assert comparacao['ci_fossil_referencia_g_co2_mj'] == 85.0

        # Redução deve ser positiva (biomassa é melhor)
        assert comparacao['reducao_g_co2_mj'] > 0
        assert comparacao['reducao_percentual'] > 0

        # Redução percentual deve estar entre 0 e 100
        assert 0 < comparacao['reducao_percentual'] < 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
