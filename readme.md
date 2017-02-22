QRCode

The two files qr_code.py and server.py facilitates s flask-RESTful server to create a QR image from client provided data. 
It can also read data from an uploaded QR image and output the data written in the image.

Steps to run :

1) update server.py with the IP of the server machine and the port of your choice in the line: 
   if name == "main": 
       qrc.run(ip, port=port, debug=True)

   What I did is create a virtual CentOS machine in Oracle VirtualBox and enabled port forwarding 
   by updating the host port and the guest port field with a port number, to be used in the above line. 
   The ip is the machine ip provided by ifconfig. 
   Please note to shut off the firewall of both Host and VM to facilitate the communication.

2) The cURL command to create a QR image with supplied information is : 
   curl -i -H "Content-Type: application/json" -X POST -d "{\"name\" : \"Niladri\", \"sex\" : \"M\", \"age\" : 31}" http://127.0.0.1:8888/qrcode
   The image would get created in the same path as the server.
   
3) Get the image and scan with a QRCode app and get the auto-generated ID.

4) cURL cmd to login : curl -i -H "Accept:application/json" -H "Authorization:Basic Njc0OTgwMzdEMEY3NjdERQ==" -X POST http://127.0.0.1:8888/qrcode/login
   the base64 encoding of the auto generated ID (mentioned in point 3) can be done in the following link :
   https://www.base64encode.org/
   Here the base64encoded version of the ID is Njc0OTgwMzdEMEY3NjdERQ==
   
5) The return value of the login curl command, on success, would be,

	HTTP/1.0 200 OK
	Content-Type: text/html; charset=utf-8
	Content-Length: 3
	Set-Cookie: token=WyI2NzQ5ODAzN0QwRjc2N0RFIl0.C43Xcw.chFt8TJ6-CuXm7aV4XX5Q4zZoyQ
	; Path=/
	Server: Werkzeug/0.11.15 Python/2.7.5
	Date: Tue, 21 Feb 2017 13:51:47 GMT

	200
	
	We would use the Set-Cookie value : token=WyI2NzQ5ODAzN0QwRjc2N0RFIl0.C43Xcw.chFt8TJ6-CuXm7aV4XX5Q4zZoyQ (the entire thing, along with 'token=')

6) The cURL cmd to upload an image to read data is : 
   curl -i -X GET -H "Content-Type: multipart/form-data" -F "file=@F:/QRCode/filename.png" --cookie "token=WyI2NzQ5ODAzN0QwRjc2N0RFIl0.C43Xcw.chFt8TJ6-CuXm7aV4XX5Q4zZoyQ" http://127.0.0.1:8888/qrcode
   The server would return the information embedded in the uploaded image.
   
7) To logout :
   curl -i -H "Content-Type: application/json" -X GET --cookie "token=WyI2NzQ5ODAzN0QwRjc2N0RFIl0.C43Xcw.chFt8TJ6-CuXm7aV4XX5Q4zZoyQ" http://127.0.0.1:8888/qrcode/logout
   
8) The token generated after successful login is valid for 2 minutes. After that the user will be automatically logged out.
