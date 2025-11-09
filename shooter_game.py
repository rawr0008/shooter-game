# Create your ow shooter

from pygame import *
from random import randint

mixer.init()
file_sound = mixer.Sound('fire.ogg')

# --- Image files ---
img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_asteroid = "asteroid.png"  # pastikan ada gambar asteroid

# --- GameSprite base class ---
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# --- Player class ---
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx - 7, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
        file_sound.play()


# --- Enemy (UFO) class ---
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lose
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -40
            lose += 1


# --- Asteroid class ---
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(30, win_width - 30)
            self.rect.y = -40
            self.speed = randint(2, 6)


# --- Bullet class ---
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


# --- Window setup ---
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))

font.init()
font2 = font.Font('Arial', 36)
font_big = font.Font('Arial', 72)

# --- Function to start/restart game ---
def reset_game():
    global monsters, asteroids, bullets, ship, score, lose, finish
    score = 0
    lose = 0
    finish = False

    monsters = sprite.Group()
    for i in range(100):
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(2, 5))
        monsters.add(monster)

    asteroids = sprite.Group()
    for i in range(1):
        asteroid = Asteroid(img_asteroid, randint(30, win_width - 30), -40, 80, 80, randint(2, 6))
        asteroids.add(asteroid)

    bullets = sprite.Group()
    ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)


# --- Start game first time ---
reset_game()

# --- Main loop ---
run = True
fire_delay = 0.1
fire_cooldown = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_r and finish:
                reset_game()

    if not finish:
        keys = key.get_pressed()

        # --- Auto fire jika tombol spasi ditekan terus ---
        if keys[K_SPACE]:
            if fire_cooldown <= 0:
                ship.fire()
                fire_cooldown = fire_delay

        if fire_cooldown > 0:
            fire_cooldown -= 1

        # --- Update semua objek ---
        window.blit(background, (0, 0))
        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()

        # --- Collision: bullet hits enemy ---
        hits = sprite.groupcollide(monsters, bullets, True, True)
        for hit in hits:
            score += 1
            new_enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(2, 5))
            monsters.add(new_enemy)

        # --- Collision: player hits enemy or asteroid ---
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            finish = True
            game_text = font_big.render("GAME OVER!", True, (255, 0, 0))
            window.blit(game_text, (win_width // 2 - 180, win_height // 2 - 50))

        # --- Draw everything ---
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        # --- Text display ---
        text = font2.render("Score: " + str(score), True, (255, 255, 255))
        window.blit(text, (10, 10))
        text_lose = font2.render("Missed: " + str(lose), True, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # --- Lose condition ---
        if lose >= 3:
            finish = True
            game_text = font_big.render("GAME OVER!", True, (255, 0, 0))
            window.blit(game_text, (win_width // 2 - 180, win_height // 2 - 50))

        # --- Win condition ---
        if score >= 100000000000:
            finish = True
            game_text = font_big.render("YOU WIN!", True, (0, 255, 0))
            window.blit(game_text, (win_width // 2 - 150, win_height // 2 - 50))

        display.update()

    else:
        # --- Tampilkan pesan retry ---
        retry_text = font2.render("Press R to Retry", True, (255, 255, 255))
        window.blit(retry_text, (win_width // 2 - 120, win_height // 2 + 40))
        display.update()

    time.delay(50)
