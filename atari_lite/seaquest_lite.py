from .game import Game, Sprite
from .actions import Action
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import itertools
import time

class Fish(Sprite):
    def __init__(self, y_pos, y_vel, x_pos, x_vel):
        Sprite.__init__(self, y_pos, y_vel, x_pos, x_vel)
        self.shape = np.asarray([[0, 0, 0],
                                 [0, 0, 0],
                                 [0, 0, 0]],
                                dtype=np.uint8)
        self.height, self.width = self.shape.shape


class Sub(Sprite):
    def __init__(self, y_pos, y_vel, x_pos, x_vel):
        Sprite.__init__(self, y_pos, y_vel, x_pos, x_vel)
        self.left_facing = np.asarray([[1, 1, 0, 0, 0, 0],
                                       [1, 0, 0, 0, 0, 0],
                                       [0, 0, 0, 0, 0, 0],
                                       [1, 0, 0, 0, 0, 0],
                                       [1, 1, 0, 0, 0, 0]],
                                      dtype=np.uint8)
        self.right_facing = np.asarray([[0, 0, 0, 0, 1, 1],
                                        [0, 0, 0, 0, 0, 1],
                                        [0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 1],
                                        [0, 0, 0, 0, 1, 1]],
                                       dtype=np.uint8)
        self.shape = self.left_facing
        self.height, self.width = self.shape.shape
        self.facing = -1

    def turn_right(self):
        self.facing = 1
        self.shape = self.right_facing

    def turn_left(self):
        self.facing = -1
        self.shape = self.left_facing


class Bullet(Sprite):
    def __init__(self, y_pos, y_vel, x_pos, x_vel):
        Sprite.__init__(self, y_pos, y_vel, x_pos, x_vel)
        self.shape = np.asarray([[0, 0, 0]], dtype=np.uint8)
        self.height, self.width = self.shape.shape


class SeaquestLite(Game):
    FIRE_DELAY = 2

    def __init__(self, seed=1):
        Game.__init__(self, seed)
        self.fire_counter = None
        self.fishes = None
        self.bullets = None
        self.sub = None
        self.reset()

    def _get_random_fish(self):
        return Fish(y_pos=np.random.randint(10, 50),
                    y_vel=0,
                    x_pos=np.random.choice([0, self.SCREEN_WIDTH - 3]),
                    x_vel=np.random.choice([-1, 1]))

    def reset(self):
        self._game_over = False
        self.fire_counter = 0
        self.fishes = [self._get_random_fish()]
        # self.fishes = [Fish(y_pos=40, y_vel=0, x_pos=0, x_vel=1)]
        self.bullets = []
        self.sub = Sub(y_pos=7, y_vel=0, x_pos=23, x_vel=0)

    def step(self, action=Action.NOOP):
        reward = 0

        if not self._game_over:
            self.fire_counter -= 1

            # Resolve sub-fish collision
            for fish in self.fishes:
                if fish.x_pos + 2 >= self.sub.x_pos >= fish.x_pos - 4 \
                        and fish.y_pos + 2 >= self.sub.y_pos >= fish.y_pos - 4:
                    self._game_over = True
                    return reward

            if action == Action.FIRE and self.fire_counter < 0:
                self.fire_counter = self.FIRE_DELAY
                if self.sub.facing < 0:
                    self.bullets.append(Bullet(y_pos=self.sub.y_pos + 2, y_vel=0,
                                               x_pos=self.sub.x_pos - 1, x_vel=-2))
                else:
                    self.bullets.append(Bullet(y_pos=self.sub.y_pos + 2, y_vel=0,
                                               x_pos=self.sub.x_pos + 4, x_vel=2))
            elif action == Action.RIGHT:
                self.sub.turn_right()
                if self.sub.x_pos < self.SCREEN_WIDTH - self.sub.width:
                    self.sub.x_pos += 1
            elif action == Action.LEFT:
                self.sub.turn_left()
                if self.sub.x_pos > 0:
                    self.sub.x_pos -= 1
            elif action == Action.UP:
                if self.sub.y_pos < self.SCREEN_HEIGHT - self.sub.height:
                    self.sub.y_pos += 1
            elif action == Action.DOWN:
                if self.sub.y_pos > 0:
                    self.sub.y_pos -= 1

            for sprite in self.fishes + self.bullets:
                sprite.y_pos += sprite.y_vel
                sprite.x_pos += sprite.x_vel

            self.bullets[:] = [bullet for bullet in self.bullets if bullet.y_pos > 0 and bullet.x_pos > 0
                               and bullet.y_pos + bullet.height < self.SCREEN_HEIGHT
                               and bullet.x_pos + bullet.width < self.SCREEN_WIDTH]

            self.fishes[:] = [fish for fish in self.fishes if fish.y_pos > 0 and fish.x_pos > 0
                              and fish.y_pos + fish.height < self.SCREEN_HEIGHT
                              and fish.x_pos + fish.width < self.SCREEN_WIDTH]

            for bullet, fish in list(itertools.product(self.bullets, self.fishes)):
                if fish.x_pos - 2 <= bullet.x_pos <= fish.x_pos + 2 \
                        and fish.y_pos <= bullet.y_pos <= fish.y_pos + 2:
                    self.fishes.remove(fish)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    reward += 1

            self._draw([self.sub] + self.fishes + self.bullets)

            if len(self.fishes) < 5:
                if np.random.random() < 0.1:
                    self.fishes.append(self._get_random_fish())

        return reward


if __name__ == '__main__':
    game = SeaquestLite(seed=1)
    # count = 0
    # reward = 0
    # start = time.time()
    # while count < 10000:
    #     reward += game.step(np.random.choice(Action))
    #     count += 1
    # end = time.time()
    # print('Reward: %d' % reward)
    # print('%f fps' % (10000. / (end - start)))
    fig = plt.figure()

    im = plt.imshow(game.get_screen(), animated=True, cmap='gray', vmax=1, vmin=0, origin='lower')


    def updatefig(*args):
        if not game.game_over():
            game.step(np.random.choice(Action))
        else:
            time.sleep(2)
            game.reset()
        im.set_array(game.get_screen())
        return im,


    ani = animation.FuncAnimation(fig, updatefig, interval=30, blit=True)
    plt.show()

    # while not game.game_over():
    #     game.step(Action.NOOP)
    #     screen = game.get_screen()
    #     # plt.imshow(screen, cmap='gray')
