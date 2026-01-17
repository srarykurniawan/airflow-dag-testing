## 🛠 Airflow DAG Testing Assignment - Data Validation & Configuration  
 
Project ini bertujuan untuk membuat dan menguji sebuah Apache Airflow DAG yang menerapkan proses data validation sederhana menggunakan pendekatan best practice testing, meliputi:

Unit testing per task  
Integration testing untuk keseluruhan DAG  

DAG dirancang agar:  
- Dapat diuji secara terisolasi  
- Tetap berjalan normal saat dieksekusi penuh  
- Aman terhadap kegagalan XCom saat mode testing  

## 📂 Struktur Project  
airflow-dag-testing-assignment/  
├── dags/  
│   ├── dag_testing_assignment.py  
│   └── tests/  
│       └── test_dag_testing_assignment.py  
├── docker-compose.yml  
└── README.md  

## ⚙️ Spesifikasi DAG  
- ✅ Konfigurasi	Nilai
- ✅ DAG ID	data_validation_dag
- ✅ Schedule	@daily
- ✅ Owner	data-engineering-team
- ✅ Retries	2
- ✅ Retry Delay	5 menit
- ✅ Catchup	Disabled
- ✅ Start Date	Static (untuk testing)

🔄 Alur DAG  
extract_task → transform_task → load_task    
1️⃣ extract_task    
Menghasilkan data dummy berbentuk list of dictionary    
Data otomatis disimpan ke XCom    
Contoh output:  
[  {"name": "apple"},  
  {"name": "banana"},  
  {"name": "orange"}  ]  
2️⃣ transform_task      
- Mengambil data dari XCom (extract_task)    
- Melakukan transformasi dengan mengubah nilai menjadi uppercase    
- Fallback mechanism:  
- Jika XCom tidak tersedia (mode airflow tasks test), task tetap berjalan dengan data dummy  
Contoh output:  
[  {"name": "APPLE"},  
  {"name": "BANANA"},  
  {"name": "ORANGE"}  ]  
3️⃣ load_task
- Melakukan validasi akhir    
- Memastikan data tidak kosong sebelum dianggap sukses    
🧪 Testing Strategy    
🔹 Unit Testing (Task-level)  
Digunakan untuk memastikan setiap task dapat berjalan secara mandiri.  
- Test extract_task  
### - airflow tasks test data_validation_dag extract_task 2025-10-22  
- Test transform_task  
### - airflow tasks test data_validation_dag transform_task 2025-10-22  

Catatan:
Saat unit test, XCom tidak tersedia sehingga transform_task menggunakan fallback data secara otomatis.  
🔹 Integration Testing (Full DAG)  
Digunakan untuk memastikan seluruh dependency dan XCom berjalan normal.  
### - airflow dags test data_validation_dag 2025-10-22  
Hasil:  
DagRun Finished
state=success

## 🧠 Best Practice yang Diterapkan
✅ Task idempotent & testable  
✅ XCom handling yang aman  
✅ Tidak bergantung pada scheduler untuk testing  
✅ DAG dapat dijalankan ulang tanpa side-effect  
✅ Struktur kode rapi & mudah dirawat  

## 🚀 Cara Menjalankan Project  
1️⃣ Jalankan Airflow  
docker compose up -d  
2️⃣ Masuk ke container Airflow  
docker exec -it airflow bash  
3️⃣ Inisialisasi Database (jika diperlukan)  
airflow db init  
4️⃣ Jalankan Testing  
Gunakan perintah unit test dan integration test seperti pada bagian Testing Strategy.  

## 📎 Catatan Tambahan
Project ini menggunakan SQLite sebagai metadata database (default Airflow)
File test berbasis pytest disediakan untuk validasi DAG parsing
DAG dirancang agar kompatibel dengan environment Docker-based Airflow

## ✅ Kesimpulan  
DAG data_validation_dag telah berhasil:
- Didefinisikan sesuai requirement
- Diuji secara unit dan integrasi
- Dijalankan tanpa error
- Memenuhi standar praktik Data Engineering menggunakan Apache Airflow
