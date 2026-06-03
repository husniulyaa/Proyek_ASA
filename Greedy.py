def Greedy(df):
    hasil = df.sort_values(by="skorSAW", ascending=False).iloc[0]
    return hasil