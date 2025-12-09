"""
Testes unitários para as 4 fases do ciclo de vida
"""

import pytest
import sys
import os
import pandas as pd

# Adicionar diretório raiz ao path para imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.fase_agricola import FaseAgricola
from src.core.fase_industrial import FaseIndustrial
from src.core.fase_distribuicao import FaseDistribuicao
from src.core.fase_uso import FaseUso


# Helper para carregar fatores
def carregar_fatores():
    """Carrega fatores de emissão do CSV"""
    caminho = os.path.join(os.path.dirname(__file__), '..', 'data', 'fatores.csv')
    df = pd.read_csv(caminho)
    fatores = {}
    for _, row in df.iterrows():
        fatores[row['parametro']] = {
            'valor': row['valor'],
            'unidade': row['unidade'],
            'fonte': row['fonte']
        }
    return fatores


class TestFaseAgricola:
    """Testes para a fase agrícola"""

    def test_calcular_emissoes_basico(self):
        """Teste básico de cálculo de emissões agrícolas"""
        fatores = carregar_fatores()
        fase = FaseAgricola(fatores)

        dados = {
            'quantidade_biomassa_kg': 1000,  # 1 tonelada
            'distancia_transporte_km': 50,
            'uso_fertilizantes_kg': 100,
            'uso_pesticidas_kg': 10,
            'luc_dluc_opcional_kg_co2': 0,
            'fator_biomassa_agricola': 50.0  # gCO2/kg
        }

        resultado = fase.calcular_emissoes(dados)

        # Verificar que o resultado é um dicionário
        assert isinstance(resultado, dict)

        # Verificar que contém as chaves esperadas
        assert 'emissoes_kg_co2' in resultado
        assert 'detalhamento' in resultado

        # Verificar que emissões são positivas
        assert resultado['emissoes_kg_co2'] > 0

        # Verificar detalhamento
        assert 'biomassa' in resultado['detalhamento']
        assert 'transporte' in resultado['detalhamento']
        assert 'fertilizantes' in resultado['detalhamento']
        assert 'pesticidas' in resultado['detalhamento']

    def test_sem_insumos(self):
        """Teste com zero insumos (apenas cultivo e transporte)"""
        fatores = carregar_fatores()
        fase = FaseAgricola(fatores)

        dados = {
            'quantidade_biomassa_kg': 1000,
            'distancia_transporte_km': 0,
            'uso_fertilizantes_kg': 0,
            'uso_pesticidas_kg': 0,
            'luc_dluc_opcional_kg_co2': 0,
            'fator_biomassa_agricola': 50.0  # gCO2/kg
        }

        resultado = fase.calcular_emissoes(dados)

        # Com fator agrícola de 50 gCO2/kg e 1000 kg = 50000 gCO2 = 50 kgCO2
        assert resultado['emissoes_kg_co2'] == pytest.approx(50.0, rel=0.01)

    def test_com_luc_dluc(self):
        """Teste incluindo emissões de LUC/dLUC"""
        fatores = carregar_fatores()
        fase = FaseAgricola(fatores)

        dados = {
            'quantidade_biomassa_kg': 1000,
            'distancia_transporte_km': 0,
            'uso_fertilizantes_kg': 0,
            'uso_pesticidas_kg': 0,
            'luc_dluc_opcional_kg_co2': 500,  # 500 kgCO2 adicional
            'fator_biomassa_agricola': 50.0  # gCO2/kg
        }

        resultado = fase.calcular_emissoes(dados)

        # 50 kgCO2 (cultivo) + 500 kgCO2 (LUC) = 550 kgCO2
        assert resultado['emissoes_kg_co2'] == pytest.approx(550.0, rel=0.01)


