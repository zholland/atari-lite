from .game import Game
import matplotlib.pyplot as plt
import scipy.misc as img

class Console:
    def __init__(self, game, seed=0, display=False, record_frames=False, record_dir=''):
        if not issubclass(game, Game):
            raise ValueError('Parameter "game" must inherit from class Game.')
        self._game = game(seed)
        self._display = display
        self._record_frames = record_frames
        self._step_count = 0
        self._record_dir = record_dir
        if self._record_dir is not '' and self._record_dir[-1] is not '/':
            self._record_dir += '/'

        if self._display:
            plt.ion()
            fig = plt.figure()
            self._im = plt.imshow(self._game.get_screen(), animated=True, cmap='gray', vmax=1, vmin=0)
            plt.show()
            plt.pause(0.0001)

        if self._record_frames:
            self._save_frame()

    def _save_frame(self):
        img.imsave('%s%d.png' % (self._record_dir, self._step_count), self._game.get_screen() * 255)

    def act(self, action):
        reward = self._game.step(action)
        self._step_count += 1
        if self._display:
            self._im.set_array(self._game.get_screen())
            plt.show()
            plt.pause(0.0001)
        if self._record_frames:
            self._save_frame()

    def reset(self):
        self._game.reset()

    def get_screen(self):
        return self._game.get_screen()

    def game_over(self):
        return self._game.game_over()
