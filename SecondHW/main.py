from SecondHW.processor import *
import multiprocessing as mp


def Generate():
    for val in range(1000):
        yield val


def _main():
    m = mp.Manager()
    q = m.Queue()
    # m.set_start_method('fork')

    with mp.Pool(10) as pool:
        pool.apply_async(generate, (q, i))
            print(q.get(block=True))
        pool.close()
        pool.join()
    

if __name__ == "__main__":
    _main()
