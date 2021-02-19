import pygame
import random
import sqlite3

pygame.init()

con = sqlite3.connect("Bilgiler.db")

cursor = con.cursor()


def tabloolustur():
    cursor.execute("CREATE TABLE IF NOT EXISTS bigiler (yuksek_skor INT)")
    con.commit()


def veriekle(skor: int):
    cursor.execute("SELECT yuksek_skor FROM bigiler")
    data = cursor.fetchall()
    cursor.execute("DELETE FROM bigiler")
    if len(data) > 0:
        if skor > data[0][0]:
            cursor.execute("INSERT INTO bigiler VALUES (" + str(skor) + ")")

        else:
            cursor.execute("INSERT INTO bigiler VALUES (" + str(data[0][0]) + ")")

    else:
        cursor.execute("INSERT INTO bigiler VALUES (" + str(skor) + ")")

    con.commit()


def skoral():
    cursor.execute("SELECT yuksek_skor FROM bigiler")
    data = cursor.fetchall()
    if len(data) > 0:
        return data[0][0]

    else:
        return 0


tabloolustur()


class Platform:
    def __init__(self, x, y):
        self.resim = pygame.image.load("platform.png")
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 43, 10)


class Giris:
    def __init__(self):
        self.ilkgiris = True


giriskontrol = Giris()


