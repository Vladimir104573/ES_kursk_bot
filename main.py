import multiprocessing
import subprocess
import time

time


def run_script(script_path):
    subprocess.run(["python", script_path], check=True)


def main():
    bot_script = "test.py"
    grabber_script = "test2.py"

    bot_process = multiprocessing.Process(target=run_script, args=(bot_script,))
    grabber_process = multiprocessing.Process(target=run_script, args=(grabber_script,))

    bot_process.start()
    time.sleep(5)
    grabber_process.start()

    bot_process.join()
    grabber_process.join()

    print("Done...")


if __name__ == '__main__':
    main()