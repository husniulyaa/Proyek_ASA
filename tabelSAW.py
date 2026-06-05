from dataProduk import getDataAsli
from skorSAW import hitungSaw

def formatRupiah(nilai):
    return f"Rp{int(nilai):,}".replace(",", "."))

def cetakTabelSaw(df):
    header = (
        f"{'Code':<6}"
        f"{'Shop':<22}"
        f"{'Price':>12}  "
        f"{'Rating':>8}  "
        f"{'Norm Price':>12}  "
        f"{'Norm Rating':>12}  "
        f"{'Score':>10}"
    )
    garis = "-" * len(header)

    print("\nNormalization & SAW Scores")
    print(garis)
    print(header)
    print(garis)

    for _, toko in df.iterrows():
        print(
            f"{toko['Kode']:<6}"
            f"{toko['Toko']:<22}"
            f"{formatRupiah(toko['Harga']):>12}  "
            f"{toko['Rating']:>8.1f}  "
            f"{toko['normHarga']:>12.6f}  "
            f"{toko['normRating']:>12.6f}  "
            f"{toko['skorSAW']:>10.6f}"
        )

    print(garis)

def cetakRankingSaw(df):
    dfRanking = df.sort_values(by="skorSAW", ascending=False).reset_index(drop=True)

    header = (
        f"{'#':<6}"
        f"{'Code':<6}"
        f"{'Shop':<22}"
        f"{'Price':>12}  "
        f"{'Rating':>8}  "
        f"{'Score':>10}"
    )
    garis = "-" * len(header)

    print("\nRanking by Score")
    print(garis)
    print(header)
    print(garis)

    for urutan, toko in dfRanking.iterrows():
        print(
            f"{urutan + 1:<6}"
            f"{toko['Kode']:<6}"
            f"{toko['Toko']:<22}"
            f"{formatRupiah(toko['Harga']):>12}  "
            f"{toko['Rating']:>8.1f}  "
            f"{toko['skorSAW']:>10.6f}"
        )

    print(garis)

def main():
    dfAsli = getDataAsli()
    dfSaw = hitungSaw(dfAsli)

    print("\nCriteria Weights:")
    print("  Price : 50% (lower = better)")
    print("  Rating: 50% (higher = better)")
    print(f"\n  Min Price: {formatRupiah(dfSaw['Harga'].min())}")
    print(f"  Max Rating: {dfSaw['Rating'].max():.1f}")

    cetakTabelSaw(dfSaw)
    cetakRankingSaw(dfSaw)

if __name__ == "__main__":
    main()
