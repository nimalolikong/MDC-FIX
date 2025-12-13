#!/bin/sh

git config --global http.proxy "http://192.168.31.95:7890" && git config --global https.proxy "http://192.168.31.95:7890"
sh -c "$(wget -O- https://install.ohmyz.sh/)"


