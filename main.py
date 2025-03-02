import cv2
import dlib
import math
import subprocess
from tkinter import Tk, Label, Button, Toplevel, Text, Scrollbar, RIGHT, Y, END, Frame
from PIL import Image, ImageTk, ImageSequence
import threading
import webbrowser
import random
from datetime import datetime

detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

baseline_angle = None
baseline_distance = None
sound_process = None
running = True
not_sitting_properly_duration = 0
timer_running = False
reports = []


def calculate_head_angle(landmarks):
    nose = landmarks[33]
    chin = landmarks[8]
    dx = chin[0] - nose[0]
    dy = chin[1] - nose[1]
    angle = math.degrees(math.atan2(dy, dx))
    return angle


def calculate_distance(landmarks):
    left_shoulder = landmarks[2]
    right_shoulder = landmarks[14]
    distance = math.sqrt((right_shoulder[0] - left_shoulder[0])**2 +
                         (right_shoulder[1] - left_shoulder[1])**2)
    return distance


def play_alert_sound():
    global sound_process
    if sound_process is None or sound_process.poll() is not None:
        try:
            sound_process = subprocess.Popen(["afplay", "alert.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"Ses çalma hatası: {e}")


def stop_alert_sound():
    global sound_process
    if sound_process and sound_process.poll() is None:
        sound_process.terminate()
        sound_process = None


def animate_gif(label, gif_frames, delay):
    """GIF animasyonunu döngü halinde çalıştırır."""
    def loop(index):
        if not running:
            return
        frame = gif_frames[index]
        label.config(image=frame)
        label.image = frame
        label.after(delay, loop, (index + 1) % len(gif_frames))

    loop(0)


def generate_report():
    """Benzersiz bir rapor oluştur."""
    global not_sitting_properly_duration
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    seconds = not_sitting_properly_duration % 60
    minutes = (not_sitting_properly_duration // 60) % 60
    hours = not_sitting_properly_duration // 3600

    duration_text = f"{seconds} saniye"
    if minutes > 0:
        duration_text = f"{minutes} dakika, {seconds} saniye"
    if hours > 0:
        duration_text = f"{hours} saat, {minutes} dakika, {seconds} saniye"

    reasons = [
        "Omurga hizasızlığı ve ağrılara neden olabilir.",
        "Boyun gerginliği ve kas spazmlarını tetikleyebilir.",
        "Kronik sırt ağrılarına yol açabilir.",
        "Akciğer kapasitesini azaltarak solunum sorunlarına neden olabilir.",
        "Dolaşımın yavaşlamasına ve bacaklarda şişmeye neden olabilir.",
        "Göz yorgunluğu ve baş ağrısına neden olabilir.",
        "Konsantrasyon kaybına yol açabilir.",
        "Sindirim sistemini olumsuz etkileyebilir.",
        "Stres seviyesini artırabilir.",
        "Uzun vadede postür bozukluğuna ve kalıcı duruş sorunlarına neden olabilir.",
        "Uyku kalitesini olumsuz etkileyebilir.",
        "Enerji seviyesinde azalmaya neden olabilir.",
        "Kas ve eklemlerde sertlik ve esneklik kaybına yol açabilir.",
        "Karbondioksit birikimini artırarak baş dönmesine neden olabilir.",
        "Eklem kireçlenmesine yol açabilir.",
        "Boyun fıtığı riskini artırabilir.",
    ]
    selected_reasons = random.sample(reasons, 5)

    suggestions = [
        "Ergonomik bir sandalye kullanarak omurganızı destekleyin.",
        "Çalışma aralıklarınızı kısa molalarla bölün.",
        "Ayaklarınızı yere düz basarak oturun.",
        "Göz hizasında bir monitör kullanın.",
        "Sık sık gerinme egzersizleri yaparak kaslarınızı rahatlatın.",
        "Her 30 dakikada bir pozisyonunuzu değiştirin.",
        "Masaj topu kullanarak sırt kaslarınızı rahatlatın.",
        "Yoga veya pilates yaparak duruşunuzu güçlendirin.",
        "Uzun süre hareketsiz kalmamaya özen gösterin.",
        "Ekran parlaklığını uygun seviyede ayarlayın.",
        "Telefon görüşmelerini ayakta yaparak hareket edin.",
        "Çalışma ortamınızı iyi aydınlatın.",
        "Aşırı kafein tüketiminden kaçının, bol su için.",
        "Sırt desteği kullanarak omurga hizanızı koruyun.",
        "Yatak pozisyonunuza dikkat edin, çok yumuşak yataklardan kaçının."
    ]
    selected_suggestions = random.sample(suggestions, 5)

    report_content = f"""
    ==========================================
    PostureDetection™ Sağlık Raporu - {now}
    ==========================================

    📊 **Düzgün Oturulmadığı Süre**:
    {duration_text}

    🚨 **Bu Süre Zarfında Neden Olabilir**:
    {chr(10).join(f"  • {reason}" for reason in selected_reasons)}

    ✅ **Sağlığınızı Koruma Önerilerimiz**:
    {chr(10).join(f"  • {suggestion}" for suggestion in selected_suggestions)}

    ==========================================
    """
    reports.append(report_content)


def show_report():
    """Tüm raporları göster."""
    report_window = Toplevel(root)
    report_window.title("Sağlık Raporu")
    report_window.geometry("800x600")
    report_window.configure(bg="#f8f9fa")

    # Header
    header = Label(report_window, text="PostureDetection™ Tüm Sağlık Raporları", font=("Helvetica", 20, "bold"), bg="#343a40", fg="white", pady=10)
    header.pack(fill="x")

    # Rapor Metni
    report_frame = Frame(report_window, bg="#ffffff")
    report_frame.pack(fill="both", expand=True, padx=20, pady=20)

    report_text = Text(report_frame, wrap="word", font=("Helvetica", 14), bg="#ffffff", fg="black", bd=0)
    scrollbar = Scrollbar(report_frame, command=report_text.yview)
    report_text.configure(yscrollcommand=scrollbar.set)

    report_text.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    for report in reports:
        report_text.insert(END, report + "\n")
    report_text.config(state="disabled")

    # Footer
    footer = Label(report_window, text="© 2025 PostureDetection™ All Rights Reserved.", font=("Helvetica", 12), bg="#343a40", fg="white", pady=10)
    footer.pack(fill="x")

def process_camera_stream(camera_label, status_label, gif_label, explanation_label, gif_frames):
    global baseline_angle, baseline_distance, running, not_sitting_properly_duration, timer_running

    # Baş açısı ve mesafe bilgileri için etiketler
    angle_label = Label(camera_label, text="Baş Açısı: N/A", font=("Helvetica", 14), fg="white", bg="black")
    angle_label.place(x=10, y=50)

    distance_label = Label(camera_label, text="Mesafe: N/A", font=("Helvetica", 14), fg="white", bg="black")
    distance_label.place(x=10, y=80)

    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("WebCam açılamadı! İzinleri kontrol edin.")
        return

    try:
        while running:
            ret, frame = cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)

            for face in faces:
                landmarks = landmark_predictor(gray, face)
                landmarks_points = [(p.x, p.y) for p in landmarks.parts()]

                # Yüz noktalarını çiz
                for point in landmarks_points:
                    cv2.circle(frame, point, 2, (0, 255, 0), -1)

                current_angle = calculate_head_angle(landmarks_points)
                current_distance = calculate_distance(landmarks_points)

                if baseline_angle is None or baseline_distance is None:
                    baseline_angle = current_angle
                    baseline_distance = current_distance
                    print(
                        f"Referans açı ve mesafe kaydedildi: Açı: {baseline_angle:.2f}, Mesafe: {baseline_distance:.2f}")

                angle_difference = abs(current_angle - baseline_angle)
                distance_difference = abs(current_distance - baseline_distance)

                # Güncel açı ve mesafe bilgilerini ekrana yazdır
                angle_label.config(text=f"Baş Açısı: {current_angle:.2f}°")
                distance_label.config(text=f"Mesafe: {current_distance:.2f}px")

                if angle_difference > 5 or distance_difference > 50:
                    status_label.config(text=f"Dik Otur! Süre: {not_sitting_properly_duration} saniye", fg="red",
                                        font=("Helvetica", 16, "bold"))
                    gif_label.place(x=650, y=450)
                    explanation_label.config(text="Lütfen kameraya doğru bir şekilde oturun.", fg="red")
                    play_alert_sound()
                    if not timer_running:
                        timer_running = True
                        threading.Thread(target=count_not_sitting_time).start()
                else:
                    status_label.config(text="Postür Uygun!", fg="green", font=("Helvetica", 16, "bold"))
                    gif_label.place_forget()
                    explanation_label.config(text="")
                    stop_alert_sound()
                    timer_running = False

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            camera_label.config(image=img)
            camera_label.image = img

    except Exception as e:
        print(f"Kamera işleme sırasında hata: {e}")
    finally:
        stop_alert_sound()
        cap.release()

def count_not_sitting_time():
    global not_sitting_properly_duration, timer_running
    while timer_running:
        not_sitting_properly_duration += 1
        threading.Event().wait(1)


def open_camera_window():
    global running, not_sitting_properly_duration
    not_sitting_properly_duration = 0
    running = True
    camera_window = Toplevel(root)
    camera_window.title("Kamera")
    camera_window.geometry("1024x768")
    camera_window.configure(bg='black')

    global camera_label, status_label, gif_label

    camera_label = Label(camera_window)
    camera_label.pack()

    # Sol üstteki durum yazısı
    status_label = Label(camera_window, text="Hazır", font=("Helvetica", 16), fg="white", bg="black")
    status_label.place(x=10, y=10)

    # Alt bilgi yazısı
    info_label = Label(camera_window, text="© 2025 PostureDetection™ All Rights Reserved.",
                       font=("Helvetica", 12), fg="gray", bg="black", cursor="hand2")
    info_label.pack(side="bottom", pady=5)

    # Sağ alt köşedeki GIF
    posture_gif = Image.open("posture_animation.gif")
    gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(posture_gif)]
    gif_label = Label(camera_window, bg="black")

    # Kısa açıklamalar
    explanation_label = Label(camera_window, text="", font=("Helvetica", 14), fg="red", bg="black")
    explanation_label.pack(side="bottom", pady=20)

    # GIF animasyonunu başlat
    animate_gif(gif_label, gif_frames, 100)

    # Kamerayı işlemek için ayrı bir iş parçacığı başlat
    threading.Thread(target=process_camera_stream, args=(camera_label, status_label, gif_label, explanation_label, gif_frames), daemon=True).start()

    # 'q' ile kamera penceresini kapat
    camera_window.bind("<q>", lambda event: close_camera_window(camera_window))


def close_camera_window(camera_window):
    global running, timer_running
    running = False
    timer_running = False
    stop_alert_sound()
    camera_window.destroy()

    # Tek bir rapor oluştur butonu
    if not hasattr(root, "report_button"):
        root.report_button = Button(root, text="Raporları Görüntüle", font=("Helvetica", 14, "bold"), fg="white", bg="#4CAF50",
                                    activebackground="#45a049", command=show_report)
        root.report_button.pack(pady=20)
        root.report_button.bind("<Enter>", lambda event: root.report_button.config(bg="#45a049"))
        root.report_button.bind("<Leave>", lambda event: root.report_button.config(bg="#4CAF50"))
    generate_report()


# Giriş Ekranı
root = Tk()
root.title("Postür Tespiti")
root.geometry("1024x768")
root.configure(bg='black')

# Arka plan GIF
background_gif = Image.open("background.gif")
background_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(background_gif)]
bg_label = Label(root, bg="black")
bg_label.place(relwidth=1, relheight=1)
animate_gif(bg_label, background_frames, 100)

# Başlık
title_label = Label(root, text="Postür Tespiti Uygulamasına Hoş Geldiniz", font=("Helvetica", 24, "bold"), fg="white", bg="black")
title_label.pack(pady=20)

# Kamerayı Başlat Butonu
start_button = Button(root, text="Kamerayı Başlat", font=("Helvetica", 16, "bold"), fg="white", bg="#007BFF",
                      activebackground="#0056b3", command=open_camera_window)
start_button.pack(pady=20)
start_button.bind("<Enter>", lambda event: start_button.config(bg="#0056b3"))
start_button.bind("<Leave>", lambda event: start_button.config(bg="#007BFF"))

root.mainloop()



