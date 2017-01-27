QRCode

The two files qr_code.py and server.py facilitates s flask-RESTful server to create a QR image from client provided data. 
It can also read data from an uploaded QR image and output the data written in the image.

Steps to run :

1) update server.py with the IP of the server machine and the port of your choice in the line: 
   if name == "main": 
       qrc.run(<ip>, port=<port>, debug=True)

   What I did is create a virtual CentOS machine in Oracle VirtualBox and enabled port forwarding 
   by updating the host port and the guest port field with a port number, to be used in the above line. 
   The ip is the machine ip provided by ifconfig. 
   Please note to shut off the firewall of both Host and VM to facilitate the communication.

2) The cURL command to create a QR image with supplied information is : 
   curl --data "<information>" http://127.0.0.1:8888/qrcode 
   The image would get created in the same path as the server.

3) The cURL cmd to upload an image to read data is : 
   curl -i -X GET -H "Content-Type: multipart/form-data" -F "file=@" http://127.0.0.1:8888/qrcode 
   The server would return the information embedded in the uploaded image.