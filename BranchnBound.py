import heapq

def BranchandBound(df):
    pq = []
    maxSkor = df["skorSAW"].max()
    root = {
        "level": 0,
        "skor": 0,
        "toko": None,
        "bound": maxSkor
    }

    heapq.heappush(pq, (-root["bound"], root))
    bestSkor = 0
    bestToko = None
    while len(pq) > 0:
        now = heapq.heappop(pq)[1]
        if now["bound"] <= bestSkor:
            continue
        if now["level"] >= len(df):
            continue

        row = df.iloc[now["level"]]
        pilihSkor = row["skorSAW"]
        if pilihSkor > bestSkor:
            bestSkor = pilihSkor
            bestToko = row["Toko"]

        childPilih = {
            "level": now["level"] + 1,
            "skor": pilihSkor,
            "toko": row["Toko"],
            "bound": pilihSkor
        }

        sisa = df.iloc[now["level"] + 1:]
        if len(sisa) > 0:
            boundTidak = sisa["skorSAW"].max()
        else:
            boundTidak = 0

        childTidak = {
            "level": now["level"] + 1,
            "skor": now["skor"],
            "toko": now["toko"],
            "bound": boundTidak
        }

        if childPilih["bound"] > bestSkor:
            heapq.heappush(pq, (-childPilih["bound"], childPilih))
        if childTidak["bound"] > bestSkor:
            heapq.heappush(pq, (-childTidak["bound"], childTidak))

    return bestToko