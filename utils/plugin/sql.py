from utils.plugin.template import PluginTemplate


class SQL_INJECTION(PluginTemplate):
    def input_data_handling(self, log):
        pass

    def detect(self, log):
        signature = "id=1 AND (SELECT"
        if signature in log:
            return True
        else:
            return False
