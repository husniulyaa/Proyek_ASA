def hitung_saw(df):
    bobot={
        "Harga": 0.5,
        "Rating": 0.5
    }

    minHarga = df["Harga"].min()
    maxRating = df["Rating"].max()
    df["normalisasiHarga"] = minHarga/df["Harga"]
    df["normalisasiRating"] = df["Rating"]/maxRating
    
    df["skorSAW"] = (df["normalisasiHarga"]*bobot["Harga"] + df["normalisasiRating"]*bobot["Rating"])

    return df
