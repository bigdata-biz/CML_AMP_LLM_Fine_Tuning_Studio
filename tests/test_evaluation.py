import pytest
from unittest.mock import patch
from sqlalchemy.exc import NoResultFound

from ft.evaluation import (
    list_evaluation_jobs,
    get_evaluation_job,
    start_evaluation_job,
    remove_evaluation_job
)

from ft.api import *
from ft.db.dao import FineTuningStudioDao
from ft.db.model import EvaluationJob


class MockCMLCreatedJob:
    def __init__(self, id: str, script: str = None, runtime_identifier: str = None):
        self.id = id
        self.script = script
        self.runtime_identifier = runtime_identifier


class MockCMLListJobsResponse:
    def __init__(self, jobs=None):
        if jobs is None:
            jobs = []
        self.jobs = jobs

# Test: Listing evaluation jobs


def test_list_evaluation_jobs():
    test_dao = FineTuningStudioDao(engine_url="sqlite:///:memory:", echo=False)

    with test_dao.get_session() as session:
        session.add(EvaluationJob(id="job1"))
        session.add(EvaluationJob(id="job2"))
        session.commit()

    res = list_evaluation_jobs(ListEvaluationJobsRequest(), dao=test_dao)
    assert len(res.evaluation_jobs) == 2
    assert res.evaluation_jobs[0].id == "job1"
    assert res.evaluation_jobs[1].id == "job2"


# Test: Getting an evaluation job by ID (happy path)
def test_get_evaluation_job_happy():
    test_dao = FineTuningStudioDao(engine_url="sqlite:///:memory:", echo=False)

    with test_dao.get_session() as session:
        session.add(EvaluationJob(id="job1"))
        session.add(EvaluationJob(id="job2"))
        session.commit()

    req = GetEvaluationJobRequest(id="job2")
    res = get_evaluation_job(req, dao=test_dao)
    assert res.evaluation_job.id == "job2"


# Test: Getting an evaluation job by ID (job missing)
def test_get_evaluation_job_missing():
    test_dao = FineTuningStudioDao(engine_url="sqlite:///:memory:", echo=False)

    with pytest.raises(NoResultFound):
        get_evaluation_job(GetEvaluationJobRequest(id="job1"), dao=test_dao)


# Test: Starting an evaluation job with missing required fields
def test_start_evaluation_job_missing_required_fields():
    test_dao = FineTuningStudioDao(engine_url="sqlite:///:memory:", echo=False)

    request = StartEvaluationJobRequest(
        base_model_id="model-id",
        dataset_id="dataset-id",
        adapter_id="adapter-id",
        prompt_id="",  # Required field is empty
        adapter_bnb_config_id="",  # Required field is empty
        model_bnb_config_id="model_bnb_config_id",
        generation_config_id="generation_config_id",
        cpu=4,
        gpu=1,
        memory=16
    )

    with pytest.raises(ValueError) as excinfo:
        start_evaluation_job(request, dao=test_dao)
    assert "Field 'prompt_id' is required in StartEvaluationJobRequest." in str(excinfo.value)


# Test: Starting an evaluation job when referenced model ID does not exist
@patch("ft.evaluation.uuid4")
def test_start_evaluation_job_missing_references(uuid4_mock):
    uuid4_mock.return_value = "job3"

    test_dao = FineTuningStudioDao(engine_url="sqlite:///:memory:", echo=False)

    request = StartEvaluationJobRequest(
        base_model_id="non_existent_model_id",
        dataset_id="dataset-id",
        adapter_id="adapter-id",
        prompt_id="prompt-id",
        adapter_bnb_config_id="adapter_bnb_config_id",
        model_bnb_config_id="model_bnb_config_id",
        generation_config_id="generation_config_id",
        cpu=4,
        gpu=1,
        memory=16
    )

    with pytest.raises(ValueError) as excinfo:
        start_evaluation_job(request, dao=test_dao)
    assert "Model with ID 'non_existent_model_id' does not exist." in str(excinfo.value)


# Test: Removing an evaluation job (happy path)
def test_remove_evaluation_job_happy():
    test_dao = FineTuningStudioDao(engine_url="sqlite:///:memory:", echo=False)

    with test_dao.get_session() as session:
        session.add(EvaluationJob(id="job1"))
        session.add(EvaluationJob(id="job2"))
        session.commit()

    req = RemoveEvaluationJobRequest(id="job1")
    res = remove_evaluation_job(req, dao=test_dao)

    with test_dao.get_session() as session:
        jobs = session.query(EvaluationJob).all()
        assert len(jobs) == 1
        assert jobs[0].id == "job2"