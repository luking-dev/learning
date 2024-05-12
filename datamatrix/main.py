from pylibdmtx.pylibdmtx import encode, decode
from PIL import Image

encoded = encode("hello world".encode("utf8"))
img = Image.frombytes("RGB", (encoded.width, encoded.height), encoded.pixels)
img.save("output.png")
print(decode(Image.open("output.png")))
