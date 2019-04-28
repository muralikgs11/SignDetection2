# Description

The repo contains the codes for training and testing red circular road sign detection system using the YOLO architecture implemented on pyTorch. The code works on Linux, MacOS and Windows. Training is done on the GTSDB dataset ** http://benchmark.ini.rub.de/?section=gtsdb&subsection=news. The dataset is stored in the data folder.

# Requirements

Python 3.7 or later with the following packages:

- `numpy`
- `torch >= 1.0.0`
- `opencv-python`
- `tqdm`

# Training

**Start Training:** Run `train.py`.

To plot the final training results run the following command.
`from utils import utils; utils.plot_results()`


# Testing

Run `detect.py` to apply trained weights to an image, the model tests the images stored in the images contained in the ./data/samples folder.

