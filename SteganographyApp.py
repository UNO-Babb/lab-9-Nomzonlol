# This app will encode or decode text messages in an image file.
# The app will use RGB channels so only PNG files will be accepted.
# This technique will focus on Least Signifigant Bit (LSB) encoding.

from PIL import Image
import os

def encode(img, msg):
    #Convert the RGB to binary
    #Then adjust pixels to encode the message binary value into the last bit.
    #Each letter will take three pixels, with a spare pixel unchanged.
    pixels = img.load() # pixels is the pixel map, 2-d list of data
    width, height = img.size
    letterSpot = 0
    pixel = 0
    letterBinary = ""
    msgLength = len(msg)
    red, green, blue = pixels[0, 0]
    pixels[0,0] = (msgLength, green, blue)

    for i in range(msgLength * 3):
        x = i % width
        y = i // width

        red, green, blue = pixels[x, y]
        redBinary = numberToBinary(red)
        greenBinary = numberToBinary(green)
        blueBinary = numberToBinary(blue)

        if pixel % 3 == 0:
            letterBinary = numberToBinary(ord(msg[letterSpot]))
            #ignore the red on the first pixel of each letter.
            greenBinary = greenBinary[0:7] + letterBinary[0]
            blueBinary = blueBinary[0:7] + letterBinary[1]
        elif pixel % 3 == 1:
            redBinary = redBinary[0:7] + letterBinary[2]
            greenBinary = greenBinary[0:7] + letterBinary[3]
            blueBinary = blueBinary[0:7] + letterBinary[4]
        else:
            redBinary = redBinary[0:7] + letterBinary[5]
            greenBinary = greenBinary[0:7] + letterBinary[6]
            blueBinary = blueBinary[0:7] + letterBinary[7]

            letterSpot = letterSpot + 1

        red = binaryToNumber(redBinary)
        blue = binaryToNumber(blueBinary)
        green = binaryToNumber(greenBinary)

        pixels[x,y] = (red, green, blue)
        pixel = pixel + 1

    #Save the file that has now been encoded.
    img.save("secretImg.png", 'png')

def decode(img):
    """Takes the image file and reads the least significant bit from the RGBA channels.
    Converts that binary to decimal to ASCII."""
    msg = ""

    pixels = img.load() #Pixels is the pixel map, a 2-dimensional list of pixel data
    red, green, blue = pixels[0, 0]
    msgLength = red
    width, height = img.size
    letterSpot = 0
    pixel = 0
    letterBinary = ""
    x = 0
    y = 0
    while len(msg) < msgLength:
        red, green, blue = pixels[x, y]
        redBinary = numberToBinary(red)
        greenBinary = numberToBinary(green)
        blueBinary = numberToBinary(blue)

        if pixel % 3 == 0:
            letterBinary = greenBinary[7] + blueBinary[7]

        elif pixel % 3 == 1:
            letterBinary = letterBinary + redBinary[7] + greenBinary[7] + blueBinary[7]

        else:
            letterBinary = letterBinary + redBinary[7] + greenBinary[7] + blueBinary[7]
            letterAscii = binaryToNumber(letterBinary)
            msg = msg + chr(letterAscii)

        pixel = pixel + 1
        x = pixel % width
        y = pixel // width

    return msg

# Helper functions

def numberToBinary(num):
    """Takes a base10 number and converts to a binary string with 8 bits"""
    binary = ""
    # Convert from decimal to binary
    binary = bin(num)[2:] # bin() adds '0b' prefix, so we remove it
    # Ensure it's 8 bits by adding leading zeros if necessary
    binary = binary.zfill(8)
    return binary

def binaryToNumber(bin_str):
    """Takes a string binary value and converts it to a base10 integer."""
    decimal = 0
    # Convert binary string to decimal
    for digit in bin_str:
        decimal = decimal * 2 + int(digit)
    return decimal

def main():
    choice = input("Would you like to (e)ncode a message or (d)ecode an image? ").lower()
    
    if choice == 'e' or choice == 'encode':
        img_path = input("Enter the path to the image file: ")
        message = input("Enter the message to encode: ")
        try:
            img = Image.open(img_path)
            encode(img, message)
            print(f"Message encoded successfully! Saved as 'secretImg.png'")
            img.close()
        except Exception as e:
            print(f"Error: {e}")
    
    elif choice == 'd' or choice == 'decode':
        img_path = input("Enter the path to the encoded image file: ")
        try:
            img = Image.open(img_path)
            decoded_msg = decode(img)
            print(f"Decoded message: {decoded_msg}")
            img.close()
        except Exception as e:
            print(f"Error: {e}")
    
    else:
        print("Invalid choice. Please run the program again and select 'e' for encode or 'd' for decode.")
    
if __name__ == '__main__':
    main()
