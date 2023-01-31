# -*- coding: utf-8 -*-
# Commented out IPython magic to ensure Python compatibility.
#%writefile app.py 
import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Análise estatística")

# Adicionando o selectbox à sidebar
st.sidebar.title("Selecione o Trade System")
opcoes = ['BB - Fechou Fora, Fechou Dentro', 'Canal de Keltner', 'Cão Farejador', 'Cruzamento Di+ Di-', 'Cruzamento MMA 17x34', 'Dave Landry', 
'Estocástico Lento 70x30', 'Estocástico Lento 80x20', 'Gambitti', 'Gasparini', 'HiLo 7 períodos', 'IFR2 (Larry Connors)', 
'IFR2 com filtro IFR14', 'IFR4 (Larry Connors)', 'InsideBar', 'Joe Biden (com filtro MMA 20)', 'Joe Biden (sem filtros)', 
'Linha das sombras', 'Máximas e Mínimas', 'Medias 3 min/max ( Larry Williams)', 'Perdigão', 'Preço de Fechamento de Reversão', 
'Sistema MMA 9', 'Stop ATR 10 períodos', 'Terminator (Larry Connors)', 'Tik Tok (com filtro)', 'TikTok', 'Turtle' ]
opcao_selecionada = st.sidebar.selectbox("Escolha uma opção:", opcoes)

st.sidebar.title("Time Frame")
time_frame = st.sidebar.selectbox("Escolha o Time Frame", ["Diário", "60 m"])

# Adicionando campos de data
st.sidebar.title("Período")
data_inicio = st.sidebar.date_input("Data início")
data_fim = st.sidebar.date_input("Data término")

amostra = 200

# Atribuir a base de dados ao sistema operacional selecionado
if st.sidebar.button("EXECUTAR"):    
    if opcao_selecionada == "Sistema MMA 9":
        df = pd.read_excel('\gasparini.xlsx')
        amostra = int(df.shape[0] * 0.15)
    elif opcao_selecionada == "Canal de Keltner":
        df = pd.read_excel('\gasparini.xlsx')
        amostra = int(df.shape[0] * 0.15)
          

    else:
        df = pd.read_excel('gasparini.xlsx')

    st.sidebar.title(opcao_selecionada)
     # Mostrando a opção selecionada pelo usuário
    st.write("Sistema:", opcao_selecionada, "Time Frame:", time_frame , "Período de:", data_inicio, "até", data_fim)
    # código para configurar a df e fazer os cálculos
    # importa a tabela

    
    amostra1 = amostra + 1
    random_rows = df.sample(amostra)
    random_rows["Lucro Acumulado"] = random_rows["Lucro"].cumsum()
    random_rows['Contagem'] = range(1,amostra1)


    contagem_lucro_positivo = (random_rows["Lucro"] > 0).sum()
    media_lucro = df[df["Lucro"] > 0]["Lucro"].mean()
    media_prejuizo = df[df["Lucro"] < 0]["Lucro"].mean()
    payoff = media_lucro/-media_prejuizo
    tx_erro = 1-contagem_lucro_positivo/amostra
    exp_mat = (media_lucro * (1 - tx_erro) + media_prejuizo * tx_erro)/100
    expmat_total = exp_mat * amostra

    
    # Cálculo básico
    st.markdown("Taxa de acerto = **{:.2f}%**".format(round(contagem_lucro_positivo/amostra*100, 2)))
    st.markdown("PayOff = **{:.2f}**".format(round(payoff, 2)))
    st.markdown("Expectativa Matemática = **{:.2f}%** por trade".format(round(exp_mat, 2)))
    st.markdown("Expectativa Matemática Total = **{:.2f}%**".format(round(expmat_total, 2)))


    #calculando Drawdown
    random_rows["Lucro Acumulado"] = random_rows["Lucro"].cumsum()
    random_rows["Drawdown"] = random_rows["Lucro Acumulado"].cummin() - random_rows["Lucro Acumulado"]
    
    st.title("Curva de Capital")
    # plotando gráfico
    fig, ax = plt.subplots()
    ax.plot(random_rows['Contagem'], random_rows['Lucro Acumulado'])
    st.pyplot()
  
    # TESTE MONTE CARLO configuração do teste
    n_simulacoes = 100

    # cria um vetor para armazenar os resultados
    resultados = np.zeros((n_simulacoes, amostra))

    # loop para simulações
    for i in range(n_simulacoes):
        # gera amostras aleatórias
        random_rows = df.sample(amostra)
        random_rows["Lucro Acumulado"] = random_rows["Lucro"].cumsum()
       # armazena os resultados
        resultados[i, :] = random_rows["Lucro Acumulado"]
    st.title("Monte Carlo")
    # plotando gráfico
    plt.figure()
    plt.plot(resultados.T)
    
    st.pyplot()
    pass
