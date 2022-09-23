
class GraphQL:

    def __init__(self, session):
        self._session = session

    def get_unassigned_devices(self) -> dict:
        """ Get a list of all Unassigned Devices"""

        arguments = {
            "query":
                "{unassignedDevices {id, dnqualifier, name, KDMCount, "
                "dateAdded, status}}"
        }

        return self._session.post('graphql', data=arguments).json()


    def get_assigned_devices(self) -> dict:
        """ Get a list of all Assigned Devices"""

        arguments = {
            "query":
                "{sites {id, name, deviceCount, KDMCount}}"
        }

        return self._session.post('graphql', data=arguments).json()


    def get_site_aliases(self) -> dict:
        """ Get a list of all Site Aliases"""

        arguments = {"query": "{sites {id, name}}"}

        return self._session.post('graphql', data=arguments).json()
