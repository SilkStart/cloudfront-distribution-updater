import unittest
import cloudfront_distribution_updater
import mock
import datetime

class CloudFrontDistributionTemplateUpdateTest(unittest.TestCase):

    def create_sample_distribution(self):
        return {
          u'Id': 'SAMPLEXXXXXXXX',
          u'Status': 'Deployed',
          u'LastModifiedTime': datetime.datetime(2015, 1, 1),
          u'DomainName': 'example.cloudfront.net',
          u'Aliases': {
            u'Items': [
              'www.example.com',
              '*.example.com'
            ],
            u'Quantity': 2
          },
          u'Origins': {
            u'Quantity': 2,
            u'Items': [
              {   
                u'Id': u'Custom-example-origin.example.com',
                u'DomainName': u'example-origin.example.com',
                u'OriginPath': u'',
                u'CustomOriginConfig': {
                  u'HTTPPort': 80,
                  u'HTTPSPort': 443,
                  u'OriginProtocolPolicy': u'match-viewer'
                }
              },
              {
                u'Id': u'Custom-example-origin-2.example.com',
                u'DomainName': u'example-origin-2.example.com',
                u'OriginPath': u'',
                u'CustomOriginConfig': {
                  u'HTTPPort': 80,
                  u'HTTPSPort': 443,
                  u'OriginProtocolPolicy': u'http-only'
                }
              }
            ]
          },
          u'DefaultCacheBehavior': {
            u'TargetOriginId': 'Custom-example-origin.example.com',
            u'ForwardedValues': {
              u'Cookies': {
                u'Forward': 'whitelist',
                u'WhitelistedNames': {
                  u'Items': [
                    'cookie1', 
                    'cookie2'
                  ],
                  u'Quantity': 2
                }
              },
              u'Headers': {
                u'Items': [
                  'Header1',
                  'Host'
                ], 
                u'Quantity': 1
              },
              u'QueryString': True
            },
            u'AllowedMethods': {
              u'CachedMethods': {
                u'Items': [
                  'HEAD',
                  'GET'
                ],
                u'Quantity': 2
              },
              u'Items': [
                'HEAD',
                'DELETE',
                'POST',
                'GET',
                'OPTIONS',
                'PUT',
                'PATCH'
              ],
              u'Quantity': 7
            },
            u'DefaultTTL': 0,
            u'MaxTTL': 0,
            u'MinTTL': 0,
            u'SmoothStreaming': False,
            u'TrustedSigners': {
              u'Enabled': False, u'Quantity': 0
            },
            u'ViewerProtocolPolicy': 'allow-all'
          },
          u'CacheBehaviors': {
            u'Items': [
              {
                u'AllowedMethods': {
                  u'CachedMethods': {
                    u'Items': [
                      'HEAD',
                      'GET'
                    ],
                    u'Quantity': 2
                  },
                  u'Items': [
                    'HEAD',
                    'GET',
                    'OPTIONS'
                  ],
                  u'Quantity': 3
                },
                u'DefaultTTL': 86400,
                u'ForwardedValues': {
                  u'Cookies': {
                    u'Forward': 'none'
                  },
                  u'Headers': {
                    u'Quantity': 0
                  },
                  u'QueryString': True
                },
                u'MaxTTL': 31536000,
                u'MinTTL': 0,
                u'PathPattern': '/res/*',
                u'SmoothStreaming': False,
                u'TargetOriginId': 'Custom-example-origin-2.example.com',
                u'TrustedSigners': {
                  u'Enabled': False,
                  u'Quantity': 0
                },
                u'ViewerProtocolPolicy': 'allow-all'
              }
            ],
            u'Quantity': 1
          },
          u'Comment': 'Test Distribution (ENV=TEST)',
          u'CustomErrorResponses': {
            u'Items': [],
            u'Quantity': 0
          },
          u'Enabled': True,
          u'PriceClass': 'PriceClass_All',
          u'Restrictions': {
            u'GeoRestriction': {
              u'Quantity': 0,
              u'RestrictionType': 'none'
            }
          },
          u'ViewerCertificate': {
            u'CloudFrontDefaultCertificate': True,
            u'MinimumProtocolVersion': 'SSLv3'
          },
          u'WebACLId': 'de305d54-75b4-431b-adb2-eb6b9e546014'
        }
        
    def create_empty_distribution(self):
        return {
          u'Id': 'EMPTYXXXXXXXXX',
          u'Status': 'Deployed',
          u'LastModifiedTime': datetime.datetime(2015, 1, 1),
          u'DomainName': 'empty.cloudfront.net',
          u'Aliases': {
            u'Items': [],
            u'Quantity': 0
          },
          u'Origins': {
            u'Quantity': 0,
            u'Items': [
              {   
                u'Id': u'Custom-example-origin.example.com',
                u'DomainName': u'example-origin.example.com',
                u'OriginPath': u'',
                u'CustomOriginConfig': {
                  u'HTTPPort': 80,
                  u'HTTPSPort': 443,
                  u'OriginProtocolPolicy': u'match-viewer'
                }
              }
            ]
          },
          u'DefaultCacheBehavior': {
            u'TargetOriginId': 'Custom-example-origin.example.com',
            u'ForwardedValues': {
              u'Cookies': {
                u'Forward': 'none',
                u'WhitelistedNames': {
                  u'Items': [],
                  u'Quantity': 0
                }
              },
              u'Headers': {
                u'Items': [], 
                u'Quantity': 0
              },
              u'QueryString': False
            },
            u'AllowedMethods': {
              u'CachedMethods': {
                u'Items': [],
                u'Quantity': 0
              },
              u'Items': [],
              u'Quantity': 0
            },
            u'DefaultTTL': 0,
            u'MaxTTL': 0,
            u'MinTTL': 0,
            u'SmoothStreaming': False,
            u'TrustedSigners': {
              u'Enabled': False, u'Quantity': 0
            },
            u'ViewerProtocolPolicy': 'allow-all'
          },
          u'CacheBehaviors': {
            u'Items': [],
            u'Quantity': 0
          },
          u'Comment': '',
          u'CustomErrorResponses': {
            u'Items': [],
            u'Quantity': 0
          },
          u'Enabled': False,
          u'PriceClass': 'PriceClass_All',
          u'Restrictions': {
            u'GeoRestriction': {
              u'Quantity': 0,
              u'RestrictionType': 'none'
            }
          },
          u'ViewerCertificate': {
            u'CloudFrontDefaultCertificate': True,
            u'MinimumProtocolVersion': 'SSLv3'
          },
          u'WebACLId': ''
        }

    def testGetTagsFromComments_multiple_tags(self):
        comment = "This part doesn't matter (KEY1=VALUE1,KEY2=VALUE2)"
        
        expected = {"key1":"value1", "key2":"value2"}
        
        tags = cloudfront_distribution_updater.tags_from_comment(comment)
        
        self.assertEqual(expected, tags)
        
    def testGetTagsFromComments_single_tag(self):
        comment = "This part doesn't matter (KEY1=VALUE1)"
        
        expected = {"key1":"value1"}
        
        tags = cloudfront_distribution_updater.tags_from_comment(comment)
        
        self.assertEqual(expected, tags)
        
    def testGetTagsFromComments_no_tags(self):
        comment = "This part doesn't matter"
        
        expected = {}
        
        tags = cloudfront_distribution_updater.tags_from_comment(comment)
        
        self.assertEqual(expected, tags)
        
    def testGetTagsFromDistributionConfig(self):
        distributionConfig = {u'Comment': u'DistributionComment (SOMEKEY=AVALUE,OTHERKEY=SOMETHINGELSE)'}

        expected = {'somekey': 'avalue', 'otherkey': 'somethingelse'}

        tags = cloudfront_distribution_updater.tags_from_distribution_config(distributionConfig)

        self.assertEqual(expected, tags)
        
    def testDistributionConfigMatchesTags_no_match(self):
        distribution_config = {u'Comment': u'DistributionComment (KEY1=VALUE1,KEY2=VALUE2)'}
        
        expected = False
        
        matches = cloudfront_distribution_updater.distribution_config_matches_tags(distribution_config, with_tags=[('key3','value3')])
        
        self.assertEqual(expected, matches)
        
    def testDistributionConfigMatchesTags_with_tag_match(self):
        distribution_config = {u'Comment': u'DistributionComment (KEY1=VALUE1,KEY2=VALUE2)'}
        
        expected = True
        
        matches = cloudfront_distribution_updater.distribution_config_matches_tags(distribution_config, with_tags=[('key1','value1')])
        
        self.assertEqual(expected, matches)
        
    def testDistributionConfigMatchesTags_without_tag_exclude(self):
        distribution_config = {u'Comment': u'DistributionComment (KEY1=VALUE1,KEY2=VALUE2)'}
        
        expected = False
        
        matches = cloudfront_distribution_updater.distribution_config_matches_tags(distribution_config, with_tags=[('key1','value1')], without_tags=[('key2','value2')])
        
        self.assertEqual(expected, matches)
        
    def testDistributionConfigMatchesTags_without_tag_miss(self):
        distribution_config = {u'Comment': u'DistributionComment (KEY1=VALUE1,KEY2=VALUE2)'}
        
        expected = True
        
        matches = cloudfront_distribution_updater.distribution_config_matches_tags(distribution_config, with_tags=[('key1','value1')], without_tags=[('key3','value3')])
        
        self.assertEqual(expected, matches)
        
    def testFilterDistributions_match_one_exclude_one(self):
        example_distributions = [
            {u'Comment': ''},
            {u'Comment': 'Some distribution (IRRELEVANT_KEY=SOMEVALUE)'},
            {u'Comment': 'Other distribution (SOMEOTHER_KEY=OTHERVALUE)'},
            {u'Comment': 'This distribution (ENV=TEST)'},
            {u'Comment': 'Template Distribution (TEMPLATE=TRUE,ENV=TEST)'}
          ]
        
        expected = [{u'Comment': 'This distribution (ENV=TEST)'}]
        
        distributions = cloudfront_distribution_updater.filter_distributions(example_distributions, with_tags=[('env','test')], without_tags=[('template','true')])
        
        self.assertEqual(expected, distributions)
        
    def testFilterDistributions_match_two(self):
        example_distributions = [
            {u'Comment': ''},
            {u'Comment': 'Some distribution (IRRELEVANT_KEY=SOMEVALUE)'},
            {u'Comment': 'Other distribution (SOMEOTHER_KEY=OTHERVALUE)'},
            {u'Comment': 'This distribution (ENV=TEST)'},
            {u'Comment': 'Template Distribution (TEMPLATE=TRUE,ENV=TEST)'}
          ]
        
        expected = [{u'Comment': 'Template Distribution (TEMPLATE=TRUE,ENV=TEST)'}]
        
        distributions = cloudfront_distribution_updater.filter_distributions(example_distributions, with_tags=[('env','test'),('template','true')])
        
        self.assertEqual(expected, distributions)
        
    def testDistributionConfigFromDistribution(self):
        distribution = self.create_sample_distribution()
        
        caller_reference_time = 1420070400
        
        expected_distribution = self.create_sample_distribution()
        del expected_distribution["Status"]
        del expected_distribution["LastModifiedTime"]
        del expected_distribution["DomainName"]
        del expected_distribution["Id"]
        expected_distribution['CallerReference'] = str(caller_reference_time)
        
        with mock.patch('time.time') as mock_time:
            mock_time.return_value = caller_reference_time
        
            result = cloudfront_distribution_updater.distribution_config_from_distribution(distribution)
        
            self.assertEqual(expected_distribution, result)
            
    def testUpdateDistributionWithTemplateDistribution(self):
        template_distribution = self.create_sample_distribution()
        
        distribution = self.create_empty_distribution()
        
        expected = {
          u'Id': 'EMPTYXXXXXXXXX',
          u'Status': 'Deployed',
          u'LastModifiedTime': datetime.datetime(2015, 1, 1),
          u'DomainName': 'empty.cloudfront.net',
          u'Aliases': {
            u'Items': [],
            u'Quantity': 0
          },
          u'Origins': {
            u'Quantity': 2,
            u'Items': [
              {   
                u'Id': u'Custom-example-origin.example.com',
                u'DomainName': u'example-origin.example.com',
                u'OriginPath': u'',
                u'CustomOriginConfig': {
                  u'HTTPPort': 80,
                  u'HTTPSPort': 443,
                  u'OriginProtocolPolicy': u'match-viewer'
                }
              },
              {
                u'Id': u'Custom-example-origin-2.example.com',
                u'DomainName': u'example-origin-2.example.com',
                u'OriginPath': u'',
                u'CustomOriginConfig': {
                  u'HTTPPort': 80,
                  u'HTTPSPort': 443,
                  u'OriginProtocolPolicy': u'http-only'
                }
              }
            ]
          },
          u'DefaultCacheBehavior': {
            u'TargetOriginId': 'Custom-example-origin.example.com',
            u'ForwardedValues': {
              u'Cookies': {
                u'Forward': 'whitelist',
                u'WhitelistedNames': {
                  u'Items': [
                    'cookie1', 
                    'cookie2'
                  ],
                  u'Quantity': 2
                }
              },
              u'Headers': {
                u'Items': [
                  'Header1',
                  'Host'
                ], 
                u'Quantity': 1
              },
              u'QueryString': True
            },
            u'AllowedMethods': {
              u'CachedMethods': {
                u'Items': [
                  'HEAD',
                  'GET'
                ],
                u'Quantity': 2
              },
              u'Items': [
                'HEAD',
                'DELETE',
                'POST',
                'GET',
                'OPTIONS',
                'PUT',
                'PATCH'
              ],
              u'Quantity': 7
            },
            u'DefaultTTL': 0,
            u'MaxTTL': 0,
            u'MinTTL': 0,
            u'SmoothStreaming': False,
            u'TrustedSigners': {
              u'Enabled': False, u'Quantity': 0
            },
            u'ViewerProtocolPolicy': 'allow-all'
          },
          u'CacheBehaviors': {
            u'Items': [
              {
                u'AllowedMethods': {
                  u'CachedMethods': {
                    u'Items': [
                      'HEAD',
                      'GET'
                    ],
                    u'Quantity': 2
                  },
                  u'Items': [
                    'HEAD',
                    'GET',
                    'OPTIONS'
                  ],
                  u'Quantity': 3
                },
                u'DefaultTTL': 86400,
                u'ForwardedValues': {
                  u'Cookies': {
                    u'Forward': 'none'
                  },
                  u'Headers': {
                    u'Quantity': 0
                  },
                  u'QueryString': True
                },
                u'MaxTTL': 31536000,
                u'MinTTL': 0,
                u'PathPattern': '/res/*',
                u'SmoothStreaming': False,
                u'TargetOriginId': 'Custom-example-origin-2.example.com',
                u'TrustedSigners': {
                  u'Enabled': False,
                  u'Quantity': 0
                },
                u'ViewerProtocolPolicy': 'allow-all'
              }
            ],
            u'Quantity': 1
          },
          u'Comment': '',
          u'CustomErrorResponses': {
            u'Items': [],
            u'Quantity': 0
          },
          u'Enabled': False,
          u'PriceClass': 'PriceClass_All',
          u'Restrictions': {
            u'GeoRestriction': {
              u'Quantity': 0,
              u'RestrictionType': 'none'
            }
          },
          u'ViewerCertificate': {
            u'CloudFrontDefaultCertificate': True,
            u'MinimumProtocolVersion': 'SSLv3'
          },
          u'WebACLId': 'de305d54-75b4-431b-adb2-eb6b9e546014'
        }
        
        self.maxDiff = None
        cloudfront_distribution_updater.update_distribution_object_with_template_distribution_object(distribution,template_distribution)
        
        self.assertEqual(expected, distribution)
        
    def testGetDistributions(self):
        example_distributions = {u'DistributionList': {u'IsTruncated': False,
          u'Items': [
            {u'Comment': ''},
            {u'Comment': 'Some distribution (IRRELEVANT_KEY=SOMEVALUE)'},
            {u'Comment': 'Other distribution (SOMEOTHER_KEY=OTHERVALUE)'},
            {u'Comment': 'This distribution (ENV=TEST)'},
            {u'Comment': 'Template Distribution (TEMPLATE=TRUE,ENV=TEST)'}
          ],
          u'Marker': '',
          u'MaxItems': 100,
          u'Quantity': 5},
         'ResponseMetadata': {'HTTPStatusCode': 200,
          'RequestId': '0c0dfb80-9ba5-11e5-b122-9bd96824993f'}
        }
        
        expected = [
            {u'Comment': ''},
            {u'Comment': 'Some distribution (IRRELEVANT_KEY=SOMEVALUE)'},
            {u'Comment': 'Other distribution (SOMEOTHER_KEY=OTHERVALUE)'},
            {u'Comment': 'This distribution (ENV=TEST)'},
            {u'Comment': 'Template Distribution (TEMPLATE=TRUE,ENV=TEST)'}
          ]
        
        with mock.patch('cloudfront_distribution_updater.cf_client.list_distributions') as mock_method:
            mock_method.return_value = example_distributions
            
            distributions = cloudfront_distribution_updater.get_distributions()
            
            self.assertEqual(expected, distributions)

    def testLambdaHandler(self):
        event = {"awslogs": {"data": "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"}}

        cloudfront_distribution_updater.lambda_handler(event, None)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()