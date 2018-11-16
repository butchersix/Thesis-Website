import os

# List of classes
allClass = [ '__ignore__', '_background_', 'aeroplane', 'bicycle', 'bird', 'boat',
             'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog',
             'horse', 'motorbike', 'person', 'potted plant', 'sheep', 'sofa', 'train',
             'tv/monitor']
allCount = [0] * len(allClass)

def countTotal():
    global allClass
    global allCount
    ds = input('Directory path: ')
    directory = os.listdir(ds)
    classCount = 0
    numberFiles = 0
    numberJSON = 0
    # initialize to 0

    print('\n----- START -----')
    for file in directory:
        filename = os.fsdecode(file)
        #if filename.startswith('peder'):
        #    break
        if filename.endswith('.json'):
            numberJSON+=1
            checkFile = open(ds + "\\" + filename)
            lines = checkFile.read()
            print("Reading " + filename + "...")
            # for cn in allClass:
            #     getOccurences = lines.count('"label": "'+ cn +'"')
            #     index = allClass.index(cn)
            #     currentCount = allCount[index]
            #     currentCount+=getOccurences
            #     allCount[index] = currentCount
            for cn in allClass:
                index = allClass.index(cn)
                currentCount = allCount[index]
                if cn in lines:
                    currentCount+=1
                allCount[index] = currentCount
        elif filename.endswith('.jpg'):
            numberFiles+=1
        else:
            continue
    print("\n----- Classes -----")
    for x in allClass:
        getIndex = allClass.index(x)
        print('[' + str(getIndex) + '] ' + x + ': ' + str(allCount[getIndex]))
    print("------- END -------\n")
    print("Total annotated: " + str(numberJSON) + "/" + str(numberFiles))
    exitNow = input("\nRetry? \n[1] Yes [Any] No. Exit now.\n")
    if exitNow == '0' or exitNow == '1':
        if exitNow == '1':
            print("\n\n----- RESTART -----\n")
            countTotal()

def countEmotion(path, emotion):
    global allClass

    emo = emotion 
    annotatorFolder = input('Enter Annotator folder path: ')
    directory = os.listdir

# def countCSV():
#     global allClass
#     global allCount
#     ds = input('Directory path: ')
#     directory = os.listdir(ds)
#     classCount = 0
#     numberFiles = 0
#     numberLOG = 0

#     print('\n----- START -----')
#     for file in directory:
#         filename = os.fsdecode(file)

#         if filename.endswith('.log'):
#             numberLog+=1


countTotal()
