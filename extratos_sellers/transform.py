import re

import numpy as np
import pandas as pd

from .config import (
    ARQ_TEMP_CONTASARECEBER,
    ARQ_TEMP_COMISSOES,
    ARQ_TEMP_CONTASARECEBER_FINAL,
    COLUNAS,
    COLUNAS_CRIADAS,
)


def extrai_nome_seller(cliente):
    resultado = re.search(r"\((.*?)\)", str(cliente))
    if resultado:
        return resultado.group(1).strip()
    return None


def prepara_para_merge() -> pd.DataFrame:
    """Faz a limpeza necessária de contas_a_receber e comissoes antes do merge."""
    try:
        df_contas_a_receber = pd.read_excel(ARQ_TEMP_CONTASARECEBER)
        df_comissoes = pd.read_excel(ARQ_TEMP_COMISSOES)

        # cria a coluna nome_resselers e aplica nela os nomes dos resselers. Isso
        # pepara para o merge
        df_contas_a_receber[COLUNAS_CRIADAS["COL_NOME_RESSELLER"]] = (
            df_contas_a_receber[COLUNAS["COL_NOME_CLIENTE"]].apply(extrai_nome_seller)
        )

        df_contas_a_receber[COLUNAS_CRIADAS["COL_NOME_RESSELLER"]] = (
            df_contas_a_receber[COLUNAS_CRIADAS["COL_NOME_RESSELLER"]]
            .str.upper()
            .str.strip()
        )
        df_comissoes[COLUNAS_CRIADAS["COL_RESSELLERS"]] = (
            df_comissoes[COLUNAS_CRIADAS["COL_RESSELLERS"]].str.upper().str.strip()
        )
        return df_contas_a_receber, df_comissoes
    except FileNotFoundError as e:
        print(
            f"Arquivo temporario de contas a receber ou comissoes não encontrados: {e}"
        )
        exit()
    except Exception as e:
        print(f"Erro: {e}")
        exit()


def merge_planilhas() -> pd.DataFrame:
    """
    Merge entre 'contas_a_receber' e 'comissoes' para obter a taxa de comissao e o nome
    de cada resseler, a partir do seller associado.
    """
    try:
        df_contas_a_receber, df_comissoes = prepara_para_merge()

        df_contas_a_receber = df_contas_a_receber.merge(
            df_comissoes[
                [
                    COLUNAS_CRIADAS["COL_RESSELLERS"],
                    COLUNAS_CRIADAS["COL_SELLERS"],
                    COLUNAS_CRIADAS["COL_COMISSAO"],
                ]
            ],
            left_on=COLUNAS_CRIADAS["COL_NOME_RESSELLER"],
            right_on=COLUNAS_CRIADAS["COL_RESSELLERS"],
            how="left",
        )
        return df_contas_a_receber
    except KeyError as e:
        print(f"Coluna não encontrada: {e}")
        exit()
    except Exception as e:
        print(f"Erro: {e}")
        exit()


def formatacao_pos_merge() -> None:
    """
    Realiza a etapa de finalização do DataFrame após o merge.

    Esta função calcula a coluna final de comissão ('TOTAL DO REPASSE (R$)'),
    remove as colunas auxiliares que foram usadas para o merge, e filtra o
    DataFrame para manter apenas as linhas com sellers válidos.
    """
    try:
        df_contas_a_receber = merge_planilhas()

        valor_comissao = (
            df_contas_a_receber[COLUNAS["COL_VALOR_RECEBIDO_PARCELA"]]
            * df_contas_a_receber[COLUNAS_CRIADAS["COL_COMISSAO"]]
        )
        df_contas_a_receber[COLUNAS_CRIADAS["COL_TOTAL_REPASSE"]] = (
            np.trunc(valor_comissao * 100) / 100
        )

        df_contas_a_receber = df_contas_a_receber.drop(
            columns=[
                COLUNAS_CRIADAS["COL_RESSELLERS"],
                COLUNAS_CRIADAS["COL_NOME_RESSELLER"],
            ]
        )

        mascara_sellers_validos = (
            df_contas_a_receber[COLUNAS_CRIADAS["COL_SELLERS"]].notna()
        ) & (df_contas_a_receber[COLUNAS_CRIADAS["COL_SELLERS"]] != "SEM SELLER")
        contas_a_receber_final = df_contas_a_receber[mascara_sellers_validos]

        contas_a_receber_final.to_excel(ARQ_TEMP_CONTASARECEBER_FINAL, index=False)
    except Exception as e:
        print(f"Erro: {e}")
        exit()


def merge_dados() -> None:
    """Orquestra as funções relacionadas ao processo de merge das planilhas."""
    formatacao_pos_merge()
