import random
import pygame
import math
from tkinter import *
from pygame import mixer
import time
import sys
from tkinter import messagebox

pygame.init()

def field_edges ():
    #Saha kenarları çizilecek beyaz kalın çizgiler halinde-- SABİT OLACAK
    pygame.draw.line(root, white, (5, 10), (995, 10), 5)  # üst çizgi
    pygame.draw.line(root, white, (5, 10), (5, 595), 5)  # sol çizgi
    pygame.draw.line(root, white, (5, 595), (995, 595), 5)  # alt çizgi
    pygame.draw.line(root, white, (995, 10), (995, 595), 5)  # sağ çizgi

    # Orta saha çizgisi, yuvarlağı ve sağ kale--SABİT OLACAK
    pygame.draw.line(root, white, (500, 10), (500, 595), 5)  # orta çizgi
    pygame.draw.circle(root, white, (500, 300), 80, 5)  # orta yuvarlak
    pygame.draw.circle(root, white, (500, 300), 10, 5)  # tam ortası

def goalpost_features():
    global goalpost_x, goalpost_y1,goalpost_y2

    # kale direkleri--SABİT OLACAK
    pygame.draw.line(root, black, (990, 230), (990, 370), 7)  # orta direk-- top bu konumdan geçerse gol olmalı
    #kale boyutu
    pygame.draw.rect(root, white, (900, 230, 145, 145), 4) #x,y ve yükseklik genişliği

    pygame.draw.circle(root,yellow,(goalpost_x,goalpost_y1),12)
    pygame.draw.circle(root,yellow,(goalpost_x,goalpost_y2),12) # alt- üst direkler


def gk_features(root,renk,gk_x,gk_y,size,bigEye=4,smallEye=2):
    # kaleci çizelim
    pygame.draw.circle(root, renk, (gk_x, gk_y), size)

    pygame.draw.circle(root, white, (gk_x   - 8, gk_y - 8), bigEye)
    pygame.draw.circle(root, black, (gk_x - 8, gk_y - 8), smallEye)  # sol göz

    pygame.draw.circle(root, white, (gk_x + 8, gk_y - 8), bigEye)
    pygame.draw.circle(root, black, (gk_x + 8, gk_y - 8), smallEye)  # sağ göz
    pygame.draw.line(root, white, (gk_x - 4, gk_y), (gk_x + 4, gk_y), smallEye)  # kaleci ağız

def player_features(root,renk,player_x,player_y,size):
    pygame.draw.circle(root, renk, (player_x, player_y), size)
    pygame.draw.circle(root, red, (player_x - 10, player_y - 5), 3)  # oyuncunun sol gözü
    pygame.draw.circle(root, red, (player_x + 10, player_y - 5), 3)  # oyuncunun sağ gözü

    pygame.draw.line(root, red,   (player_x - 10, player_y + 10), (player_x + 10, player_y + 10))  # oyuncunun ağzı
    pygame.draw.line(root, black, (player_x + 20, player_y), (player_x + 40, player_y))  # oyuncunun sağ kolu.
    pygame.draw.line(root, black, (player_x - 40, player_y), (player_x - 20, player_y))  # oyuncunun sol kolu

def corner():
    pygame.draw.arc(root, white, (930, 0, 70, 70), math.radians(140), math.radians(0), 6)
    pygame.draw.arc(root, white, (940, 550, 70, 70), 0, math.radians(210), 6)

# Top vurulduğunda görsel efekt
def shooting_affect(root, player_x, player_y):
    # Vuruş anında parlama veya genişleme efekti
    pygame.draw.circle(root, (255, 255, 0), (player_x, player_y), 36, 3)
    pygame.draw.circle(root, (255, 100, 0), (player_x, player_y), 40, 2)

def music_adding():
    #Topa vurulunca cıkan çarpışma sesi
    mixer.music.load("hit.wav")
    volume_level = 0.05  # müziği yükledik ve ses seviyesini ayarladık.
    mixer.music.set_volume(volume_level)  # başlangıc sesi
    mixer.music.play()

def name_adding():
    global name
    name = entry1.get()
    entry1.delete(0,"end")

def time_update():
    current_time = time.strftime("%H:%M:%S")  # Saat ve dakika formatını alıyoruz
    date_lbl.config(text=current_time)  # Etiketi güncelliyoruz
    date_lbl.after(1000, time_update)  # 1000 ms (1 saniye) sonra tekrar çağrılır

