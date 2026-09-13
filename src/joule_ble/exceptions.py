"""Exceptions for Joule Bluetooth communication."""

from __future__ import annotations


class JouleError(Exception):
    """Base exception for all Joule errors."""


class JouleConnectionError(JouleError):
    """Exception raised when failing to connect to or disconnect from the Joule."""


class JouleAuthenticationError(JouleError):
    """Exception raised when pairing, key exchange, or auth fails."""


class JouleCommandError(JouleError):
    """Exception raised when a command is rejected by the Joule."""

    def __init__(self, message: str, result_code: int | None = None) -> None:
        super().__init__(message)
        self.result_code = result_code


class JouleTimeoutError(JouleError):
    """Exception raised when a command or reply times out."""
