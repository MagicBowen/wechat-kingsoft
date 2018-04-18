# dada-qrcode
This is a QRCode generate and scan program

## dependency

### macos

```
brew install zbar
pip install zbarlight
pip install qrcode
pip install pillow
```

### centos

```
wget http://downloads.sourceforge.net/project/zbar/zbar/0.10/zbar-0.10.tar.gz  
tar -zvxf zbar-0.10.tar.gz  
yum install pdftk ImageMagick ImageMagick-devel ghostscript python-imaging python-devel
cd zbar-0.1
./configure --without-gtk --without-qt
make &&make install

pip install zbarlight
pip install qrcode
pip install pillow
```

### ubuntu

```
wget http://downloads.sourceforge.net/project/zbar/zbar/0.10/zbar-0.10.tar.gz  
tar -zvxf zbar-0.10.tar.gz  
sudo apt-get install libqt4-dev
apt-get install python-gtk2-dev
apt-get install imagemagick libmagickwand-dev
cd zbar-0.1
export CFLAGS=""
./configure
make
make install
pip3 install zbarlight
pip3 install qrcode
pip3 install pillow
```

## usage
import DadaQrCode

```generate image```

DadaQrCode.generate('{"category":"cloths", "brand":"babary", "size":"XXXL"}', "input.jpg", "output.jpg")

result = DadaQrCode.scan("output.jpg")