def snowy_mode():
    for i in range(len(snow)):  # kar yağdırma işlemi başlar.
        pygame.draw.circle(root, white, snow[i],4) #kar boyut
        snow[i][1] += 1  # burada i hem x hem y koordinatı içerdiği için i-1 demek y 'yi i-0 demek x'i temsil eder. Burada y koordinatını 1 artırarak

        if snow[i][1] > 570:  # yeni kar tanesi eklenir.
            snow[i][1] = random.randint(-40,-10)  # y koordinatına yeni bir kar tanesi ekledik.
            snow[i][0] = random.randint(0,1008)  # yağan karı bir de rastgele olarak x konumuna ekleyelim. yoksa hep aynı noktaya düşerler.

def quit_btn():
    sys.exit() # bu butona tıklandığında tüm sistem kapanır(gui-pygame)

def training_mode():
    pygame.init()

def player_obstacle_collision(player_x,player_y,obstacle_x,obstacle_y):

    player_obstacle_distance_x = abs(player_x - obstacle_x)
    player_obstacle_distance_y = abs(player_y - obstacle_y)

    if player_obstacle_distance_x < 30 and player_obstacle_distance_y < 30:
        if player_x < obstacle_x:
            player_x -= 10
        if player_x > obstacle_x:
            player_x += 10
        if player_y < obstacle_y:
            player_y -= 10
        if player_y > obstacle_y:
            player_y += 10
    return player_x,player_y  # bu fonk'u 3 kez cağırarak e baraj için de geçerli kılıyoruz.

def ball_obstacle_collision (ball_x,ball_y,obstacle_x,obstacle_y):

    top_baraj_mesafesi_x = abs(ball_x - obstacle_x)
    top_baraj_mesafesi_y = abs(ball_y - obstacle_y)

    if top_baraj_mesafesi_x <26 and top_baraj_mesafesi_y <26:
        if ball_x < obstacle_x:
            ball_x -= 10
        if ball_x > obstacle_x:
            ball_x += 10
        if ball_y < obstacle_y:
            ball_y -= 10
        if ball_y > obstacle_y:
            ball_y += 10  #üsttekiyle aynı mantık 1-1.

    return ball_x,ball_y

def freekick_mode():
    global score_counter,obstacle_x,obstacle_y,obstacle_distance

    player_features(root,black,obstacle_x,obstacle_y,20)
    player_features(root,black,obstacle_x,obstacle_y + obstacle_distance,20)
    player_features(root,black,obstacle_x,obstacle_y + (obstacle_distance*2),20)

def start_btn():
    global weather_selection #aşağıda kullanmak için genel bir değişken oluşturduk
    global mode_selection # antrenman-frikik modlarını tutacak

    if strVar.get() == "snowy" and strVar2.get() == "training":
        weather_selection= "snowy"
        mode_selection = "training"
        window.destroy()
        pygame.init()

    elif strVar.get() == "snowy" and strVar2.get() == "freekick":
        weather_selection = "snowy"
        mode_selection = "freekick"
        window.destroy()
        pygame.init()

    if strVar.get() == "normal" and strVar2.get() == "training":
        weather_selection = "normal"
        mode_selection = "training"
        window.destroy()
        pygame.init()

    elif strVar.get() == "normal" and strVar2.get() == "freekick":
        weather_selection = "normal"
        mode_selection = "freekick"
        window.destroy()
        pygame.init()

window = Tk()
window.geometry("500x500")
window.config(bg="Brown")
window.resizable(height=False,width=False)
window.title("Ball Punching")

weather_selection = "normal" #varsayılan olarak ayarladık bunu. seçime göre değişebilir
mode_selection = "training" #varsayılan olarak antrenmanla başlasın. seçime göre değişsin.

# 0.sütun bölümü
lbl_game_mode= Label(window,text="Game Mode",bg="Brown",fg="Pink",font=("Times New Roman",14))
canv1 = Canvas(window,height=3,width=150,bg="aqua",highlightthickness=1,highlightbackground="aqua")

#antrenman-frikik modlarından birisinin seçimini tutar.
strVar2 = StringVar()
strVar2.set(None)

rbtn_training = Radiobutton(window,text="Training Mode",fg="white",bg="brown",value="training",
                             variable=strVar2,
                             selectcolor="black",
                             activebackground="white")

rbtn_freekick = Radiobutton(window,text="Freekick Mode", fg="white",bg="brown",value="freekick",variable=strVar2,
                             selectcolor="black",
                             activebackground="white")

for i in range(5):
    canv2 = Canvas(window,height=2,width=170,bg="black",highlightthickness=1,highlightbackground="green")
    canv2.grid(row=4 , column=i,pady=20)

