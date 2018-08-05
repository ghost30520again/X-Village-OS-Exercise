import threading
import queue
import os

buffer_size = 5

lock = threading.Lock()
queue = queue.Queue(buffer_size)
file_count = 0

def producer(top_dir, queue_buffer):

    files = os.listdir(top_dir)
    queue.put(top_dir,block=True,timeout=10)
    for f in files:
        filepath = os.path.join(top_dir, f)
        if os.path.isdir(filepath):
            producer(filepath,queue_buffer)
           
    return    

def consumer(queue_buffer):
    global file_count
    lock.acquire()

    while not queue_buffer.empty():
        obj = queue_buffer.get(block=True,timeout=10)
        newpath=os.listdir(obj)
        for f in newpath: 
            new=os.path.join(obj,f)
            if os.path.isfile(new):
                
                file_count = file_count + 1      
    lock.release()           

def main():
    producer_thread = threading.Thread(target = producer, args = ('./testdata', queue))

    consumer_count = 20
    consumers = []
    for i in range(consumer_count):
        consumers.append(threading.Thread(target = consumer, args = (queue,)))

    producer_thread.start()
    for c in consumers:
        c.start()

    producer_thread.join()
    for c in consumers:
        c.join()

    print(file_count, 'files found.')

if __name__ == "__main__":
    main()