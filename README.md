# PostureDetection™

PostureDetection™, yapay zeka ve yüz tanıma teknolojilerini kullanarak oturma pozisyonunuzu analiz eden bir uygulamadır. Düzgün oturmadığınızda sesli uyarılar verir, raporlar oluşturur ve sağlığınızı korumanız için öneriler sunar.

## ✨ Özellikler

- 🔍 **Gerçek zamanlı yüz ve omuz pozisyonu analizi** (Dlib kullanarak)
- ✅ **Baş açısı ve mesafe hesaplamaları**
- 🎧 **Sesli uyarı sistemi**
- 📊 **Sağlık raporları oluşturma ve öneriler sunma**
- 🎨 **Animasyonlu bildirim desteği**

## 📸 Ekran Görüntüleri

### 1. **Ana Ekran & Uygulama Arayüzü**
<img width="803" alt="Ekran Resmi 2025-03-03 07 07 15" src="https://github.com/user-attachments/assets/980621bc-7ea3-4466-861c-85910e5aa8da" />


### 2. **Yüz Algılama & Pozisyon Analizi**
<img width="1136" alt="Ekran Resmi 2025-03-03 07 06 48" src="https://github.com/user-attachments/assets/4d1d839d-761f-4460-85a1-f403a9c37064" />


### 3. **Hatalı Oturma Uyarısı**
<img width="1136" alt="Ekran Resmi 2025-03-03 07 06 55" src="https://github.com/user-attachments/assets/1bad9ea8-9bd8-46c1-ac4b-99aa634d9f5e" />


### 4. **Sağlık Raporu Örneği**
<img width="803" alt="Ekran Resmi 2025-03-03 07 07 15" src="https://github.com/user-attachments/assets/b32f8780-4c0b-43d3-bcdb-860a4d5087c4" />


## 🌟 Kullanılan Teknolojiler

- **Python** 
- **OpenCV & Dlib** (Görüntü işleme ve yüz algılama)
- **Tkinter** (Kullanıcı arayüzü)
- **PIL** (Görsel işleme)
- **Subprocess** (Sesli uyarı sistemi)

## ⚡ Kurulum ve Kullanım

1. Gerekli bağımlılıkları yükleyin:
   ```sh
   pip install -r requirements.txt
   ```

2. `shape_predictor_68_face_landmarks.dat` dosyasını [buradan](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2) indirip proje klasörüne ekleyin.

3. Uygulamayı başlatın:
   ```sh
   python main.py
   ```

## 🛠 Sorun Giderme

- **Hata:** `shape_predictor_68_face_landmarks.dat bulunamadı.`  
  **Çözüm:** Dosyanın proje dizinine eklendiğinden emin olun.

- **Hata:** `cv2 module not found.`  
  **Çözüm:** `pip install opencv-python` komutunu çalıştırın.

## ✨ Katkıda Bulunma
Her türlü katkıya açığız! Fork'layıp PR oluşturabilirsiniz. 

## 💌 Lisans
Bu proje **MIT Lisansı** ile lisanslanmıştır.
