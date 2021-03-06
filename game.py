#1 引入需要的模块
import pygame
import random
import time
import sys
#1 配置图片地址
IMAGE_PATH = 'imgs/'
# 配置音乐地址
MUSIC_PATH = 'music/'
# 配置音效地址
SOUND_PATH = 'sound/'
#1 设置页面宽高
scrrr_width=800
scrrr_height =560
#1 创建控制游戏结束的状态
GAMEOVER = False
#4 图片加载报错处理
LOG = '文件:{}中的方法:{}出错'.format(__file__,__name__)
#3 创建地图类
class Map():
    #3 存储两张不同颜色的图片名称
    map_names_list = [IMAGE_PATH + 'map5.png', IMAGE_PATH + 'map4.png']
    #3 初始化地图
    def __init__(self, x, y, img_index):
        self.image = pygame.image.load(Map.map_names_list[img_index])
        self.position = (x, y)
        # 是否能够种植
        self.can_grow = True
    #3 加载地图
    def load_map(self):
         MainGame.window.blit(self.image,self.position)
#4 植物类
class Plant(pygame.sprite.Sprite):
    def __init__(self):
        super(Plant, self).__init__()
        self.live=True

    # 加载图片
    def load_image(self):
        if hasattr(self, 'image') and hasattr(self, 'rect'):
            MainGame.window.blit(self.image, self.rect)
        else:
            print(LOG)
