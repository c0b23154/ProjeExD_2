import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1600, 900
DELTA = {  # 移動量辞書
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRect,または,爆弾Rect
    戻り値：真理値タプル（横方向，縦方向）
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def kk_rtz(s_mv: tuple, kk_sf):
    """
    
    """
    if s_mv[0] == 0:
        if s_mv[1] == -5:
            kk_sf = pg.transform.flip(kk_sf, False, True)
    return {s_mv:kk_sf}


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    kk_cryimg = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    kk_cryrct_1 = kk_cryimg.get_rect()
    kk_cryrct_2 = kk_cryimg.get_rect()
    kk_cryrct_1.center = 600, 470
    kk_cryrct_2.center = 1025, 470
    bomb =pg.Surface((20, 20))  # 一辺が20のからのSureFaceをつくる
    pg.draw.circle(bomb, (255, 0, 0), (10, 10), 10)
    bomb.set_colorkey((0, 0, 0))
    bomb_rct = bomb.get_rect()
    bomb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bomb_rct):  # 衝突判定
            last = pg.Surface((WIDTH, HEIGHT))
            pg.draw.rect(last, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
            last_rct = last.get_rect()
            last_rct.center = 800, 450
            last.set_alpha(200)
            screen.blit(last, last_rct)
            fonto = pg.font.Font(None, 80)
            txt = fonto.render("Game Over", True, (255, 255, 255))
            screen.blit(txt, [660, 450])
            screen.blit(kk_cryimg, kk_cryrct_1)
            screen.blit(kk_cryimg, kk_cryrct_2)
            pg.display.update()
            time.sleep(5)
        
            
            return  #ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():  # for文で辞書からkeyと要素を取り出す
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # ぶつかった場合、移動をなかったことにする
        bomb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bomb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        # kk = kk_rtz(sum_mv)
        screen.blit(kk_img, kk_rct)
        screen.blit(bomb, bomb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
