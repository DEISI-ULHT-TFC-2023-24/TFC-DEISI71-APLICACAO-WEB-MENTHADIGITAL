def multiple_appends(listname, *element):
    listname.extend(element)

def most_frequent(List):
    if len(List) > 0:
        return max(set(List), key=List.count)
    else:
        return '0'