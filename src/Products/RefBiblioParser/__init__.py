import logging
from zope.i18nmessageid import MessageFactory
MessageFactory = ProductsRefBiblioParserMessageFactory = MessageFactory('Products.RefBiblioParser') 
logger = logging.getLogger('Products.RefBiblioParser')
def initialize(context):
    """Initializer called when used as a Zope 2 product.""" 
