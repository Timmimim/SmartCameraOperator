import glob, os

# Current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
#print(current_dir)

data_dir1 = f"{current_dir}/iteration-3-1/Kirchhellen_Snaps"
data_dir2 = f"{current_dir}/iteration-3-1/ffmpeg1"
data_dir3 = f"{current_dir}/iteration-3-1/ffmpeg2"
data_dir4 = f"{current_dir}/iteration-3-1/crops_ffmpeg1"
data_dir5 = f"{current_dir}/iteration-3-1/crops"
data_dir3 = f"{current_dir}/iteration-3-1/ffmpeg3"
data_dir4 = f"{current_dir}/iteration-3-1/crops_ffmpeg3"

# Percentage of images to be used for the test set
percentage_test = 10

# Create and/or truncate train.txt and test.txt
file_train = open('horsey_Kirchhellen_3_train.txt', 'w')
file_test = open('horsey_Kirchhellen_3_test.txt', 'w')

# Populate train.txt and test.txt
counter = 1
index_test = round(100 / percentage_test)

for pathAndFilename in glob.iglob(os.path.join(data_dir1, "*.png")):

    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    if counter == index_test:
        counter = 1
        file_test.write(data_dir1 + "/" + title + '.png' + "\n")

    else:
        file_train.write(data_dir1 + "/" + title + '.png' + "\n")
        counter = counter + 1
        
for pathAndFilename in glob.iglob(os.path.join(data_dir2, "*.png")):

    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    if counter == index_test:
        counter = 1
        file_test.write(data_dir2 + "/" + title + '.png' + "\n")

    else:
        file_train.write(data_dir2 + "/" + title + '.png' + "\n")
        counter = counter + 1
        
for pathAndFilename in glob.iglob(os.path.join(data_dir3, "*.png")):

    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    if counter == index_test:
        counter = 1
        file_test.write(data_dir3 + "/" + title + '.png' + "\n")

    else:
        file_train.write(data_dir3 + "/" + title + '.png' + "\n")
        counter = counter + 1

for pathAndFilename in glob.iglob(os.path.join(data_dir4, "*.png")):

    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    if counter == index_test:
        counter = 1
        file_test.write(data_dir4 + "/" + title + '.png' + "\n")

    else:
        file_train.write(data_dir4 + "/" + title + '.png' + "\n")
        counter = counter + 1

for pathAndFilename in glob.iglob(os.path.join(data_dir5, "*.png")):

    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    if counter == index_test:
        counter = 1
        file_test.write(data_dir5 + "/" + title + '.png' + "\n")

    else:
        file_train.write(data_dir5 + "/" + title + '.png' + "\n")
        counter = counter + 1
