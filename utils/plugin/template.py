from abc import ABC, abstractmethod
import copy


class PluginTemplate(ABC):
    def __init__(self, data=None):
        self.logs = data or []  # Every plugin is capable to handle multiple log records.

    def load_data(self, data):
        self.logs = data

    def pop_data(self):
        logs = copy.deepcopy(self.logs)
        self.logs = []
        return logs

    def run(self):
        self.multi_detect()

    @abstractmethod
    def input_data_handling(self, log):
        """
        The procedure to handle the input data into plugin code.
            e.g. convert log dict and other background information into
            context string and prompt string for LLM.
        :param log:
        :return: expected input data for plugin.
        """
        pass

    @abstractmethod
    def detect(self, log):
        """
        Detect one log record after input_data_handling.
        :param log: one log record.
        :return: True or False | Detected Result.
        """
        pass

    def multi_detect(self):
        """
        Detect multiple log records.
        :return: generator of True or False | Detected Result for each log.
        """
        for log in self.logs:
            # TODO: multi-thread to process log info.
            result = self.detect(log)

            # Check if 'tag' key exists in log, if not, initialize it as an empty dictionary
            if 'tag' not in log:
                log['tag'] = {}

            # Set the detection result
            log['tag'][type(self).__name__] = result
