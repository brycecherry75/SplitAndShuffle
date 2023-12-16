import argparse, struct, sys, os, ctypes

if __name__ == "__main__":
  parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
  parser.add_argument("--inputfile", help="File to split")
  args = parser.parse_args()

ValidParameters = True

if not args.inputfile:
  ValidParameters = False
  print("ERROR: Input file not specified")
else:
  filename = args.inputfile
  FileSize = os.path.getsize(filename)
  if (FileSize % 4) != 0:
    ValidParameters = False
    print("ERROR: File size is not a multiple of 4")

if ValidParameters == True:
  filename = args.inputfile
  FileSize = os.path.getsize(filename)
  InputFileBuffer = (ctypes.c_byte * FileSize)()
  InputFile = open(filename, 'rb')
  InputFileBuffer = InputFile.read(FileSize)
  OutputBufferLength = int(FileSize / 2)
  OutputBuffer = (ctypes.c_byte * OutputBufferLength)()
  for CurrentFile in range (2):
    for ByteToTransfer in range (int(OutputBufferLength / 2)):
      OutputBuffer[(ByteToTransfer * 2)] = InputFileBuffer[((ByteToTransfer * 4) + (CurrentFile * 2))]
      OutputBuffer[(ByteToTransfer * 2) + 1] = InputFileBuffer[((ByteToTransfer * 4) + (CurrentFile * 2) + 1)]
    OutputFileName = filename[0]
    DecimalPointFound = False
    for FileNameCharactersToTransfer in range (len(filename)):
      if FileNameCharactersToTransfer > 0:
        if filename[FileNameCharactersToTransfer] == '.' and DecimalPointFound == False:
          DecimalPointFound = True
          OutputFileName = OutputFileName + '_' + str(CurrentFile)
          OutputFileName = OutputFileName + '.'
        else:
          OutputFileName = OutputFileName + filename[FileNameCharactersToTransfer]
    if DecimalPointFound == False:
      OutputFileName = OutputFileName + '_' + str(CurrentFile)
    OutputFile = open(OutputFileName, 'wb')
    OutputFile.write(OutputBuffer)
    OutputFile.close()
  InputFile.close()
  print("Split complete")