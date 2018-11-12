#
# ATM.py
# CS3070 
#
# created: Spring '16
# updated: Summer '17
#


import random
import time

from ATMMessage import *


'''The ATM client objects '''
class ATM(object):

    EXIT = 'exit'

##########################################
#Constructor

    def __init__(self, cName, seed, connectionIn):

        self.atmConection = connectionIn

        self.transactionTotal = 0
        
        self.name = cName
        self.again = True
        random.seed(seed)


        

##########################################
#Instance Methods


    def execute(self):
        '''this is the function passed to SL_Kernel.getNewProcess which serves as the processes "Run loop" '''
        

        while self.again:

            if self.__delayToNextTransaction__() == ATM.EXIT:
                break

            #select deposit or withdrawal amount
            transactionAmount = int( random.random() * 300)

            pull = random.random()
            if pull < 0.2:     #check balance, no transaction to compute
                transactionAmount = 0       
                # self.atmConection.send( ATMMessage.wrap(GET_BALANCE, 0) )
                # balance = self.__recieveBalance__()
                # if balance == ATM.EXIT:
                #     break

            else:
                if pull < 0.6:   #withdrawal
                    transactionAmount = -transactionAmount
                else:            #deposit
                    pass
                
                self.atmConection.send( ATMMessage.wrap(PUT_BALANCE, transactionAmount) ) #send transaction request/update
                ##atm balance must be locked after transaction amount sent

                # self.atmConection.send( ATMMessage.wrap(GET_BALANCE, 0) )   
                
                self.transactionTotal += transactionAmount      #counter for total transaction amounts incurred
                ##atm balance lock has been released
            balance = self.__recieveBalance__()     #get updated balance
            

            if balance == ATM.EXIT:
                break

                # balance += transactionAmount
            if pull < 0.2:    # did a balance inquiry, only need balance
                print ( self.name + ' balance inquiry: ' + str(balance) + '\n', end = ''  )
            else:             # did a transaction, need amount and updated balance
                print ( self.name + ' transaction for: ' + str(transactionAmount) + ', balance of: ' + str(balance) + '\n', end = ''  )
                


        print('   ATM machine', self.name, 'shutting down; transaction total was:', self.transactionTotal )
        

 
    def __recieveBalance__(self):
        '''returns EXIT to indicate a shutdown was recieved, returns the balance otherwise'''
        message = self.atmConection.recv()

        if message == SHUTDOWN:
            self.__stop__()
            return ATM.EXIT
        
        else:
            (operation, amount) = ATMMessage.unwrap(message)
            if operation == BALANCE:
                balance = amount
                return balance
                
            else:
                raise RuntimeError(operation + 'is not a return balance account operation')                    




    def __stop__(self):
        self.again = False




    def __didWeRecieveShutdownMsg__(self):
        '''return True if we did, False if not.'''
        msg = False
        if self.atmConection.poll():
            msg = self.atmConection.recv()
            if msg == SHUTDOWN:
                return True
            else:
                raise RuntimeError(msg + 'is not a shutdown so it is recvieved out of order')                    
                
        return False       




    def __delayToNextTransaction__(self):
        ''' simulated queuing delays to allow the user take care of other business, process sleeps during delay.

            Interactions with SHUTDOWN messages that are affected by or affect the delay state are handled,
            returns ATM.EXIT if a SHUTDOWN is ordered prior to completing the delay for other business. '''

        if self.__didWeRecieveShutdownMsg__():
            return ATM.EXIT
        else:
            time.sleep( random.random() * 0.2 )   #0 to 2-tenths of a second

        if self.__didWeRecieveShutdownMsg__():
            return ATM.EXIT
        
        return None


    def setProcessReference(self, st):
        ''' having this is a requirement of SL_Kernel for any program process'''
        self.processReference = st
