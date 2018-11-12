#
# Semaphore.py
# CS3070 
#
# created: Spring '16
# updated: Summer '17
#

'''This is the Semaphore implementaion class.'''
from SL_Kernel import *
from SL_Memory import *
from SL_Process import *
from SL_Queue import *

class Semaphore(object):

##########################################
#Constructor

    def __init__(self, n, simKernel):
        ''' use as provided.
            - n is the number to set the Semaphore counter to initially
            - simKernel provides the access to the simulated kernel a real OS
                 would have when constructing a Semaphore'''
        
        self.OS = simKernel
        self.OS.write("counter",n)
        self.counter = self.OS.read("counter")
        self.queue = self.OS.getQueue()
        self.lock = self.OS.getAtomicLock()    
        '''
        attach(i, queue)
        i= detach (queue)
        RL: Ready List
        PID: CPU register holding ID of the running process
        '''
##########################################
#Instance Methods

    def wait(self, caller):
        ''' semaphore wait functionality.
            - caller is the process asking "wait?"
              (you will need caller because this is a simulated system,
               a production OS has this info available as part of the PCB)'''
        #TODO: implement
        self.lock.acquire()
        #with self.lock:
        self.counter -= 1
        self.OS.write("counter",self.counter)
        if self.counter < 0:
          self.queue.put(caller)
          self.lock.release()
          caller.sleep()
        else:
          self.lock.release()
        return
        '''
        with s.lock:
          s.c--
          if s.c<0 then 
            SAVESW
            attach(PID, s.q)
            set PID = detach(RL)
            LOADSW
        return
        '''
    def signal(self, caller):
        ''' semaphore signal functionality.
            - caller is the process providing the "signal"
              (you will need caller because this is a simulated system,
               a production OS has this info available as part of the PCB)'''
        #TODO: implement 

        self.lock.acquire()
        #with self.lock:
        self.counter +=1
        self.OS.write("counter",self.counter)
        if self.counter <= 0:
          process = self.queue.get()
          self.lock.release()
          process.wake()
          caller.slp_yeild()
        else:
          self.lock.release()
        return
        '''
          with s.lock:
            s.c++
            if s.c<= 0 then
              P = detach(s.q)
              attach(P,RL)
            return
        '''
            

                
 



