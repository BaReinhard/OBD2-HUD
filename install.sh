sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install pulseaudio-module-bluetooth bluez-tools
sudo gpasswd -a xbian pulse
sudo gpasswd -a xbian lp
sudo gpasswd -a pulse lp
sudo gpasswd -a xbian audio
sudo gpasswd -a pulse audio
sudo gpasswd -a pi pulse
sudo gpasswd -a pi lp
sudo gpasswd -a pulse lp
sudo gpasswd -a pi audio
sudo gpasswd -a pulse audio
sudo gpasswd -a root pulse
sudo gpasswd -a root lp
sudo gpasswd -a pulse lp
sudo gpasswd -a root audio
sudo gpasswd -a pulse audio
sudo sh -c "echo 'extra-arguments = --exit-idle-time=-1 --log-target=syslog' >> /etc/pulse/client.conf"
sudo hciconfig hci0 up
sudo hciconfig hci0 class 0x200420
sudo reboot

sudo bluetoothctl
agent KeyboardOnly
default-agent
scan on
pair xx:xx:xx:...
trust xx:xx:xx:...
exit