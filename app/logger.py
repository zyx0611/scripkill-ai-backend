import logging

# # Configure logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # Set logging level to DEBUG for more detailed output
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# logger.addHandler(ch)

def getLogger(__name__):
    # Configure logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set logging level to DEBUG for more detailed output
   
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    
    logger.addHandler(ch)
    return logger