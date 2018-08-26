#!/usr/bin/env python3

import picamera
import os
import datetime
from time import sleep
from ftplib import FTP_TLS
from configparser import ConfigParser


if __name__ == '__main__':

    # 画像キャプチャ
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        # camera warm-up time
        sleep(2)
        camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.annotate_foreground = picamera.Color('white')
        camera.annotate_background = picamera.Color('black')
        camera.capture('capture.jpg')

    # FTPS
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

        # 画像の保存先に移動
        images_dir = config.get('web', 'images_dir')
        place = config.get('web', 'place')
        # TODO: 保存先のディレクトリが存在しない場合の処理を書く
        ftps.cwd(images_dir + '/' + place)

        with open('capture.jpg', 'rb') as f:
            ftps.storbinary("STOR capture.jpg", f)
        ftps.dir()
