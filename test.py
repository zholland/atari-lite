import atari_lite as al
import numpy as np

if __name__ == '__main__':
    console = al.Console(al.SeaquestLite, display=False, seed=0, record_frames=True, record_dir='record')
    count = 0
    while count < 999:
        console.act(np.random.choice(al.Action))
        count += 1
