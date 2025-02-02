from datetime import datetime, timezone
from unittest import TestCase

class MGraph__RSS__Test_Data(TestCase):

    def test_rss_data(self):
        return {
                  'channel': {
                    'description': 'Leading technology blog covering latest developments in software engineering and development practices',
                    'extensions': {},
                    'image': None,
                    'items': [
                      {
                        'categories': [],
                        'content': {},
                        'creator': 'None',
                        'description': 'A critical security update has been released for DevTools Pro that addresses multiple vulnerabilities in the core authentication system. These vulnerabilities could potentially allow unauthorized access to development environments.\n"The authentication protocol implementation needed significant improvements," said security researcher ABC XYZ, who identified the issues',
                        'enclosure': None,
                        'extensions': {
                          'author': 'editor@aaa-bbb-ccc-news.com (Tech Blog)',
                          'enclosure': {
                            'length': '10485760',
                            'type': 'image/jpeg',
                            'url': 'https://aaa-bbb-ccc-news.com/images/security-update.jpg'
                          }
                        },
                        'guid': '1a2b3c4d-5e6f-7g8h-9i0j-k1l2m3n4o5p6',
                        'link': 'https://aaa-bbb-ccc-news.com/2025/01/devtools-security-update.html',
                        'pubDate': 'Mon, 27 Jan 2025 19:30:00 +0530',
                        'thumbnail': {},
                        'title': 'DevTools Pro Security Update Addresses Authentication Vulnerabilities'
                      },
                      {
                        'categories': [],
                        'content': {},
                        'creator': 'None',
                        'description': 'Welcome to your weekly technology roundup! This week we explore the latest innovations in cloud computing, emerging trends in software architecture, and important updates in development tools.\nAs we dive into these topics, we\'ll provide you with practical insights',
                        'enclosure': None,
                        'extensions': {
                          'author': 'editor@aaa-bbb-ccc-news.com (Tech Blog)',
                          'enclosure': {
                            'length': '8388608',
                            'type': 'image/jpeg',
                            'url': 'https://aaa-bbb-ccc-news.com/images/weekly-roundup.jpg'
                          }
                        },
                        'guid': '2b3c4d5e-6f7g-8h9i-0j1k-l2m3n4o5p6q7',
                        'link': 'https://aaa-bbb-ccc-news.com/2025/01/weekly-tech-roundup-27-jan.html',
                        'pubDate': 'Mon, 27 Jan 2025 18:00:00 +0530',
                        'thumbnail': {},
                        'title': '📱 Weekly Tech Roundup: Latest Developments and Insights [27 January]'
                      },
                      {
                        'categories': [],
                        'content': {},
                        'creator': 'None',
                        'description': 'The Software Development Standards Organization announces new guidelines for microservice architecture implementation. These guidelines aim to establish best practices for designing and deploying microservices at scale.\nThe new standards address key challenges',
                        'enclosure': None,
                        'extensions': {
                          'author': 'editor@aaa-bbb-ccc-news.com (Tech Blog)',
                          'enclosure': {
                            'length': '9437184',
                            'type': 'image/jpeg',
                            'url': 'https://aaa-bbb-ccc-news.com/images/microservices.jpg'
                          }
                        },
                        'guid': '3c4d5e6f-7g8h-9i0j-k1l2-m3n4o5p6q7r8',
                        'link': 'https://aaa-bbb-ccc-news.com/2025/01/microservice-guidelines-analysis.html',
                        'pubDate': 'Mon, 27 Jan 2025 16:45:00 +0530',
                        'thumbnail': {},
                        'title': 'Understanding the New Microservice Architecture Guidelines'
                      },
                      {
                        'categories': [],
                        'content': {},
                        'creator': 'None',
                        'description': 'A new development team has successfully implemented an innovative approach to continuous integration, drawing inspiration from established methodologies while introducing unique optimizations.\nThe project, known as BuildFlow, combines traditional CI practices with machine learning',
                        'enclosure': None,
                        'extensions': {
                          'author': 'editor@aaa-bbb-ccc-news.com (Tech Blog)',
                          'enclosure': {
                            'length': '7340032',
                            'type': 'image/jpeg',
                            'url': 'https://aaa-bbb-ccc-news.com/images/buildflow.png'
                          }
                        },
                        'guid': '4d5e6f7g-8h9i-0j1k-l2m3-n4o5p6q7r8s9',
                        'link': 'https://aaa-bbb-ccc-news.com/2025/01/buildflow-ci-innovation.html',
                        'pubDate': 'Mon, 27 Jan 2025 13:15:00 +0530',
                        'thumbnail': {},
                        'title': 'BuildFlow: Revolutionizing Continuous Integration with Smart Automation'
                      }
                    ],
                    'language': 'en-us',
                    'last_build_date': 'Tue, 28 Jan 2025 02:15:00 +0530',
                    'link': 'https://aaa-bbb-ccc-news.com',
                    'title': 'Tech Blog',
                    'update_frequency': '1',
                    'update_period': 'hourly'
                  },
                  'extensions': {},
                  'namespaces': {},
                  'version': '2.0'
                }

    # Helper function to create test item
    def create_test_item(self, guid, title, description, categories, timestamp):
        return {
            'categories': categories,
            'content': {},
            'creator': 'test_author',
            'description': description,
            'enclosure': None,
            'extensions': {
                'author': 'test@example.com (Test Author)',
                'enclosure': {
                    'length': '10000',
                    'type': 'image/jpeg',
                    'url': f'https://test.com/images/{guid}.jpg'
                }
            },
            'guid': guid,
            'link': f'https://test.com/{guid}',
            'pub_date': {
                'date_time_utc': datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S +0000'),
                'date_utc': datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d'),
                'raw_value': datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%a, %d %b %Y %H:%M:%S +0000'),
                'time_since': '1 hour(s) ago',
                'time_utc': datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%H:%M'),
                'timestamp_utc': timestamp
            },
            'thumbnail': {},
            'title': title
        }

 # this code was used to create the test data
 #    def test_load_from_url(self):
 #        url      = '{feed-url}}'
 #        xml_data = GET(url)
 #        xml_file = Xml__File__Load().load_from_string(xml_data)
 #        xml_dict = Xml__File__To_Dict().to_dict(xml_file)
 #        rss_feed = RSS__Feed__Parser().from_dict(xml_dict)
 #
 #        feed_json = rss_feed.json()
 #        feed_json['channel']['items'] = feed_json['channel']['items'][0:4]
 #        pprint(feed_json)