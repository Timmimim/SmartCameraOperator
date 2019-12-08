import csv
import os
import shutil as sh

class Label:
    def __init__(self, type, x, y, width, height):
        self.type, self.x, self.y, self.width, self.height = int(type)-1, x, y, width, height

class User:
    def __init__(self, username):
        self.name = username
        self.labelledImages = []

class Image:
    def __init__(self, imgPath):
        chars = list(imgPath)
        filenameYet = False
        path, filename = "", ""
        for char in chars:
            if char == "/":
                filenameYet = True
            elif not filenameYet:
                path += char
            elif char == ".":
                break
            else:
                filename += char
        self.path = path
        self.filename = filename
        self.labels = []


with open('rimondo_filtered.csv', newline='') as csvfile:
    labelList = list(csv.reader(csvfile, delimiter = ",", quotechar = "|"))

    print(f"Read a total of {len(labelList)-1} labels.")

    i = 0
    users = []
    usernames = []
    for label in labelList:
        if label[1] == "username":
            pass
        else:
            if label[1] not in usernames:
                usernames.append(label[1])

    for currUsername in usernames:
        currUser = User(currUsername)

        labelledByUser = list(filter(lambda x: x[1] == currUsername, labelList))
        images = []
        for label in labelledByUser:
            if label[2] not in images:
                images.append(label[2])

        labelsPerImageByCurrUser = list()
        for imagePath in images:
            currImage = Image(imagePath)
            labelsPerImageByCurrUser = list(filter(lambda x: x[2] == imagePath, labelledByUser))

            for label in labelsPerImageByCurrUser:
                labelForCurrImageByCurrUser = Label(label[3], label[4], label[5], label[6], label[7])
                currImage.labels.append(labelForCurrImageByCurrUser)
                i+=1
            currUser.labelledImages.append(currImage)

        users.append(currUser)
    print(f"Assigned {i} labels to {len(users)} users.")


    i=0
    learnDataDirName = "data_and_labels"
    os.makedirs(learnDataDirName, exist_ok=True)
    for user in users:
        for image in user.labelledImages:
            descriptorFileName = f"{learnDataDirName}/{user.name}_{image.path}_{image.filename}"
            file = open(f"{descriptorFileName}.txt", "w+")
            for label in image.labels:
                i+=1
                file.write(f"{label.type} {label.x} {label.y} {label.width} {label.height}\n")
            file.close()
            sh.copyfile(f"./frames/{image.path}/{image.filename}.png", f"{descriptorFileName}.png")
    print(f"Saved {i} labels.")
