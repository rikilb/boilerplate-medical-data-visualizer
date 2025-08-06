import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv("medical_examination.csv")

# 2
def asignar_sobrepeso(fila): 
    peso = fila["weight"]
    altura = fila["height"]/100
    imc = peso/((altura)**2)
    if imc > 25:
        return 1
    else:
        return 0
    
df['overweight'] = df.apply(asignar_sobrepeso, axis=1) #np.where((df["weight"]/(df["height"]/100)**2) > 25, 1, 0) # ** para exponentes en pandas
#El método apply genera un bucle y le pasa cada fila como argumentos a la funcion,con axis=0 le paso la columna


# 3
df["cholesterol"] = np.where(df["cholesterol"] > 1, 1, 0) #(df['cholesterol'] > 1).astype(int)
df["gluc"] = np.where(df["gluc"] > 1, 1, 0) #(df['gluc'] > 1).astype(int)

# 4
def draw_cat_plot():
    # 5
    df_cat = pd.melt(df,id_vars=["cardio"],value_vars=["cholesterol","gluc","smoke","alco","active","overweight"])


    # 6
    df_cat = df_cat.groupby(["cardio","variable","value"]).size().reset_index(name="total")
    

    # 7
    figura = sns.catplot(
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        data=df_cat,
        kind='bar'
    )

    # 8
    fig = figura.fig


    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    df_heat = df[(df["ap_lo"]<=df["ap_hi"]) & (df['height'] >= df['height'].quantile(0.025))
                          & (df['height'] <= df['height'].quantile(0.975)) 
                          & (df['weight'] <= df['weight'].quantile(0.975))
                          & (df['weight'] >= df['weight'].quantile(0.025))]

    # 12
    corr = df_heat.corr() #Asi se crea la matriz de correlacion

    # 13
    mask = np.triu(np.ones_like(corr, dtype=bool)) #Máscara para eliminar datos del triangulo superior y que no aparezcan en el heatmap (Datos redundantes)



    # 14
    fig, ax = plt.subplots()

    # 15
    sns.heatmap(
        corr,
        annot=True,
        fmt=".1f",
        cmap="coolwarm",
        center=0,
        linewidths=.5,
        cbar_kws={'shrink':.5},
        ax=ax,
        mask=mask
    )


    # 16
    fig.savefig('heatmap.png')
    return fig
