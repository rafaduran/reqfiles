"""Reqfiles excptions module."""

class ReqfilesException(Exception):
    """Base class for all Reqfiles exceptions."""


class ParserError(ReqfilesException):
    """Requirements parsing exception."""
