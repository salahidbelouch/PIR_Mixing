import random
import numpy as np

def binary_sum(bin_a, bin_b):
    # Make sure the binary numbers have the same number of bits by padding them with leading 0s
    max_len = max(len(bin_a), len(bin_b))
    bin_a = bin_a.zfill(max_len)
    bin_b = bin_b.zfill(max_len)
    
    # Initialize the result
    result = ""
    
    # Initialize the carry bit
    carry = 0
    
    # Iterate through the binary numbers and add each corresponding pair of bits
    for i in range(max_len):
        bit_a = int(bin_a[max_len - i - 1])
        bit_b = int(bin_b[max_len - i - 1])
        sum_ = bit_a + bit_b + carry
        result = str(sum_ % 2) + result
        carry = sum_ // 2
    
    # Add the carry bit to the result if it's 1
    if carry == 1:
        result = "1" + result
    
    return result

def generate_random_binary():
    # Initialize result
    result = ""
    
    # Generate 17 random bits
    for i in range(17):
        result += str(random.randint(0, 1))
    
    return result


def binary_to_integer(bin_str):
    # Initialize result
    result = 0
    
    # Iterate through the binary string and add the corresponding value of each bit to the result
    for i in range(len(bin_str)):
        result += int(bin_str[i]) * (2 ** (len(bin_str) - i - 1))
    
    return result

def integer_to_binary(n):
    # Initialize result
    result = ""
    
    # Continuously divide the number by 2 and store the remainder until the number is 0
    while n > 0:
        result = str(n % 2) + result
        n = n // 2
    
    # Return the result padded with leading 0s to make it 8 bits long
    return result.zfill(17)

def get_ascii_value(c):
    return ord(c)

def binary_negation(bin_str):
    # Invert all the bits (change all 0s to 1s and all 1s to 0s)
    negation = ""
    for bit in bin_str:
        if bit == "0":
            negation += "1"
        else:
            negation += "0"
    
    # Add 1 to the one's complement
    carry = 1
    result = ""
    for i in range(17):
        sum_ = int(negation[16 - i]) + carry
        result = str(sum_ % 2) + result
        carry = sum_ // 2
    
    return result

def find_roots(coefficients):
    return np.roots(coefficients)

def find_messagesASCII(sum):
    s1=sum[0]
    s2=sum[1]
    s3=sum[2]


    an = 1
    an_1 = s1
    an_2 = (an_1 * s1 - s2) / 2
    an_3 = (an_2 * s1 - an_1 * s2 + s3) / 3
    return -find_roots([an, an_1, an_2, an_3])



keys_1=  generate_random_binary()
keys_2=  generate_random_binary()
keys_3=  generate_random_binary()

user_1=[ binary_negation(keys_1), keys_2]
user_2=[ binary_negation(keys_2), keys_3]
user_3=[ binary_negation(keys_3), keys_1]

user_1_Smessage= "!"
user_2_Smessage= "!"
user_3_Smessage= '!'

user_1_AsciiMessage=get_ascii_value(user_1_Smessage)
user_2_AsciiMessage=get_ascii_value(user_2_Smessage)
user_3_AsciiMessage=get_ascii_value(user_3_Smessage)

sums=[]

for i in range(1,4):
    print( "round : " + str(i))
    user_1_Bmessage= integer_to_binary(user_1_AsciiMessage**i)
    user_2_Bmessage= integer_to_binary(user_2_AsciiMessage**i)
    user_3_Bmessage= integer_to_binary(user_3_AsciiMessage**i)

    print("Binary"+user_1_Bmessage,user_2_Bmessage,user_3_Bmessage)

    user_1_Bmessage_toSend=binary_sum(user_1_Bmessage,binary_sum(user_1[0],user_1[1]))
    user_2_Bmessage_toSend=binary_sum(user_2_Bmessage,binary_sum(user_2[0],user_2[1]))
    user_3_Bmessage_toSend=binary_sum(user_3_Bmessage,binary_sum(user_3[0],user_3[1]))

    print("To send : "+ user_1_Bmessage_toSend,user_2_Bmessage_toSend,user_3_Bmessage_toSend)

    message_sum = binary_sum(user_1_Bmessage_toSend,binary_sum(user_2_Bmessage_toSend,user_3_Bmessage_toSend))

    print("sum :" + message_sum[1:])

    print(int(message_sum[2:], 2))
    sums.append(int(message_sum[2:], 2))

messages=find_messagesASCII(sums)
print(messages)
for m in messages:
    print(chr(round(m)))

    


