#  Take Home Test Backend Developer (Django) position at Katekima.

## Task 1
**Implemntasi Linear Feedback Shift Register(LFSR)**  
###### disini saya membuat beberapa mini app untuk implementasi LFSR
1. Implementasi LFSR basic 
    ###### Program ini mengimplementasikan Linear Feedback Shift Register (LFSR) dengan rumus dasar, menghasilkan output yang teracak.
2. Implemntasi LFSR General
    ###### Pada program LFSR General ini, saya telah melakukan optimalisasi dan meningkatkan fleksibilitasnya, memungkinkan pengguna untuk berinteraksi langsung dengan sistem melalui terminal. Pengguna dapat dengan mudah menyesuaikan parameter dan melihat hasilnya secara real-time, menjadikan proses pengacakan lebih dinamis dan dapat disesuaikan dengan kebutuhan. 
3. Ceking semua output dari LFSR basic, genaral, dan output yang diharapkan soal
    ###### Pada program ceking ini, saya melakukan verifikasi terhadap output yang dihasilkan dari berbagai versi program, yaitu LFSR Basic dan LFSR General. Verifikasi ini berpedoman pada output yang telah tersedia pada soal, dengan tujuan untuk memastikan bahwa hasil yang dihasilkan sesuai dengan yang diharapkan. Proses pencocokan dilakukan pada setiap state untuk memastikan bahwa pengacakan berjalan dengan akurat dan konsisten.
###### Hasil Output dapat dilihat di img/LFSR
## Task 2
**Pembuatan app backend menggunakan django-rest-framewoork**  
###### Hasil APInya dapat dilihat pada 
1. img/Items
2. img/Puchasing
3. img/Sell

## Blocks Output report

```
{
    "result": {
        "items": [
            {
                "date": "24-03-2025",
                "description": "Deskripsi Pembelian",
                "code": "P-001",
                "in_qty": 0,
                "in_price": "60000.00",
                "in_total": "0.00",
                "out_qty": 0,
                "out_price": 0,
                "out_total": 0,
                "stock_qty": [
                    0
                ],
                "stock_price": [
                    "60000.00"
                ],
                "stock_total": [
                    "0.00"
                ],
                "balance_qty": 0,
                "balance": "0.00"
            },
            {
                "date": "24-03-2025",
                "description": "Deskripsi Pembelian",
                "code": "P-002",
                "in_qty": 0,
                "in_price": "50000.00",
                "in_total": "0.00",
                "out_qty": 0,
                "out_price": 0,
                "out_total": 0,
                "stock_qty": [
                    0
                ],
                "stock_price": [
                    "50000.00"
                ],
                "stock_total": [
                    "0.00"
                ],
                "balance_qty": 0,
                "balance": "0.00"
            },
            {
                "date": "24-03-2025",
                "description": "Deskripsi Pembelian",
                "code": "S-001",
                "in_qty": 0,
                "in_price": 0,
                "in_total": 0,
                "out_qty": 10,
                "out_price": "50000.00",
                "out_total": "0.00",
                "stock_qty": [
                    0
                ],
                "stock_price": [
                    "50000.00"
                ],
                "stock_total": [
                    "0.00"
                ],
                "balance_qty": 0,
                "balance": 0
            },
            {
                "date": "24-03-2025",
                "description": "Deskripsi Pembelian",
                "code": "S-002",
                "in_qty": 0,
                "in_price": 0,
                "in_total": 0,
                "out_qty": 5,
                "out_price": "50000.00",
                "out_total": "0.00",
                "stock_qty": [
                    0
                ],
                "stock_price": [
                    "50000.00"
                ],
                "stock_total": [
                    "0.00"
                ],
                "balance_qty": 0,
                "balance": 0
            }
        ],
        "item_code": "I-001",
        "name": "History Book",
        "unit": "Pcs",
        "summary": {
            "in_qty": 0,
            "out_qty": 0,
            "balance_qty": 0,
            "balance": 0
        }
    }
}
```




