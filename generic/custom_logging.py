import logging


def custom_log(name_variable, variable_to_log):
    logger = logging.getLogger(__name__)
    logger.error('##############')
    logger.error("The variable '{}' has the value:".format(name_variable))
    logger.error('{}'.format(variable_to_log))
