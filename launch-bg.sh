#!/bin/bash
setterm -term linux -back default -fore black -clear all
fbi -t 2 -1 -d /dev/fb1 -noverbose -a $MENUDIR/Kali-Pi-2.8.jpg
