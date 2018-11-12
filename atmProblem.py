#
# atmProblem.py
# CS3070 
#
# created: Spring '16
# updated: Summer '17
#

from multiprocessing import Pipe   #https://docs.python.org/3.6/library/multiprocessing.html

from SL_Kernel import *


from ATMMessage import *
from ATMServer import *
from ATM import *


if __name__ == '__main__':

    #sim OS setup
    OS = SL_Kernel()
    
    #set account name and initial value
    OS.write('CS3070', 2000)

    #bidirectional (full duplex) communication channel
    alice_atmServer_client_conn, alice_atm_conn = Pipe(True)
    bob_atmServer_client_conn,   bob_atm_conn = Pipe(True)




    #prep ATMServers
    #Servers are independent programs running on same hardware
    randomSeed = 42
    transactionLimit = 40
    program1 = ATMServer('Alice',   randomSeed, 'CS3070', transactionLimit, alice_atmServer_client_conn, None, OS)
    program2 = ATMServer(  'Bob', randomSeed+1, 'CS3070', transactionLimit,   bob_atmServer_client_conn, None, OS)

    #finish OS registration of the ATMServers program's Processes
    P1 = OS.getNewProcessOnSharedHardware( program1 )
    P2 = OS.getNewProcessOnSharedHardware( program2 )
    
    #boot up ATMServers
    P1.start()
    P2.start()


    #prep ATMs, ATMs are independent programs running on independent hardware
    program3 = ATM('Alice', randomSeed+2, alice_atm_conn)
    program4 = ATM(  'Bob', randomSeed+3,   bob_atm_conn)
    
    #finish OS registration of ATMs program's Processes 
    P3 = OS.getNewProcess( program3 )
    P4 = OS.getNewProcess( program4 )

    #boot up ATMs
    P3.start()
    P4.start()
    
    #clean shutdown
    P1.join()
    P2.join()
    P3.join()
    P4.join()

    final =  OS.read('CS3070')
    print('Final account total is', final)
    
    print('Done with ATMs!')

