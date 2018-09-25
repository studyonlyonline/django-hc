#get list of values enclosed in given tags
def seperateStringOnBasisOfHtmlTags(data, seperated_on):
    print  ("DATA ---> ", data)
    copy_data = data
    for tag in seperated_on:
        splited_string_list = copy_data.split(tag)
        joined_string  = "".join(splited_string_list)
        # print("Splitted string ", splited_string_list)
        # print("joined string ", joined_string)
        copy_data = joined_string.rstrip("\r\n")

    return splited_string_list
