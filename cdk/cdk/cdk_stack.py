from aws_cdk import CfnOutput, RemovalPolicy, Stack
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as route53targets
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3deploy
from constructs import Construct


class CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ROOT_DOMAIN_NAME = self.node.try_get_context("ROOT_DOMAIN_NAME")
        DOMAIN_NAME = f"blog.{ROOT_DOMAIN_NAME}"
        HOSTED_ZONE_ID = self.node.try_get_context("HOSTED_ZONE_ID")
        CERTIFICATE_ARN = self.node.try_get_context("CERTIFICATE_ARN")

        # Make a web server.
        bucket = s3.Bucket(
            self,
            "WebBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            public_read_access=True,
            website_error_document="404.html",
            website_index_document="index.html",
        )

        # Expose the web server through CloudFront.
        distribution = cloudfront.Distribution(
            self,
            "Distribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(bucket)
            ),
            certificate=acm.Certificate.from_certificate_arn(
                self, "Certificate", certificate_arn=CERTIFICATE_ARN
            ),
            domain_names=[DOMAIN_NAME],
        )

        # Deploy site contents to the bucket.
        s3deploy.BucketDeployment(
            self,
            "DeployWebsite",
            sources=[s3deploy.Source.asset("../nextjs-blog/.next/server/pages")],
            destination_bucket=bucket,
            distribution=distribution,
        )

        #
        zone = route53.HostedZone.from_hosted_zone_attributes(
            self,
            "HostedZone",
            hosted_zone_id=HOSTED_ZONE_ID,
            zone_name=ROOT_DOMAIN_NAME,
        )

        route53.ARecord(
            self,
            "SubDomainRecord",
            zone=zone,
            target=route53.RecordTarget.from_alias(
                route53targets.CloudFrontTarget(distribution)
            ),
            record_name=DOMAIN_NAME,
        )

        # Output distribution's domain name.
        CfnOutput(
            self,
            "DistributionDomainName",
            value=distribution.distribution_domain_name,
            export_name=f"{construct_id}:DistributionDomainName",
        )

        # Output web_bucket's URL.
        CfnOutput(
            self,
            "WebBucketUrl",
            value=bucket.bucket_website_url,
        )