lbl_weather = Label(window,text="Weather",bg="Brown",fg="Pink",font=("Times New Roman",14))
canv3 = Canvas(window,height=3,width=150,bg="aqua",highlightthickness=1,highlightbackground="aqua")

canv1.grid(row=1,column=0,padx=5,pady=5)
lbl_game_mode.grid(row=0,column=0,padx=5,pady=5)
rbtn_training.grid(row=2 , column=0,padx=5,pady=5)
rbtn_freekick.grid(row=3 , column= 0,padx=5,pady=5)
lbl_weather.grid(row=0 , column=1,padx=5,pady=5)
canv3.grid(row=1,column=1,padx=5,pady=5)

#karlı veya normal hava modlarından birisinin seçimini tutar.
strVar = StringVar()
strVar.set(None) #

rbtn_snoowy = Radiobutton(window,text="Snowy",bg="Brown",fg="aqua",value="snowy",variable=strVar,
                             selectcolor="black",
                             activebackground="white")

rbtn_normal = Radiobutton(window,text="Normal",bg="Brown",fg="aqua",value="normal",variable=strVar,
                             selectcolor="black",
                             activebackground="white")

txt = Label(window,text="Welcome to the Game\n"
                        "10.03.2025",
            font=("Times New Roman",10,"italic")
            ,height=13,width=25,bg="brown",fg="aqua",)

lbl_nick = Label(window,text = "Name :",bg="Brown",font=("Times New Roman",14,"italic"))
entry1 = Entry(window,width=20)
btn_ok = Button(window,text="OK",font=("Times New Roman",8),command=name_adding,width=6)
date_lbl = Label(window,text="Date",height=1,width=8,bg="brown")

rbtn_snoowy.grid(row=2 , column= 1,padx=5,pady=5)
rbtn_normal.grid(row= 3, column=1,padx=5,pady=5)
txt.grid(row=10 , column=0)
lbl_nick.grid(row=5, column=0)
entry1.grid(row=5 , column=1)
btn_ok.grid(row=5 , column=2)
date_lbl.grid(row=0, column=2)

time_update()

canv4 = Canvas(window,height=3,width=150,bg="aqua",highlightthickness=1,highlightbackground="aqua")
canv4.grid(row=1,column=2,padx=5,pady=5)

for i in range(3):
    canv5 = Canvas(window,height=1,width=170)
    canv5.grid(row=7 , column=i,pady=40)

btn_start = Button(window,text="Start",height=2,width=10,command=start_btn)
btn_start.grid(row=8 , column= 1,pady=5)

btn_quit = Button(window,text="Quit",height=2,width=10,command=quit_btn)
btn_quit.grid(row=9 , column= 1)

window.mainloop()

#Renkler:
green =(120,200,0)
blue =(0,255,255)
red = (255,0,0)
yellow =(255,255,55)
white =(255,255,255)
black = (0,0,0)

#Başlangıc Konumları ve hızları:
root_x = 1000
root_y = 600
root = pygame.display.set_mode((root_x,root_y))

ball_x1 = 985
ball_x2= 985

ball_y1 = 5
ball_y2 = 595

ball_vx = 0  # topun x-ekseni hızı
ball_vy = 0  # topun y-ekseni hızı
friction = 0.95  # sayı 0 a yaklaştıkca top o kadar cabuk durur. 1 e yaklaştıkca sürtünmeyi azaltıyoruz.

player_x =500
player_y =250
player_x_speed = 4
player_y_speed = 4

gk_x =985
gk_y =300
gk_y_speed = 3

#üst ve alt direkler
goalpost_x = 990
goalpost_y1 = 230
goalpost_y2 = 370

obstacle_x = 850
obstacle_y = 270
obstacle_distance = 30
score_counter = 0  # skor tutar

FPS = 50 #oyun hızı için
fpsClock = pygame.time.Clock() # fps eklemeyi başlattık

ball_x = random.choice([ball_x1,ball_x2])
ball_y = random.choice([ball_y1,ball_y2]) # top, rastgele köşeden başlayacak.

snow = []
for i in range(100):
        x = random.randint(0, 1000)
        y = random.randint(0, 600)
        snow.append([x, y])