class BizimOyunumuz:
    def __init__(self):
        self.pencere_genisligi = 360
        self.pencere_yuksekligi = 720
        self.Pencere = pygame.display.set_mode((self.pencere_genisligi, self.pencere_yuksekligi))
        pygame.display.set_caption("Platform Jump")
        self.Arkaplan = pygame.image.load("arkaplan.png")
        self.Oyuncu = pygame.image.load("nokta.png").convert_alpha()
        self.OyuncuScaleX = 30
        self.OyuncuScaleY = 30
        self.Oyuncu = pygame.transform.scale(self.Oyuncu, (self.OyuncuScaleX, self.OyuncuScaleY))

        self.Platformlar = list()
        for i in range(-120, 841, 120):
            self.Platformlar.append(Platform(random.choice(range(0, 300)), i))
        self.OyuncuX = 100
        self.OyuncuY = 300
        self.Clock = pygame.time.Clock()
        self.asagi_hiz = 0
        self.ivme = 0
        self.ivme_ilkzaman = pygame.time.get_ticks()
        self.ivme_sonzaman = pygame.time.get_ticks()
        self.font = pygame.font.SysFont("Arial", 35)
        if giriskontrol.ilkgiris:
            self.yuksekskor = skoral()

        else:
            self.yuksekskor = self.yeniyuksekskor
            self.oncekielskor = self.skor

        self.skor = 0
        self.eskiskor = self.skor
        self.yeniskor = self.skor
        self.yeniyuksekskor = self.skor
        self.OyuncuRect = pygame.Rect(self.OyuncuX, self.OyuncuY, 30, 30)
        self.Tus = pygame.key.get_pressed()
        self.sabity = 300 - self.OyuncuY
        self.OyunDurumu = "Lobi"
        self.PlayButton = pygame.image.load("Play Button.png").convert_alpha()
        self.PlayButton = pygame.transform.scale(self.PlayButton, (250, 80))
        self.PlayButtonRect = pygame.Rect(50, 550, 250, 80)
        self.mouse = pygame.mouse
        self.mousex, self.mousey = self.mouse.get_pos()[0], self.mouse.get_pos()[1]
        self.mousecollid = pygame.Rect(self.mousex, self.mousey, 2, 2)

        self.lobi_ivmeilkzaman = pygame.time.get_ticks()
        self.lobi_ivmesonzaman = pygame.time.get_ticks()
        self.LobiPlatform = Platform(150, 420)
        self.LobiPlatform.rect = pygame.Rect(self.LobiPlatform.x, self.LobiPlatform.y - 25, 43, 30)
        self.OyuncuLobi = self.Oyuncu
        self.OyuncuLobiX = 160
        self.OyuncuLobiY = 320
        self.OyuncuLobiRect = pygame.Rect(self.OyuncuLobiX, self.OyuncuLobiY, 30, 30)
        self.asagi_hizlobi = 0
        self.ivmelobi = 0
        self.LobiFont = pygame.font.SysFont("Arial", 45)

    def Cizim(self):

        self.Pencere.blit(self.Arkaplan, (0, 0))
        if self.OyunDurumu == "Lobi":
            self.Pencere.blit(self.LobiFont.render("Platform Jump", True, (0, 0, 0)), (50, 70))
            self.Pencere.blit(self.PlayButton, (50, 550))
            self.Pencere.blit(self.font.render("Yüksek Skor: " + str(self.yuksekskor), True, (0, 0, 0)), (55, 460))
            if not giriskontrol.ilkgiris:
                self.Pencere.blit(self.font.render(
                    "Önceki Skor: " + str(self.oncekielskor), True, (0, 0, 0)), (70, 495))
            self.Pencere.blit(self.OyuncuLobi, (self.OyuncuLobiX, self.OyuncuLobiY))
            self.Pencere.blit(self.LobiPlatform.resim, (self.LobiPlatform.x, self.LobiPlatform.y))
            self.lobi_ivmesonzaman = pygame.time.get_ticks()
            self.OyuncuLobiRect = pygame.Rect(self.OyuncuLobiX, self.OyuncuLobiY, 30, 30)
            if self.ivmelobi != 5 and self.lobi_ivmesonzaman - self.lobi_ivmeilkzaman > 400:
                self.ivmelobi += 1
                self.lobi_ivmeilkzaman = pygame.time.get_ticks()

            self.asagi_hizlobi += self.ivmelobi
            self.OyuncuLobiY += self.asagi_hizlobi
            if self.OyuncuLobiRect.colliderect(self.LobiPlatform.rect):
                self.asagi_hizlobi = -8
                self.ivmelobi = 0
                self.lobi_ivmeilkzaman = pygame.time.get_ticks()
                self.lobi_ivmesonzaman = pygame.time.get_ticks()

        if self.OyunDurumu == "Oyun":
            self.Pencere.blit(self.Oyuncu, (self.OyuncuX, self.OyuncuY))
            self.Pencere.blit(self.font.render(str(self.skor), True, (0, 0, 0)), (285, 20))
            for platform in self.Platformlar:
                self.Pencere.blit(platform.resim, (platform.x, platform.y))

        self.Clock.tick(60)
        pygame.display.update()

    def Oyun(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                veriekle(self.yuksekskor)
                return "Son"

        self.Tus = pygame.key.get_pressed()
        if self.Tus[pygame.K_ESCAPE]:
            veriekle(self.yuksekskor)
            return "Son"

        if self.OyunDurumu == "Lobi":
            self.mousex, self.mousey = self.mouse.get_pos()[0], self.mouse.get_pos()[1]
            self.mousecollid = pygame.Rect(self.mousex, self.mousey, 2, 2)
            if self.mouse.get_pressed(3)[0] == 1 and self.mousecollid.colliderect(self.PlayButtonRect):
                self.OyunDurumu = "Oyun"
            self.Pencere.blit(self.OyuncuLobi, (self.OyuncuLobiX, self.OyuncuLobiY))

        elif self.OyunDurumu == "Oyun":
            if self.Tus[pygame.K_LEFT]:
                self.OyuncuX -= 3

            if self.Tus[pygame.K_RIGHT]:
                self.OyuncuX += 3

            self.OyuncuRect = pygame.Rect(self.OyuncuX, self.OyuncuY, 30, 30)

            for platform in self.Platformlar:
                platform.rect = pygame.Rect(platform.x, platform.y, 43, 10)
                if platform.y > 840:
                    self.Platformlar.remove(platform)
                    self.Platformlar.append(Platform(random.choice(range(0, 300)), -240))

                if platform.y < -1500:
                    self.OyunDurumu = "Lobi"
                    if self.yuksekskor < self.skor:
                        self.yeniyuksekskor = self.skor
                    else:
                        self.yeniyuksekskor = self.yuksekskor

                    self.oncekielskor = self.skor
                    giriskontrol.ilkgiris = False
                    self.__init__()

            for platform in self.Platformlar:
                if self.OyuncuRect.colliderect(platform.rect) and self.asagi_hiz < 0:
                    self.ivme = 0
                    self.asagi_hiz = 15
                    break

            self.ivme_sonzaman = pygame.time.get_ticks()
            if self.ivme != 5 and self.ivme_sonzaman - self.ivme_ilkzaman > 400:
                self.ivme += 1
                self.ivme_ilkzaman = pygame.time.get_ticks()

            self.asagi_hiz -= self.ivme

            self.OyuncuY += self.asagi_hiz
            self.sabity = 300 - self.OyuncuY

            self.eskiskor = self.skor
            self.skor -= int(self.sabity / 3)
            self.yeniskor = self.skor
            if self.yeniskor > self.eskiskor:
                self.yeniyuksekskor = self.yeniskor

            self.OyuncuY = 300
            for platform in self.Platformlar:
                platform.y -= self.sabity

            if self.OyuncuX > self.pencere_genisligi:
                self.OyuncuX = 0

            elif self.OyuncuX < 0:
                self.OyuncuX = self.pencere_genisligi

        self.Cizim()


Oyun = BizimOyunumuz()

while True:
    Durum = Oyun.Oyun()
    if Durum == "Son":
        break