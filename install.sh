#!/bin/bash

sudo apt install xclip xsel
cp octaned.service.sample /etc/systemd/system/octaned.service
mkdir $HOME/.octane/
cp octane.py $HOME/.octane/
cp octane.sxhkdrc.sample %HOME/.octane/octane.sxhkdrc
chmod 644 /etc/systemd/system/octaned.service
systemctl enable octane.service