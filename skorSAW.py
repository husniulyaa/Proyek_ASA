def hitungSaw(df):
    # Hitung skor SAW
    dfHasil = df.copy()
    
    hargaMinimum = dfHasil["Harga"].min()
    ratingMaksimum = dfHasil["Rating"].max()
    
    dfHasil["normHarga"] = hargaMinimum / dfHasil["Harga"]
    dfHasil["normRating"] = dfHasil["Rating"] / ratingMaksimum
    
    dfHasil["skorSAW"] = (dfHasil["normHarga"] * 0.5) + \
                         (dfHasil["normRating"] * 0.5)
                         
    return dfHasil
