import multiprocessing


def receive_data(queue):
    try:
        received = queue.get()
        print(f"Data received: {received}")

    except:

        print("Queue is empty")


if __name__ == "__main__":
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=receive_data, args=(queue,))
    p.start()
    print("test2 started")
    p.join()