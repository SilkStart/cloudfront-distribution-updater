# Copyright 2015 SilkStart Technology Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import boto3
import StringIO
import gzip
import json
import copy
import time

cf_client = boto3.client('cloudfront')

def tags_from_comment(comment):
    '''
    Parse a distribution comment to get the tags.
    '''
    
    "Look for tags in the comments if they exist"
    matches = re.search(r'\((([A-Za-z0-9]+=[A-Za-z0-9]+,)*[A-Za-z0-9]+=[A-Za-z0-9]+)\)',comment)

    if matches:
        return {key.lower():value.lower() for key,value in [match.split('=') for match in matches.groups()[0].split(',')]}
    return {}

def tags_from_distribution_config(distributionConfig):
    '''
    Get the tag set from the common on a distribution configuration
    '''
    return tags_from_comment(distributionConfig.get('Comment',''))

def distribution_config_matches_tags(distribution_config, with_tags=None, without_tags=None):
    '''
    Check if a distribution config matches a set of tags, but not another set of tags
    '''
    if not with_tags:
        with_tags = []
    if not without_tags:
        without_tags = []
    
    tags = tags_from_distribution_config(distribution_config)
    
    return (not without_tags or any((not key in tags or tags[key] != value for key,value in without_tags))) and \
        all(key in tags and tags[key] == value for key,value in with_tags)

def filter_distributions(distribution_configs,with_tags=None,without_tags=None):
    '''
    Filters a set of distributions to those matching a set of tags, but not another set.
    '''
    return [distribution for distribution in distribution_configs
            if distribution_config_matches_tags(distribution, with_tags, without_tags)]

def get_distributions():
    '''
    Get all of the distributions
    '''
    return cf_client.list_distributions()['DistributionList']['Items']

def distribution_config_from_distribution(distribution):
    distribution_copy = copy.deepcopy(distribution)
    
    distribution_copy.pop('Status',None)
    distribution_copy.pop('LastModifiedTime',None)
    distribution_copy.pop('DomainName',None)
    distribution_copy.pop('Id',None)
    
    distribution_copy['CallerReference'] = unicode(int(time.time()))
    
    return distribution_copy

def update_distribution_object_with_template_distribution_object(distribution, template_distribution):
    attributes_to_copy = ['Origins','DefaultCacheBehavior','CacheBehaviors','CustomErrorResponses','PriceClass',
        'Restrictions','WebACLId']
    
    for attribute in attributes_to_copy:
        distribution[attribute] = copy.deepcopy(template_distribution[attribute])
        
def update_distribution_id_with_template_distribution_id(distribution_id, template_distribution_id):
    distribution_result = cf_client.get_distribution(Id=distribution_id)
    template_distribution_config = cf_client.get_distribution(Id=template_distribution_id)['Distribution']['DistributionConfig']
    
    distribution_config = distribution_result['Distribution']['DistributionConfig']
    
    update_distribution_object_with_template_distribution_object(distribution_config,template_distribution_config)
    
    cf_client.update_distribution(Id=distribution_id,DistributionConfig=distribution_config,IfMatch=distribution_result['ETag'])
    

def lambda_handler(event, context):
    '''
    Handles a change in the cloudfront distribution.
    '''
    fileobj = StringIO.StringIO(event['awslogs']['data'].decode('base64'))
    data = json.loads(gzip.GzipFile(fileobj=fileobj).read())
    for logEvent in data['logEvents']:
        message = json.loads(logEvent['message'])
        distributionConfig = message['requestParameters']['distributionConfig']
        
        print "Distribution change occurred for {distributionId}".format(distributionId=message['requestParameters']['id'])
        
        tags = tags_from_distribution_config(distributionConfig)
        
        template = tags.get('template','false')
        if template == 'true':
            pass