#5 向日葵类
class Sunflower(Plant):
    def __init__(self,x,y):
        super(Sunflower, self).__init__()
        self.image = pygame.image.load('imgs/sunflower.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 50
        self.hp = 100
        #5 时间计数器
        self.time_count = 0

    #5 新增功能：生成阳光
    def produce_money(self):
        self.time_count += 1
        if self.time_count == 125:
            MainGame.money += 25
            self.time_count = 0
    #5 向日葵加入到窗口中
    def display_sunflower(self):
        MainGame.window.blit(self.image,self.rect)
# 坚果类
class Nut(Plant):
    def __init__(self,x,y):
        super(Nut, self).__init__()
        self.image = pygame.image.load('imgs/nut.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 50
        self.hp = 1000
        
    #5 坚果加入到窗口中
    def display_nut(self):
        MainGame.window.blit(self.image,self.rect)
#6 豌豆射手类
class PeaShooter(Plant):
    def __init__(self,x,y):
        super(PeaShooter, self).__init__()
        # self.image 为一个 surface
        self.image = pygame.image.load('imgs/peashooter.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 100
        self.hp = 200
        #6 发射计数器
        self.shot_count = 0

    #6 增加射击方法
    def shot(self):
        #6 记录是否应该射击
        should_fire = False
        for zombie in MainGame.zombie_list:
            if zombie.rect.y == self.rect.y and zombie.rect.x < 800 and zombie.rect.x > self.rect.x:
                should_fire = True
        #6 如果活着
        if self.live and should_fire:
            self.shot_count += 1
            #6 计数器到25发射一次
            if self.shot_count == 25:
                #6 基于当前豌豆射手的位置，创建子弹
                peabullet = PeaBullet(self)
                #6 将子弹存储到子弹列表中
                MainGame.peabullet_list.append(peabullet)
                self.shot_count = 0

    #6 将豌豆射手加入到窗口中的方法
    def display_peashooter(self):
        MainGame.window.blit(self.image,self.rect)


#6.5 寒冰射手类
class IcePeaShooter(Plant):
    def __init__(self,x,y):
        super(IcePeaShooter, self).__init__()
        # self.image 为一个 surface
        self.image = pygame.image.load('imgs/icepeashooter.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 175
        self.hp = 200
        #6 发射计数器
        self.shot_count = 0

    #6 增加射击方法
    def shot(self):
        #6 记录是否应该射击
        should_fire = False
        for zombie in MainGame.zombie_list:
            if zombie.rect.y == self.rect.y and zombie.rect.x < 800 and zombie.rect.x > self.rect.x:
                should_fire = True
        #6 如果活着
        if self.live and should_fire:
            self.shot_count += 1
            #6 计数器到25发射一次
            if self.shot_count == 25:
                #6 基于当前豌豆射手的位置，创建子弹
                icepeabullet = IcePeaBullet(self)
                #6 将子弹存储到子弹列表中
                MainGame.icepeabullet_list.append(icepeabullet)
                self.shot_count = 0

    #6 将寒冰射手加入到窗口中的方法
    def display_peashooter(self):
        MainGame.window.blit(self.image,self.rect)

#7 豌豆子弹类
class PeaBullet(pygame.sprite.Sprite):
    def __init__(self,peashooter):
        self.live = True
        self.image = pygame.image.load('imgs/peabullet.png')
        self.damage = 50
        self.speed  = 10
        self.rect = self.image.get_rect()
        self.rect.x = peashooter.rect.x + 60
        self.rect.y = peashooter.rect.y + 15

    def move_bullet(self):
        #7 在屏幕范围内，实现往右移动
        if self.rect.x < scrrr_width:
            self.rect.x += self.speed
        else:
            self.live = False

    #7 新增，子弹与僵尸的碰撞
    def hit_zombie(self):
        for zombie in MainGame.zombie_list:
            if pygame.sprite.collide_rect(self,zombie):
                #打中僵尸之后，修改子弹的状态，
                self.live = False
                #僵尸掉血
                zombie.hp -= self.damage
                if zombie.hp <= 0:
                    zombie.live = False
                    self.nextLevel()
    #7闯关方法
    def nextLevel(self):
        MainGame.score += 20
        MainGame.remnant_score -=20
        for i in range(1,100):
            if MainGame.score==100*i and MainGame.remnant_score==0:
                    MainGame.remnant_score=100*i
                    MainGame.shaoguan+=1
                    if MainGame.shaoguan==6:
                        MainGame().gameOverw()
                    MainGame.produce_zombie*=0.5



    def display_peabullet(self):
        MainGame.window.blit(self.image,self.rect)

#7.5 寒冰子弹类
class IcePeaBullet(pygame.sprite.Sprite):
    def __init__(self,peashooter):
        self.live = True
        self.image = pygame.image.load('imgs/icepeabullet.png')
        self.damage = 50
        self.speed  = 10
        self.rect = self.image.get_rect()
        self.rect.x = peashooter.rect.x + 60
        self.rect.y = peashooter.rect.y + 15

    def move_bullet(self):
        #7 在屏幕范围内，实现往右移动
        if self.rect.x < scrrr_width:
            self.rect.x += self.speed
        else:
            self.live = False

    #7 新增，子弹与僵尸的碰撞
    def hit_zombie(self):
        for zombie in MainGame.zombie_list:
            if pygame.sprite.collide_rect(self,zombie):
                #打中僵尸之后，修改子弹的状态，
                self.live = False
                #僵尸掉血
                zombie.hp -= self.damage
                zombie.speedreduction=125
                if zombie.hp <= 0:
                    zombie.live = False
                    self.nextLevel()
    #7闯关方法
    def nextLevel(self):
        MainGame.score += 20
        MainGame.remnant_score -=20
        for i in range(1,100):
            if MainGame.score==100*i and MainGame.remnant_score==0:
                    MainGame.remnant_score=100*i
                    MainGame.shaoguan+=1
                    if MainGame.shaoguan==6:
                        MainGame().gameOverw()
                    MainGame.produce_zombie*=0.5



    def display_peabullet(self):
        MainGame.window.blit(self.image,self.rect)
#9 僵尸类
class Zombie(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Zombie, self).__init__()
        self.speedreduction=0
        self.image = pygame.image.load('imgs/zombie.png')
        self.rect = self.image.get_rect()
        self.x=x
        self.rect.x = x
        self.rect.y = y
        self.hp = 1000
        self.damage = 2
        self.speed = 0.5
        self.live = True
        self.stop = False
    #9 僵尸的移动
    def move_zombie(self):
        if self.live and not self.stop:
            if self.speedreduction>0:
                self.x-=0.6*self.speed
                self.speedreduction-=1
            else:
                self.x-=self.speed
            self.rect.x = self.x
            if self.rect.x < -80:
                
                #8 调用游戏结束方法
                MainGame().gameOverz()

    #9 判断僵尸是否碰撞到植物，如果碰撞，调用攻击植物的方法
    def hit_plant(self):
        for plant in MainGame.plants_list:
            if pygame.sprite.collide_rect(self,plant):
                #8  僵尸移动状态的修改
                self.stop = True
                self.eat_plant(plant)
    #9 僵尸攻击植物
    def eat_plant(self,plant):
        #9 植物生命值减少
        plant.hp -= self.damage
        #9 植物死亡后的状态修改，以及地图状态的修改
        if plant.hp <= 0:
            a = plant.rect.y // 80 - 1
            b = plant.rect.x // 80
            map = MainGame.map_list[a][b]
            map.can_grow = True
            plant.live = False
            #8 修改僵尸的移动状态
            self.stop = False



    #9 将僵尸加载到地图中
    def display_zombie(self):
        MainGame.window.blit(self.image,self.rect)
#1 主程序
class MainGame():
    #2 创建关数，得分，剩余分数，钱数
    shaoguan = 1
    score = 0
    remnant_score = 100
    money = 50
    #3 存储所有地图坐标点
    map_points_list = []
    #3 存储所有的地图块
    map_list = []
    #4 存储所有植物的列表
    plants_list = []
    #7 存储所有豌豆子弹的列表
    peabullet_list = []
    #8存储所有寒冰子弹的列表
    icepeabullet_list = []
    #9 新增存储所有僵尸的列表
    zombie_list = []
    count_zombie = 0
    produce_zombie = 100
    #1 加载游戏窗口
    def init_window(self):
        #1 调用显示模块的初始化
        pygame.display.init()
        #1 创建窗口
        MainGame.window = pygame.display.set_mode([scrrr_width,scrrr_height])

    #2 文本绘制
    def draw_text(self, content, size, color):
        pygame.font.init()
        font = pygame.font.SysFont('kaiti', size)
        text = font.render(content, True, color)
        return text

    #2 加载帮助提示
    def load_help_text(self):
        text1 = self.draw_text('左键：向日癸 右键：豌豆射手 ', 20, (0, 150, 150))
        text2 = self.draw_text('中键：寒冰射手 滚轮上：坚果', 20, (0, 150, 150))
        text3 = self.draw_text('滚轮下：铲子', 20, (0, 150, 150))
        sun=pygame.image.load(IMAGE_PATH+"sun1.png")
        card1=pygame.image.load(IMAGE_PATH+"card1.png")
        card2=pygame.image.load(IMAGE_PATH+"card2.png")
        card3=pygame.image.load(IMAGE_PATH+"card3.png")
        card4=pygame.image.load(IMAGE_PATH+"card4.png")
        MainGame.window.blit(sun, (10, 12))
        MainGame.window.blit(card1, (450, 3))
        MainGame.window.blit(card2, (540, 3))
        MainGame.window.blit(card3, (630, 3))
        MainGame.window.blit(card4, (720, 3))
        MainGame.window.blit(text1, (150, 5))
        MainGame.window.blit(text2, (150, 30))
        MainGame.window.blit(text3, (300, 55))

    #3 初始化坐标点
    def init_plant_points(self):
        for y in range(1, 7):
            points = []
            for x in range(10):
                point = (x, y)
                points.append(point)
            MainGame.map_points_list.append(points)
            #print("MainGame.map_points_list", MainGame.map_points_list)

    #3 初始化地图
    def init_map(self):
        for points in MainGame.map_points_list:
            temp_map_list = list()
            for point in points:
                # map = None
                if (point[0] + point[1]) % 2 == 0:
                    map = Map(point[0] * 80, point[1] * 80, 0)
                else:
                    map = Map(point[0] * 80, point[1] * 80, 1)
                # 将地图块加入到窗口中
                temp_map_list.append(map)
                #print("temp_map_list", temp_map_list)
            MainGame.map_list.append(temp_map_list)
        #print("MainGame.map_list", MainGame.map_list)

    #3 将地图加载到窗口中
    def load_map(self):
        for temp_map_list in MainGame.map_list:
            for map in temp_map_list:
                map.load_map()

    #6 加载植物
    def load_plants(self):
        for plant in MainGame.plants_list:
            #6 优化加载植物的处理逻辑
            if plant.live:
                if isinstance(plant, Sunflower):
                    plant.display_sunflower()
                    plant.produce_money()
                elif isinstance(plant, PeaShooter):
                    plant.display_peashooter()
                    plant.shot()
                elif isinstance(plant, IcePeaShooter):
                    plant.display_peashooter()
                    plant.shot()
                elif isinstance(plant, Nut):
                    plant.display_nut()
                    #plant.shot()
            else:
                MainGame.plants_list.remove(plant)

    #7 加载所有子弹的方法
    def load_peabullets(self):
        for b in MainGame.peabullet_list:
            if b.live:
                b.display_peabullet()
                b.move_bullet()
                # v1.9 调用子弹是否打中僵尸的方法
                b.hit_zombie()
            else:
                MainGame.peabullet_list.remove(b)
        for ib in MainGame.icepeabullet_list:
            if ib.live:
                ib.display_peabullet()
                ib.move_bullet()
                # v1.9 调用子弹是否打中僵尸的方法
                ib.hit_zombie()
            else:
                MainGame.icepeabullet_list.remove(ib)

    #8事件处理

    def deal_events(self):
        #8 获取所有事件
        eventList = pygame.event.get()
        #8 遍历事件列表，判断
        for e in eventList:
            if e.type == pygame.QUIT:
                self.gameOver()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                # print('按下鼠标按键')
               # print(e.pos)
                # print(e.button)#左键1  按下滚轮2 上转滚轮为4 下转滚轮为5  右键 3

                x = e.pos[0] // 80
                y = e.pos[1] // 80
                #print(x, y)
                map = MainGame.map_list[y - 1][x]
                #print(map.position)
                #8 增加创建时候的地图装填判断以及金钱判断
                if e.button == 1:
                    if map.can_grow and MainGame.money >= 50:
                        sunflower = Sunflower(map.position[0], map.position[1])
                        MainGame.plants_list.append(sunflower)
                        #print('当前植物列表长度:{}'.format(len(MainGame.plants_list)))
                        map.can_grow = False
                        MainGame.money -= 50
                elif e.button == 3:
                    if map.can_grow and MainGame.money >= 100:
                        peashooter = PeaShooter(map.position[0], map.position[1])
                        MainGame.plants_list.append(peashooter)
                        #print('当前植物列表长度:{}'.format(len(MainGame.plants_list)))
                        map.can_grow = False
                        MainGame.money -= 100
                elif e.button == 2:
                    if map.can_grow and MainGame.money >= 175:
                        icepeashooter = IcePeaShooter(map.position[0], map.position[1])
                        MainGame.plants_list.append(icepeashooter)
                        #print('当前植物列表长度:{}'.format(len(MainGame.plants_list)))
                        map.can_grow = False
                        MainGame.money -= 175
                elif e.button == 4:
                    if map.can_grow and MainGame.money >= 50:
                        nut = Nut(map.position[0], map.position[1])
                        MainGame.plants_list.append(nut)
                        #print('当前植物列表长度:{}'.format(len(MainGame.plants_list)))
                        map.can_grow = False
                        MainGame.money -= 50
                elif e.button == 5:
                    if not map.can_grow:
                        for plant in MainGame.plants_list:
                            if plant.rect.x==map.position[0] and plant.rect.y==map.position[1]:
                                plant.live=False
                                map.can_grow=True
                                break
                         

    #9 新增初始化僵尸的方法
    def init_zombies(self):
        for i in range(1, 7):
            dis = random.randint(1, 5) * 200
            zombie = Zombie(800 + dis, i * 80)
            MainGame.zombie_list.append(zombie)

    #9将所有僵尸加载到地图中
    def load_zombies(self):
        for zombie in MainGame.zombie_list:
            if zombie.live:
                zombie.display_zombie()
                zombie.move_zombie()
                # v2.0 调用是否碰撞到植物的方法
                zombie.hit_plant()
            else:
                MainGame.zombie_list.remove(zombie)
    # 初始化bgm
    def playbgm(self):
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_PATH+'Laura Shigihara - Graze the Roof.mp3')
        pygame.mixer.music.play(-1,0)
    #1 开始游戏
    def start_game(self):
        #1 初始化窗口
        self.init_window()
        # 播放BGM
        self.playbgm()
        #3 初始化坐标和地图
        self.init_plant_points()
        self.init_map()
        #9 调用初始化僵尸的方法
        self.init_zombies()
        #1 只要游戏没结束，就一直循环
        while not GAMEOVER:
            #1 渲染白色背景
            MainGame.window.fill((255, 255, 255))
            #2 渲染的文字和坐标位置
            MainGame.window.blit(self.draw_text('{}'.format(MainGame.money), 30, (0, 150, 150)), (60, 15))
            MainGame.window.blit(self.draw_text(
                '当前关数{}，得分{},距离下关还差{}分'.format(MainGame.shaoguan, MainGame.score, MainGame.remnant_score), 15,
                (0, 150, 150)), (5, 60))
            self.load_help_text()

            #3 需要反复加载地图
            self.load_map()
            #6 调用加载植物的方法
            self.load_plants()
            #7  调用加载所有子弹的方法
            self.load_peabullets()
            #8 调用事件处理的方法
            self.deal_events()
            #9 调用展示僵尸的方法
            self.load_zombies()
            #9 计数器增长，每数到100，调用初始化僵尸的方法
            MainGame.count_zombie += 1
            if MainGame.count_zombie > MainGame.produce_zombie:
                self.init_zombies()
                MainGame.count_zombie = 0
                #print("刷新僵尸")
            #9 pygame自己的休眠
            pygame.time.wait(10)
            #1 实时更新
            pygame.display.update()
    # 因僵尸达到屋内导致游戏结束
    def gameOverz(self):
        
        MainGame.window.blit(self.draw_text('僵尸吃掉了你的脑子！！！！', 50, (255, 0, 0)), (150, 250))
        pygame.display.update()
        pygame.mixer.music.stop()
        pygame.mixer.music.load(SOUND_PATH+'gameover.mp3')
        pygame.mixer.music.play(1,0)
        pygame.time.wait(4000)
        #print('游戏结束')
        pygame.time.wait(400)
        global GAMEOVER
        GAMEOVER = True
    # 因通关五关而游戏结束
    def gameOverw(self): 
        MainGame.window.blit(self.draw_text('你赢了！！！！', 50, (255, 0, 0)), (150, 250))
        pygame.display.update()
        pygame.mixer.music.stop()
        pygame.mixer.music.load(SOUND_PATH+'win.mp3')
        pygame.mixer.music.play(1,0)
        pygame.time.wait(4000)
        #print('游戏结束')
        pygame.time.wait(400)
        global GAMEOVER
        GAMEOVER = True
    #10 程序结束方法
    def gameOver(self):
        
        MainGame.window.blit(self.draw_text('游戏结束', 50, (255, 0, 0)), (300, 200))
        pygame.display.update()
        #print('游戏结束')
        #pygame.time.wait(1000)
        global GAMEOVER
        GAMEOVER = True

        
        
#1 启动主程序
if __name__ == '__main__':
    game = MainGame()
    game.start_game()