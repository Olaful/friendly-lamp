import asyncio
from threading import Thread
import multiprocessing

def asyncRun(func, num=5, *args, **kwargs):
    """
    异步执行传入的函数
    """
    tasklist = []
    for _ in range(num):
        tasklist.append(func(*args, **kwargs))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasklist))

def threadRun(func, num, *args, **kwargs):
    for _ in range(5):
        thread = Thread(target=func, *args, **kwargs)
        thread.start()

def processRun(func, num=5, *args, **kwargs):
    """
    多进程执行函数
    """
    num_cpus = multiprocessing.cpu_count()
    process = []
    for _ in range(num_cpus):
        p = multiprocessing.Process(target=threadRun, args=(func,), kwargs={'num':num})
        p.start()
        process.append(p)
    for p in process:
        p.join()
