from PIL import Image as image
import numpy, sys

file = None
if len(sys.argv) < 2: sys.exit(f"Usage: python {sys.argv[0]} <filename> [size]")
else: file = sys.argv[1]
size = 2*int(int(sys.argv[2])/2) if len(sys.argv) > 2 else 40

def display_tuple(couple: numpy.ndarray) -> None:
    px = [';'.join([str(px) for px in c]) for c in couple]
    print(f"\33[1;38;2;{px[1]};48;2;{px[0]}m▄\33[0m", end="")

try: img = numpy.array(image.open(file).convert('RGB').resize((size,size)))
except: sys.exit("Failed to open file")
for y in range(0,img.shape[0],2):
    for x in range(img.shape[1]): display_tuple(img[y:y+2,x])
    print("")
