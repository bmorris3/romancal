"""Tests for the DQ Init module and DMS 25 and DMS 26 requirements"""

import os

import pytest
import roman_datamodels as rdm
from metrics_logger.decorators import metrics_logger

from romancal.step import DQInitStep
from romancal.stpipe import RomanStep

from .regtestdata import compare_asdf


@metrics_logger("DMS25")
@pytest.mark.bigdata
def test_dq_init_image_step(rtdata, ignore_asdf_paths):
    """DMS25 Test: Testing retrieval of best ref file for image data,
    and creation of a ramp file with CRDS selected mask file applied."""

    input_file = "r0000101001001001001_01101_0001_WFI01_uncal.asdf"
    rtdata.get_data(f"WFI/image/{input_file}")
    rtdata.input = input_file

    # Test CRDS
    step = DQInitStep()
    model = rdm.open(rtdata.input)
    step.log.info(
        "DMS25 MSG: Testing retrieval of best "
        "ref file for image data, "
        "Success is creation of a ramp file with CRDS selected "
        "mask file applied."
    )

    step.log.info(f'DMS25 MSG: First data file: {rtdata.input.rsplit("/", 1)[1]}')
    ref_file_path = step.get_reference_file(model, "mask")
    step.log.info(
        f'DMS25 MSG: CRDS matched mask file: {ref_file_path.rsplit("/", 1)[1]}'
    )
    ref_file_name = os.path.split(ref_file_path)[-1]

    assert "roman_wfi_mask" in ref_file_name

    # Test DQInitStep
    output = "r0000101001001001001_01101_0001_WFI01_dqinit.asdf"
    rtdata.output = output
    args = ["romancal.step.DQInitStep", rtdata.input]
    step.log.info(
        "DMS25 MSG: Running data quality initialization step."
        " The first ERROR is expected, due to extra CRDS parameters"
        " not having been implemented yet."
    )
    RomanStep.from_cmdline(args)
    ramp_out = rdm.open(rtdata.output)
    step.log.info(
        "DMS25 MSG: Does ramp data contain pixeldq from mask file? :"
        f' {("roman.pixeldq" in ramp_out.to_flat_dict())}'
    )
    assert "roman.pixeldq" in ramp_out.to_flat_dict()

    rtdata.get_truth(f"truth/WFI/image/{output}")
    diff = compare_asdf(rtdata.output, rtdata.truth, **ignore_asdf_paths)
    step.log.info(
        "DMS25 MSG: Was the proper data quality array initialized"
        " for the ramp data produced? : "
        f"{diff.identical}"
    )
    assert diff.identical, diff.report()


@metrics_logger("DMS25")
@pytest.mark.bigdata
def test_dq_init_grism_step(rtdata, ignore_asdf_paths):
    """DMS25 Test: Testing retrieval of best ref file for grism data,
    and creation of a ramp file with CRDS selected mask file applied."""

    input_file = "r0000201001001001001_01101_0001_WFI01_uncal.asdf"
    rtdata.get_data(f"WFI/grism/{input_file}")
    rtdata.input = input_file

    # Test CRDS
    step = DQInitStep()
    model = rdm.open(rtdata.input)
    step.log.info(
        "DMS25 MSG: Testing retrieval of best "
        "ref file for grism data, "
        "Success is creation of a ramp file with CRDS selected "
        "mask file applied."
    )

    step.log.info(f'DMS25 MSG: First data file: {rtdata.input.rsplit("/", 1)[1]}')
    ref_file_path = step.get_reference_file(model, "mask")
    step.log.info(
        f'DMS25 MSG: CRDS matched mask file: {ref_file_path.rsplit("/", 1)[1]}'
    )
    ref_file_name = os.path.split(ref_file_path)[-1]

    assert "roman_wfi_mask" in ref_file_name

    # Test DQInitStep
    output = "r0000201001001001001_01101_0001_WFI01_dqinit.asdf"
    rtdata.output = output
    args = ["romancal.step.DQInitStep", rtdata.input]
    step.log.info(
        "DMS25 MSG: Running data quality initialization step."
        "The first ERROR is expected, due to extra CRDS parameters "
        "not having been implemented yet."
    )
    RomanStep.from_cmdline(args)
    ramp_out = rdm.open(rtdata.output)
    step.log.info(
        "DMS25 MSG: Does ramp data contain pixeldq from mask file? :"
        f' {("roman.pixeldq" in ramp_out.to_flat_dict())}'
    )
    assert "roman.pixeldq" in ramp_out.to_flat_dict()

    rtdata.get_truth(f"truth/WFI/grism/{output}")
    diff = compare_asdf(rtdata.output, rtdata.truth, **ignore_asdf_paths)
    step.log.info(
        "DMS25 MSG: Was proper data quality initialized "
        "ramp data produced? : "
        f"{diff.identical}"
    )
    assert diff.identical, diff.report()
