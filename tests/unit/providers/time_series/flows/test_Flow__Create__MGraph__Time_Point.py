from unittest                                                               import TestCase
from mgraph_db.providers.time_series.flows.Flow__Create__MGraph__Time_Point import Flow__Create__MGraph__Time_Point
from osbot_utils.utils.Env                                                  import load_dotenv

class test_Flow__Create__MGraph__Time_Point(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.flow_create_time_point = Flow__Create__MGraph__Time_Point()

    def test__setUpClass(self):
       with self.flow_create_time_point as _:
           assert type(_) is Flow__Create__MGraph__Time_Point

    def test__start_flow(self):
        load_dotenv()
        with self.flow_create_time_point as _:
            #_.png_create = True
            _.setup()
            #_.flow_config.raise_flow_error = False
            #_.flow_config.
            _.execute()
            _.print_log_messages()
