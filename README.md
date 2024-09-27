# _Characters in Translation: Decrypting Tulu to Kannada_

_This project focuses on developing a deep learning-based solution for translating characters from the Tulu script to Kannada. Tulu, an ancient Dravidian language spoken primarily in coastal Karnataka, lacks adequate computational resources for digitization and translation. This project leverages deep learning algorithms to recognize Tulu characters and translate them into Kannada. The use of maxpooling and Adam optimizer helped achieve 95% accuracy, providing a robust and efficient solution for cross-language character recognition._

## Project Workflow

**1. Preprocessing and Character Segmentation**

_The dataset consists of scanned A4 sheets containing handwritten Tulu characters, arranged in a 6x9 grid. In the preprocessing stage, each sheet is binarized (converted to black and white), and individual characters are extracted from each cell of the grid. These segmented characters are stored in separate folders, representing each Tulu character._

**2. Data Augmentation**

_To improve the model's ability to generalize to different handwriting styles, various augmentations are applied to the images. These include slanting the characters to simulate different writing angles. This process increases the size of the dataset and introduces variability, helping the model to handle diverse character styles._
