import os, argparse, math, csv
import numpy as np
import cv2

parser = argparse.ArgumentParser()
parser.add_argument("--image-source")
parser.add_argument("--image-names")
parser.add_argument("--image-captions")
parser.add_argument("--image-destination")
parser.add_argument("--image-dimension")
parser.add_argument("--grid-dimension") 
parser.add_argument("--grid-size") 
parser.add_argument("--force-odd-size", action = 'store_true')
parser.add_argument("--grid-type")
parser.add_argument("--grayscale-images", action = 'store_true')
parser.add_argument("--invert-chirality", action = 'store_true')
parser.add_argument("--grid-flip-up-down", action = 'store_true')
parser.add_argument("--grid-flip-left-right", action = 'store_true')
parser.add_argument("--save-png", action = 'store_true')
parser.add_argument("--save-jpg", action = 'store_true')
parser.add_argument("--black-blank-image", action = 'store_true')
parser.add_argument("--top-left-pixel")
parser.add_argument("--bottom-right-pixel")
arguments = parser.parse_args()

def parse_arguments(arguments):
    number_of_pixels = 10000000
    grid_size = arguments.grid_size
    image_source = arguments.image_source
    image_names = arguments.image_names
    image_captions = arguments.image_captions
    image_destination = arguments.image_destination
    image_dimension  = arguments.image_dimension
    grid_dimension  = arguments.grid_dimension
    grayscale_images = bool(arguments.grayscale_images)
    save_png = bool(arguments.save_png)
    save_jpg = bool(arguments.save_jpg)
    force_odd_size = bool(arguments.force_odd_size)
    black_blank_image = bool(arguments.black_blank_image)
    grid_type = arguments.grid_type
    invert_chirality = bool(arguments.invert_chirality)
    grid_flip_up_down = bool(arguments.grid_flip_up_down)
    grid_flip_left_right = bool(arguments.grid_flip_left_right)
    top_left_pixel = arguments.top_left_pixel
    bottom_right_pixel = arguments.bottom_right_pixel

    if grayscale_images:
        image_depth = 1
    else:
        image_depth = 3
    if save_jpg == False and save_png == False:
        save_png = True

    image_dimension = image_dimension.split()
    image_dimension = (int(image_dimension[0]), int(image_dimension[1]))
    if grid_dimension is None:
        scale = int(math.floor(math.sqrt(number_of_pixels/(image_dimension[0]*image_dimension[1]))))
        if scale == 0:
            scale += 1
        grid_dimension = (scale * image_dimension[0], scale * image_dimension[1]);
    else:
        grid_dimension = grid_dimension.split()
        grid_dimension = (int(grid_dimension[0]), int(grid_dimension[1]))
        
    if top_left_pixel is not  None:
        top_left_pixel = top_left_pixel.split()
        top_left_pixel = (int(top_left_pixel[0]), int(top_left_pixel[1]))
    else:
        top_left_pixel = (0, 0)
    if bottom_right_pixel is not  None:
        bottom_right_pixel = bottom_right_pixel.split()
        bottom_right_pixel = (int(bottom_right_pixel[0])+1, int(bottom_right_pixel[1])+1)
    else:
        bottom_right_pixel = (image_dimension[1], image_dimension[0])

    if not os.path.exists(image_destination):
        os.mkdir(image_destination)

    names_all = []

    # Blank Image (to be put if total number of images is not a square)
    blank = "_"
    captions_all = {blank:blank}
    blank_image = np.zeros([image_dimension[1],image_dimension[0],image_depth], dtype = np.uint8)
    blank_image.fill(0 if black_blank_image else 255)

    with open(image_names) as filenames:
        for line in filenames:
            names_all.append(line.strip())

    with open(image_captions, 'r') as filenames:
        lines = csv.reader(filenames, delimiter = '|')
        for line in lines:
            captions_all[line[0].strip()] = line[1].strip()

    if grid_size == None:
        n = int(np.ceil(math.sqrt(len(names_all))))
    else:
        n = int(grid_size)

    image_input_extension = ['png', 'jpg', 'jpeg']
    return n, grid_type, invert_chirality, grid_flip_up_down, grid_flip_left_right, captions_all, names_all, blank, blank_image, image_source, image_destination, image_dimension, grid_dimension, top_left_pixel, bottom_right_pixel, image_input_extension, grayscale_images, save_png, save_jpg, force_odd_size

def get_names(i, names, blank):
    if i < len(names):
        return names[i]
    else:
        return blank

def updateGrid(grid, x, y, counter,n):
    if x >=  0 and x < n  and y >=  0 and y < n:
        grid[x][y] = counter
    return counter+1

