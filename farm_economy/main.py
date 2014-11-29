import farm_economy.swi as swi
import farm_economy.server as server


import sys
def main():
    port = int(sys.argv[1]) if len(sys.argv)>1 else 8080
    addr = ''
    swi.browser(port)
    swi.start(server.Server, port, addr=addr)

if __name__ == '__main__':
    main()
