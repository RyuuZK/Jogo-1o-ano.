import pyxel
import math
import random

class Inimigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.img = 2
        self.w, self.h = 24, 12
        self.transp = 7
        self.hp = 5
        self.speed = 0.7
        self.last_hit_time = -999

    def update(self, player_x, player_y):
        if pyxel.frame_count % 10 == 0:
            self.frame = (self.frame + 1) % 2
        dx = player_x - self.x
        dy = player_y - self.y
        dist = math.hypot(dx, dy) or 1
        self.x += dx / dist * self.speed
        self.y += dy / dist * self.speed

    def draw(self):
        pyxel.blt(self.x, self.y, self.img,
                  0, self.frame * self.h,
                  self.w, self.h, self.transp)

    def hitbox(self):
        margin = 4
        return (self.x + margin, self.y + margin,
                self.x + self.w - margin, self.y + self.h - margin)


class Jogo:
    def __init__(self):
        pyxel.init(160, 120, title="Mago Sobrevivente")
        pyxel.mouse(True)

        pyxel.image(0).load(0, 0, "mapa.png")
        pyxel.image(1).load(0, 0, "mago.png")
        pyxel.image(2).load(0, 0, "morcego.png")

        self.estado = "menu"

        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.x, self.y = 80, 60
        self.speed = 1.2
        self.frame = 0
        self.dir = "right"
        self.hp = 5
        self.alive = True

        self.score = 0
        self.kills = 0
        self.wave_limit = 4

        self.upgrade_points = 0
        self.upgrade_menu = None
        self.shot_cooldown = 12
        self.last_shot = -999
        self.damage = 2
        self.multishot = 0
        self.upgrades_count = {
            "atk_speed": 0,
            "damage": 0,
            "hp": 0,
            "multishot": 0,
        }

        self.fireballs = []
        self.inimigos = [self.spawn_inimigo()]

    def spawn_inimigo(self):
        while True:
            side = random.choice(["top", "bottom", "left", "right"])
            if side == "top":
                x, y = random.randint(0, 160), -10
            elif side == "bottom":
                x, y = random.randint(0, 160), 130
            elif side == "left":
                x, y = -10, random.randint(0, 120)
            else:
                x, y = 170, random.randint(0, 120)

            if abs(x - self.x) > 20 and abs(y - self.y) > 20:
                return Inimigo(x, y)

    def update(self):
        if self.estado == "menu":
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.estado = "jogando"
            return

        if self.estado == "gameover":
            if pyxel.btnp(pyxel.KEY_R):
                self.reset()
                self.estado = "jogando"
            return

        if self.upgrade_menu:
            if pyxel.btnp(pyxel.KEY_1):
                self.choose_upgrade(self.upgrade_menu[0])
            if pyxel.btnp(pyxel.KEY_2):
                self.choose_upgrade(self.upgrade_menu[1])
            if pyxel.btnp(pyxel.KEY_3):
                self.choose_upgrade(self.upgrade_menu[2])
            return

        moved = False
        if pyxel.btn(pyxel.KEY_A):
            self.x -= self.speed
            self.dir = "left"
            moved = True
        if pyxel.btn(pyxel.KEY_D):
            self.x += self.speed
            self.dir = "right"
            moved = True
        if pyxel.btn(pyxel.KEY_W):
            self.y -= self.speed
            moved = True
        if pyxel.btn(pyxel.KEY_S):
            self.y += self.speed
            moved = True
        self.x = max(0, min(self.x, 160 - 16))
        self.y = max(0, min(self.y, 120 - 16))
        if moved and pyxel.frame_count % 8 == 0:
            self.frame = (self.frame + 1) % 2

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.frame_count - self.last_shot > self.shot_cooldown:
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            origin_x, origin_y = self.x + 8, self.y + 8
            dx, dy = mx - origin_x, my - origin_y
            dist = math.hypot(dx, dy) or 1
            speed_fb = 2.5
            vx, vy = dx / dist * speed_fb, dy / dist * speed_fb
            self.fireballs.append([origin_x, origin_y, vx, vy])
            self.last_shot = pyxel.frame_count

            for i in range(self.multishot):
                angle = (i+1) * (math.pi/6)
                self.fireballs.append([origin_x, origin_y,
                                       vx*math.cos(angle)-vy*math.sin(angle),
                                       vx*math.sin(angle)+vy*math.cos(angle)])

        novas = []
        for fb in self.fireballs:
            fb[0] += fb[2]
            fb[1] += fb[3]
            if -16 <= fb[0] <= 176 and -16 <= fb[1] <= 136:
                novas.append(fb)
        self.fireballs = novas

        for inimigo in self.inimigos:
            inimigo.update(self.x, self.y)
            for fb in self.fireballs:
                if (inimigo.x < fb[0] < inimigo.x + inimigo.w and
                    inimigo.y < fb[1] < inimigo.y + inimigo.h):
                    inimigo.hp -= self.damage
                    self.fireballs.remove(fb)
                    if inimigo.hp <= 0:
                        self.inimigos.remove(inimigo)
                        self.score += 10
                        self.kills += 1
                        self.upgrade_points += 10
                        if self.kills == 15:
                            self.wave_limit = 6
                        elif self.kills == 50:
                            self.wave_limit = 8
                        if self.upgrade_points % 50 == 0:
                            self.open_upgrade_menu()
                    break

            ix1, iy1, ix2, iy2 = inimigo.hitbox()
            if (self.x < ix2 and self.x + 16 > ix1 and
                self.y < iy2 and self.y + 16 > iy1):
                if pyxel.frame_count - inimigo.last_hit_time > 120:
                    self.hp -= 1
                    inimigo.last_hit_time = pyxel.frame_count
                    if self.hp <= 0:
                        self.alive = False
                        self.estado = "gameover"

        if len(self.inimigos) < self.wave_limit:
            self.inimigos.append(self.spawn_inimigo())

    def open_upgrade_menu(self):
        upgrades = ["atk_speed", "damage", "hp", "multishot"]
        self.upgrade_menu = random.sample(upgrades, 3)

    def choose_upgrade(self, upgrade):
        if upgrade == "atk_speed" and self.upgrades_count["atk_speed"] < 5:
            self.shot_cooldown = max(2, self.shot_cooldown - 2)
            self.upgrades_count["atk_speed"] += 1
        elif upgrade == "damage" and self.upgrades_count["damage"] < 10:
            self.damage += 1
            self.upgrades_count["damage"] += 1
        elif upgrade == "hp" and self.upgrades_count["hp"] < 10:
            self.hp += 2
            self.upgrades_count["hp"] += 1
        elif upgrade == "multishot" and self.upgrades_count["multishot"] < 3:
            self.multishot += 1
            self.upgrades_count["multishot"] += 1
        self.upgrade_menu = None

    def draw(self):
        pyxel.cls(0)

        if self.estado == "menu":
            pyxel.text(45, 40, "MAGO SOBREVIVENTE", 10)
            pyxel.text(40, 70, "Pressione ENTER para jogar", 7)
            return

        pyxel.blt(0, 0, 0, 0, 0, 160, 120)

        if self.estado == "jogando":
            u, v = (self.frame * 16, 0) if self.dir == "right" else (self.frame * 16, 16)
            pyxel.blt(self.x, self.y, 1, u, v, 16, 16, 7)

            for fb in self.fireballs:
                pyxel.circ(int(fb[0]), int(fb[1]), 2, 10)

            for inimigo in self.inimigos:
                inimigo.draw()

            pyxel.text(2, 2, f"HP:{self.hp}", 7)
            pyxel.text(2, 9, f"Score:{self.score}", 7)

            if self.upgrade_menu:
                pyxel.text(25, 35, "Escolha um UPGRADE:", 8)
                for i, up in enumerate(self.upgrade_menu):
                    nome = {
                        "atk_speed": "+Atk Speed",
                        "damage": "+Dano",
                        "hp": "+HP",
                        "multishot": "+Disparo Extra"
                    }[up]
                    pyxel.text(25, 50 + i * 10, f"{i+1} - {nome}", 7)

        elif self.estado == "gameover":
            pyxel.text(50, 50, "VOCE PERDEU!", 8)
            pyxel.text(30, 70, "Aperte R para recomeçar", 7)


Jogo()