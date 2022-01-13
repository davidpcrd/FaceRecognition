import queue
from threading import Thread
from queue import Queue
import wget
import time

class Downloader(Thread):
    def __init__(self, queue: Queue, n):
        Thread.__init__(self, name=f"Thread-Downloader.{n}", daemon=True)
        self.queue = queue
        self.n = n
        self.block = False
        self.current_state = 0 # nombre de wget fait
             
    def run(self):
 
        print(f"start thread #{self.n}")
        while not self.block:
            try:

                task = self.queue.get(timeout=1)
                try:
                    wget.download(task["img"], task["path"], bar=None)
                except:
                    pass
                self.queue.task_done()
                self.current_state+=1
            except queue.Empty as e: # Quand le timeout est appeler, cette erreur est generer. Sinon ca bloque indefiniment
                pass
        print(f"stop thread #{self.n}")
          
    def kill_thread(self):
        self.block = True

    def get_current_state(self):
        return self.current_state

class Info(Thread):
    def __init__(self, workers, total):
        Thread.__init__(self, name="Thread-Info", daemon=True)
        self.workers = workers
        self.block = False
        self.total = total

    def run(self):
        while not self.block:
            current_state = 0
            for worker in self.workers:
                current_state += worker.get_current_state()
            print(f"{current_state:<2}/{self.total} || {round(current_state*100/self.total):>2}%")
            time.sleep(0.5)
    def kill_thread(self):
        self.block = True
