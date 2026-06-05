import heapq

def algoritmaBranchAndBound(df):
    # Cari toko terbaik dengan Branch and Bound
    antrianPrioritas = []
    batasSkorAwal = df["skorSAW"].max()
    
    akar = {
        "level": 0,
        "skor": 0,
        "toko": None,
        "bound": batasSkorAwal
    }
    
    heapq.heappush(antrianPrioritas, (-akar["bound"], akar))
    
    skorTerbaik = -1
    tokoTerbaik = None
    
    while len(antrianPrioritas) > 0:
        boundNegatif, nodeSekarang = heapq.heappop(antrianPrioritas)
        boundSekarang = -boundNegatif
        
        if boundSekarang <= skorTerbaik:
            continue
            
        if nodeSekarang["level"] >= len(df):
            continue
            
        toko = df.iloc[nodeSekarang["level"]]
        skorPilih = toko["skorSAW"]
        
        if skorPilih > skorTerbaik:
            skorTerbaik = skorPilih
            tokoTerbaik = toko["Toko"]
            
        cabangPilih = {
            "level": nodeSekarang["level"] + 1,
            "skor": skorPilih,
            "toko": toko["Toko"],
            "bound": skorPilih
        }
        
        sisaData = df.iloc[nodeSekarang["level"] + 1:]
        if len(sisaData) > 0:
            boundTidak = sisaData["skorSAW"].max()
        else:
            boundTidak = 0
            
        cabangTidak = {
            "level": nodeSekarang["level"] + 1,
            "skor": nodeSekarang["skor"],
            "toko": nodeSekarang["toko"],
            "bound": boundTidak
        }
        
        if cabangPilih["bound"] > skorTerbaik:
            heapq.heappush(antrianPrioritas, (-cabangPilih["bound"], cabangPilih))
             
        if cabangTidak["bound"] > skorTerbaik:
            heapq.heappush(antrianPrioritas, (-cabangTidak["bound"], cabangTidak))

    return df[df["Toko"] == tokoTerbaik].iloc[0]
