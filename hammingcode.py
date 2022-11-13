import numpy as np


def generate_unity_matrix(d):
    return np.eye(d, dtype=int)


def get_data_bits_length_as_matrix(w):
    return list(map(int, w))


class HammingCode:
    # Constructor HammingCode(m)
    def __init__(self, codeword):
        self.parityMatrix = None
        self.parityBitsMatrix = None
        self.codeword = codeword
        self.k = len(userinput) - 1
        self.codewordLength = (2 ** self.k) - 1
        self.dataBitsLength = (2 ** self.k) - self.k - 1
        self.parity_unity_matrix = generate_unity_matrix(self.k)
        self.generator_unity_matrix = generate_unity_matrix(self.dataBitsLength)

    # Create generatormatrix
    def get_generator_matrix(self):
        parityBitsMatrix = self.get_parity_bits_matrix()
        generatorMatrix = np.append(self.generator_unity_matrix,
                                    [parityBitsMatrix[i] for i in range(0, len(parityBitsMatrix))])
        return np.reshape(generatorMatrix, (self.codewordLength, self.dataBitsLength))

    # Check and return result vector
    def get_check_matrix(self, codeword):
        codewordMatrix = get_data_bits_length_as_matrix(codeword)
        self.parityBitsMatrix = self.get_parity_bits_matrix()
        self.parityMatrix = np.hstack((self.parityBitsMatrix, self.parity_unity_matrix))

        return np.matmul(self.parityMatrix, codewordMatrix) % 2

    def encode(self):
        codewordMatrix = get_data_bits_length_as_matrix(self.codeword)
        generatorMatrix = self.get_generator_matrix()
        result = np.matmul(generatorMatrix, codewordMatrix) % 2

        return ''.join([str(i) for i in result])

    def decode(self, codeword):
        result = self.get_check_matrix(codeword)

        if np.all((result % 2 == 0)):
            return codeword[0:self.dataBitsLength]
        else:
            # failure codeword found, search the failure position and correct it then run decode again
            print('Failure codeword:', codeword)
            index = self.get_position(result)
            print("Position of failure:", index + 1)
            replaceChar = "0"
            if codeword.rfind("1", index, index + 1) == -1:
                replaceChar = "1"

            print("Bit-flipped codeword:", codeword)
            codeWord = codeword[:index] + replaceChar + codeword[index + 1:]
            print("Corrected codeword:  ", codeWord)

            return self.decode(codeWord)

    def get_position(self, result):
        positionArray = [0] * len(self.parityMatrix[0])

        for i in range(len(result)):
            for j in range(len(self.parityMatrix[i])):
                if self.parityMatrix[i][j] == result[i]:
                    positionArray[j] += 1

        return positionArray.index(max(positionArray))

    def get_parity_bits_matrix(self):
        parityBitsBinary = [bin(i)[2:].zfill(self.k) for i in range(1, self.codewordLength + 1)]
        datenBitsIndex = [i for i in range(1, self.codewordLength + 1) if (i & (i - 1)) != 0]
        parityBitsMatrix = [int(parityBitsBinary[dI - 1][-(pI + 1)]) for pI in range(0, self.k) for dI in datenBitsIndex]

        return np.reshape(parityBitsMatrix, (self.k, self.dataBitsLength))


while True:
    print()
    print("~~~~~~~~~~~~~~~~ (7, 4)-Hamming-Code ~~~~~~~~~~~~~~~~")
    userinput = str(input("Please enter new codeword or x for exit:\n> "))
    if userinput == "x":
        break

    if len(userinput) == 4:
        code = HammingCode(userinput)
        encoded = code.encode()
        print('Encoded: ' + encoded)
        while True:
            bitflip = str(input("Manipulate one bitflip: "))
            if len(bitflip) == 7:
                break
        decoded = code.decode(bitflip)
        print('Decoded: ' + decoded)
        print()
    else:
        print("Incorrect value. Try again. E.g. 1000")
        print()
