"""
Testes unitários para o módulo de validação
"""

import pytest
import sys
import os

# Adicionar diretório raiz ao path para imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.validacao import Validador


class TestValidador:
    """Testes para o validador de entradas"""

    def test_validar_positivo_sucesso(self):
        """Teste de validação de valor positivo - sucesso"""
        valido, msg = Validador.validar_positivo(10.0, "Quantidade")

        assert valido is True
        assert msg == ""

    def test_validar_positivo_zero(self):
        """Teste de validação de zero (deve passar)"""
        valido, msg = Validador.validar_positivo(0, "Quantidade")

        assert valido is True
        assert msg == ""

    def test_validar_positivo_negativo(self):
        """Teste de validação de valor negativo - falha"""
        valido, msg = Validador.validar_positivo(-5.0, "Quantidade")

        assert valido is False
        assert "positivo" in msg.lower()
        assert "Quantidade" in msg

    def test_validar_range_sucesso(self):
        """Teste de validação de range - sucesso"""
        valido, msg = Validador.validar_range(50.0, "Temperatura", 0.0, 100.0)

        assert valido is True
        assert msg == ""

    def test_validar_range_abaixo_minimo(self):
        """Teste de validação de range - abaixo do mínimo"""
        valido, msg = Validador.validar_range(-10.0, "Temperatura", 0.0, 100.0)

        assert valido is False
        assert "entre" in msg.lower()

    def test_validar_range_acima_maximo(self):
        """Teste de validação de range - acima do máximo"""
        valido, msg = Validador.validar_range(150.0, "Temperatura", 0.0, 100.0)

        assert valido is False
        assert "entre" in msg.lower()

    def test_validar_fase_agricola_valida(self):
        """Teste de validação de fase agrícola - dados válidos"""
        dados = {
            'quantidade_biomassa_kg': 1000,
            'distancia_transporte_km': 50,
            'uso_fertilizantes_kg': 100,
            'uso_pesticidas_kg': 10,
            'luc_dluc_opcional_kg_co2': 0
        }

        valido, erros = Validador.validar_fase_agricola(dados)

        assert valido is True
        assert len(erros) == 0

    def test_validar_fase_agricola_biomassa_zero(self):
        """Teste de validação de fase agrícola - biomassa zero"""
        dados = {
            'quantidade_biomassa_kg': 0,  # Inválido
            'distancia_transporte_km': 50,
            'uso_fertilizantes_kg': 100,
            'uso_pesticidas_kg': 10,
            'luc_dluc_opcional_kg_co2': 0
        }

        valido, erros = Validador.validar_fase_agricola(dados)

        assert valido is False
        assert len(erros) > 0
        assert any("biomassa" in erro.lower() for erro in erros)

    def test_validar_fase_agricola_biomassa_muito_alta(self):
        """Teste de validação de fase agrícola - biomassa muito alta"""
        dados = {
            'quantidade_biomassa_kg': 2_000_000,  # Acima do limite
            'distancia_transporte_km': 50,
            'uso_fertilizantes_kg': 100,
            'uso_pesticidas_kg': 10,
            'luc_dluc_opcional_kg_co2': 0
        }

        valido, erros = Validador.validar_fase_agricola(dados)

        assert valido is False
        assert len(erros) > 0

    def test_validar_fase_industrial_valida(self):
        """Teste de validação de fase industrial - dados válidos"""
        dados = {
            'energia_eletrica_kwh': 500,
            'energia_termica_mj': 2000,
            'agua_m3': 10
        }

        valido, erros = Validador.validar_fase_industrial(dados)

        assert valido is True
        assert len(erros) == 0

    def test_validar_fase_industrial_energia_negativa(self):
        """Teste de validação de fase industrial - energia negativa"""
        dados = {
            'energia_eletrica_kwh': -100,  # Inválido
            'energia_termica_mj': 2000,
            'agua_m3': 10
        }

        valido, erros = Validador.validar_fase_industrial(dados)

        assert valido is False
        assert len(erros) > 0

    def test_validar_fase_distribuicao_valida(self):
        """Teste de validação de fase distribuição - dados válidos"""
        dados = {
            'modal_transporte': 'rodoviario',
            'distancia_km': 100
        }

        valido, erros = Validador.validar_fase_distribuicao(dados)

        assert valido is True
        assert len(erros) == 0

    def test_validar_fase_distribuicao_modal_invalido(self):
        """Teste de validação de fase distribuição - modal inválido"""
        dados = {
            'modal_transporte': 'aereo',  # Não suportado
            'distancia_km': 100
        }

        valido, erros = Validador.validar_fase_distribuicao(dados)

        assert valido is False
        assert len(erros) > 0
        assert any("modal" in erro.lower() for erro in erros)

    def test_validar_fase_uso_valida(self):
        """Teste de validação de fase uso - dados válidos"""
        dados = {
            'tipo_combustao': 'caldeira'
        }

        valido, erros = Validador.validar_fase_uso(dados)

        assert valido is True
        assert len(erros) == 0

    def test_validar_fase_uso_tipo_invalido(self):
        """Teste de validação de fase uso - tipo inválido"""
        dados = {
            'tipo_combustao': 'turbina'  # Não suportado
        }

        valido, erros = Validador.validar_fase_uso(dados)

        assert valido is False
        assert len(erros) > 0

    def test_validar_completo_valido(self):
        """Teste de validação completa - todos os dados válidos"""
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

        valido, erros_por_fase = Validador.validar_completo(dados_entrada)

        assert valido is True
        assert len(erros_por_fase) == 0

    def test_validar_completo_biomassa_invalida(self):
        """Teste de validação completa - biomassa inválida"""
        dados_entrada = {
            'biomassa': 'carvao',  # Não suportado
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

        valido, erros_por_fase = Validador.validar_completo(dados_entrada)

        assert valido is False
        assert 'biomassa' in erros_por_fase

    def test_validar_completo_multiplos_erros(self):
        """Teste de validação completa - múltiplos erros"""
        dados_entrada = {
            'biomassa': 'pinus',
            'fase_agricola': {
                'quantidade_biomassa_kg': 0,  # Erro: zero
                'distancia_transporte_km': -10,  # Erro: negativo
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
                'modal_transporte': 'espacial',  # Erro: inválido
                'distancia_km': 200
            },
            'fase_uso': {
                'tipo_combustao': 'caldeira'
            }
        }

        valido, erros_por_fase = Validador.validar_completo(dados_entrada)

        assert valido is False
        assert 'fase_agricola' in erros_por_fase
        assert 'fase_distribuicao' in erros_por_fase
        assert len(erros_por_fase['fase_agricola']) >= 2  # Pelo menos 2 erros


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
