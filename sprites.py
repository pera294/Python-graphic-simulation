import math
import random
from itertools import permutations

import pygame
import os
import config


class BaseSprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, x, y, file_name, transparent_color=None, wid=config.SPRITE_SIZE, hei=config.SPRITE_SIZE):
        pygame.sprite.Sprite.__init__(self)
        if file_name in BaseSprite.images:
            self.image = BaseSprite.images[file_name]
        else:
            self.image = pygame.image.load(os.path.join(config.IMG_FOLDER, file_name)).convert()
            self.image = pygame.transform.scale(self.image, (wid, hei))
            BaseSprite.images[file_name] = self.image
        # making the image transparent (if needed)
        if transparent_color:
            self.image.set_colorkey(transparent_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Surface(BaseSprite):
    def __init__(self):
        super(Surface, self).__init__(0, 0, 'terrain.png', None, config.WIDTH, config.HEIGHT)


class Coin(BaseSprite):
    def __init__(self, x, y, ident):
        self.ident = ident
        super(Coin, self).__init__(x, y, 'coin.png', config.DARK_GREEN)

    def get_ident(self):
        return self.ident

    def position(self):
        return self.rect.x, self.rect.y

    def draw(self, screen):
        text = config.COIN_FONT.render(f'{self.ident}', True, config.BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)


class CollectedCoin(BaseSprite):
    def __init__(self, coin):
        self.ident = coin.ident
        super(CollectedCoin, self).__init__(coin.rect.x, coin.rect.y, 'collected_coin.png', config.DARK_GREEN)

    def draw(self, screen):
        text = config.COIN_FONT.render(f'{self.ident}', True, config.RED)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)


class Agent(BaseSprite):
    def __init__(self, x, y, file_name):
        super(Agent, self).__init__(x, y, file_name, config.DARK_GREEN)
        self.x = self.rect.x
        self.y = self.rect.y
        self.step = None
        self.travelling = False
        self.destinationX = 0
        self.destinationY = 0

    def set_destination(self, x, y):
        self.destinationX = x
        self.destinationY = y
        self.step = [self.destinationX - self.x, self.destinationY - self.y]
        magnitude = math.sqrt(self.step[0] ** 2 + self.step[1] ** 2)
        self.step[0] /= magnitude
        self.step[1] /= magnitude
        self.step[0] *= config.TRAVEL_SPEED
        self.step[1] *= config.TRAVEL_SPEED
        self.travelling = True

    def move_one_step(self):
        if not self.travelling:
            return
        self.x += self.step[0]
        self.y += self.step[1]
        self.rect.x = self.x
        self.rect.y = self.y
        if abs(self.x - self.destinationX) < abs(self.step[0]) and abs(self.y - self.destinationY) < abs(self.step[1]):
            self.rect.x = self.destinationX
            self.rect.y = self.destinationY
            self.x = self.destinationX
            self.y = self.destinationY
            self.travelling = False

    def is_travelling(self):
        return self.travelling

    def place_to(self, position):
        self.x = self.destinationX = self.rect.x = position[0]
        self.y = self.destinationX = self.rect.y = position[1]

    # coin_distance - cost matrix
    # return value - list of coin identifiers (containing 0 as first and last element, as well)
    def get_agent_path(self, coin_distance):
        pass


class ExampleAgent(Agent):
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):
        path = [i for i in range(1, len(coin_distance))]
        random.shuffle(path)
        return [0] + path + [0]


class Aki(Agent):
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):

        curr = 0
        next = 0

        min = 9999
        path = [0]

        for i in range(0, len(coin_distance) - 1):

            for j in range(0, len(coin_distance)):

                if 0 < coin_distance[curr][j] < min and j not in path:
                    min = coin_distance[curr][j]
                    next = j

            path.append(next)
            curr = next
            min = 9999

        print(path + [0])

        return path + [0]


class Jocke(Agent):
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):

        min_cost = 9999
        cost = 0
        best_path=[int]

        index_ids = [i for i in range(1, len(coin_distance))]
        all_paths = list(permutations(index_ids))

        for num in range(0, len(all_paths)):
            curr = 0
            cost = 0

            for cnt in range(0, len(coin_distance) - 1):
                next = all_paths[num][cnt]
                cost += coin_distance[curr][next]

                curr = next

            next = 0
            cost += coin_distance[curr][next]

            if cost < min_cost:
                min_cost = cost
                best_path = list(all_paths[num])

        # print(min_cost)
        print([0]+best_path+[0])

        return [0]+best_path+[0]


