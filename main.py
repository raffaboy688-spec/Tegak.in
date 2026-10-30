import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import cv2
import mediapipe as mp
import time
import sys
import numpy as np
import threading
import platform

# Import winsound khusus untuk pengguna Windows
if platform.system() == "Windows":
    import winsound

# Konfigurasi Warna CLI
C = '\033[96m'  # Cyan
G = '\033[92m'  # Green
Y = '\033[93m'  # Yellow
R = '\033[91m'  # Red
X = '\033[0m'   # Reset

# Load MediaPipe
mp_pose = mp.solutions.pose
mp_face_mesh = mp.solutions.face_mesh
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5, refine_landmarks=True)

# --- GLOBAL STATE ---
is_running = False
is_active = True
show_cam = True
cam_scale = 1.0

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_ascii_header():
    header = f"""
{C}  ========================================================={X}
{Y}        _____                _      _       
       |_   _|__  __ _  __ _| | __ (_)_ __  
         | |/ _ \/ _` |/ _` | |/ / | | '_ \ 
         | |  __/ (_| | (_| |   < _| | | | |
         |_|\___|\__, |\__,_|_|\_(_)_|_| |_|
                 |___/                      {X}
{C}         >>> Jaga Postur & Fokusmu Hari Ini! <<<{X}
{C}  ========================================================={X}
"""
    print(header)

def calculate_ear(landmarks, eye_indices):
    top = np.array([landmarks[eye_indices[0]].x, landmarks[eye_indices[0]].y])
    bottom = np.array([landmarks[eye_indices[1]].x, landmarks[eye_indices[1]].y])
    left = np.array([landmarks[eye_indices[2]].x, landmarks[eye_indices[2]].y])
    right = np.array([landmarks[eye_indices[3]].x, landmarks[eye_indices[3]].y])
    
    vertical_dist = np.linalg.norm(top - bottom)
    horizontal_dist = np.linalg.norm(left - right)
    
    if horizontal_dist == 0: return 0
    return vertical_dist / horizontal_dist

def trigger_alarm(tingkat="bahaya"):
    """
    Fungsi untuk membunyikan alarm keras
    Tingkat: 'bahaya' (ngantuk) atau 'peringatan' (bungkuk)
    """
    if platform.system() == "Windows":
        if tingkat == "bahaya":
            # Frekuensi 2500Hz, durasi 600ms (Sangat Nyaring)
            winsound.Beep(2500, 600)
        else:
            # Frekuensi 1500Hz, durasi 300ms (Lumayan Nyaring)
            winsound.Beep(1500, 300)
    else:
        # Untuk Mac/Linux: Beep berulang
        bunyi = '\a\a\a' if tingkat == "bahaya" else '\a'
        sys.stdout.write(bunyi)
        sys.stdout.flush()

def terminal_listener():
    global is_running, is_active, show_cam, cam_scale
    while is_running:
        try:
            cmd = input().strip().lower()
            if cmd == 'q': is_running = False
            elif cmd == 'p': is_active = not is_active
            elif cmd == 'h': 
                show_cam = not show_cam
                if not show_cam: cv2.destroyAllWindows()
            elif cmd == '+': cam_scale = min(2.5, cam_scale + 0.2)
            elif cmd == '-': cam_scale = max(0.3, cam_scale - 0.2)
            sys.stdout.write('\033[1A\033[K') 
        except:
            pass

def menu_penjelasan():
    clear_screen()
    draw_ascii_header()
    print(f"{G}--- PENJELASAN PROGRAM ---{X}")
    print("Tegak.in mendeteksi posisi mata dan postur tubuhmu.")
    print("Jika kamu mengantuk atau membungkuk, program akan membunyikan")
    print("alarm nyaring dan menampilkan peringatan visual merah di layar.")
    input(f"\n{Y}[Tekan Enter untuk kembali ke Menu Utama]{X}")

def menu_latar_belakang():
    clear_screen()
    draw_ascii_header()
    print(f"{G}--- LATAR BELAKANG MASALAH ---{X}")
    print("Mencegah sindrom 'Tech Neck' dan kelelahan saat menatap layar.")
    input(f"\n{Y}[Tekan Enter untuk kembali ke Menu Utama]{X}")

def menu_panduan():
    clear_screen()
    draw_ascii_header()
    print(f"{G}--- PANDUAN PENGGUNAAN ---{X}")
    print(f"  {Y}[p]{X} : Pause / Resume AI")
    print(f"  {Y}[h]{X} : Sembunyikan / Tampilkan UI Kamera")
    print(f"  {Y}[+]{X} / {Y}[-]{X} : Zoom Kamera")
    print(f"  {Y}[q]{X} : Keluar Aplikasi")
    input(f"\n{Y}[Tekan Enter untuk kembali ke Menu Utama]{X}")

def pengaturan_kamera():
    clear_screen()
    draw_ascii_header()
    print(f"{G}--- PENGATURAN SESI FOKUS ---{X}")
    
    try:
        durasi = input("1. Masukkan durasi sesi (menit) [Default: 25]: ")
        durasi = int(durasi) if durasi.strip() else 25
    except ValueError:
        durasi = 25

    tampil = input("2. Tampilkan jendela kamera? (y/n) [Default: y]: ").strip().lower()
    global show_cam
    show_cam = False if tampil == 'n' else True

    print("3. Ukuran jendela kamera awal:")
    print("   [1] Normal (100%) | [2] Kecil (50%) | [3] Besar (150%)")
    ukuran = input("   Pilih (1/2/3) [Default: 1]: ").strip()
    
    global cam_scale
    if ukuran == '2': cam_scale = 0.5
    elif ukuran == '3': cam_scale = 1.5
    else: cam_scale = 1.0

    print(f"\n{C}[*] Memulai AI dalam 3 detik...{X}")
    time.sleep(3)
    jalankan_ai(durasi)

