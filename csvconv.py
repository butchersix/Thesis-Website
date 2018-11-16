# CSV Format
import csv
import os
import decimal
import shutil

allClass = [ 'background', 'aeroplane', 'bicycle', 'bird', 'boat',
             'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog',
             'horse', 'motorbike', 'person', 'potted plant', 'sheep', 'sofa', 'train',
             'tv/monitor']

colorKeywords = ['Red', 'Yellow', 'Green', 'Cyan', 'Blue', 'Magenta']
columns = []
columns.append('filename')
columns.extend(allClass)

# Extend color to columns.
for color in colorKeywords:
    columns.append(color)
    columns.append('n_' + color.lower())

columns.append('emotion')
row = []

def generate():
    global allClass
    global row
    ds = input('Directory path: ')
    directory = os.listdir(ds)
    i = 0

    for file in directory:
        filename = os.fsdecode(file)
        currentRow = [0] * len(columns)
        # print(len(columns))
        # For limiting rows.
        i+=1
        if i > 3000:
            break
        
        # Check if it is a log file.
        if filename.endswith('.log'):
            fn = filename[:-4]
            currentRow[0] = fn
            checkFile = open(ds + '\\' + filename)
            lines = checkFile.readlines()
            
            # Iterate allClass.
            for line in lines:
                # In label list.
                if any(classes in line for classes in allClass):
                    currentLine = line.split()
                    cl = currentLine[2]
                    currentLabel = cl[:-1]
                    currentValue = currentLine[3]
                    index = columns.index(currentLabel)
                    currentRow[index] = currentValue
                # In color family list.
                elif any(cfamily in line for cfamily in colorKeywords):
                    currentLine = line.split()
                    cf = currentLine[0]
                    currentFamily = cf[:-1]
                    currentPercentage = currentLine[1]
                    numberOfInstances = currentLine[3]
                    index = columns.index(currentFamily)
                    currentRow[index] = currentPercentage
                    index = columns.index('n_' + currentFamily.lower())
                    currentRow[index] = numberOfInstances
                # Not matching any keywords.
                else:
                    continue
            emotionOfPainting = getEmotionLabel(filename)
            indexOfEmotion = columns.index('emotion')
            currentRow[indexOfEmotion] = emotionOfPainting
            row.append(currentRow)
        else:
            continue        
    createFile()

items = []
folders = ['AMBIGUOUS', 'anger', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust']

def scanRoot():
    global items
    global folders
    path = input('Annotator Directory: ')

    limit_emo = 29
    # Iterate over each folder.
    for folder in folders:
        npath = os.listdir(path+'\\'+folder+'\\')
        print('Scanning ' + folder + '...')
        files = []
        #limit_counter = 0
        for painting in npath:
            files.append(painting)
            #limit_counter+=1
            #if limit_counter >= limit_emo:
            #    break
        print('Total paintings for ' + folder + ': ' + str(len(files)))
        items.append(files)
    print(str(len(items)))
    # getSample()
    # generate()

def getSample():
    global items
    temp = []
    for item in items:
        temp.extend(item)

    toLogs = [w.replace('.jpg', '.log') for w in temp]
    # logs: C:\Users\K Ann\Documents\GitHub\Ground-Truth\logs
    # default: C:\Users\K Ann\Documents\GitHub\Thesis\Thesis Data\Wikiart Painting Dataset\Batch 1
    ds = input('Path of the files: ')

    # default: C:\Users\K Ann\Documents\GitHub\Ground-Truth\sample
    dest_folder = r"C:\Users\K Ann\Documents\GitHub\Ground-Truth\sample"
    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)
    os.makedirs(dest_folder)

    directory = os.listdir(ds)
    for file in directory:
        if file in toLogs:
            shutil.copy(ds+'\\'+file, dest_folder)
    print('Done! Check files at ' + str(dest_folder))
            
    

def getEmotionLabel(painting):
    # Code here for getting the annotated emotion and append it to row.
    global items
    global folders
    i = 0
    for x in items:
        temp = [w.replace('.jpg', '.log') for w in x]
        # print(temp)
        if painting in temp:
            return folders[i]
        i = i + 1
    return ''

def createFile():
    filename = input('Enter new name: ')
    # Change to desired output directory.
    mainDirectory = r'C:\\Users\\K Ann\\Documents\\GitHub\\Ground-Truth\\'

    # Create file.
    with open(mainDirectory+filename+'.csv', 'w', newline='') as file:
        wr = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        cl = [x.lower() for x in columns]
        wr.writerow(cl)

        for rows in row:
            wr.writerow(rows)
        print('File created!')

def main_process():
    scanRoot()
    decision = input('What do you want to do? \n [0] Get list of paintings from one annotator. \n [1] Generate .csv file. \n [Any] Exit \n')
    if decision == '0':
        getSample()
    elif decision == '1':
        generate()
    else:
        exit()
    main_process()

# Main Process
main_process()