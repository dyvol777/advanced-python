from SecondHW.processor import *
from SecondHW.vk_API import *
import multiprocessing as mp
import time


def _main():
    with mp.Pool(5) as pool:
        for i in pool.imap_unordered(generate, range(50)):
            post_img(i)
            time.sleep(0.05)
        pool.close()
        pool.join()
    print('all ok!')
    

if __name__ == "__main__":
    _main()
