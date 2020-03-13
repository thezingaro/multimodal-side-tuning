from __future__ import print_function, division

import math
from warnings import filterwarnings

import torch
from torch.backends import cudnn
from torch.utils.data import DataLoader

import conf
from datasets.tobacco import TobaccoImageDataset
from models.mobilenet import FineTuneModel
from models.utils import ImageTrainingPipeline

filterwarnings("ignore")

torch.manual_seed(conf.core.seed)
cudnn.deterministic = True

print('\nLoading data...', end=' ')
image_dataset = TobaccoImageDataset(conf.dataset.image_root_dir, conf.dataset.image_lengths)
image_dataloaders = {
    x: DataLoader(image_dataset.datasets[x],
                  batch_size=conf.dataset.image_batch_sizes[x],
                  shuffle=bool(x == 'train' or x == 'val'),
                  num_workers=0,
                  pin_memory=True)
    for x in conf.dataset.image_batch_sizes
}
print('done.')

print('\nModel train and evaluation...')
image_model = FineTuneModel(len(image_dataset.classes)).to(conf.core.device)
image_criterion = torch.nn.CrossEntropyLoss().to(conf.core.device)
image_optimizer = torch.optim.SGD(image_model.parameters(), lr=conf.model.image_lr, momentum=conf.model.image_momentum)
image_scheduler = torch.optim.lr_scheduler.LambdaLR(image_optimizer,
                                                    lambda epoch: conf.model.image_lr * math.sqrt(
                                                        1 - epoch / conf.model.image_num_epochs))
pipeline = ImageTrainingPipeline(image_model,
                                 image_optimizer,
                                 image_criterion,
                                 image_scheduler)
pipeline.run(image_dataloaders['train'],
             image_dataloaders['val'],
             image_dataloaders['test'],
             conf.model.image_num_epochs)