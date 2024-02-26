import utils
from constants import e_box_table, s_boxes, p_box_table, ip_inverse_table


def encrypt(input_str):
    bin_input = utils.str_to_bin(input_str)
    # Initialize lists to store round keys
    round_keys = utils.generate_round_keys()

    ip_result_str = utils.ip_on_bin_rep(bin_input)

    # The initial permutation result is divided into 2 half
    lpt = ip_result_str[:32]
    rpt = ip_result_str[32:]

    for round_num in range(16):
        # Perform expansion (32 bits to 48 bits)
        expanded_res = [rpt[i - 1] for i in e_box_table]

        # Convert the result back to a string for better visualization
        expanded_res_str = ''.join(expanded_res)
        round_key_str = round_keys[round_num]

        xor_res_str = ''.join(str(int(expanded_res_str[i]) ^ int(round_key_str[i])) for i in range(48))

        # Split the 48-bit string into 8 groups of 6 bits each
        six_bit_groups = [xor_res_str[i:i + 6] for i in range(0, 48, 6)]

        s_box_substituted = ''

        # Apply S-box substitution for each 6-bit group
        for i in range(8):
            row_bits = int(six_bit_groups[i][0] + six_bit_groups[i][-1], 2)
            col_bits = int(six_bit_groups[i][1:-1], 2)
            s_box_value = s_boxes[i][row_bits][col_bits]
            s_box_substituted += format(s_box_value, '04b')

        p_box_res = [s_box_substituted[i - 1] for i in p_box_table]
        lpt_list = list(lpt)
        new_rpt_str = ''.join([str(int(lpt_list[i]) ^ int(p_box_res[i])) for i in range(32)])

        lpt = rpt
        rpt = new_rpt_str

    # Perform the final permutation (IP-1)
    res = rpt + lpt
    cipher = ''.join([res[ip_inverse_table[i] - 1] for i in range(64)])
    return utils.bin_to_ascii(cipher)


def decrypt(cipher):
    round_keys = utils.generate_round_keys()

    # Apply Initial Permutation
    ip_dec_res_str = utils.ip_on_bin_rep(cipher)

    lpt = ip_dec_res_str[:32]
    rpt = ip_dec_res_str[32:]

    for round_num in range(16):
        expanded_res_str = ''.join([rpt[i - 1] for i in e_box_table])
        round_key_str = round_keys[15 - round_num]
        xor_res = ''.join(str(int(expanded_res_str[i]) ^ int(round_key_str[i])) for i in range(48))
        six_bit_groups = [xor_res[i:i + 6] for i in range(0, 48, 6)]
        s_box_substituted = ''

        for i in range(8):
            row_bits = int(six_bit_groups[i][0] + six_bit_groups[i][-1], 2)
            cols_bits = int(six_bit_groups[i][1: -1], 2)

            s_box_substituted += format(s_boxes[i][row_bits][cols_bits], '04b')

        p_box_res = [s_box_substituted[i - 1] for i in p_box_table]
        lpt_list = list(lpt)
        new_rpt_str = ''.join([str(int(lpt_list[i]) ^ int(p_box_res[i])) for i in range(32)])

        lpt = rpt
        rpt = new_rpt_str

    res = rpt + lpt
    cipher = ''.join([res[ip_inverse_table[i] - 1] for i in range(64)])

    return utils.bin_to_ascii(cipher)
