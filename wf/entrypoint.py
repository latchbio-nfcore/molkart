from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, segmentation_min_area: typing.Optional[int], segmentation_max_area: typing.Optional[int], cellpose_chan2: typing.Optional[int], cellpose_custom_model: typing.Optional[str], ilastik_pixel_project: typing.Optional[LatchFile], ilastik_multicut_project: typing.Optional[LatchFile], skip_clahe: typing.Optional[bool], create_training_subset: typing.Optional[bool], input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], multiqc_methods_description: typing.Optional[str], segmentation_method: str, cellpose_diameter: typing.Optional[int], cellpose_chan: typing.Optional[int], cellpose_pretrained_model: typing.Optional[str], cellpose_flow_threshold: typing.Optional[float], cellpose_edge_exclude: typing.Optional[bool], mesmer_image_mpp: typing.Optional[float], mesmer_compartment: typing.Optional[str], mindagap_boxsize: typing.Optional[int], mindagap_loopnum: typing.Optional[int], clahe_cliplimit: typing.Optional[float], clahe_nbins: typing.Optional[int], clahe_pixel_size: typing.Optional[float], clahe_kernel: typing.Optional[float], crop_size_x: typing.Optional[int], crop_size_y: typing.Optional[int], crop_amount: typing.Optional[int], crop_nonzero_fraction: typing.Optional[float]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('segmentation_method', segmentation_method),
                *get_flag('segmentation_min_area', segmentation_min_area),
                *get_flag('segmentation_max_area', segmentation_max_area),
                *get_flag('cellpose_diameter', cellpose_diameter),
                *get_flag('cellpose_chan', cellpose_chan),
                *get_flag('cellpose_chan2', cellpose_chan2),
                *get_flag('cellpose_pretrained_model', cellpose_pretrained_model),
                *get_flag('cellpose_custom_model', cellpose_custom_model),
                *get_flag('cellpose_flow_threshold', cellpose_flow_threshold),
                *get_flag('cellpose_edge_exclude', cellpose_edge_exclude),
                *get_flag('mesmer_image_mpp', mesmer_image_mpp),
                *get_flag('mesmer_compartment', mesmer_compartment),
                *get_flag('ilastik_pixel_project', ilastik_pixel_project),
                *get_flag('ilastik_multicut_project', ilastik_multicut_project),
                *get_flag('mindagap_boxsize', mindagap_boxsize),
                *get_flag('mindagap_loopnum', mindagap_loopnum),
                *get_flag('clahe_cliplimit', clahe_cliplimit),
                *get_flag('clahe_nbins', clahe_nbins),
                *get_flag('clahe_pixel_size', clahe_pixel_size),
                *get_flag('clahe_kernel', clahe_kernel),
                *get_flag('skip_clahe', skip_clahe),
                *get_flag('create_training_subset', create_training_subset),
                *get_flag('crop_size_x', crop_size_x),
                *get_flag('crop_size_y', crop_size_y),
                *get_flag('crop_amount', crop_amount),
                *get_flag('crop_nonzero_fraction', crop_nonzero_fraction),
                *get_flag('input', input),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_molkart", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_molkart(segmentation_min_area: typing.Optional[int], segmentation_max_area: typing.Optional[int], cellpose_chan2: typing.Optional[int], cellpose_custom_model: typing.Optional[str], ilastik_pixel_project: typing.Optional[LatchFile], ilastik_multicut_project: typing.Optional[LatchFile], skip_clahe: typing.Optional[bool], create_training_subset: typing.Optional[bool], input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], multiqc_methods_description: typing.Optional[str], segmentation_method: str = 'mesmer', cellpose_diameter: typing.Optional[int] = 30, cellpose_chan: typing.Optional[int] = 0, cellpose_pretrained_model: typing.Optional[str] = 'cyto', cellpose_flow_threshold: typing.Optional[float] = 0.4, cellpose_edge_exclude: typing.Optional[bool] = True, mesmer_image_mpp: typing.Optional[float] = 0.138, mesmer_compartment: typing.Optional[str] = 'whole-cell', mindagap_boxsize: typing.Optional[int] = 3, mindagap_loopnum: typing.Optional[int] = 40, clahe_cliplimit: typing.Optional[float] = 0.01, clahe_nbins: typing.Optional[int] = 256, clahe_pixel_size: typing.Optional[float] = 0.138, clahe_kernel: typing.Optional[float] = 25, crop_size_x: typing.Optional[int] = 400, crop_size_y: typing.Optional[int] = 400, crop_amount: typing.Optional[int] = 4, crop_nonzero_fraction: typing.Optional[float] = 0.4) -> None:
    """
    nf-core/molkart

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, segmentation_method=segmentation_method, segmentation_min_area=segmentation_min_area, segmentation_max_area=segmentation_max_area, cellpose_diameter=cellpose_diameter, cellpose_chan=cellpose_chan, cellpose_chan2=cellpose_chan2, cellpose_pretrained_model=cellpose_pretrained_model, cellpose_custom_model=cellpose_custom_model, cellpose_flow_threshold=cellpose_flow_threshold, cellpose_edge_exclude=cellpose_edge_exclude, mesmer_image_mpp=mesmer_image_mpp, mesmer_compartment=mesmer_compartment, ilastik_pixel_project=ilastik_pixel_project, ilastik_multicut_project=ilastik_multicut_project, mindagap_boxsize=mindagap_boxsize, mindagap_loopnum=mindagap_loopnum, clahe_cliplimit=clahe_cliplimit, clahe_nbins=clahe_nbins, clahe_pixel_size=clahe_pixel_size, clahe_kernel=clahe_kernel, skip_clahe=skip_clahe, create_training_subset=create_training_subset, crop_size_x=crop_size_x, crop_size_y=crop_size_y, crop_amount=crop_amount, crop_nonzero_fraction=crop_nonzero_fraction, input=input, outdir=outdir, email=email, multiqc_title=multiqc_title, multiqc_methods_description=multiqc_methods_description)