class Uki(Agent):
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):

        def init_main_list():
            for i in range(1, len(coin_distance)):
                main_list.append(([], i, coin_distance[0][i]))

            main_list.sort(key=lambda main_list: (main_list[2], -len(main_list[0]), main_list[1]))

        def add_to_main_list(pth, next, cost):
            main_list.append((pth, next, cost))

            #main_list.sort(key=lambda main_list: (main_list[2], -len(main_list[0]), main_list[1]))

        def calculate():
            temp=main_list.pop(0)

            if temp[1] not in temp[0] and temp[1] == 0:
                finished[0]=1

            if temp[1] not in temp[0] and temp[1] !=0 :

                for i in range(0, len(coin_distance)):

                    if i == 0 and len(temp[0]) < len(coin_distance) - 2:
                        pass

                    else :
                        if i not in temp[0] and i != temp[1]:

                            if temp[0] == []:
                                add_to_main_list([temp[1]], i, temp[2] + coin_distance[temp[1]][i])
                            else:
                                pth1 = list(temp[0])
                                pth2 = temp[1]
                                pth1.append(pth2)
                                add_to_main_list(pth1, i, temp[2] + coin_distance[pth2][i])

        main_list = []
        path = []
        finished = [0]

        init_main_list()
        # add_to_main_list([1,4,3,2],1,37)

        while finished[0] != 1:
            calculate()
            main_list.sort(key=lambda main_list: (main_list[2], -len(main_list[0]), main_list[1]))


        # print(main_list)

        path = list(main_list[0][0])
        print([0] + path + [0])

        return [0] + path + [0]


class Micko(Agent):
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):

        def calculate_mst(nodes) :

            outMST = [i for i in nodes]
            #outMST = nodes
            inMST = [outMST.pop(0)]

            cost = 0

            matrix = [[0 for i in range(len(coin_distance))] for j in range(len(coin_distance))]

            while len(outMST) != 0:

                min=9999

                for i in inMST:
                    for j in range(0, len(coin_distance)):
                        if i != j and coin_distance[i][j] < min  and i in inMST and j in outMST:
                            min = coin_distance[i][j]
                            oldnode = i
                            newnode = j


                matrix[oldnode][newnode] = min
                matrix[newnode][oldnode] = min
                cost += matrix[oldnode][newnode]
                inMST.append(newnode)
                outMST.remove(newnode)

            # print(matrix)
            # print(cost)
            return cost

        def init_main_list():

            for i in range(1, len(coin_distance)):
                main_list.append(([], i, coin_distance[0][i], calculate_mst(allnodes)))

            main_list.sort(key=lambda main_list: (main_list[2] + main_list[3], -len(main_list[0]), main_list[1]))

        def add_to_main_list(pth, next, cost, mst):
            main_list.append((pth, next, cost, mst))
            main_list.sort(key=lambda main_list: (main_list[2] + main_list[3], -len(main_list[0]), main_list[1]))
            #radi brze kad je ovde sort

        def add_to_final_list(pth, next, cost):
            final_list.append((pth, next, cost))

        def calculate():
            temp = main_list.pop(0)

            if temp[1] not in temp[0] and temp[1] == 0:
                add_to_final_list(temp[0], temp[1], temp[2])
                finished[0] = 1

            if temp[1] not in temp[0] and temp[1] != 0:

                for i in range(0, len(coin_distance)):

                    if i == 0 and len(temp[0]) < len(coin_distance) - 2:
                        pass

                    else:
                        if i not in temp[0] and i != temp[1]:

                            if temp[0] == []:
                                add_to_main_list([temp[1]], i, temp[2] + coin_distance[temp[1]][i], calculate_mst(allnodes))
                            else:
                                pth1 = list(temp[0])
                                pth2 = temp[1]
                                pth1.append(pth2)

                                nodes = [node for node in allnodes if node not in pth1]
                                nodes.append(pth2)
                                nodes.append(pth1[0])
                                # print(nodes)
                                add_to_main_list(pth1, i, temp[2] + coin_distance[pth2][i], calculate_mst(nodes))

        main_list = []
        final_list = []
        path = []
        finished = [0]
        allnodes = [i for i in range(0, len(coin_distance))]

        init_main_list()
        # add_to_main_list([1,4,3,2],1,37,30)
        # print(main_list)


        while finished[0] != 1:
            calculate()
            # print(main_list)
            #main_list.sort(key=lambda main_list: (main_list[2], -len(main_list[0]), main_list[1]))

        #print(final_list)
        #print("---------------------------")
        #print(cost)
        path = list(final_list[0][0])
        print([0] + path + [0])

        return [0] + path + [0]