def jalankan_ai(durasi_menit):
    global is_running, is_active, show_cam, cam_scale
    is_running = True
    is_active = True

    clear_screen()
    draw_ascii_header()
    print(f"{C}[KONTROL] p: Pause | h: Hide/Show Cam | +/-: Zoom Cam | q: Keluar{X}")
    print(f"[*] Sesi {durasi_menit} menit dimulai...\n")
    
    threading.Thread(target=terminal_listener, daemon=True).start()
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened(): cap = cv2.VideoCapture(0)
    
    start_time = time.time()
    session_duration = durasi_menit * 60
    
    right_eye = [159, 145, 33, 133]
    left_eye = [386, 374, 362, 263]
    last_print_time = 0

    while cap.isOpened() and is_running:
        ret, frame = cap.read()
        if not ret: break

        remaining_time = session_duration - (time.time() - start_time)
        if remaining_time <= 0: break
        
        minutes, seconds = int(remaining_time // 60), int(remaining_time % 60)
        timer_str = f"{minutes:02d}:{seconds:02d}"
        
        kondisi_bahaya = False
        kondisi_bungkuk = False

        if is_active:
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pose_results = pose.process(image_rgb)
            face_results = face_mesh.process(image_rgb)
            status_msg = f"[{G}AMAN{X}] Terdeteksi fokus & postur baik.  "

            # Deteksi Ngantuk
            if face_results.multi_face_landmarks:
                for face_landmarks in face_results.multi_face_landmarks:
                    landmarks = face_landmarks.landmark
                    avg_ear = (calculate_ear(landmarks, right_eye) + calculate_ear(landmarks, left_eye)) / 2.0
                    if avg_ear < 0.20:
                        status_msg = f"[{R}BAHAYA{X}] WOY BANGUN! Mata terpejam!"
                        kondisi_bahaya = True

            # Deteksi Bungkuk
            if pose_results.pose_landmarks and not kondisi_bahaya:
                pl = pose_results.pose_landmarks.landmark
                nose_y = pl[mp_pose.PoseLandmark.NOSE.value].y
                avg_shoulder_y = (pl[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y + pl[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y) / 2.0
                if (avg_shoulder_y - nose_y) < 0.15:
                    status_msg = f"[{Y}PERINGATAN{X}] Jangan bungkuk! Tegakkan punggung!"
                    kondisi_bungkuk = True
        else:
            status_msg = f"[{C}PAUSED{X}] AI dinonaktifkan sementara.     "

        # Tembak Alarm Bunyi Nyaring (Thread terpisah agar tidak lag kamera)
        if kondisi_bahaya:
            threading.Thread(target=trigger_alarm, args=("bahaya",), daemon=True).start()
        elif kondisi_bungkuk:
            threading.Thread(target=trigger_alarm, args=("peringatan",), daemon=True).start()

        # Render Terminal
        if time.time() - last_print_time > 0.3:
            cam_status = f"{G}ON{X}" if show_cam else f"{Y}OFF{X}"
            sys.stdout.write(f"\r[Timer: {C}{timer_str}{X}] [Kamera: {cam_status}] -> {status_msg} \033[K")
            sys.stdout.flush()
            last_print_time = time.time()

        # Render UI Kamera
        if show_cam:
            disp_frame = cv2.flip(frame, 1)

            # Efek Visual (Layar Berkedip Merah + Teks Raksasa)
            if kondisi_bahaya:
                overlay = disp_frame.copy()
                cv2.rectangle(overlay, (0, 0), (disp_frame.shape[1], disp_frame.shape[0]), (0, 0, 255), -1)
                cv2.addWeighted(overlay, 0.4, disp_frame, 0.6, 0, disp_frame)
                cv2.putText(disp_frame, "BANGUN!!!", (50, int(disp_frame.shape[0]/2)), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 10)
            elif kondisi_bungkuk:
                cv2.putText(disp_frame, "TEGAKKAN PUNGGUNG!", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

            if not is_active:
                cv2.putText(disp_frame, "AI PAUSED", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            if cam_scale != 1.0:
                h, w = disp_frame.shape[:2]
                disp_frame = cv2.resize(disp_frame, (int(w * cam_scale), int(h * cam_scale)))

            cv2.imshow('Tegak.in', disp_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'): is_running = False
            elif key == ord('p'): is_active = not is_active
            elif key == ord('h'): 
                show_cam = False
                cv2.destroyAllWindows()
            elif key == ord('=') or key == ord('+'): cam_scale = min(2.5, cam_scale + 0.2)
            elif key == ord('-'): cam_scale = max(0.3, cam_scale - 0.2)

    cap.release()
    cv2.destroyAllWindows()
    print(f"\n\n{G}[*] Sesi Selesai. Kembali ke menu utama...{X}")
    time.sleep(2)

def main():
    while True:
        clear_screen()
        draw_ascii_header()
        print(f"{C}--- MENU UTAMA ---{X}")
        print("1. Mulai Sesi / Start")
        print("2. Penjelasan Program")
        print("3. Latar Belakang Masalah")
        print("4. Panduan Cara Penggunaan")
        print("5. Keluar Aplikasi")
        print(f"{C}------------------{X}")
        
        pilihan = input("Pilih menu (1-5): ").strip()
        
        if pilihan == '1': pengaturan_kamera()
        elif pilihan == '2': menu_penjelasan()
        elif pilihan == '3': menu_latar_belakang()
        elif pilihan == '4': menu_panduan()
        elif pilihan == '5':
            clear_screen()
            print(f"{G}Terima kasih telah menggunakan Tegak.in. Tetap sehat dan produktif!{X}")
            sys.exit(0)

if __name__ == "__main__":
    main()
