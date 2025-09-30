from typing import final


class RepositorySaveError(Exception): ...


@final
class RepositoryConflictError(Exception): ...
