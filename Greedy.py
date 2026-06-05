def algoritmaGreedy(df):
    # Ambil toko dengan skor SAW tertinggi
    tokoTerbaik = df.sort_values(by="skorSAW", ascending=False).iloc[0]
    return tokoTerbaik
