A Python Notebook which generates a counterclockwise spiral grid of images.

The motivation behind the program is combine all memorable images into one image. For eg., one wanted to combine their favourite moment from each anime they have watched into a grid. 

A limitation is that all images need to be of same dimensions. This can be fixed by resizing but I have left that work open.

## Working

- It concatenates all the images vertically and horizontally according to a spiral grid.

- Then it outputs the original and resized (compressed) version of this image grid. It also outputs a caption which specifies the image names from left to right, top to bottom in the grid.

- If a square grid is not possible, it will generate the smallest square grid that can fit given images and fill empty places with blank images (completely white).

## Requirements
- Python 3 with libraries `os`, `math`, `NumPy`, `csv`, `OpenCV`.

- A folder containing all required images in `png` format.

- A `Names.txt` file which contains the corresponding image names say, of anime on each line (preferably sorted). Only the image names contained here will be used. [Example file](Example/Names.txt)

- A `Complete_names.txt` which maps image names to anime names (can be in any order) in the format `<image_name> | <anime_name>`. [Example file](Example/Complete_names.txt)

- A directory specifying the destination of generated files.

### Example
An anime grid example is given [here](https://cutt.ly/animegrid) with the caption as
```
From Left to Right, Top to Bottom
Ping Pong the Animation, Elfen Lied, Death Parade, Bakemonogatari, Horimiya, Vivy: Fluorite Eye's Song, Chainsaw Man
Mononoke, Fate/Zero, The Promised Neverland, Re:Zero - Starting Life in Another World, Made in Abyss, Mob Psycho 100, 86
Mushi-Shi, Your Name, Death Note, Fullmetal Alchemist: Brotherhood, Attack on Titan, Mushoku Tensei: Jobless Reincarnation, Cyberpunk: Edgerunners
My Dress Up Darlnig, Land of the Lustrous, Violet Evergarden, Hunter x Hunter, Steins;Gate, Kaguya-sama: Love Is War, Erased
A Silent Voice, One Outs, Vinland Saga, Monster, Code Geass, Odd Taxi, Devilman Crybaby
Weathering with You, One Punch Man, Your Lie in April, Terror in Resonance, Spy x Family, Parasyte: The Maxim, Summer Time Rendering
Anohana: The Flower We Saw That Day, Prison School, Domestic Girlfriend, Love and Lies, Jujutsu Kaisen, Uncle From Another World, Bocchi the Rock!
```