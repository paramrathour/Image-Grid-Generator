A Python Script which generates a grid of images. It also accounts for the ordering between these images provided the user specifies one.

The motivation behind this project is to combine all memorable images into one image while also exploiting their order of importance. For eg., this is useful when one wants to combine their favourite moment from each anime they have watched into a grid and they also want to arrange these pictures considering the amount of personal impact.

![example anime grid](https://github.com/paramrathour/website-assets/blob/main/anime-grid.jpg)

## Working
- It concatenates all the images vertically and horizontally to form a square grid of appropriate size. If a square grid is not possible then we fill empty places with blank images.

- If an ordering is provided, these images can be put in a normal row-major or horizontal snake-like or a counterclockwise spiral pattern. By passing `invert-chirality` parameter, the analogous column-major or vertical snake-like or a clockwise spiral pattern.

- Then it outputs the original and resized (compressed) version of this image grid. It also outputs a text file containing captions which specifies the image names from left to right, top to bottom in the grid. 

- The idea here is to use two files, one containing short abbreviations (image names) that map to their complete name (used in caption names). This as opposed to using image file names themselves as captions allows us to have caption names that were otherwise not allowed by the filesystem.

## Requirements
- Python 3 with libraries `NumPy`, `OpenCV`.
- A folder containing images in `png`/`jpg`/`jpeg` format.
- A file `image-names.txt` file which contains the corresponding image names on each line (preferably ordered). Only the image names contained here will be used.
- A file `image-captions.txt` which maps image names to caption names (can be in any order) in the format `<image-name> | <anime-name>`. 

## Example
Consider the pictures of Mandelbrot set with different zooom iterations. Then the iteration number is a suitable image name ([file](Example/image-names.txt)), and the names describing each iteration are suitable caption names ([file](Example/image-captions.txt)).

An example command to generate grid for images in the example directory is as below
```
python grid-generator.py --image-source 'Example/Pics/' --image-names 'Example/image-names.txt'
--image-captions 'Example/image-captions.txt' --image-destination 'Example/Outputs/'
--image-dimension '2560 1920' --grid-type 'snake' --save-jpg
```
This generates `jpg` images of the resultant horizontal snake-like grid pattern, where each image in grid is of size $2560\times1920$.

<img src="Example/Outputs/4by4.jpg" alt="Output Image" style="width=100%"/>

## Options
#### Required Parameters
    --image-source               Folder path: source of images ('png'/'jpg'/'jpeg')
    --image-destination          Folder path: destination of generated grid images
    --image-names                File: name of images
    --image-captions             File: map of image names to caption names
    --image-dimension            Integer Pair: <image-width image-height>
    --grid-type                  String: Either 'normal' or 'snake' or 'spiral'
#### Optional Parameters
    --grid-dimension             Integer Pair: <grid-width grid-height> for the compressed images
    --grid-size                  Integer: size of image grid (n images by n images)
    --force-odd-size             Pass if desired grid dimension is odd, will keep the first ordered
                                 image exactly at center in case of a spiral grid
    --grayscale-images           Pass if images are grayscale
    --invert-chirality           Pass if a grid with inverse chirality is required
    --grid-flip-up-down          Pass if a vertically flipped grid is required
    --grid-flip-left-right       Pass if a horizontally flipped grid is required
    --save-png                   Pass if desired output image extension is 'png'
    --save-jpg                   Pass if desired output image extension is 'jpg'
    --black-blank-image          Pass if desired blank images are required to be all black

For image cropping (0-based-indexing of pixel coordinates)

    --top-left-pixel             Integer Pair: <x-coordinate y-coordinate> of top left pixel
    --bottom-right-pixel         Integer Pair: <x-coordinate y-coordinate> of bottom right pixel

### Behaviour without optional commands
- No arguments need to be supplied when passing `grayscale-images`, `invert-chirality`, `save-png`, `save-jpg`, `force-odd-size`, `black-blank-image`.
- If at least one of `grid-width` and `grid-height` are not provided then the compressed output grid image will be the largest image of size less than 10 megapixels with the same scale as input image dimensions unless the given image size itself is greater than 10 megapixels and has an irreducable aspect ratio.
- If `grid-dimension` is not provided then it will automatically generate the smallest square grid that can fit all the given images and fill empty spots with blank images.
- If `grayscale-images` is not provided then the default behaviour is to assume all images are colored.
- If none of `save-jpg` and `save-png` is provided then the default behaviour is to save `png` images.
- If `black-blank-image` is not provided then the default behaviour is to assume blank images are all white.
- The image will be cropped from top left pixel to bottom right pixel if both x-coordinate and y-coordinate are specified for each case.
  - If only the top left pixel parameters are supplied then bottom right pixel is assumed to be the bottom right corner pixel.
  - If only the bottom right pixel parameters are supplied then top left pixel is assumed to be the top left corner pixel.
- Not supplying other optional arguments has no unintended consequences.

### Limitations
- All images should have same color format (i.e. either all images are grayscale, or all are colored).
- All images must have same dimension (`image-width` by `image-height`) for best results, in case a file is not of given dimension then I will rescaled to `image-width` by `image-height`. Then after scaling, the provided cropping parameters will be considered.
- All images need not have same extension but unique image names must have unique extensions corresponding to them.