def generate_grid(n, grid_type, invert_chirality, grid_flip_up_down, grid_flip_left_right):

    grid = np.zeros((n,n),dtype = int)
    image_status = np.zeros((n,n),dtype = int)
    counter = 0
    if grid_type == 'spiral':
        right = lambda x, y: (x, y+1)
        left  = lambda x, y: (x, y-1)
        up    = lambda x, y: (x-1, y)
        down  = lambda x, y: (x+1, y)
        direction_mapping = {0:right, 1:up, 2:left, 3:down}
        find_direction = lambda x, invert_chirality:(x+2*invert_chirality)%4 if x%2 == 0 else x%4
        counter = counter + 1
        x = n//2
        y = (n-1+invert_chirality)//2
        i = 0
        while (counter < n*n):
            repeat = (i//2)+1
            for z in range(repeat):
                x,y = direction_mapping[find_direction(i, invert_chirality)](x, y)
                counter = updateGrid(grid, x, y, counter,n)
            i = i+1
    elif grid_type == 'normal' or grid_type == 'snake':
        counter = 0
        for i in range(n):
            for j in range(n):
                grid[i][j] = counter
                counter = counter + 1
        if grid_type == 'snake':
            flip_even_rows = lambda i,x: np.flip(x) if i%2 != 0 else x
            grid = np.array([flip_even_rows(i,row) for i, row in enumerate(grid)])
        if invert_chirality:
            grid = grid.transpose();
    if grid_flip_up_down:
        grid = np.flipud(grid)
    if grid_flip_left_right:
        grid = np.fliplr(grid)
    return grid, image_status

def get_grid(i,j, grid, names):
    if grid[i][j] < len(names):
        return grid[i][j]
    else:
        return -1

def crop(image, top_left_pixel, bottom_right_pixel):
    return image[top_left_pixel[0]:bottom_right_pixel[0], top_left_pixel[1]:bottom_right_pixel[1]]

def find_image(i, j, grid, names, image_source, image_status, blank, blank_image, image_dimension, top_left_pixel, bottom_right_pixel, image_input_extension, grayscale_images):
    path = image_source + get_names(get_grid(i, j, grid, names), names, blank)
    files = [path + '.' +  extension for extension in image_input_extension]
    check = [os.path.isfile(file) for file in files]
    if (sum(check) == 0 or get_grid(i, j, grid, names) == -1):
        image = blank_image
    else:
        file = check.index(True)
        file = files[file]
        image = (cv2.imread(file, cv2.IMREAD_GRAYSCALE) if grayscale_images else cv2.imread(file, cv2.IMREAD_COLOR))
        image_status[i][j] = 1
    image = cv2.resize(image, image_dimension, interpolation = cv2.INTER_CUBIC)
    image = crop(image, top_left_pixel, bottom_right_pixel)
    return image

def concatenate_images(image_grid):
    return cv2.vconcat([cv2.hconcat(row) for row in image_grid])

def generate_caption(n, names, captions_all, grid, image_status, blank, image_destination):
    string = "From Left to Right, Top to Bottom\n"
    sep = ", "
    for i in range(n):
        for j in range(n):
            if image_status[i][j]:
                string +=  captions_all[get_names(get_grid(i, j, grid, names), names, blank)] + (sep if j < n-1 else "")
            else:
                string +=  "_" + (sep if j < n-1 else "")
        string +=  ("\n" if i < n-1 else "")
    with open(image_destination + ".txt", 'w') as file:
        file.write(string)

def generate_image_grid_with_caption(n, grid_type, invert_chirality, grid_flip_up_down, grid_flip_left_right, captions_all, names_all, blank, blank_image, image_source, image_destination, image_dimension, grid_dimension, top_left_pixel, bottom_right_pixel, image_input_extension, grayscale_images, save_png, save_jpg, force_odd_size):
    n = 2*n//2 + 1 if force_odd_size else n # To make sure n is odd 
    names = names_all[:n*n]
    grid, image_status = generate_grid(n, grid_type, invert_chirality, grid_flip_up_down, grid_flip_left_right)
    image_destination +=  str(n) + "by" + str(n)
    image_grid = [[find_image(i, j, grid, names, image_source, image_status, blank, blank_image, image_dimension, top_left_pixel, bottom_right_pixel, image_input_extension, grayscale_images) for j in range(n)] for i in range(n)]
    output = concatenate_images(image_grid)
    image_compressed = cv2.resize(output, grid_dimension, interpolation = cv2.INTER_CUBIC)
    if save_jpg:
        cv2.imwrite(image_destination + '.' + 'jpg', output)
        cv2.imwrite(image_destination + '_compressed.' + 'jpg', image_compressed)
    if save_png:
        cv2.imwrite(image_destination + '.' + 'png', output)
        cv2.imwrite(image_destination + '_compressed.' + 'png', image_compressed)
    generate_caption(n, names, captions_all, grid, image_status, blank, image_destination)

n, grid_type, invert_chirality, grid_flip_up_down, grid_flip_left_right, captions_all, names_all, blank, blank_image, image_source, image_destination, image_dimension, grid_dimension, top_left_pixel, bottom_right_pixel, image_input_extension, grayscale_images, save_png, save_jpg, force_odd_size = parse_arguments(arguments)    
generate_image_grid_with_caption(n, grid_type, invert_chirality, grid_flip_up_down, grid_flip_left_right, captions_all, names_all, blank, blank_image, image_source, image_destination, image_dimension, grid_dimension, top_left_pixel, bottom_right_pixel, image_input_extension, grayscale_images, save_png, save_jpg, force_odd_size)