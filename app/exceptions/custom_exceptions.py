class AuthenticationException(Exception):
    pass


class AuthorizationException(Exception):
    pass


class ResumeParsingException(Exception):
    pass


class FileValidationException(Exception):
    pass


class LLMGenerationException(Exception):
    pass


class JobMatchingException(Exception):
    pass