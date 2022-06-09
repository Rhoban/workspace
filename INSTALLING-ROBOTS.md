# Installing robots

## Packages

```
apt-get install gdb python3 python-is-python3 vim git htop net-tools chrony
```

## Password-less sudoer

Add the following line to `/etc/sudoers`:

```
rhoban ALL=(ALL) NOPASSWD:ALL
```

## OpenVINO

If using Intel and GPU, install:

* https://docs.openvino.ai/latest/openvino_docs_install_guides_install_runtime.html

## Disabling GRUB delay

Disable the GRUB delays so that we don't wait

## Add user to dialout group

Run the following:

```
sudo adduser rhoban dialout
```

To ensure the user can access the serial ports.

## UDEV rules

Place the following in `/etc/udev/rules.d`:

```
# 45-maple.rules
# Ensuring maple is /dev/maple
ATTRS{idProduct}=="1001", ATTRS{idVendor}=="0110", MODE="664", GROUP="plugdev"
ATTRS{idProduct}=="1002", ATTRS{idVendor}=="0110", MODE="664", GROUP="plugdev"
ATTRS{idProduct}=="0003", ATTRS{idVendor}=="1eaf", MODE="664", GROUP="plugdev" SYMLINK+="maple"
ATTRS{idProduct}=="0004", ATTRS{idVendor}=="1eaf", MODE="664", GROUP="plugdev" SYMLINK+="maple"
SUBSYSTEM=="tty", ATTRS{manufacturer}=="Rhoban", MODE="664", GROUP="plugdev" SYMLINK+="maple"
```

```
# 50-usb.rules
# Ensuring USB ethernet are usbeth
SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTRS{idVendor}=="0b95", KERNEL=="eth*", NAME="usbeth"
SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTRS{idVendor}=="0bda", KERNEL=="eth*", NAME="usbeth"
```

```
# 70-wifi.rules
# Ensuring WiFi is wlan0
ACTION=="add", SUBSYSTEM=="net", KERNELS=="0000:02:00.0", NAME:="wlan0"
ACTION=="add", SUBSYSTEM=="net", KERNELS=="0000:3a:00.0", NAME:="wlan0"
```

## Configuring NetPlan

### Removing NetworkManager

Run the following commands to disable NetworkManager service:

```
sudo systemctl stop NetworkManager.service
sudo systemctl disable NetworkManager.service
sudo systemctl stop NetworkManager-wait-online.service
sudo systemctl disable NetworkManager-wait-online.service
sudo systemctl stop NetworkManager-dispatcher.service
sudo systemctl disable NetworkManager-dispatcher.service
sudo systemctl stop network-manager.service
sudo systemctl disable network-manager.service
```

You can check using `networkctl`, if everything is OK, it should show "configured" in green.


### Configuring network interfaces

Place following configurations in `/etc/netplan`:

```yaml
# /etc/netplan/00-installer-config-wifi.yaml
network:
  version: 2
  wifis:
    wlan0:
      addresses: [192.168.0.41/24]
      access-points:
        RHOBAN:
          password: PASSWORD
      nameservers:
        addresses: [192.168.0.1]
      dhcp4: false
      dhcp6: false
      routes:
        - to: default
          via: 192.168.0.1 
```

```yaml
# /etc/netplan/00-installer-config.yaml
network:
  ethernets:
## FlyCap Camera Interface
    eno1:
      addresses: [10.2.0.101/24]
      mtu: 9000
      dhcp4: false
      dhcp6: false

## Ethernet USB Interface
    usbeth:
      addresses: [10.0.0.1/24]
      dhcp4: false
      dhcp6: false
  version: 2
```

## Setup the hostnames

Edit `/etc/hostname` AND `/etc/hosts` to update the hostnames.