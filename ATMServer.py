#
# ATMServer.py
# CS3070 
#
# created: Spring '16
# updated: Winter '17
#


import random

from ATMMessage import *
from SL_Kernel import *
from Semaphore import *


'''This is bank's ATM server class.
There are multiples of these running at the bank which may access the same accounts at the same time. It
does not matter if we think of them running on the same huge machine or many little ones, the data is shared.

It does not matter if the data is shared inside a database, a data structure, in a Non Uniform Memory Access
RAM, or in a standard RAM.  Shared is shared and essentially the only thing that changes is timing.
'''
class ATMServer(object):


##########################################
#Constructor

    def __init__(self, cName, seed, account, transactionLimit, connectionOut, unused, kernel):
        
        #hardware initialization
        self.OS = kernel
        self.OS.read(account)   #verify we are connected to proper memory

        self.serverConection = connectionOut
        self.name = cName
        self.account = account

        
        self.__TRANSACTION_LIMIT__ = transactionLimit
        
        self.again = True
        random.seed(seed)
        
        self.semaphore = Semaphore(1, self.OS)
        

##########################################
#Instance Methods


    def execute(self):
        '''this is the function passed to SL_Kernel.getNewProcessOnSharedHardware
           which serves as the processes "Run loop" '''

        i = 0
        while self.again:

            #check and act on sim's stop condition 
            if i >= self.__TRANSACTION_LIMIT__:
                self.again = False
                break

            i += 1
            
            #waiting for next message
            message = self.serverConection.recv()               #receiving message from ATM
            (operation, amount) = ATMMessage.unwrap(message)

            # if operation == PUT_BALANCE:                      #if ATM wants to update balance, ensure it is not locked
            #     self.putBalance(amount)                       #put updated balance sent by ATM, line 74
                
            # elif operation == GET_BALANCE:
            if operation == PUT_BALANCE:                        #only dealing with puts now
                #enter crit section
                self.semaphore.wait(self.processReference)
                balance = self.getBalance()                     #get balance request from memory
                updatedBalance = balance + amount               #add transaction amount to balance
                self.putBalance(updatedBalance)                 #update balance in memory
                self.semaphore.signal(self.processReference)
                #crit section done
                msg = ATMMessage.wrap(BALANCE, updatedBalance)
                self.serverConection.send(msg)                  #sending balance back to ATM
                    
            else:
                raise RuntimeError(operation + 'is an unrecognized account operation')                    
       
        self.serverConection.send(SHUTDOWN)
        print('   ATMServer', self.name, 'shut down')



    def getBalance(self):
        return self.OS.read(self.account)


    def putBalance(self, newBalance):           #if ATM wants to update balance, ensure it is not locked
        self.OS.write(self.account, newBalance)



    def setProcessReference(self, st):
        ''' having this is a requirement of SL_Kernel for any program process'''
        self.processReference = st



