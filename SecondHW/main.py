from SecondHW.processor import *
from SecondHW.vkAPI import *
import multiprocessing as mp


def _main():
    with mp.Pool(10) as pool:
        for i in pool.imap_unordered(generate, range(10)):
            postIMG(i)
        pool.close()
        pool.join()
    print('all ok!')
    

if __name__ == "__main__":
    _main()
