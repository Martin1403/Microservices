from pathlib import Path

from ariadne import make_executable_schema

from chat.api.queries import query
from chat.api.mutations import mutation

schema = make_executable_schema(
    (Path(__file__).parent / 'schema.graphql').read_text(),
    [query, mutation, ]
)
