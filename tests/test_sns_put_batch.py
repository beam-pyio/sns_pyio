import pytest
from src.sns_pyio import SnsUploader, SNSOptions # TODO: Ideally, there would be no src. here
from moto import mock_aws
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam import Create

@pytest.fixture()
def spec_pipeline_options():
    return SNSOptions(
        '--aws_access_key_id',
        '',
        '--aws_secret_access_key',
        '',
        '--aws_region_name',
        '',
        '--topic_arn',
        ''
    )

@pytest.fixture()
def spec_test_sns_messages():
    return [
        {
            "": "",
            "": "",
            "": "",
            "": "",
            "": "",
            "": "",
            "": "",
            "": "",
            "": "",
        }
    ]
@mock_aws
class TestSnsPutBatch:

    def test_put_1_record_into_sns_is_successful(
            self,
            spec_pipeline_options,
            spec_test_sns_messages
    ):

        pipeline_options = spec_pipeline_options

        with TestPipeline(options=pipeline_options) as pipeline:
            _s, _f = (pipeline
                      | Create(spec_test_sns_messages)
                      | SnsUploader(pipeline_options.get('topic_arn'), pipeline_options)
            )


