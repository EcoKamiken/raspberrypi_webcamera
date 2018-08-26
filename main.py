import os
from ftplib import FTP_TLS
from configparser import ConfigParser

if __name__ == '__main__':

    config = ConfigParser()
    conf_dir = os.path.dirname(__file__)
    config.read(conf_dir + '/' + 'config.ini', 'UTF-8')

    host = config.get('ftp', 'host')
    port = config.getint('ftp', 'port')
    user = config.get('ftp', 'user')
    passwd = config.get('ftp', 'passwd')
    timeout = config.getint('ftp', 'timeout')

    with FTP_TLS() as ftps:
        ftps.connect(host, port)
        ftps.login(user, passwd)
        ftps.prot_p()
        ftps.dir()