import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from scipy.stats import norm, zscore


st.title('Calculadora amostral')

tab1, tab2 = st.tabs(["🧪 Teste AB", "🔎 Amostra Representativa"])

tab1.subheader("Calculadora para Testes AB")
periodo = tab1.number_input('### Qual o período do teste em dias?', value=15, min_value= 7, label_visibility="visible")

direcao = tab1.text_input('### O teste tem por objetivo um aumento ou queda do indicador? (A / Q)', value='A')

tab1.write(f'### Insira algumas estatísticas sobre o indicador que deseja medir (em um período de {periodo} dias):')
tab1.write(f'##### Obs.: Considere um período recente mas que não esteja ocorrendo outros testes ou fatores importantes')


minimo = tab1.number_input('Valor mínimo', 0.3)
media = tab1.number_input('Valor médio', 0.40)
maximo = tab1.number_input('Valor máximo', 0.60)

iqr = maximo - minimo
media_aparada = ((periodo * media) - minimo - maximo)/(periodo - 2)

var_s = abs((maximo / media_aparada) -1)
var_i = abs((minimo / media_aparada) -1)
var = (((var_s + var_i )/2)/2)

tab1.write(f'###### A média sem influência dos valores mínimo e máximo é: {round(media_aparada, 2)}')


#incremento_bau = ((float(maximo) * 1.2) - float(media)) #depois melhorar esse valor para ter mais inteligência


if direcao == 'A':
    #ls = round(media + incremento_bau, 2)
    ls = round(media_aparada * (1 + var), 2)
else:
    #ls = round(media - incremento_bau, 2)
    ls = round(media_aparada * (1 - var), 2)

concorda = tab1.text_input(f'##### O indicador terá um patamar acima da média se atingir um valor médio de {str(ls)}. Deseja manter esse valor de comparação? (S/N)')


if concorda == 'S':
    valor2 = ls
else:
    valor2 = tab1.number_input('Qual valor você espera atingir no teste (que fará você pensar "😯 Uau, este teste funcionou"?')

power = tab1.number_input('Insira o poder do teste', value = 0.95)
sig = tab1.number_input('Insira a significância', value = 0.05)

def sample_power_probtest(p1, p2, power=power, sig=sig):
    z = norm.isf([sig/2]) #two-sided t test
    zp = -1 * norm.isf([power]) 
    d = (p1-p2)
    s =2*((p1+p2) /2)*(1-((p1+p2) /2))
    n = s * ((zp + z)**2) / (d**2)
    return int(round(n[0]))

valor_amostras = sample_power_probtest(media, valor2)
tab1.write(f'### O valor da amostra é: {valor_amostras} para cada público A e B')


tab2.subheader("Calculadora para amostra representativa")
tab2.write('👷🏽‍♀️ Estamos trabalhando nisso')