running = True
while running:
    keys = pygame.key.get_pressed()  # hangi tuşa basıldığını al
    root.fill(green)# arka plan sürekli yeşil olacak

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Top ve oyuncu
    pygame.draw.circle(root, white, (ball_x, ball_y), 12)  # top boy konum vs.
    pygame.draw.circle(root, red, (ball_x, ball_y), 14, 2)  # top etrafı çizgisi

    x1 = 120
    for i in range(4):  # Orta saha deseni
        pygame.draw.circle(root, white, (500, 300), x1, 4)
        x1 += 50

    # oyun özellik fonksiyonları:
    field_edges()
    goalpost_features()
    player_features(root,blue,player_x,player_y,24)
    corner()

    # Top ve oyuncu
    pygame.draw.circle(root, white, (ball_x, ball_y), 12)
    pygame.draw.circle(root, red, (ball_x, ball_y), 14, 2)

    gk_features(root,red,gk_x,gk_y,12)

    #kaleci hareketlendirme:
    gk_y += gk_y_speed
    if gk_y >= 370 or gk_y <=230: # kaleci 2 direk arasındaysa
        gk_y_speed *= -1 # kalecinin yönünü ters çevirir.

    player_features(root,blue,player_x  ,player_y,24)

    if 'name' in globals():
        font = pygame.font.SysFont("Times New Roman", 14)
        name_text = font.render(name, True, black)
        root.blit(name_text, (player_x-8 , player_y - 28)) # avatar ekledik

    # W-A-S-D ve SPACE tuş atamaları:
    if (keys[pygame.K_w]):
        player_y -= player_y_speed
    if (keys[pygame.K_s]):
        player_y += player_y_speed
    if (keys[pygame.K_a]):
        player_x -= player_x_speed
    if (keys[pygame.K_d]):
        player_x += player_x_speed

    # SPACE'E basıldığında topun hareketleri:
    if (keys[pygame.K_SPACE]):  # şimdi burada topa vurduğumuz anlar için hesap yapacağız.
        player_features(root, blue, player_x, player_y, 34)
        pygame.draw.circle(root, yellow, (player_x, player_y), 36,)

        if 'name' in globals():
            font = pygame.font.SysFont("Times New Roman", 14)
            name_text = font.render(name, True, black)
            root.blit(name_text, (player_x-10 , player_y-10 ))

        # İki nokta arasındaki gerçek mesafeyi hesaplama -- pisagor teoremiyle .. c^2 = a^2 + b^2
        distance = math.sqrt((player_x - ball_x) ** 2 + (player_y - ball_y) ** 2) # bu şekilde oyuncuyla 360 derece vuruş yapabiliriz.

        # Eğer oyuncu ve top yakınsa
        if distance < 34 + 12:
            # Vuruş vektörünü hesaplama (oyuncudan topa doğru)
            dx = ball_x - player_x
            dy = ball_y - player_y
            music_adding() # oyuncu topa vurursa, müzik calışır.

            # Vektörü normalize etme
            length = math.sqrt(dx ** 2 + dy ** 2)
            if length > 0:
                dx = dx / length
                dy = dy / length

            # Topa vektör yönünde hız uygulama
            shoot_power = 15
            ball_vx += dx * shoot_power
            ball_vy += dy * shoot_power

    #Topun kenar çizgilerine geldiğindeki hareketleri
    if  ball_x <= 12  or ball_x >= 988 :
        ball_vx *= -1 # hız tersine yöne dönsün

        if ball_x <=12: # top sol kenara carparsa konuma geri gelsin.
            ball_x = random.randint(10,30)
        if ball_x >= 988: # eğer sağ kenara çarparsa
            ball_x = random.randint(970,990)

    if ball_y <= 12 or ball_y >= 588 :
        ball_vy *= -1

        if ball_y <=12:
            ball_y = random.randint(10,30)
        if ball_y >= 588:
            ball_y = random.randint(570,590)

    if 980 <= ball_x <= 990 and  230 <= ball_y <= 370:
        score_counter +=1 # eğer top bu koordinatlar arasındaysa, yani gol olursa skor 1 artsın. ve top kaybolup ortada goool yazsın.
        #sonrasındaysa yine rastgele bir köşeden gelsin.

        gol_font = pygame.font.SysFont("Times New Roman", 60)
        gol_text = gol_font.render("GOOOOOOOL", True,(black))  # bunu render'leyerek ekrana bastırılabilecek hale getiriyoruz.

        score_font = pygame.font.SysFont("Arial", 20)
        score_text = score_font.render(f"Score : {score_counter}", True, white)

        root.blit(gol_text,(500,300))
        root.blit(score_text,(20,20))
        pygame.display.flip() # ekranı yenileyecek.
        pygame.time.delay(1500) # 1.5 sn ekranda gözükecekler.

        ball_x = random.choice([ball_x1,ball_x2])
        ball_y = random.choice([ball_y1,ball_y2])

