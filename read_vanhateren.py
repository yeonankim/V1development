%http://bethgelab.org/datasets/vanhateren/
import numpy, array
def main(filename):
    with open(filename, 'rb') as handle:
       s = handle.read()
    arr = array.array('H', s)
    arr.byteswap()
    img = numpy.array(arr, dtype='uint16').reshape(1024, 1536)
if __name__ == "__main__":
	main()