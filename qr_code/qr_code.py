import qrcode
import qrtools

img = qrcode.make('name: Niladri\n ID : 12345')

img.save("filename.png")

qr = qrtools.QR()

qr.decode("filename.png")

print qr.data

