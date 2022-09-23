from features.steps.api.api_utils.graphql import GraphQL
from features.steps.api.api_utils.v1 import V1
from features.steps.api.api_utils.requests_session import RequestsSession


class ProducerFrontendServiceAPI:
  def __init__(self, base_url):
    self._session = RequestsSession(base_url)
    self.v1 = V1(self._session)
    self.graphQL = GraphQL(self._session)
