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


#update session object

def updateSessionObject(request,key, data):
    obj = request.session.get(key, {})
    for key1,value in data.items():
        print ("key ", key1 , "value ", value)
        if int(value) == -1 and obj.get(key1) is not None:
            print ("deleting ")
            del obj[key1]
        elif int(value) > 0:
            obj[key1] = value

    print("key is ", key)
    request.session[key] = obj
    print ("Adding to cart update session object", request.session.get(key))
    request.session.modified = True
    return request.session

