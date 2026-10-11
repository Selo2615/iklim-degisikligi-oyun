import random
import sys
import pygame

# Pygame başlatma
pygame.init()

# Ekran Boyutları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Eco-Guardian: Şehri Kurtar! - Hackathon Projesi")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
BLUE = (52, 152, 219)
GRAY = (127, 140, 141)

# Zamanlayıcı ve Fontlar
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 36, bold=True)


class Player(pygame.sprite.Sprite):

  def __init__(self):
    super().__init__()
    # Oyuncu karakteri (Yeşil kutu yerine temsili bir eko-karakter)
    self.image = pygame.Surface((50, 50))
    self.image.fill(GREEN)
    self.rect = self.image.get_rect()
    self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70)
    self.speed = 7

  def update(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
      self.rect.x -= self.speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      self.rect.x += self.speed

    # Ekran sınırları
    if self.rect.left < 0:
      self.rect.left = 0
    if self.rect.right > SCREEN_WIDTH:
      self.rect.right = SCREEN_WIDTH


class Item(pygame.sprite.Sprite):

  def __init__(self, item_type):
    super().__init__()
    self.item_type = item_type  # 'good' (yeşil enerji) veya 'bad' (çöp/karbon)
    self.image = pygame.Surface((30, 30))

    if self.item_type == "good":
      self.image.fill(BLUE)  # Temiz enerji / Fidan
    else:
      self.image.fill(RED)  # Karbon / Çöp

    self.rect = self.image.get_rect()
    self.rect.x = random.randint(0, SCREEN_WIDTH - 30)
    self.rect.y = random.randint(-150, -50)
    self.speed = random.randint(3, 7)

  def update(self):
    self.rect.y += self.speed
    if self.rect.top > SCREEN_HEIGHT:
      self.rect.y = random.randint(-150, -50)
      self.rect.x = random.randint(0, SCREEN_WIDTH - 30)


# Oyun Grupları ve Değişkenleri
all_sprites = pygame.sprite.Group()
items = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Çatışma nesneleri üretme
for i in range(8):
  item_type = "good" if random.random() > 0.4 else "bad"
  item = Item(item_type)
  all_sprites.add(item)
  items.add(item)

score = 0
carbon_level = 50  # Başlangıç karbon seviyesi (0-100)
running = True

# Ana Oyun Döngüsü
while running:
  # Olay Kontrolü
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Güncellemeler
  all_sprites.update()

  # Çarpışma Kontrolleri
  hits = pygame.sprite.spritecollide(player, items, True)
  for hit in hits:
    if hit.item_type == "good":
      score += 10
      carbon_level = max(0, carbon_level - 5)  # Karbonu düşür
    else:
      score -= 5
      carbon_level = min(100, carbon_level + 10)  # Karbonu artır

    # Yeni nesne ekle
    new_type = "good" if random.random() > 0.4 else "bad"
    new_item = Item(new_type)
    all_sprites.add(new_item)
    items.add(new_item)

  # Dinamik Arka Plan Rengi (Karbon seviyesine göre kirlilik efekti)
  bg_red = min(255, int(carbon_level * 2))
  bg_green = max(50, 220 - int(carbon_level * 1.5))
  bg_blue = max(50, 220 - int(carbon_level * 1.5))
  screen.fill((bg_red, bg_green, bg_blue))

  # Çizimler
  all_sprites.draw(screen)

  # Arayüz Bilgileri (HUD)
  score_text = font.render(f"Puan (Temiz Enerji): {score}", True, WHITE)
  carbon_text = font.render(f"Atmosfer Kirliliği (PPM): {carbon_level}", True,
                            WHITE if carbon_level < 70 else RED)

  screen.blit(score_text, (20, 20))
  screen.blit(carbon_text, (20, 50))

  # Oyun Bitiş Koşulu (Karbon seviyesi 100 olursa dünya kirlenir)
  if carbon_level >= 100:
    screen.fill(BLACK)
    game_over_text = title_font.render(
        "DÜNYA AŞIRI KİRLENDİ! İklim Krizi Kazandı.", True, RED)
    tip_text = font.render("İpucu: Karbon ayak izini azaltmak için geri dönüşüm yap!",
                           True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 320, SCREEN_HEIGHT // 2 - 50))
    screen.blit(tip_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 10))
    pygame.display.flip()
    pygame.time.wait(4000)
    running = False

  pygame.display.flip()
  clock.tick(60)

pygame.quit()
sys.exit()