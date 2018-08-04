import multiprocessing
import random
import numpy as np
import time

def thread_func(row_start,row_end,result_queue,matA,matB):

    print(row_start,row_end)

    result = {}

    for row in range(row_start,row_end):      
        result[row] = np.matmul(matA[row], matB)
    result_queue.put(result)

def main():

    matA = np.random.randint(2, size = (100, 100))
    matB = np.random.randint(2, size = (100, 100))
    result = np.zeros((matA.shape[0], matB.shape[1]))
   
    result_queue = multiprocessing.Manager().Queue()
    processes = 10
    jobs = []
    new_list = []

    for row in range(processes):
        process = multiprocessing.Process(target = thread_func,args = (row*10,(10*row)+10,result_queue,matA,matB))
        jobs.append(process)

    start_time = time.time() 
    for process in jobs:
        process.start()

    for process in jobs:
        process.join()

   
    while not result_queue.empty(): 
        result = result_queue.get()
        for k in list(result):
            new = result[k].tolist()
            new_list.append(new)
        

    print('Answer is correct:', np.all(np.matmul(matA, matB) == new_list))
        
    end_time = time.time()

    print('Time elapsed:\t', end_time - start_time)

if __name__ == "__main__":
    main()