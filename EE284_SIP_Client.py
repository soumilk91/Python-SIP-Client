import sys

import pjsua as pj

import threading

import time



# Method to print Log of callback class

def log_cb(level, str, len):

    print(str),



# Account Callback class to get notifications of Account registration

class MyAccountCallback(pj.AccountCallback):

    def __init__(self, acc):

        pj.AccountCallback.__init__(self, acc)



# Call Callback to receive events from Call

class SRCallCallback(pj.CallCallback):

    def __init__(self, call=None):

        pj.CallCallback.__init__(self, call)

    

    

    def on_state(self):

        print("Call is :", self.call.info().state_text),

        print("last code :", self.call.info().last_code),

        print("(" + self.call.info().last_reason + ")")

        

    # This is the notification when call's media state is changed

    def on_media_state(self):

        global lib

        if self.call.info().media_state == pj.MediaState.ACTIVE:

            # Connect the call to sound device

            call_slot = self.call.info().conf_slot

            lib.conf_connect(call_slot, 0)

            lib.conf_connect(0, call_slot)

            print("Hey !!!!! Hope you are doing GOOD !!!!!!!!!!")

            print (lib)


# Lets start our main loop here

try:

    # Start of the Main Class

    # Create library instance of Lib class

    lib = pj.Lib()



    # Instantiate library with default config

    lib.init(log_cfg = pj.LogConfig(level=3, callback=log_cb))



    # Configuring one Transport Object and setting it to listen at 5060 port and UDP protocol

    trans_conf = pj.TransportConfig()

    print "-------------------------LETS START THE REGISTRATION PROCESS----------------------"
    print "\n\n"


    trans_conf.port = 5060       # 5060 is default port for SIP

    a=raw_input("Please Enter the IP address of the Client: ")
    print "Using the default port number for SIP: 5060"

    trans_conf.bound_addr = a
    #169.254.10.120"     # IP address of PJSIP client

    transport = lib.create_transport(pj.TransportType.UDP,trans_conf)



    # Starting the instance of Lib class

    lib.start()

    lib.set_null_snd_dev()



    # Configuring Account class to register with Registrar server

    # Giving information to create header of REGISTER SIP message

    

    ab4=raw_input("Enter IP address of the Server: ")
    ab=raw_input("Enter Username: ")
    ab1=raw_input("Enter Password: ")
    ab2=raw_input("Do you want to use the display name same as the username  Y/N ??")
    if ab2=="y" or ab2=="Y":
        ab3=ab
    else:
        ab3=raw_input("Enter Display Name: ")

"""
    acc_conf = pj.AccountConfig(domain = '169.254.10.100', username = '2010', password = 'bhumika', display = '2010',

                               registrar = 'sip:169.254.10.100:5060', proxy = 'sip:169.254.10.100:5060')

    acc_conf.id = "sip:2010"

    acc_conf.reg_uri = "sip:169.254.10.100:5060"

"""

    acc_conf = pj.AccountConfig(domain = ab4, username = ab, password = ab1, display = ab3,

                               registrar = 'sip:'+ab4+'5060', proxy = 'sip:'+ab4+'5060')

    acc_conf.id = "sip:"+ab

    acc_conf.reg_uri = 'sip:'+ab4+'5060'

    acc_callback = MyAccountCallback(acc_conf)

    acc = lib.create_account(acc_conf,cb=acc_callback)



    # creating instance of AccountCallback class

    acc.set_callback(acc_callback)



    print('\n')
    print "Registration Complete-----------"
    print('Status=', acc.info().reg_status, \

         '(' + acc.info().reg_reason + ')')



    ab5=raw_input("Do you want to make a call right now ??   Y/N")

    if ab5="y" or ab5="Y":

    # Starting Calling process.
        b=raw_input("Enter the destination URI: ")

        call = acc.make_call(b, SRCallCallback())

        

        

        # Waiting Client side for ENTER command to exit

        print('Press <ENTER> to exit and destroy library')

        input = sys.stdin.readline().rstrip('\r\n')



        # We're done, shutdown the library

        lib.destroy()

        lib = None

    else:

        print" Unregistering ---------------------------"
        time.sleep(2)
        print "Destroying Libraries --------------"
        time.sleep(2)
        lib.destroy()
        lib = None
        sys.exit(1)


except pj.Error, e:

    print("Exception: " + str(e))

    lib.destroy()

    lib = None

    sys.exit(1)

