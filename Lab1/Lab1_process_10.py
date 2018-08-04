import numpy as np
import threading
import random
import time

matA = np.random.randint(2, size = (10, 10))
matB = np.random.randint(2, size = (10, 10))
result = np.zeros((matA.shape[0], matB.shape[1]))

def thread_func(row_star,row_end): #做矩陣相乘的動作
    print(row_star,row_end)
    for row in range(row_star,row_end):      
        result[row] = matA[row].dot(matB)
    #print(result)

def main():
    # How many thread you want to use
    thread_num = 10                              
    
    threads = []

    # Assign job to threads     
    for row in range(0, thread_num):
        thread = threading.Thread(target = thread_func, args = (row*1,(1*row)+10))             
        threads.append(thread)

    start_time = time.time()    
    # run all threads
    for thread in threads:       
        thread.start()

    # Wait for threads finish    
    for thread in threads:
        thread.join()

    print('Answer is correct:', np.all(np.matmul(matA, matB) == result))
        
    end_time = time.time()

    print('Time elapsed:\t', end_time - start_time)
     
if __name__ == "__main__":
    main()