#oyuncu, kaleci mesafe kontrolü (çarpışma için)
    player_x_difference = abs(player_x-  gk_x)
    player_y_difference = abs(player_y - gk_y)

    if player_x_difference <36 and player_y_difference <36 :
        if player_x < gk_x: #oyuncu kalecinin solundaysa
            player_x -= 20 # 20 br sola vur x mesafesinde
        if player_y < gk_y : # oyuncu, kalecinin üstündeyse yukarı vur
            player_y -= 20
        if player_y > gk_y : #oyuncu kalecinin altındaysa onu asağı vur
            player_y += 20

    #kaleci kurtarışı
    ball_x_difference = abs(ball_x-gk_x)
    ball_y_difference = abs(ball_y-gk_y)

    if ball_x_difference < 24 and ball_y_difference < 24 :
        if ball_x < gk_x:
            ball_x -= random.randint(20,50) # eğer top kalecinin solundaysa 20 ileri vurur
        if ball_y < gk_y: # eğer top kalecinin altındaysa
            ball_y -= random.randint(20,50) # topu aşağı vur
        if ball_y > gk_y: #top kalecinin üstündeyse
            ball_y += random.randint(20,50)

#oyuncu top sürmesi için mesafe kontrolü
    player_ball_difference_x=  abs(player_x-ball_x)
    player_ball_difference_y = abs(player_y-ball_y)

    if player_ball_difference_x <32 and player_ball_difference_y <32 :
        if player_x < ball_x:
            ball_x += 5
        if player_x > ball_x:
            ball_x -= 5
        if player_y < ball_y: #oyuncu topun üstündeyse, topu aşağı sür
            ball_y += 5
        if player_y > ball_y:
            ball_y -= 5

    player_goalpost_difference_x = abs(player_x - goalpost_x)  # oyuncu ve direğin x mesafesi
    goalposts_y = [goalpost_y1, goalpost_y2]  # üst ve alt direk y koordinatları

    for goalpost_y in goalposts_y:
        player_goalpost_difference_y = abs(player_y - goalpost_y)

        if player_goalpost_difference_x < 24 and player_goalpost_difference_y < 24:  # çarpışma kontrolü
            if player_x < goalpost_x:
                player_x -= 10
            if player_y < goalpost_y:
                player_y -= 10
            elif player_y > goalpost_y:  # else if kullanarak kontrol sayısını azalttım
                player_y += 10

    ball_goalpost_difference_x = abs(ball_x - goalpost_x) # top- direk farkı
    goalposts_y = [goalpost_y1, goalpost_y2]  # üst ve alt direk y koordinatları

    for goalpost_y in goalposts_y:
        ball_goalpost_difference_y = abs(ball_y - goalpost_y)

        if ball_goalpost_difference_x < 24 and ball_goalpost_difference_y < 24:
            if ball_x < goalpost_x:
                ball_x -= 5
            if ball_y < goalpost_y:
                ball_y -= 5
            if ball_y > goalpost_y:
                ball_y += 5

    if mode_selection == "freekick":
        freekick_mode()

        # Sırayla her bir baraj oyuncusu için çarpışma kontrolü yap
        player_x, player_y = player_obstacle_collision(player_x, player_y, obstacle_x, obstacle_y)  # Üst baraj
        player_x, player_y = player_obstacle_collision(player_x, player_y, obstacle_x, obstacle_y + obstacle_distance)  # Orta baraj
        player_x, player_y = player_obstacle_collision(player_x, player_y, obstacle_x, obstacle_y + (obstacle_distance * 2))  # Alt baraj

        ball_x, ball_y = ball_obstacle_collision(ball_x, ball_y,  obstacle_x,obstacle_y)
        ball_x, ball_y = ball_obstacle_collision(ball_x, ball_y , obstacle_x , obstacle_y + obstacle_distance)
        ball_x, ball_y = ball_obstacle_collision(ball_x, ball_y , obstacle_x , obstacle_y + (obstacle_distance * 2))


    ball_x += ball_vx
    ball_y += ball_vy # topun hızını konumuyla toplayarak topa hız verdik. ancak burada bırakırsak top süreki hareket eder ve durmaz

    ball_vx *= friction
    ball_vy *= friction # her döngüde hızı sürtünmeye göre azaltıyoruz

    if weather_selection == "snowy":
        snowy_mode()
    if mode_selection == "training":
        training_mode()
    if mode_selection == "freekick":
        freekick_mode()

    pygame.display.flip()
    fpsClock.tick(FPS)

pygame.quit()




