from models import FusionSideNetFc, FusionSideNetFcResNet, MobileNet, ResNet, SideNetResNet, SideNetMobileNet, ShawnNet

# model = FusionSideNetFc(300, num_classes=10, alphas=[.3, .3, .4], dropout_prob=.5, side_fc=512)
# print(sum(p.numel() for p in model.parameters()))
# model = FusionSideNetFc(300, num_classes=10, alphas=[.3, .3, .4], dropout_prob=.5, side_fc=1024)
# print(sum(p.numel() for p in model.parameters()))
# model = FusionSideNetFcResNet(300, num_classes=10, alphas=[.3, .3, .4], dropout_prob=.5, side_fc=512)
# print(sum(p.numel() for p in model.parameters()))
# model = FusionSideNetFcResNet(300, num_classes=10, alphas=[.3, .3, .4], dropout_prob=.5, side_fc=1024)
# print(sum(p.numel() for p in model.parameters()))
# model = MobileNet(10)
# print(sum(p.numel() for p in model.parameters()))
model = SideNetResNet(10)
print(sum(p.numel() for p in model.parameters()))
model = SideNetMobileNet(10)
print(sum(p.numel() for p in model.parameters()))
model = ShawnNet(300, num_classes=10)
print(sum(p.numel() for p in model.parameters()))