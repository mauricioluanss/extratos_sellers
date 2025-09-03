import pandas as pd

from .config import (
    ARQ_CONTASARECEBER,
    ARQ_COMISSOES,
    ARQ_TEMP_CONTASARECEBER,
    ARQ_TEMP_COMISSOES,
    COLUNAS,
)


def carrega_contas_a_receber() -> None:
    try:
        df = pd.read_excel(
            ARQ_CONTASARECEBER, usecols=list(COLUNAS.values()), decimal=","
        )
        df.columns = df.columns.str.strip()

        df.to_excel(ARQ_TEMP_CONTASARECEBER, index=False)
    except FileNotFoundError as e:
        print(f"O arquivo {ARQ_CONTASARECEBER} não foi encontrado\n: {e}")
        exit()
    except Exception as e:
        print(f"Erro: {e}")
        exit()


def carrega_comissoes() -> None:
    try:
        df = pd.read_excel(ARQ_COMISSOES, sheet_name=None)
        df_comissoes = df["comissoes"]
        df_comissoes.columns = df_comissoes.columns.str.strip()

        df_comissoes.to_excel(ARQ_TEMP_COMISSOES, index=False)
    except FileNotFoundError as e:
        print(f"Arquivo {ARQ_COMISSOES} não encontrado\n: {e}")
        exit()
    except Exception as e:
        print(f"Erro: {e}")
        exit()


def carrega_planilhas() -> None:
    carrega_contas_a_receber()
    carrega_comissoes()