class TestFaseIndustrial:
    """Testes para a fase industrial"""

    def test_calcular_emissoes_basico(self):
        """Teste básico de cálculo de emissões industriais"""
        fatores = carregar_fatores()
        fase = FaseIndustrial(fatores)

        dados = {
            'energia_eletrica_kwh': 1000,
            'energia_termica_mj': 5000,
            'agua_m3': 10
        }

        resultado = fase.calcular_emissoes(dados)

        # Verificar estrutura
        assert isinstance(resultado, dict)
        assert 'emissoes_kg_co2' in resultado
        assert 'detalhamento' in resultado

        # Verificar que emissões são positivas
        assert resultado['emissoes_kg_co2'] > 0

        # Verificar detalhamento
        assert 'energia_eletrica' in resultado['detalhamento']
        assert 'energia_termica' in resultado['detalhamento']
        assert 'agua' in resultado['detalhamento']

    def test_apenas_energia_eletrica(self):
        """Teste com apenas energia elétrica"""
        fatores = carregar_fatores()
        fase = FaseIndustrial(fatores)

        dados = {
            'energia_eletrica_kwh': 1000,
            'energia_termica_mj': 0,
            'agua_m3': 0
        }

        resultado = fase.calcular_emissoes(dados)

        # Com fator de 95 gCO2/kWh = 0.095 kgCO2/kWh
        # 1000 kWh × 0.095 = 95 kgCO2
        assert resultado['emissoes_kg_co2'] == pytest.approx(95.0, rel=0.01)

    def test_sem_consumos(self):
        """Teste sem consumos (emissões zero)"""
        fatores = carregar_fatores()
        fase = FaseIndustrial(fatores)

        dados = {
            'energia_eletrica_kwh': 0,
            'energia_termica_mj': 0,
            'agua_m3': 0
        }

        resultado = fase.calcular_emissoes(dados)

        assert resultado['emissoes_kg_co2'] == 0


class TestFaseDistribuicao:
    """Testes para a fase de distribuição"""

    def test_transporte_rodoviario(self):
        """Teste de transporte rodoviário"""
        fatores = carregar_fatores()
        fase = FaseDistribuicao(fatores)

        dados = {
            'modal_transporte': 'rodoviario',
            'distancia_km': 100,
            'quantidade_biomassa_kg': 1000
        }

        resultado = fase.calcular_emissoes(dados)

        # Verificar estrutura
        assert isinstance(resultado, dict)
        assert 'emissoes_kg_co2' in resultado
        assert 'detalhamento' in resultado

        # Verificar que emissões são positivas
        assert resultado['emissoes_kg_co2'] > 0

    def test_transporte_maritimo(self):
        """Teste de transporte marítimo (mais eficiente)"""
        fatores = carregar_fatores()
        fase = FaseDistribuicao(fatores)

        dados_rodoviario = {
            'modal_transporte': 'rodoviario',
            'distancia_km': 1000,
            'quantidade_biomassa_kg': 1000
        }

        dados_maritimo = {
            'modal_transporte': 'maritimo',
            'distancia_km': 1000,
            'quantidade_biomassa_kg': 1000
        }

        resultado_rod = fase.calcular_emissoes(dados_rodoviario)
        resultado_mar = fase.calcular_emissoes(dados_maritimo)

        # Transporte marítimo deve ter menores emissões
        assert resultado_mar['emissoes_kg_co2'] < resultado_rod['emissoes_kg_co2']

    def test_distancia_zero(self):
        """Teste com distância zero"""
        fatores = carregar_fatores()
        fase = FaseDistribuicao(fatores)

        dados = {
            'modal_transporte': 'rodoviario',
            'distancia_km': 0,
            'quantidade_biomassa_kg': 1000
        }

        resultado = fase.calcular_emissoes(dados)

        assert resultado['emissoes_kg_co2'] == 0


class TestFaseUso:
    """Testes para a fase de uso"""

    def test_combustao_biomassa(self):
        """Teste de combustão de biomassa (biogênico = 0)"""
        fatores = carregar_fatores()
        fase = FaseUso(fatores)

        dados = {
            'tipo_combustao': 'caldeira',
            'quantidade_biomassa_kg': 1000,
            'pci': 18.5  # MJ/kg
        }

        resultado = fase.calcular_emissoes(dados)

        # Verificar estrutura
        assert isinstance(resultado, dict)
        assert 'emissoes_kg_co2' in resultado
        assert 'emissoes_biogenicas_kg_co2' in resultado
        assert 'detalhamento' in resultado

        # Emissões líquidas devem ser zero (CF=0)
        assert resultado['emissoes_kg_co2'] == 0

        # Emissões biogênicas devem ser calculadas
        assert resultado['emissoes_biogenicas_kg_co2'] > 0

    def test_calculo_emissoes_biogenicas(self):
        """Teste de cálculo correto de emissões biogênicas"""
        fatores = carregar_fatores()
        fase = FaseUso(fatores)

        dados = {
            'tipo_combustao': 'caldeira',
            'quantidade_biomassa_kg': 1000,
            'pci': 18.5  # MJ/kg
        }

        resultado = fase.calcular_emissoes(dados)

        # Emissões biogênicas = quantidade × PCI × fator_combustao_biogenico
        # 1000 kg × 18.5 MJ/kg × 0.1 kgCO2/MJ = 1850 kgCO2
        assert resultado['emissoes_biogenicas_kg_co2'] == pytest.approx(1850.0, rel=0.01)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
