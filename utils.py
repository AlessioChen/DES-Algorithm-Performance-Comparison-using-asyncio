from constants import ip_table, pc1_table, shift_schedule, pc2_table


def str_to_bin(input_str: str) -> str:
    """
    Conversion of string to binary of 64 bits
    """
    bin_str = ''

    for char in input_str:
        # Get ASCII value of the character and convert it to binary
        bin_str += format(ord(char), '08b')
        bin_str = bin_str[:64]

    # Pad or truncate the binary representation to 64 bits
    bin_str = bin_str[:64].ljust(64, '0')
    return bin_str


def bin_to_ascii(bin_str: str) -> str:
    return ''.join([chr(int(bin_str[i:i + 8], 2)) for i in range(0, len(bin_str), 8)])


def ip_on_bin_rep(bin_representation: str) -> str:
    """
    Implementation of initial permutation on the binary str
    """
    return ''.join(bin_representation[ip_table[i] - 1] for i in range(64))


def key_in_bin_conv(key: str = 'abcdefgh') -> str:
    """
    Convert the characters to binary and concatenate to form a 64-bit binary string
    """
    return ''.join(format(ord(char), '08b') for char in key)


def generate_round_keys() -> [str]:
    # Key into binary
    bin_key = key_in_bin_conv()
    pc1_key_str = ''.join(bin_key[bit - 1] for bit in pc1_table)

    # Split the 56-bit key into two 28-bit halves
    c0 = pc1_key_str[:28]
    d0 = pc1_key_str[28:]
    round_keys = []

    for round_num in range(16):
        # Perform left circular shift on C and D
        c0 = c0[shift_schedule[round_num]:] + c0[: shift_schedule[round_num]]
        d0 = d0[shift_schedule[round_num]:] + d0[: shift_schedule[round_num]]
        # Concatenate C and D
        cd_concatenated = c0 + d0

        # Apply the PC2 permutation
        round_key = ''.join(cd_concatenated[bit - 1] for bit in pc2_table)

        # store the PC2 permutation
        round_keys.append(round_key)
    return round_keys
