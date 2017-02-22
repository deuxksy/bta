import threading
import datetime
import time
import random


class ThreadClass(threading.Thread):
    def run(self):
        now = datetime.datetime.now()
        time.sleep(random.randint(0, 9))
        print("{} {}".format(self.getName(), now))


if __name__ == '__main__':
    for i in range(10):
        t = ThreadClass()
        t.setName(i)
        t.start()
