import time

import torch
from PIL import Image
import torchtext
import torchvision.transforms.functional as tf
import torch.nn.functional as F

from models import FusionSideNetFc

device = 'cuda' if torch.cuda.is_available() else 'cpu'

if __name__ == '__main__':
    for i in ['2045630056', '2077189218', '2501052565', '2084568423', '24008317']:
        nlp = torchtext.vocab.GloVe('42B')
        model = FusionSideNetFc(300, num_classes=10, alphas=[.3, .2, .5], dropout_prob=.5, side_fc=1024).to(device)
        img = Image.open(
            f'./data01/stefanopio.zingaro/datasets/original/Tobacco3482-jpg/ADVE/{i}.jpg')
        f = open(f'/data01/stefanopio.zingaro/datasets/original/QS-OCR-small/ADVE/{i}.txt',
                  'rb')
        t0 = time.time()

        img = img.convert('RGB')
        img = img.resize((384, 384))
        img = tf.to_tensor(img)
        img = tf.normalize(img, [0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

        t1 = time.time()

        text = f.read()
        doc = [nlp[token.decode('UTF-8')] for token in text.split()]
        padding = 500 - len(doc)
        txt = F.pad(torch.stack(doc), [0, 0, 0, padding])

        t2 = time.time()

        img, txt = img.unsqueeze(0), txt.unsqueeze(0)
        output = model((img, txt))

        print(f'IMAGE: {t1 - t0:.3f}\n'
              f'TEXT: {t2 - t1:.3f}\n'
              f'TOTAL: {time.time() - t0:.3f}')
