import threading
import queue

# =========================
# TASK QUEUE
# =========================

task_queue = queue.Queue()

# số worker chạy song song
WORKER_COUNT = 5


# =========================
# WORKER FUNCTION
# =========================

def worker():

    while True:

        try:

            func, args = task_queue.get()

            func(*args)

        except Exception as e:

            print("Worker error:", e)

        finally:

            task_queue.task_done()


# =========================
# START WORKERS
# =========================

def start_workers():

    for i in range(WORKER_COUNT):

        t = threading.Thread(
            target=worker,
            daemon=True
        )

        t.start()


# =========================
# ADD TASK
# =========================

def add_task(func, *args):

    task_queue.put((func, args))


# =========================
# WAIT ALL TASKS
# =========================

def wait_all():

    task_queue.join()