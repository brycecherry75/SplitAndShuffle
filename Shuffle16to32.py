import argparse, struct, sys, os, ctypes

if __name__ == "__main__":
  parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
  parser.add_argument("--inputfile0", help="Input file 0")
  parser.add_argument("--inputfile1", help="Input file 1")
  parser.add_argument("--outputfile", help="Output file")
  args = parser.parse_args()

ValidParameters = True

if not args.outputfile:
  ValidParameters = False
  print("ERROR: Output file not specified")
if not args.inputfile0:
  ValidParameters = False
  print("ERROR: Input file 0 not specified")
elif not os.path.isfile(args.inputfile0):
  ValidParameters = False
  print("ERROR:", args.inputfile0, "not found")
if not args.inputfile1:
  ValidParameters = False
  print("ERROR: Input file 1 not specified")
elif not os.path.isfile(args.inputfile1):
  ValidParameters = False
  print("ERROR:", args.inputfile1, "not found")

if ValidParameters == True:
  filename0 = args.inputfile0
  filename1 = args.inputfile1
  FileSize0 = os.path.getsize(filename0)
  FileSize1 = os.path.getsize(filename1)
  if FileSize0 != FileSize1:
    ValidParameters = False
    print("ERROR: Input file sizes are all not the same")
  elif (FileSize0 % 2) != 0:
    ValidParameters = False
    print("ERROR: File sizes are not a multiple of 2")

if ValidParameters == True:
  filename0 = args.inputfile0
  filename1 = args.inputfile1
  FileSize = os.path.getsize(filename0)
  OutputFileName = args.outputfile
  OutputBuffer = (ctypes.c_byte * (FileSize * 2))()
  InputBuffer = (ctypes.c_byte * FileSize)()
  InputFile = open(filename0, 'rb')
  InputBuffer = InputFile.read(FileSize)
  InputFile.close()
  for ByteToTransfer in range (int(FileSize / 2)):
    OutputBuffer[((ByteToTransfer * 4) + 0)] = InputBuffer[(ByteToTransfer * 2)]
    OutputBuffer[((ByteToTransfer * 4) + 1)] = InputBuffer[(ByteToTransfer * 2) + 1]
  InputFile = open(filename1, 'rb')
  InputBuffer = InputFile.read(FileSize)
  InputFile.close()
  for ByteToTransfer in range (int(FileSize / 2)):
    OutputBuffer[((ByteToTransfer * 4) + 2)] = InputBuffer[(ByteToTransfer * 2)]
    OutputBuffer[((ByteToTransfer * 4) + 3)] = InputBuffer[(ByteToTransfer * 2) + 1]
  OutputFile = open(OutputFileName, 'wb')
  OutputFile.write(OutputBuffer)
  OutputFile.close()
  print("Shuffle complete")