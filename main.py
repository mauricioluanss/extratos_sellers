# -*- coding: utf-8 -*-
#
# main.py, ajustar_comissoes_especiais.py
# Projeto: Extratos Sellers
# Autor: Mauricio Luan
# Data de criação: 07/08/2025
# Descrição: Gera relatórios de contas a receber e comissões para cada seller.
#
# Copyright (c) 2025 Payer Serviços de Pagamento LTDA. Todos os direitos reservados.

from extratos_sellers.load import carrega_planilhas
from extratos_sellers.transform import merge_dados
from extratos_sellers.save import salva_extratos_por_seller


def main():
    carrega_planilhas()
    merge_dados()
    salva_extratos_por_seller()


main()
