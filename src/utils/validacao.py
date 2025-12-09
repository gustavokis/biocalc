"""
Módulo para validação de entradas
Valida dados de entrada do usuário antes dos cálculos
"""

from typing import Dict, Any, List, Tuple


class Validador:
    """Classe para validação de entradas"""

    @staticmethod
    def validar_positivo(valor: float, nome_campo: str) -> Tuple[bool, str]:
        """
        Valida se o valor é positivo.

        Args:
            valor: Valor a validar
            nome_campo: Nome do campo para mensagem de erro

        Returns:
            Tupla (valido, mensagem_erro)
        """
        if valor < 0:
            return False, f"{nome_campo} deve ser um valor positivo (valor: {valor})"
        return True, ""

    @staticmethod
    def validar_range(valor: float, nome_campo: str, min_val: float, max_val: float) -> Tuple[bool, str]:
        """
        Valida se o valor está dentro de um range.

        Args:
            valor: Valor a validar
            nome_campo: Nome do campo
            min_val: Valor mínimo
            max_val: Valor máximo

        Returns:
            Tupla (valido, mensagem_erro)
        """
        if valor < min_val or valor > max_val:
            return False, f"{nome_campo} deve estar entre {min_val} e {max_val} (valor: {valor})"
        return True, ""

    @staticmethod
    def validar_fase_agricola(dados: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Valida dados da fase agrícola.

        Args:
            dados: Dicionário com dados da fase agrícola

        Returns:
            Tupla (valido, lista_de_erros)
        """
        erros = []

        # Quantidade de biomassa (obrigatório, > 0, < 1.000.000 kg)
        biomassa = dados.get('quantidade_biomassa_kg', 0)
        if biomassa <= 0:
            erros.append("Quantidade de biomassa deve ser maior que zero")
        elif biomassa > 1_000_000:
            erros.append("Quantidade de biomassa muito alta (máximo: 1.000.000 kg)")

        # Distância de transporte (>= 0, < 1000 km razoável para transporte curto)
        distancia = dados.get('distancia_transporte_km', 0)
        valido, msg = Validador.validar_positivo(distancia, "Distância de transporte")
        if not valido:
            erros.append(msg)
        elif distancia > 1000:
            erros.append("AVISO: Distância de transporte muito alta para fase agrícola (>1000 km)")

        # Fertilizantes (>= 0, < 100.000 kg)
        fertilizantes = dados.get('uso_fertilizantes_kg', 0)
        valido, msg = Validador.validar_positivo(fertilizantes, "Uso de fertilizantes")
        if not valido:
            erros.append(msg)
        elif fertilizantes > 100_000:
            erros.append("Uso de fertilizantes muito alto (máximo razoável: 100.000 kg)")

        # Pesticidas (>= 0, < 10.000 kg)
        pesticidas = dados.get('uso_pesticidas_kg', 0)
        valido, msg = Validador.validar_positivo(pesticidas, "Uso de pesticidas")
        if not valido:
            erros.append(msg)
        elif pesticidas > 10_000:
            erros.append("Uso de pesticidas muito alto (máximo razoável: 10.000 kg)")

        # LUC/dLUC opcional (pode ser 0 ou >= 0)
        luc = dados.get('luc_dluc_opcional_kg_co2', 0)
        valido, msg = Validador.validar_positivo(luc, "LUC/dLUC")
        if not valido:
            erros.append(msg)

        return len(erros) == 0, erros

    @staticmethod
    def validar_fase_industrial(dados: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Valida dados da fase industrial.

        Args:
            dados: Dicionário com dados da fase industrial

        Returns:
            Tupla (valido, lista_de_erros)
        """
        erros = []

        # Energia elétrica (>= 0, < 1.000.000 kWh)
        energia_eletrica = dados.get('energia_eletrica_kwh', 0)
        valido, msg = Validador.validar_positivo(energia_eletrica, "Energia elétrica")
        if not valido:
            erros.append(msg)
        elif energia_eletrica > 1_000_000:
            erros.append("Consumo de energia elétrica muito alto (máximo razoável: 1.000.000 kWh)")

        # Energia térmica (>= 0, < 10.000.000 MJ)
        energia_termica = dados.get('energia_termica_mj', 0)
        valido, msg = Validador.validar_positivo(energia_termica, "Energia térmica")
        if not valido:
            erros.append(msg)
        elif energia_termica > 10_000_000:
            erros.append("Consumo de energia térmica muito alto (máximo razoável: 10.000.000 MJ)")

        # Água (>= 0, < 100.000 m³)
        agua = dados.get('agua_m3', 0)
        valido, msg = Validador.validar_positivo(agua, "Consumo de água")
        if not valido:
            erros.append(msg)
        elif agua > 100_000:
            erros.append("Consumo de água muito alto (máximo razoável: 100.000 m³)")

        return len(erros) == 0, erros

    @staticmethod
    def validar_fase_distribuicao(dados: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Valida dados da fase de distribuição.

        Args:
            dados: Dicionário com dados da fase de distribuição

        Returns:
            Tupla (valido, lista_de_erros)
        """
        erros = []

        # Modal de transporte (obrigatório)
        modal = dados.get('modal_transporte', '')
        modais_validos = ['rodoviario', 'maritimo', 'ferroviario']
        if modal not in modais_validos:
            erros.append(f"Modal de transporte inválido. Opções: {', '.join(modais_validos)}")

        # Distância (>= 0, < 50.000 km)
        distancia = dados.get('distancia_km', 0)
        valido, msg = Validador.validar_positivo(distancia, "Distância de distribuição")
        if not valido:
            erros.append(msg)
        elif distancia > 50_000:
            erros.append("Distância de distribuição muito alta (máximo razoável: 50.000 km)")

        return len(erros) == 0, erros

    @staticmethod
    def validar_fase_uso(dados: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Valida dados da fase de uso.

        Args:
            dados: Dicionário com dados da fase de uso

        Returns:
            Tupla (valido, lista_de_erros)
        """
        erros = []

        # Tipo de combustão (opcional, mas se fornecido deve ser válido)
        tipo = dados.get('tipo_combustao', 'caldeira')
        tipos_validos = ['caldeira', 'fornalha', 'outro']
        if tipo not in tipos_validos:
            erros.append(f"Tipo de combustão inválido. Opções: {', '.join(tipos_validos)}")

        return len(erros) == 0, erros

    @staticmethod
    def validar_completo(dados_entrada: Dict[str, Any]) -> Tuple[bool, Dict[str, List[str]]]:
        """
        Valida todos os dados de entrada.

        Args:
            dados_entrada: Dicionário completo com todos os dados

        Returns:
            Tupla (valido, dicionario_de_erros_por_fase)
        """
        erros_por_fase = {}

        # Validar biomassa
        biomassa = dados_entrada.get('biomassa', '')
        biomassas_validas = ['amendoim', 'pinus', 'eucalipto']
        if biomassa not in biomassas_validas:
            erros_por_fase['biomassa'] = [f"Biomassa inválida. Opções: {', '.join(biomassas_validas)}"]

        # Validar fase agrícola
        dados_agricola = dados_entrada.get('fase_agricola', {})
        valido, erros = Validador.validar_fase_agricola(dados_agricola)
        if not valido:
            erros_por_fase['fase_agricola'] = erros

        # Validar fase industrial
        dados_industrial = dados_entrada.get('fase_industrial', {})
        valido, erros = Validador.validar_fase_industrial(dados_industrial)
        if not valido:
            erros_por_fase['fase_industrial'] = erros

        # Validar fase distribuição
        dados_distribuicao = dados_entrada.get('fase_distribuicao', {})
        valido, erros = Validador.validar_fase_distribuicao(dados_distribuicao)
        if not valido:
            erros_por_fase['fase_distribuicao'] = erros

        # Validar fase uso
        dados_uso = dados_entrada.get('fase_uso', {})
        valido, erros = Validador.validar_fase_uso(dados_uso)
        if not valido:
            erros_por_fase['fase_uso'] = erros

        return len(erros_por_fase) == 0, erros_por_fase
