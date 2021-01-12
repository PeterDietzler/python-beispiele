'''
Preprocessor function
Comments out or in lines in the given files which are between #ifdef keyword and #endif.

The keywords #ifdef, #endif and #PRE must be stand in the first column

Example:
Set define:
define = ["WINDOWS"]

Then blocks begin with #ifdef WINDOWS will be inserted in the code
and blocks which has another keyword than WINDOWS will be commented with #PRE
When you run preProcessor.py you would get following results for example:

#ifdef WINDOWS
    if self.recievedList[0] == '$batV':
        try:
            self.batVoltage = (round(float(self.recievedList[1]), 2))
            f = open(cwd + "/log/PlotBat.txt", 'a+')
            f.write("{}\n".format(time.strftime("%X,") + self.receivedMessage))
            f.close()
        except Exception as e:
            print('$batV received: ', e)
#endif

#ifdef PI
#PRE     if self.recievedList[0] == '$per':
#PRE         try:
#PRE             f = open(cwd + "/log/PlotPer.txt", 'a+')
#PRE             f.write("{}\n".format(self.receivedMessage))
#PRE             f.close()
#PRE         except Exception as e:
#PRE             print('per: ', e)
#endif

'''

# Each keyword in define means, that this section is inserted to the code
# If an "#ifdef keyword" is found and keyword is not in the define list, the section will be comment with "#PRE" until
# "#endif" is found

# put in here the keywords for the blocks, which should be enabled in the code
define = ["WINDOWS"]
#define = ["PI"]

# put in here all available keywords which are used in the code
keywords = ["WINDOWS", "PI"]

# put in here the filnames to process
files = ["globalvars.py", "testOnly.py"]

lines = []
state = 0
file = ""

def processLineComment(i, line):
    global state
    global lines

    #print(i, line)
    splitLine = line.split(" ")
    firstItem = splitLine[0].strip()
    # search for #ifdef statement and exclude keyword
    if state == 0:
        if firstItem == "#ifdef":
            if splitLine[1].strip() not in define:  # if keyword not in define, comment block out
                state = 1
    # search for #endif. If not found, check if line is already excluded.
    # if not, exclude. when find "#ifdef" then #endif is missing
    elif state == 1:
        if firstItem == "#endif":
            state = 0
            return
        elif firstItem == "#ifdef":
            print("ERROR: #endif missing: ", file, i)
            exit(1)
        elif firstItem == "#PRE":
            return
        # put 5 chars in. last is space
        lines[i] = "#PRE " + line

def processLineUnCommentALL(i, line):
    global state
    global lines

    #print(i, line)
    splitLine = line.split(" ")
    if splitLine[0].strip() == "#PRE":
        # remove 5 chars. last is space
        lines[i] = line[5:]


def check_IF_END(i, line):
    global state
    global lines

    #print(i, line)
    splitLine = line.split(" ")
    firstItem = splitLine[0].strip()

    # search for #ifdef statement
    # when find #PRE or #endif give out error
    if state == 0:
        if firstItem == "#ifdef":
            if splitLine[1].strip() not in keywords:  # if keyword is not in keywords, maybe a type error
                print("ERROR: keyword not in keywords: ", splitLine[1].strip(), file, i+1)
                exit(1)
            else:
                state = 1
        elif firstItem == "#PRE":
            print("ERROR: #ifdef missing: ", file, i)
            exit(1)
        elif firstItem == "#endif":
            print("ERROR: #ifdef missing: ", file, i)
            exit(1)


    # search for #endif.
    # when find #ifdef give out error
    elif state == 1:
        if firstItem == "#endif":
            state = 0
            return
        elif splitLine[0].strip() == "#ifdef":
            print("ERROR: #endif missing: ", file, i)
            exit(1)


# main code:
if __name__ == '__main__':
    # run through all files
    for fileName in files:

        file = fileName

        print("processing file: ", file)
        # read in file
        with open(file) as f:
            lines = f.readlines()
        f.close()

        # first check ifdef and endif statements
        state = 0
        for i, line in enumerate(lines):
            check_IF_END(i, line)

        if state == 1:
            print("ERROR: last #endif missing ", file)
            exit(1)

        # second uncomment all lines
        state = 0
        for i, line in enumerate(lines):
            processLineUnCommentALL(i, line)


        # third comment lines
        state = 0
        for i, line in enumerate(lines):
            processLineComment(i, line)
        if state == 1:
            print("ERROR: last #endif missing ", file)
            exit(1)

        # save to file
        with open(file, 'w') as f:
            for line in lines:
                f.write(line)