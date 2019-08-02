import numpy as np
from torch.utils.data import Dataset


class dataset(Dataset):
    def __init__(self, image, mask, ignore=None, sky=None, aug_sky=[0, 0], part='train', f_val=0.1, seed=1):
        """ custom pytorch dataset class to load deepCR-mask training data
        :param image: image with CR
        :param mask: CR mask
        :param ignore: loss mask, e.g., bad pixel, saturation, etc.
        :param sky: (np.ndarray) [N,] sky background level
        :param aug_sky: [negative number, positive number]. Add sky background by aug_sky[0] * sky to aug_sky[1] * sky.
        :param part: either 'train' or 'val'. split by 0.8, 0.2
        :param f_val: percentage of dataset reserved as validation set.
        :param seed: fix numpy random seed to seed, for reproducibility.
        """

        np.random.seed(seed)
        len = image.shape[0]
        assert f_val < 1
        f_train = 1 - f_val
        if sky is None:
            sky = np.zeros_like(image)
        if ignore is None:
            ignore = np.zeros_like(image)
        if part == 'train':
            self.image = image[np.s_[:int(len * f_train)]]
            self.mask = mask[np.s_[:int(len * f_train)]]
            self.ignore = ignore[np.s_[:int(len * f_train)]]
            self.sky = sky[np.s_[:int(len * f_train)]]
        elif part == 'val':
            self.image = image[np.s_[int(len * f_train):]]
            self.mask = mask[np.s_[int(len * f_train):]]
            self.ignore = ignore[np.s_[int(len * f_train):]]
            self.sky = sky[np.s_[int(len * f_train):]]
        else:
            self.image = image
            self.mask = mask
            self.ignore = ignore
            self.sky = sky
        self.aug_sky = aug_sky

    def __len__(self):
        return self.image.shape[0]

    def __getitem__(self, i):
        a = (self.aug_sky[0] + np.random.rand() * (self.aug_sky[1] - self.aug_sky[0])) * self.sky[i]
        return self.image[i] + a, self.mask[i], self.ignore[i]