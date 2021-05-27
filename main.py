import time


def timer():
    global count
    count = 0
    filename = input("Which file you want to search in?: ")
    inputname = input("Type the string you want to search: ")
    start = time.time()
    exactmatch, delmatch, submatch, tranmatch, insertmatch = main(filename, inputname)
    end = time.time()
    if len(exactmatch) > 0:
        print(str(len(exactmatch)) + " Exact Match at: " + str(exactmatch) + "\n")

    else:
        print(str(len(delmatch)) + " Deletion Match at: " + str(delmatch) + "\n")
        print(str(len(submatch)) + " Substitution Match at: " + str(submatch) + "\n")
        print(str(len(tranmatch)) + " Transpositions Match at: " + str(tranmatch) + "\n")
        print(str(len(insertmatch)) + " Insertion Match at: " + str(insertmatch) + "\n")
    print("Number of times basic operation is performed: " + str(count) + "\n")
    print("Time: " + str(end - start))


NO_OF_CHARS = 256


def badcharheuristic(string, size):
    badchar = [-1] * NO_OF_CHARS
    for i in range(size):
        badchar[ord(string[i])] = i
    return badchar


def search(txt, pat):
    global count
    m = len(pat)
    n = len(txt)
    match = []
    badchar = badcharheuristic(pat, m)
    s = 0
    found = False
    while s <= n - m:
        temp = []
        j = m - 1
        while j >= 0 and (pat[j] == txt[s + j] or pat[j] == "?"):
            temp.append(txt[s+j])
            count += 1
            j -= 1
        if j < 0:
            temp = temp[::-1]
            temp = "".join(temp)
            match.append(tuple((str(s) + "-" + str(s + m - 1), temp)))
            s += (m - badchar[ord(txt[s + m])] if s + m < n else 1)
            found = True
        else:
            s += max(1, j - badchar[ord(txt[s + j])])
    return found, match


def main(filename, inputstr):
    file = "textfiles/" + filename
    f = open(file, "r")
    text = f.read()
    text = text.strip("\n")
    leninput = len(inputstr)
    delmatch = []
    submatch = []
    tranmatch = []
    insertmatch = []
    exact, exactmatch = search(text, inputstr)
    check = []
    if not exact:
        for i in range(leninput):
            temp = list(inputstr)
            temp.pop(i)
            string1 = "".join(temp)
            temp2 = string1 not in check
            if temp2:
                check.append(string1)
                temp1, tempmatch = search(text, string1)
                if temp1:
                    delmatch = delmatch + tempmatch
            temp = list(inputstr)
            temp[i] = "?"
            string2 = "".join(temp)
            temp4, tempmatch2 = search(text, string2)
            if temp4:
                submatch = submatch + tempmatch2
            check.clear()
            if i < leninput-1:
                templist = list(inputstr)
                templist[i], templist[i+1] = templist[i+1], templist[i]
                tempstr = "".join(templist)
                if tempstr not in check:
                    check.append(tempstr)
                    temp3, tempmatch1 = search(text, tempstr)
                    if temp3:
                        tranmatch = tranmatch + tempmatch1
            check.clear()
            temp = list(inputstr)
            temp.insert(i, "?")
            string3 = "".join(temp)
            temp5, tempmatch3 = search(text, string3)
            if temp5:
                insertmatch = insertmatch + tempmatch3
    print("Searching " + filename + " for " + inputstr + "\n")
    return exactmatch, delmatch, submatch, tranmatch, insertmatch


if __name__ == '__main__':
    timer()
