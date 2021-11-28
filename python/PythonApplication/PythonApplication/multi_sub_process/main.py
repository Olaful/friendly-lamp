# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time
import os
from selenium import webdriver
from threading import Thread

from logger import get_logger

logger = None
running = True
driver = None


def exit_handler():
    print(f'{os.getpid()} is exit')
    global running
    running = False


def open_chrome():
    global driver
    driver = webdriver.Chrome()
    driver.get('https://www.baidu.com')


def listen_close_signal(pipe_close_signal, pipe_send_signal):
    def listen():
        pid = pipe_close_signal.recv()
        print('recv pid: ', pid)
        if pid == os.getpid():
            exit_handler()
        else:
            pipe_send_signal.send(pid)    # continue delivery signal
        pass
    t = Thread(target=listen, args=(), daemon=True)
    t.start()


def init(**msg):
    global logger
    logger = get_logger(msg['name'])
    logger.info(f'logger[{msg["name"]}] init success')

    open_chrome()

    listen_close_signal(msg['pipe_recv_close_signal'], msg['pipe_send_close_signal'])


def shutdown():
    if driver:
        logger.info('close the browser driver')
        driver.quit()
    import logging
    logger.info('close the logging')
    logging.shutdown()


def main(**msg):
    init(**msg)
    while running:
        logger.info(f"{msg['name']} is running...")
        time.sleep(3)

    shutdown()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # pipe must defined in main
    from process_mgr import ProcessMgr, pipe_send_close_signal, pipe_recv_close_signal
    process_mgr = ProcessMgr(pipe_send_close_signal)
    num = 5
    processes = [{'name': f'process_{i}', 'pipe_recv_close_signal': pipe_recv_close_signal,
                  'pipe_send_close_signal': pipe_send_close_signal} for i in range(num)]
    for p in processes:
        # when init a process, that it will load the newest code, just like hot loading
        new_p = process_mgr.init_process(1, target=main, name=p['name'], kwargs=p, daemon=True)
        process_mgr.add(p['name'], new_p)
        process_mgr.start(p['name'])
        time.sleep(5)

    process_mgr.loop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
