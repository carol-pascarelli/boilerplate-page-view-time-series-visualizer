import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

# Registrar conversores do Matplotlib para lidar com datas
register_matplotlib_converters()

# Carregar os dados do CSV, parseando a coluna 'date' como um objeto de data e definindo-a como índice
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')

# Filtrar os dados para remover valores extremos (fora dos percentis 2.5% e 97.5%)
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

# Ordem dos meses, para garantir a correta sequência nos gráficos
months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def draw_line_plot():
    # Desenha o gráfico de linha
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(df.index, df['value'], color='red', label='Page Views')
    
    # Definir título e rótulos
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")  # Certifique-se de que o rótulo seja "Date"
    ax.set_ylabel("Page Views")
    ax.legend()

    # Salvar e retornar a figura
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Criar uma cópia do DataFrame original para o gráfico de barras
    df_bar = df.copy()
    
    # Extrair o nome dos meses e o ano das datas no índice
    df_bar['month'] = df_bar.index.month_name()
    df_bar['year'] = df_bar.index.year
    
    # Organizar os dados em formato de tabela pivot, agrupando por ano e mês
    df_pivot = pd.pivot_table(df_bar, values='value', index='year', columns='month', aggfunc='mean')
    
    # Ajustar a ordem das colunas para seguir a sequência dos meses
    df_pivot = df_pivot.reindex(columns=months_order)

    # Criar o gráfico de barras
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Plotar a tabela pivot como gráfico de barras
    df_pivot.plot(kind='bar', ax=ax)
    
    # Definir os rótulos dos eixos e a legenda
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months", labels=months_order, loc='upper left')

    # Salvar a imagem do gráfico
    fig.savefig('bar_plot.png')
    
    return fig

def draw_box_plot():
    # Preparar os dados para os gráficos de box plot
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    
    # Extrair ano e mês da coluna 'date'
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    
    # Configurar os subplots para os dois gráficos de box plot
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))

    # Box plot por ano, para visualizar tendências gerais ao longo dos anos
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    axes[0].set_title("Year-wise Box Plot (Trend)")

    # Box plot por mês, para visualizar a sazonalidade nos dados
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    # Salvar a imagem dos box plots
    fig.savefig('box_plot.png')
    
    return fig
