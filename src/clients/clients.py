#!/usr/bin/env python3

import boto3

class Clients(object):
    def __init__(self, **kwargs):
        if ('region_name' in kwargs and kwargs['region_name'] is not None):
            self.region_name = kwargs['region_name']
        else:
            # set region to a default if no present
            self.region_name = "us-east-1"

        # read aws credentials/profile if provided 
        if ('aws_access_key_id' in kwargs and 'aws_secret_access_key' in kwargs and kwargs['aws_access_key_id'] is not None and kwargs['aws_secret_access_key'] is not None):
            session = boto3.session.Session(
                aws_access_key_id = kwargs['aws_access_key_id'],
                aws_secret_access_key = kwargs['aws_secret_access_key']
            )
        elif ('aws_profile' in kwargs and kwargs['aws_profile'] is not None):
            session = boto3.Session(profile_name=self.profile_name, region_name=self.region)
        else:
            # if aws credentails are set as env vars or using a role
            session = boto3.session.Session()

        self.eks = session.client('eks', region_name=self.region_name)
