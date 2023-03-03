from .utils import filter_and_sort_dict_list


class SSMManager:
    def __init__(self, session):
        self._session = session
        self.client = self._session.client("ssm")
        self._parameters = None
        self._instances = None

    @property
    def parameters(self):
        if not self._parameters:
            response = self.client.describe_parameters().get("Parameters")
            _ = [
                item.update({"Account": self._session.profile_name})
                for item in response
            ]
            self._parameters = response
        return self._parameters

    @property
    def instances(self):
        response = self.client.describe_instance_information().get(
            "InstanceInformationList"
        )
        _ = [item.update({"Account": self._session.profile_name}) for item in response]
        self._instances = response
        return self._instances

    # WIP: This method is not working yet
    def run_command(self, instance_ids, document_name, parameters, comment):
        response = self.client.send_command(
            InstanceIds=instance_ids,
            DocumentName=document_name,
            Parameters=parameters,
            Comment=comment,
        )
        return response

    def to_dict(self, filtered=True):
        if not filtered:
            return {"Parameters": self.parameters, "Instances": self.instances}

        return {
            "Parameters": filter_and_sort_dict_list(
                self.parameters, ["Account", "Name", "Type", "LastModifiedDate"]
            ),
            "Instances": filter_and_sort_dict_list(
                self.instances,
                [
                    "Account",
                    "ComputerName",
                    "InstanceId",
                    "PingStatus",
                    "LastPingDateTime",
                    "AgentVersion",
                    "IsLatestVersion",
                    "ResourceType",
                    "IPAddress",
                    "PlatformType",
                    "PlatformName",
                    "PlatformVersion",
                    # "ActivationId",
                    # "IamRole",
                    # "LastSuccessfulPingDateTime",
                    # "AssociationStatus",
                ],
            ),
        }
