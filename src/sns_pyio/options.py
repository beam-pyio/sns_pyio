import argparse
from apache_beam.options.pipeline_options import PipelineOptions


class SNSOptions(PipelineOptions):

    @classmethod
    def _add_argparse_args(cls, parser) -> None:
        """
        The method _add_argparser_args is not implemented in parent class PipelineOptions.
        This is the implementation that will be picked up.

        :param parser: _BeamArgumentParser
        :return: None
        """
        # These options are passed to the SQS IO Client
        parser.add_argument(
            '--aws_access_key_id',
            default=None,
            help='The secret key to use when creating the sns client.')
        parser.add_argument(
            '--aws_secret_access_key',
            default=None,
            help='The secret access key to use when creating the sns client.')
        parser.add_argument(
            '--aws_region_name',
            default=None,
            help='The name of the region associated with the sns client.')
        parser.add_argument(
            '--topic_arn',
            default=None,
            help='The arn of the sns topic to publish messages to.')

        # TODO: Are the below options relevant now?

        parser.add_argument(
            '--ssl_cert_verify',
            default=None,
            help='Whether or not to verify SSL certificates with the sns client.')
        parser.add_argument(
            '--disable_ssl',
            default=False,
            action='store_true',
            help=(
                'Whether or not to use SSL with the sqs client. '
                'By default, SSL is used.'))
        parser.add_argument(
            '--session_token',
            default=None,
            help='The session token to be used when creating the client')