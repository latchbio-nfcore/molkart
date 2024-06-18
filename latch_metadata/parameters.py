
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'segmentation_method': NextflowParameter(
        type=str,
        default='mesmer',
        section_title='Segmentation methods and options',
        description='List of segmentation tools to apply to the image written as a comma separated string: mesmer,cellpose,ilastik would run all three options.',
    ),
    'segmentation_min_area': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Minimum area size (in pixels) for segmentation masks.',
    ),
    'segmentation_max_area': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Maximum area size (in pixels) for segmenation masks.',
    ),
    'cellpose_diameter': NextflowParameter(
        type=typing.Optional[int],
        default=30,
        section_title=None,
        description='Cell diameter, if 0 will use the diameter of the training labels used in the model, or with built-in model will estimate diameter for each image.',
    ),
    'cellpose_chan': NextflowParameter(
        type=typing.Optional[int],
        default=0,
        section_title=None,
        description='Specifies the channel to be segmented by Cellpose.',
    ),
    'cellpose_chan2': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Specifies nuclear channel index for Cellpose if using pretrained models such as cyto.',
    ),
    'cellpose_pretrained_model': NextflowParameter(
        type=typing.Optional[str],
        default='cyto',
        section_title=None,
        description='Pretrained Cellpose model to be used for segmentation.',
    ),
    'cellpose_custom_model': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Custom Cellpose model can be provided by the user.',
    ),
    'cellpose_flow_threshold': NextflowParameter(
        type=typing.Optional[float],
        default=0.4,
        section_title=None,
        description='Flow error threshold for Cellpose.',
    ),
    'cellpose_edge_exclude': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Should cells detected near image edges be excluded.',
    ),
    'mesmer_image_mpp': NextflowParameter(
        type=typing.Optional[float],
        default=0.138,
        section_title=None,
        description='Pixel size in microns for segmentation with Mesmer.',
    ),
    'mesmer_compartment': NextflowParameter(
        type=typing.Optional[str],
        default='whole-cell',
        section_title=None,
        description='Compartment to be segmented with Mesmer (nuclear, whole-cell)',
    ),
    'ilastik_pixel_project': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Provide ilastik with a pixel classification project to produce probability maps.',
    ),
    'ilastik_multicut_project': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Provide ilastik with a multicut project to create segmentation masks.',
    ),
    'mindagap_boxsize': NextflowParameter(
        type=typing.Optional[int],
        default=3,
        section_title='Image preprocessing',
        description='Box size used by Mindagap to overcome gaps, a larger number allows to overcome large gaps, but results in less fine details in the filled grid.',
    ),
    'mindagap_loopnum': NextflowParameter(
        type=typing.Optional[int],
        default=40,
        section_title=None,
        description='Loop number performed by Mindagap. Lower values are faster, but the result is less good.',
    ),
    'clahe_cliplimit': NextflowParameter(
        type=typing.Optional[float],
        default=0.01,
        section_title=None,
        description='Contrast limit for localized changes in contrast by CLAHE.',
    ),
    'clahe_nbins': NextflowParameter(
        type=typing.Optional[int],
        default=256,
        section_title=None,
        description='Number of histogram bins to be used by CLAHE.',
    ),
    'clahe_pixel_size': NextflowParameter(
        type=typing.Optional[float],
        default=0.138,
        section_title=None,
        description='Pixel size to be used by CLAHE.',
    ),
    'clahe_kernel': NextflowParameter(
        type=typing.Optional[float],
        default=25,
        section_title=None,
        description='Kernel size to be used by CLAHE.',
    ),
    'skip_clahe': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Specifies whether contrast-limited adaptive histogram equalization should be skipped.',
    ),
    'create_training_subset': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Training subset options',
        description='Create subset for training a segmentation model.',
    ),
    'crop_size_x': NextflowParameter(
        type=typing.Optional[int],
        default=400,
        section_title=None,
        description='Indicates crop size on x axis.',
    ),
    'crop_size_y': NextflowParameter(
        type=typing.Optional[int],
        default=400,
        section_title=None,
        description='Indicates crop size on y axis.',
    ),
    'crop_amount': NextflowParameter(
        type=typing.Optional[int],
        default=4,
        section_title=None,
        description='Number of crops you would like to extract.',
    ),
    'crop_nonzero_fraction': NextflowParameter(
        type=typing.Optional[float],
        default=0.4,
        section_title=None,
        description='Indicates fraction of pixels per crop above global threshold to ensure tissue and not only background is selected.',
    ),
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

