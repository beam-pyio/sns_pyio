import apache_beam
import pytest
from src.sns_pyio import SnsUploader, SNSOptions, IOStatus
from moto import mock_aws
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to
from apache_beam import Create
import random
import string
import boto3


@pytest.fixture()
def spec_pipeline_options(create_mock_sns_topic):
    return SNSOptions([
        '--aws_access_key_id',
        'test_key_id',
        '--aws_secret_access_key',
        'test_access_key',
        '--aws_region_name',
        'us-east-1',
        '--topic_arn',
        create_mock_sns_topic
    ])


@pytest.fixture(scope="function")
def aws():
    with mock_aws():
        yield boto3.client('sns', region_name='us-east-1')


@pytest.fixture(scope="function")
def create_mock_sns_topic(aws):
    resp = boto3.client('sns', region_name='us-east-1').create_topic(Name='MyTopic')
    return resp.get('TopicArn', '')


@pytest.fixture()
def spec_test_sns_message():
    return [
        {
            "Id": ''.join(random.choice(string.ascii_lowercase) for i in range(10)),
            "Message": "",
            "Subject": "",
            "MessageStructure": "json",
            "MessageAttributes": {
                "Origin": {
                    "DataType": "String",
                    "StringValue": "Sydney"
                },
                "Destination": {
                    "DataType": "String",
                    "StringValue": "Singapore"
                }
            }
        }
    ]


@mock_aws
class TestSnsPutBatch:

    def test_put_1_record_into_sns_is_successful(
            self,
            spec_pipeline_options,
            spec_test_sns_message
    ):

        pipeline_options = spec_pipeline_options

        with TestPipeline(options=pipeline_options) as pipeline:
            results = (pipeline
                      | Create(spec_test_sns_message)
                      | SnsUploader(pipeline_options.topic_arn, pipeline_options)
            )

            assert isinstance(
                results[IOStatus.SUCCESS.value],
                apache_beam.PCollection
            )

            assert_that(
                final_res,
                equal_to(spec_test_sns_message)
            )


