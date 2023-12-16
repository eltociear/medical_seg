# dataset settings
dataset_type = 'PolypSeg'
data_root = "/root/siton-gpfs-archive/haoshao/data/medical_image_segmentation/Polyp_Segmentation_mmsegmentation/"'data/DRIVE'
img_scale = (512,512)
crop_size = (224,224)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations'),
    dict(
        type='RandomResize',
        scale=img_scale,
        ratio_range=(0.5, 2.0),
        keep_ratio=True),
    dict(type='RandomCrop', crop_size=crop_size, cat_max_ratio=0.75),
    dict(type='RandomFlip', prob=0.5),
    dict(type='PhotoMetricDistortion'),
    dict(type='PackSegInputs')
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='Resize', scale=img_scale, keep_ratio=True),
    # add loading annotation after ``Resize`` because ground truth
    # does not need to do resize data transform
    dict(type='LoadAnnotations'),
    dict(type='PackSegInputs')
]
img_ratios = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75]
tta_pipeline = [
    dict(type='LoadImageFromFile', backend_args=None),
    dict(
        type='TestTimeAug',
        transforms=[
            [
                dict(type='Resize', scale_factor=r, keep_ratio=True)
                for r in img_ratios
            ],
            [
                dict(type='RandomFlip', prob=0., direction='horizontal'),
                dict(type='RandomFlip', prob=1., direction='horizontal')
            ], [dict(type='LoadAnnotations')], [dict(type='PackSegInputs')]
        ])
]
train_dataloader = dict(
    batch_size=4,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(type='InfiniteSampler', shuffle=True),
    dataset=dict(
        type='RepeatDataset',
        times=40000,
        dataset=dict(
            type=dataset_type,
            data_root=data_root,
            data_prefix=dict(
                img_path="/root/siton-gpfs-archive/haoshao/data/medical_image_segmentation/Polyp_Segmentation_mmsegmentation/TrainDataset/image/",
                seg_map_path="/root/siton-gpfs-archive/haoshao/data/medical_image_segmentation/Polyp_Segmentation_mmsegmentation/TrainDataset/mask/"),
            pipeline=train_pipeline)))
val_dataloader = dict(
    batch_size=1,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        data_prefix=dict(
            img_path="/root/siton-gpfs-archive/haoshao/data/medical_image_segmentation/Polyp_Segmentation_mmsegmentation/TestDataset/TestDataset/Kvasir/images/",
            seg_map_path="/root/siton-gpfs-archive/haoshao/data/medical_image_segmentation/Polyp_Segmentation_mmsegmentation/TestDataset/TestDataset/Kvasir/mask/"),
        pipeline=test_pipeline))
test_dataloader = val_dataloader

val_evaluator = dict(type='IoUMetric', iou_metrics=['mDice'])
test_evaluator = val_evaluator

#CVC-ColonDB  CVC-ClinicDB Kvasir ETIS-LaribPolypDB CVC-300