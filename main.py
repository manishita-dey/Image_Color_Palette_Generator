from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import numpy as np
import matplotlib as plt
from PIL import Image


UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route("/")
def home():
        return render_template('home_page.html')


@app.route("/image", methods = ['POST'])
def upload_image():
    image = request.files['filename']
    # image_file_name = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))

    # Converting the image received in numpy array
    img = Image.open(image)
    img = np.array(img)

    # Flatting the numpy array to obtain all unique colors as rows and RGB pixels as columns
    # Also obtaining the frequency of each unique color occuring in the image
    all_color_palette_arr, occcurCount = np.unique(img.reshape(-1, img.shape[2]), axis=0, return_counts=True)

    # Zipping both the above arrays
    list_of_colors_and_occurence = zip(all_color_palette_arr, occcurCount)

    # Converting the zip into list
    zipped = list(list_of_colors_and_occurence)

    # Sorting the above obtained list in descending order of occurence frequency
    res = sorted(zipped, key = lambda x: x[1], reverse=True)

    # splicing the final obtained list to obtain top 10 most common occuring color in image
    final_top_10 = res[:10]

    color_list = []
    # converting to hexcode
    for color in final_top_10:
        hexcode = '#%02x%02x%02x' % (color[0][0],color[0][1], color[0][2])

        color_list.append(hexcode)


    return render_template('image_details.html', filename = image.filename, color_palette = color_list)


if __name__ == '__main__':
    app.run(debug=True)
