import random

def hillClimbOnce(df, indeksAwal, jumlahTetangga=100):
    # Proses HC sekali dari titik awal
    indeksSekarang = indeksAwal
    skorSekarang = df.iloc[indeksSekarang]["skorSAW"]
    
    daftarIndeks = list(range(len(df)))
    
    while True:
        adaPerbaikan = False
        skorTetanggaTerbaik = skorSekarang
        indeksTetanggaTerbaik = indeksSekarang
        
        calonTetangga = random.sample(daftarIndeks, min(jumlahTetangga, len(daftarIndeks)))
        
        for indeks in calonTetangga:
            if indeks == indeksSekarang:
                continue
                
            skorTetangga = df.iloc[indeks]["skorSAW"]
            
            if skorTetangga > skorTetanggaTerbaik:
                skorTetanggaTerbaik = skorTetangga
                indeksTetanggaTerbaik = indeks
                adaPerbaikan = True
        
        if adaPerbaikan:
            indeksSekarang = indeksTetanggaTerbaik
            skorSekarang = skorTetanggaTerbaik
        else:
            break
            
    return df.iloc[indeksSekarang]

def algoritmaHillClimbing(df, maxRestart=10):
    # Cari toko terbaik dengan HC & random restart
    tokoTerbaik = None
    skorTerbaik = -1
    
    for _ in range(maxRestart):
        indeksAwal = random.randint(0, len(df) - 1)
        hasilLokal = hillClimbOnce(df, indeksAwal)
        
        if hasilLokal["skorSAW"] > skorTerbaik:
            skorTerbaik = hasilLokal["skorSAW"]
            tokoTerbaik = hasilLokal
            
    return tokoTerbaik
