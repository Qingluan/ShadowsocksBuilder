from checkout import checkout_softs , top_install_soft,   normal_install_soft,get_uninstall_softs,copy_file,run_shdowsocks,get_shadow_status
import argparse


def getArgs():
    desc = """
    this is a easy soft for quickly build a vpn by use shadowsocks and ssh
    support apt-get and yum 
    """

    parser = argparse.ArgumentParser(usage="help docs ",description=desc)
    parser.add_argument("-u","--user",help="set login info exp: -u \"qingluan 111.111.111.111  \"" )
    parser.add_argument("-c","--passwd",default=None,help="set password within ssh")
    parser.add_argument("-p","--port",default="22",help="this represent ssh's port ,default is \"22\" ")

    parser.add_argument("-s","--get-status",default=False,action="store_true",help="if this option selected , will just get status in remote server ")

    return parser.parse_args()



class ShadowBuilder(object):

    def __init__(self,login_info,passwd=None):
        self.login_info = login_info
        self.checkout_softs = ["pip","ssserver"]
        self.passwd = passwd
    def work(self):
        softs = self.checkout_softs

        print("start checkout ====> ")
        uninstall = checkout_softs(self.login_info,softs,self.passwd)

        top,normal = get_uninstall_softs(uninstall)
        
        if  top ==[] and  normal ==[]:
            print("start build new ====> ")
            self.build()
        else:
            if top:
                print(top_install_soft(self.login_info,top,self.passwd))
            if normal:
                print(normal_install_soft(self.login_info,normal,self.passwd))

            print("start build ====> ")
            self.build()

    def build(self):

        copy_file(self.login_info,"default_config.json","~",self.passwd)
        run_shdowsocks(self.login_info,self.passwd)


    def get_Stat(self):
        softs = self.checkout_softs

        uninstall = checkout_softs(self.login_info,softs,self.passwd)
        print(uninstall)
        top,normal = get_uninstall_softs(uninstall)
        if top or normal:
            print("follow is not installed : \n",top,normal)
            return False
        else:
            
            print(get_shadow_status(self.login_info,self.passwd))

if __name__ == "__main__":
    args = getArgs()

    user,ip = args.user.split()
    port = args.port
    passwd = args.passwd
    shadowsocks_help = ShadowBuilder([user,ip,port],passwd)
    if args.get_status:
        shadowsocks_help.get_Stat()
    else:
        shadowsocks_help.work()






        

        


