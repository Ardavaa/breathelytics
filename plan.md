# Breathelytics: Aplikasi Analisis Suara Pernapasan berbasis AI

## 1. Deskripsi Aplikasi yang Akan Dibuat

Aplikasi yang akan kami kembangkan adalah sebuah platform berbasis web terdesentralisasi bernama **Breathelytics** yang memanfaatkan teknologi Machine Learning untuk menganalisis suara pernapasan guna mendeteksi potensi kondisi pernapasan yaitu COPD, Healthy, URTI, Bronchiectasis, dan Pneumonia. Breathelytics mengintegrasikan model *machine learning* berbasis *deep learning* (Convolutional Neural Network/CNN) yang dilatih menggunakan fitur audio seperti MFCC, Chroma STFT, dan Mel Spectrogram, serta *Large Language Model* (LLM) untuk memberikan interpretasi hasil analisis dalam bahasa yang mudah dipahami pengguna.

Kode yang telah dikembangkan mencakup *pipeline* pemrosesan audio, pelatihan model, dan inferensi menggunakan format ONNX, yang memungkinkan aplikasi ini untuk dijalankan secara portabel dan efisien. Aplikasi ini akan diakses melalui antarmuka web sederhana, memungkinkan pengguna mengunggah file audio pernapasan, mendapatkan hasil analisis, dan menerima rekomendasi awal berdasarkan diagnosis yang diprediksi.

## 2. Fungsi-Fungsi yang Minimal Harus Ada pada Aplikasi

Berdasarkan kode yang ada dan kebutuhan proyek, berikut adalah fungsi-fungsi minimal yang harus ada pada aplikasi Breathelytics:

1. **Upload dan Pemrosesan Audio**  
   - Pengguna dapat mengunggah file audio (format WAV) melalui antarmuka web.
   - Sistem akan memproses audio dengan mengekstrak fitur seperti MFCC, Chroma STFT, dan Mel Spectrogram menggunakan library `librosa`, serta menyesuaikan panjang audio ke durasi tetap (6 detik) untuk konsistensi analisis.

2. **Prediksi Penyakit Pernapasan**  
   - Model Deep Learning (CNN yang diekspor ke ONNX) akan menganalisis fitur audio yang diekstrak untuk memprediksi kelas penyakit pernapasan (COPD, Healthy, URTI, Bronchiectasis, dan Pneumonia).
   - Hasil prediksi akan mencakup indeks kelas yang diprediksi dan probabilitas untuk setiap kelas.

3. **Interpretasi Hasil**  
   - Menggunakan LLM (dapat diintegrasikan di masa depan), aplikasi akan memberikan penjelasan sederhana tentang hasil prediksi dalam bahasa yang ramah pengguna, misalnya: "Berdasarkan analisis suara pernapasan Anda, terdeteksi kemungkinan COPD dengan probabilitas 60%. Segera konsultasikan ke dokter untuk pemeriksaan lebih lanjut."

4. **Penyimpanan dan Portabilitas Model**  
   - Model disimpan dalam format ONNX untuk portabilitas dan efisiensi inferensi, serta *pipeline* inferensi diserialisasi menggunakan `pickle` untuk memudahkan penggunaan ulang.

5. **Antarmuka Pengguna Berbasis Web**  
   - Antarmuka sederhana yang memungkinkan pengguna mengunggah audio, melihat hasil prediksi, dan mengunduh laporan jika diperlukan.

## 3. Rencana Bagian Program yang Akan Menggunakan OOP dan/atau FP

Kami merencanakan penggunaan paradigma pemrograman berikut untuk mengoptimalkan struktur dan fungsionalitas aplikasi:

### a. Object-Oriented Programming (OOP)

OOP akan digunakan untuk mengorganisasi kode secara modular dan memudahkan pengelolaan komponen aplikasi. Berikut adalah bagian-bagian yang akan memanfaatkan OOP:

1. **Kelas `AudioInferencePipeline`**  
   - **Deskripsi**: Kelas ini mengenkapsulasi seluruh *pipeline* inferensi, termasuk pemrosesan audio, inferensi model ONNX, dan prediksi kelas. Atribut seperti `onnx_model_path`, `max_len`, `sr`, dan metode seperti `preprocess` dan `predict` dikelola dalam satu objek.


2. **Kelas Model CNN (`MFCCModel`, `CromaModel`, `MSpecModel`)**  
   - **Deskripsi**: Model *deep learning* dibangun sebagai kelas-kelas yang mewarisi `nn.Module`, dengan lapisan-lapisan seperti konvolusi, *batch normalization*, dan *pooling* didefinisikan dalam metode `__init__`. Logika inferensi diatur dalam metode `forward`.

3. **Kelas Dataset (`AudioDataset`)**  
   - **Deskripsi**: Kelas ini mengelola data pelatihan dan validasi dalam format PyTorch `Dataset`, dengan metode `__len__` dan `__getitem__` untuk mengakses fitur audio dan label.

4. **Rencana Ekstensi**:  
   - **Kelas `WebInterface`**: Untuk mengelola logika antarmuka web (unggah file, tampilan hasil).
   - **Kelas `ResultInterpreter`**: Untuk mengintegrasikan LLM dan menghasilkan penjelasan hasil prediksi.

### b. Functional Programming (FP)

FP akan digunakan untuk memproses data secara deklaratif dan meminimalkan efek samping, terutama pada bagian pemrosesan audio dan transformasi data. Berikut adalah rencananya:

1. **Fungsi `preprocess_audio` dan `getFeatures`**  
   - **Deskripsi**: Fungsi-fungsi ini murni (*pure functions*) yang menerima input audio dan mengembalikan fitur seperti MFCC, Chroma STFT, dan Mel Spectrogram tanpa mengubah *state* eksternal.
   - **Keunggulan FP**: Fungsi ini idempoten dan mudah diuji, memastikan konsistensi hasil pemrosesan.

2. **Fungsi `softmax`**  
   - **Deskripsi**: Fungsi ini mengubah *logits* menjadi probabilitas secara deterministik tanpa efek samping.
   - **Keunggulan FP**: Memudahkan *debugging* dan komposisi dengan fungsi lain.

3. **Rencana Ekstensi**:  
   - **Fungsi Transformasi Data**: Fungsi tambahan untuk normalisasi atau augmentasi audio (misalnya, `normalize_audio`, `add_noise`) akan ditulis sebagai *pure functions*.
   - **Pipeline Pemrosesan**: Menggunakan komposisi fungsi untuk menggabungkan langkah-langkah pemrosesan (contoh: `predict = softmax ∘ run_inference ∘ preprocess`).

### c. Kombinasi OOP dan FP

Kami akan menggabungkan kedua paradigma untuk memaksimalkan kelebihan masing-masing:
- **OOP untuk Struktur Besar**: Kelas seperti `AudioInferencePipeline` akan mengelola *state* dan logika tingkat tinggi (misalnya, inisialisasi model ONNX).
- **FP untuk Pemrosesan Data**: Fungsi-fungsi dalam kelas (misalnya, `preprocess`) akan ditulis dengan prinsip FP untuk memastikan keandalan dan kemudahan pemeliharaan.
- **Contoh Implementasi**: Metode `predict` dalam `AudioInferencePipeline` memanggil fungsi `preprocess` (FP) dan kemudian menjalankan inferensi pada model yang dikelola sebagai objek (OOP).