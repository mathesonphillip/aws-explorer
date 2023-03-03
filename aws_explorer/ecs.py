from .utils import filter_and_sort_dict_list


class ECSManager:
    def __init__(self, session):
        self._session = session
        self.client = self._session.client("ecs")
        self._clusters = None
        self._services = None
        self._task_definitions = None

    @property
    def clusters(self):
        response = self.client.describe_clusters()
        del response["ResponseMetadata"]

        # print(response)

        # .get("clusters")

        # _ = [
        #     item.update({"Account": self._session.profile_name})
        #     for item in response
        # ]

        # self._clusters = response

        return response

    @property
    def services(self):
        if not self._services:
            service_arns = self.client.list_services().get("serviceArns")

            response = self.client.describe_services(services=service_arns).get(
                "serviceArns"
            )

            # _ = [
            #     item.update({"Account": self._session.profile_name})
            #     for item in response
            # ]
            self._services = response

        return self._services

    # @property
    # def task_definitions(self):
    #     if not self._task_definitions:
    #         response = self.client.list_task_definitions().get("taskDefinitionArns")

    #         # _ = [
    #         #     item.update({"Account": self._session.profile_name})
    #         #     for item in response
    #         # ]
    #         self._task_definitions = response

    #     return self._task_definitions

    def to_dict(self, filtered=True):
        # if not filtered:
        return {
            "Clusters": self.clusters,
            # "Services": self.services,
            # "TaskDefinitions": self.task_definitions,
        }

        return {
            "Clusters": filter_and_sort_dict_list(
                self.clusters,
                [
                    "createdAt",
                    "registeredAt",
                    "updatedAt",
                ],
            ),
            # "Services": filter_and_sort_dict_list(
            #     self.services,
            #     [
            #         "createdAt",
            #         "deployments",
            #         "events",
            #         "loadBalancers",
            #         "pendingCount",
            #         "runningCount",
            #         "updatedAt",
            #     ],
            # ),
            "TaskDefinitions": filter_and_sort_dict_list(
                self.task_definitions,
                [
                    "createdAt",
                    "compatibilities",
                    "containerDefinitions",
                    "executionRoleArn",
                    "family",
                    "ipcMode",
                    "networkMode",
                    "pidMode",
                    "placementConstraints",
                    "proxyConfiguration",
                    "requiresCompatibilities",
                    "revision",
                    "status",
                    "taskRoleArn",
                ],
            ),
        }
