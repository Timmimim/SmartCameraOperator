import glob, os

# Current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
#print(current_dir)

data_dir = f"{current_dir}/data_and_labels"
print(data_dir)
# Percentage of images to be used for the test set
percentage_test = 10

# Create and/or truncate train.txt and test.txt
file_train = open('horsey_train.txt', 'w')
file_test = open('horsey_test.txt', 'w')

# Populate train.txt and test.txt
counter = 1
index_test = round(100 / percentage_test)

for pathAndFilename in glob.iglob(os.path.join(data_dir, "*.png")):

    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    if counter == index_test:
        counter = 1
        file_test.write(data_dir + "/" + title + '.png' + "\n")

    else:
        file_train.write(data_dir + "/" + title + '.png' + "\n")
        counter = counter + 1