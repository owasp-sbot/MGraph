from osbot_utils.helpers.xml.Xml__File__To_Dict import Xml__File__To_Dict
from osbot_utils.helpers.xml.Xml__File__Load    import Xml__File__Load
from osbot_utils.utils.Http                     import GET
from osbot_utils.type_safe.Type_Safe            import Type_Safe


class MGraph_RSS(Type_Safe):
    pass

    def feed_url__to__json(self, url):
        feed_xml = GET(url)
        return self.feed_xml__to__json(feed_xml)

    def feed_xml__to__json(self, feed_xml):
        xml_file = Xml__File__Load   ().load_from_string(feed_xml)
        xml_dict = Xml__File__To_Dict().to_dict(xml_file)
        return xml_dict