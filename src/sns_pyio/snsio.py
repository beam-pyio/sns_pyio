from apache_beam.transforms.ptransform import InputT, OutputT

from .boto3_client import SnsClient
from apache_beam import PTransform, PCollection, ParDo, DoFn
from apache_beam.options.pipeline_options import PipelineOptions
from typing import Optional, Union, Dict, Any, Tuple


class _ImplSnsUploader(DoFn):

    def __init__(
            self,
            topic_arn: str,
            options: Union[PipelineOptions, Dict]
    ):
        super().__init__()
        self.client = None
        self.options = options
        self.topic_arn = topic_arn

    def setup(self):
        self.client = SnsClient(self.options)

    def start_bundle(self):
        pass

    def process(self, element: Dict[str, Any], *args, **kwargs):

        _success, _fail = self.client.publish_batch(
            topic_arn=self.topic_arn,
            batch_of_records=element
        )
        yield _success, _fail

    def finish_bundle(self):
        pass

    def teardown(self):
        self.client.close()


class SnsUploader(PTransform):

    def __init__(self, topic_arn: str, options: Union[PipelineOptions, Dict[str, Any]]):
        super().__init__()
        self.topic_arn = topic_arn
        self.options = options

    def expand(self, pcoll: PCollection) -> Tuple[PCollection, PCollection]:

        return pcoll | ParDo(
            _ImplSnsUploader(
                self.topic_arn,
                self.options
            )
        )

