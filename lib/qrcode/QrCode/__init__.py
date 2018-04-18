import qrcode
from PIL import Image
import zbarlight

def generate(data, inputImg, outImg):
	qr = qrcode.QRCode(
    	version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=4,
	 	border=4);
	
	qr.add_data(data)
	qr.make(fit=True)
	qrimg = qr.make_image()

	base_img = Image.open(inputImg)
	base_img.paste(qrimg)
	base_img.save(outImg)


def scan(path):
	with open(path, 'rb') as image_file:
	    image = Image.open(image_file)
	    image.load()

	codes = zbarlight.scan_codes('qrcode', image)
	return codes