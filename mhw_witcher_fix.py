def fix_slot_data(data):
    search_bytes = bytearray.fromhex("15000000D81812CE")
    replace_bytes = bytearray.fromhex("FFFFFFFF00000000")

    start_index = int("001A8D44", 16)
    end_index = int("001ACD44", 16)

    for i in range(start_index, end_index - len(search_bytes) + 1):
        if data[i : i + len(search_bytes)] == search_bytes:
            data[end_index:end_index] = replace_bytes
            del data[i : i + len(search_bytes)]
            break

    index = int("001ACE90", 16)
    data[index] &= 0b11111011

    return data
