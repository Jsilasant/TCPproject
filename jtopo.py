from mininet.topo import Topo 

class MyTopo(Topo):
    def __init__(self):
        Topo.__init__(self)
        switch = self.addSwitch('s1')
        for h in range(3):
            host = self.addHost('h%s' % (h+1))
            self.addLink(host, switch)

topos = {'mytopo': (lambda: MyTopo() ) }
