from eplaunch.workflows.base import BaseWorkflow


class CoeffCheckWorkflow(BaseWorkflow):

    def name(self):
        return "CoeffCheck"

    def description(self):
        return "Run Coeff Check"

    def get_file_types(self):
        return ["*.cci"]

    def get_extra_data(self):
        return {"Hey, it's extra": "data"}
