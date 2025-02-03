import multiprocessing
import time


def send_data(queue):
    data = {"message": "Hello from test.py"}
    queue.put(data)
    print("Data sent")


if __name__ == "__main__":
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=send_data, args=(queue,))
    p.start()
    print("test started")
    p.join()