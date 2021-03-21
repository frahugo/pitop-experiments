# Blinky

Experiment with Python and [Pi-top](https://pi-top.com) with the expansion kit.

Run the app, scan the QR code with your mobile phone, access the web site and try it.

Links:

- [Pi-top Python SDK](https://github.com/pi-top/pi-top-Python-SDK)
- [Documentation](https://pi-top-pi-top-python-sdk.readthedocs-hosted.com/en/stable/)

## Set-up

1. Plug a push button in port D0
1. Plug a LED in port D1

## To run

    python3 main.py

## To generate the QR code

Visit https://barcode.tec-it.com/en/QRCode?data=http%3A%2F%2Fpi-top.local%3A5000%2F

Download the image and convert it to right size for Pitop mini screen:

    convert barcode.gif -gravity center -extent 128x64 -negate welcome.gif
