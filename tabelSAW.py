from dataProduk import df as dataShopee
from skorSAW import hitung_saw


def formatRupiah(nilai):
    return f"Rp{int(nilai):,}".replace(",", ".")

def cetakTabelSAW(df):
    header = (
        f"{'Kode':<6}"
        f"{'Toko':<22}"
        f"{'Harga':>12}  "
        f"{'Rating':>8}  "
        f"{'Norm Harga':>12}  "
        f"{'Norm Rating':>12}  "
        f"{'Skor SAW':>10}"
    )
    garis = "-" * len(header)

    print("TABEL HASIL NORMALISASI DAN PERHITUNGAN SKOR SAW")
    print(garis)
    print(header)
    print(garis)

    for i, row in df.iterrows():
        print(
            f"{row['Kode']:<6}"
            f"{row['Toko']:<22}"
            f"{formatRupiah(row['Harga']):>12}  "
            f"{row['Rating']:>8.1f}  "
            f"{row['normalisasiHarga']:>12.6f}  "
            f"{row['normalisasiRating']:>12.6f}  "
            f"{row['skorSAW']:>10.6f}"
        )

    print(garis)

def cetakRankingSAW(df):
    dfRanking = df.sort_values(by="skorSAW", ascending=False).reset_index(drop=True)

    header = (
        f"{'Rank':<6}"
        f"{'Kode':<6}"
        f"{'Toko':<22}"
        f"{'Harga':>12}  "
        f"{'Rating':>8}  "
        f"{'Skor SAW':>10}"
    )
    garis = "-" * len(header)

    print("\nTABEL RANKING TOKO BERDASARKAN SKOR SAW")
    print(garis)
    print(header)
    print(garis)

    for i, row in dfRanking.iterrows():
        print(
            f"{i + 1:<6}"
            f"{row['Kode']:<6}"
            f"{row['Toko']:<22}"
            f"{formatRupiah(row['Harga']):>12}  "
            f"{row['Rating']:>8.1f}  "
            f"{row['skorSAW']:>10.6f}"
        )

    print(garis)

def main():
    dfSaw = hitung_saw(dataShopee.copy())

    print("Bobot kriteria:")
    print("- Harga  : 0.5 (cost)")
    print("- Rating : 0.5 (benefit)\n")

    print(f"Nilai minimum Harga  : {formatRupiah(dfSaw['Harga'].min())}")
    print(f"Nilai maksimum Rating: {dfSaw['Rating'].max():.1f}\n")

    cetakTabelSAW(dfSaw)
    cetakRankingSAW(dfSaw)

if __name__ == "__main__":
    main()
