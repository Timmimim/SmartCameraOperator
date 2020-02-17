import glob, os
import random
import pandas as pd
from PIL import Image

# Current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

data_dir = f"{current_dir}/iteration-3-1/ffmpeg1"
out_dir = os.path.join(current_dir, "iteration-3-1/crops_ffmpeg1")

for pathAndFilename in glob.iglob(os.path.join(data_dir, "*.png")):

	title, ext = os.path.splitext(os.path.basename(pathAndFilename))

	data = pd.read_csv(f"{data_dir}/{title}.txt", sep=" ", header=None)
	data.columns = ["detected_class", "x", "y", "w", "h"] 

	if data.shape[0] == 1:

		im = Image.open(f"{data_dir}/{title}.png")
		width, height = im.size

		# set coordinates of BoundingBox ((x,y) top-left corner)
		x = int((data.x[0] - .5*data.w[0]) * width)
		y = int((data.y[0] - .5*data.h[0]) * height)
		w = int((data.x[0] + .5*data.w[0]) * width)
		h = int((data.y[0] + .5*data.h[0]) * height)

		# set maximum extensions to either side
		max_left_extension = x
		max_top_extension = y
		max_right_extension = width - w - 1
		max_bottom_extension = height - h - 1

		x_extended = x - int(.175*random.randrange(0, max_left_extension))
		y_extended = y - int(.1*random.randrange(0, max_top_extension))
		w_extended = w + int(.05*random.randrange(0, max_right_extension))
		h_extended = h + int(.15*random.randrange(0, max_bottom_extension))

		im = im.crop((x_extended, y_extended, w_extended, h_extended))
		im.save(f"{out_dir}/{title}.png")
		im.close()

		# re-calculate yolo-style BB center coordinates
		x = x - x_extended
		y = y - y_extended
		
		new_width = w_extended - x_extended
		new_height = h_extended - y_extended

		w = data.w[0] * width 
		h = data.h[0] * height 
			
		x += .5 * w
		y += .5 * h

		print(title, new_width, new_height)

		# normalise coordinates to fit YOLO training format requirements
		x_norm = x / new_width
		y_norm = y / new_height
		w_norm = w / new_width
		h_norm = h / new_height
				
		# open txt file stream
		txt_file = open(f"{out_dir}/{title}.txt", "w+")
		txt_file.write(f"{data.detected_class[0]} {x_norm} {y_norm} {w_norm} {h_norm}\n")
		txt_file.close()


	else:	# multiple labels in one image, crop out each

		for i,label in enumerate(data.values):
			
			im = Image.open(f"{data_dir}/{title}.png")
			width, height = im.size

			l_class, l_x, l_y, l_w, l_h = label
			l_class = int(l_class)
            
			# set coordinates of BoundingBox ((x,y) top-left corner)
			x = int((l_x - .5*l_w) * width)
			y = int((l_y - .5*l_h) * height)
			w = int((l_x + .5*l_w) * width)
			h = int((l_y + .5*l_h) * height)

			# set maximum extensions to either side
			max_left_extension = x
			max_top_extension = y
			max_right_extension = width - w - 1
			max_bottom_extension = height - h - 1

			x_extended = x - int(.175*random.randrange(0, max_left_extension))
			y_extended = y - int(.1*random.randrange(0, max_top_extension))
			w_extended = w + int(.05*random.randrange(0, max_right_extension))
			h_extended = h + int(.15*random.randrange(0, max_bottom_extension))

			im = im.crop((x_extended, y_extended, w_extended, h_extended))
			im.save(f"{out_dir}/{title}_{i}.png")
			im.close()

			# re-calculate yolo-style BB center coordinates
			x = x - x_extended
			y = y - y_extended
			
			new_width = w_extended - x_extended
			new_height = h_extended - y_extended

			w = l_w * width 
			h = l_h * height 
			
			x += .5 * w
			y += .5 * h

			print(title, new_width, new_height)

			# normalise coordinates to fit YOLO training format requirements
			x_norm = x / new_width
			y_norm = y / new_height
			w_norm = w / new_width
			h_norm = h / new_height
					
			# open txt file stream
			txt_file = open(f"{out_dir}/{title}_{i}.txt", "w+")
			txt_file.write(f"{l_class} {x_norm} {y_norm} {w_norm} {h_norm}\n")
			txt_file.close()
