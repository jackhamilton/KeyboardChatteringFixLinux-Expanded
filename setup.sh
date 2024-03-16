sudo pip3 install -r requirements.txt
sudo mkdir /usr/lib/KeyboardChatteringFix/
sudo cp -r src /usr/lib/KeyboardChatteringFix/
sudo cp chattering_fix.sh /usr/lib/KeyboardChatteringFix
sudo cp chattering_fix.service /usr/lib/systemd/system
sudo mkdir /root/.config/KeyboardChatteringFix
sudo cp config /root/.config/KeyboardChatteringFix/config
sudo systemctl enable --now chattering_fix
echo "Successfully installed. You may now remove this folder."
