import boto3
from apache_beam.options.pipeline_options import PipelineOptions
from typing import List, Dict, LiteralString, Any, Union, Tuple
from .options import SNSOptions


class SnsClient(object):
    """
    Wrapper for boto3 library
    """
    def __init__(self, options):
        if isinstance(options, PipelineOptions):
            sns_options = options.view_as(SNSOptions)
            access_key_id = sns_options.aws_access_key_id
            secret_access_key = sns_options.aws_secret_access_key
            session_token = sns_options.session_token
            use_ssl = not sns_options.disable_ssl
            region_name = sns_options.aws_region_name
            verify = sns_options.ssl_cert_verify
        else:
            access_key_id = options.get('aws_access_key_id')
            secret_access_key = options.get('aws_secret_access_key')
            session_token = options.get('session_token')
            use_ssl = not options.get('disable_ssl', False)
            region_name = options.get('aws_region_name')
            verify = options.get('ssl_cert_verify')

        session = boto3.session.Session()

        self.client = session.client(
            service_name='sns',
            region_name=region_name,
            use_ssl=use_ssl,
            verify=verify,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            aws_session_token=session_token
        )

    def get_client(self):
        return self.client

    def publish_batch(
            self,
            batch_of_records: Union[List[Dict], Dict],
            topic_arn: str
    ) -> Tuple[List[Dict[str, str]], List[Dict[str, Any]]]:

        _success, _fail = self.client.publish_batch(
            topic_arn = topic_arn,
            public_batch_request_entries = batch_of_records
        )

        return _success, _fail

    def list_topics(self, next_token: str = '', **kwargs) -> Dict[LiteralString, Any]:
        pass

    def list_subscriptions(self, next_token: str = '', **kwargs) -> Dict[LiteralString, Any]:
        pass

    def list_subscriptions_by_topic(self,
                                    topic_arn: str = '',
                                    next_token: str = '', **kwargs
                                    ) -> Dict[LiteralString, Any]:
        pass

    def close(self):
        self.client.close()
