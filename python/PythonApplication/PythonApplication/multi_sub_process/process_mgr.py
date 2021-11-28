import time
import os
import signal
import subprocess
import multiprocessing
from multiprocessing import Pipe

pipe_recv_close_signal, pipe_send_close_signal = Pipe(duplex=False)


class ProcessMgr(object):
    def __init__(self, pipe_close_signal):
        self._processes = dict()
        self._max_run_time = 0
        self._pipe_send_close_signal = pipe_close_signal

    def init_process(self, _type=0, *args, **kwargs):
        """
        :param _type: 0|subprocess; 1|multiprocessing
        :return:
        """
        if _type == 0:
            cmd = ['python', 'main.py']
            p = subprocess.Popen(cmd, shell=True)
        else:
            p = multiprocessing.Process(**kwargs)
        return p

    @staticmethod
    def get_pid(p):
        pid = getattr(p, 'ident', None) or getattr(p, 'pid')
        return pid

    def add(self, name, process):
        self._processes[name] = process

    def delete(self, name):
        self._processes.pop(name, None)

    def get(self, name):
        return self._processes.get(name, None)

    def start(self, name):
        p = self._processes[name]
        if hasattr(p, 'start'):
            p.start()

    def stop(self, name):
        # use queue to communicate with subprocess to notify close
        p = self._processes[name]
        self._pipe_send_close_signal.send(self.get_pid(p))

    def kill(self, name):
        self._processes[name].kill()

    def terminate(self, name):
        self._processes[name].terminate()

    def ctrl_c_event(self, name):
        p = self._processes[name]
        pid = getattr(p, 'ident', None) or getattr(p, 'pid')
        os.kill(pid, signal.CTRL_C_EVENT)

    def loop(self):
        self._max_run_time = time.time() + 0.166 * 60
        while True:
            print('Current process status: ')
            for name, p in self._processes.items():
                print(repr(p))
                if p.is_alive() and time.time() > self._max_run_time:
                    print('stop the process: ', name)
                    self.stop(name)
            time.sleep(5)
