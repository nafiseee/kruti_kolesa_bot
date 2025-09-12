import pandas as pd
df = pd.read_excel('works_norm.xlsx',names = ['work','time','type','sale','group'])
df_spare = pd.read_excel('spares.xlsx',names = ['spare','type','group'])