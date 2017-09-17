"""
Exception module for ceph wrapper class
"""
class FunctionNotImplemented(Exception):
    """
    Function not yet finished
    """
    def __str__(self):
        return "This function is not yet available/completed."


class UnsupportedRequestType(Exception):
    """
    If a requested body type is not mapped
    """
    def __str__(self):
        return "Unknown request type."


class UnsupportedBodyType(Exception):
    """
    If a requested body type is not mapped
    """
    def __str__(self):
        return "This type of body is not supported for this API call."
