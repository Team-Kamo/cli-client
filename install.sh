#!/bin/bash

mkdir $HOME/.octane/
cp octane.py $HOME/.octane/
cp octane.sxhkdrc.sample %HOME/.octane/octane.sxhkdrc

cp octaned.service.sample /etc/systemd/system/octaned.service
chmod 644 /etc/systemd/system/octaned.service
systemctl enable octane.service
