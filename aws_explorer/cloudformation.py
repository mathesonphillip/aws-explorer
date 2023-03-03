from .utils import filter_and_sort_dict_list, get_logger


class CloudFormationManager:
    _logger = get_logger(__name__)

    def __init__(self, session):
        self._logger.debug(f"{session.profile_name:<20} cloudformation.__init__()")
        self._session = session
        self.client = self._session.client("cloudformation")
        self._stacks = None
        self._stack_resources = None

    @property
    def stacks(self):
        if not self._stacks:
            self._logger.debug(f"{self._session.profile_name:<20} stacks (not cached)")
            # FILTER out DELETE_COMPLETE stacks

            _stacks = []

            for stack in self.client.list_stacks().get("StackSummaries"):
                if stack.get("StackStatus") == "DELETE_COMPLETE":
                    continue
                _stacks.append(stack)

            # Add Account to each item
            _ = [
                item.update({"Account": self._session.profile_name}) for item in _stacks
            ]

            self._stacks = _stacks

            return self._stacks

        self._logger.debug(f"{self._session.profile_name:<20} stacks (cached)")
        return self._stacks

    @property
    def stack_resources(self):
        if not self._stack_resources:
            self._logger.debug(
                f"{self._session.profile_name:<20} stack_resources (not cached)"
            )

            result = []
            for stack in self.stacks:
                if stack.get("StackStatus") == "DELETE_COMPLETE":
                    continue

                stack_name = stack.get("StackName")
                resources = self.client.list_stack_resources(StackName=stack_name)[
                    "StackResourceSummaries"
                ]
                result.extend(resources)

            _ = [
                item.update({"Account": self._session.profile_name}) for item in result
            ]
            self._stack_resources = result

        self._logger.debug(f"{self._session.profile_name:<20} stack_resources (cached)")
        return self._stack_resources

    # TODO: Add drift detection
    def detect_drift(self):
        """This method is used to detect drift in CloudFormation stacks."""

        stack_drift_detection_ids = []
        for stack in self.stacks:
            if stack.get("StackStatus") == "DELETE_COMPLETE":
                continue

            stack_name = stack.get("StackName")
            drift_id = self.client.detect_stack_drift(StackName=stack_name).get(
                "StackDriftDetectionId"
            )
            stack_drift_detection_ids.append(drift_id)

        return stack_drift_detection_ids

    def to_dict(self, filtered=True):
        """This method is used to convert the object to Dict."""
        if not filtered:
            return {
                "Stacks": self.stacks,
                "StackResources": self.stack_resources,
            }

        return {
            "Stacks": filter_and_sort_dict_list(
                self.stacks,
                [
                    "Account",
                    "StackName",
                    "StackStatus",
                    "CreationTime",
                    "LastUpdatedTime",
                    "DriftInformation",
                    # "StackStatusReason",
                    "TemplateDescription",
                ],
            ),
            "StackResources": filter_and_sort_dict_list(
                self.stack_resources,
                [
                    "Account",
                    "StackName",
                    "DriftInformation",
                    "ResourceType",
                    "ResourceStatus",
                    "LogicalResourceId",
                    "PhysicalResourceId",
                    "LastUpdatedTimestamp",
                    # "ResourceStatusReason",
                    # "ModuleInfo",
                ],
            ),
        }
