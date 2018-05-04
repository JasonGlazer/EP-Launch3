import os
import subprocess
import platform

from eplaunch.workflows.base import BaseEPLaunch3Workflow, EPLaunch3WorkflowResponse


class ColumnNames(object):
    Errors = 'Errors'
    Warnings = 'Warnings'
    Runtime = 'Runtime [s]'


class EPlusRunManager(object):

    # This will eventually be a path relative to this script.
    # Since these workflows will live at /EnergyPlus/Install/workflows/energyplus.py
    # We will generate the path dynamically from __file__ and os.path.join to get to the E+ binary
    if platform.system() == 'Windows':
        EnergyPlusBinary = 'c:\\EnergyPlusV8-8-0\\energyplus.exe'
    else:
        EnergyPlusBinary = '/home/edwin/Programs/EnergyPlus-8-9-0/energyplus'

    @staticmethod
    def get_end_summary(end_file_path):
        contents = open(end_file_path, 'r').read()
        if 'EnergyPlus Completed Successfully' not in contents:
            return False, None, None, None
        last_line_tokens = contents.split(' ')
        num_warnings = int(last_line_tokens[3])
        num_errors = int(last_line_tokens[5])
        time_position_marker = contents.index('Time=')
        time_string = contents[time_position_marker:]
        num_hours = int(time_string[5:7])
        num_minutes = int(time_string[10:12])
        num_seconds = float(time_string[16:21])
        runtime_seconds = num_seconds + num_minutes/60 + num_hours/3600
        return True, num_errors, num_warnings, runtime_seconds


class EnergyPlusWorkflowSI(BaseEPLaunch3Workflow):

    def name(self):
        return "EnergyPlus SI"

    def description(self):
        return "Run EnergyPlus with SI unit system"

    def get_file_types(self):
        return ["*.idf", "*.imf"]

    def get_extra_data(self):
        return {"Hey, it's extra": "data"}

    def get_interface_columns(self):
        return [ColumnNames.Errors, ColumnNames.Warnings, ColumnNames.Runtime]

    def main(self, run_directory, file_name, args):

        full_file_path = os.path.join(run_directory, file_name)

        file_name_no_ext, extention = os.path.splitext(file_name)

        # run E+ and gather (for now fake) data
        process = subprocess.run([EPlusRunManager.EnergyPlusBinary, '--output-prefix',file_name_no_ext, '--design-day', file_name], cwd=run_directory)
        status_code = process.returncode

        # for i in range(5):
        #     time.sleep(1)
        #     if self.abort:
        #         return EPLaunch3WorkflowResponse(
        #             success=False,
        #             message="Abort command accepted!",
        #             column_data={}
        #         )
        if status_code != 0:
            return EPLaunch3WorkflowResponse(
                success=False,
                message="EnergyPlus failed for file: %s!" % full_file_path,
                column_data={}
            )

        end_file_path = os.path.join(run_directory, 'eplusout.end')
        success, errors, warnings, runtime = EPlusRunManager.get_end_summary(end_file_path)
        column_data = {ColumnNames.Errors: errors, ColumnNames.Warnings: warnings, ColumnNames.Runtime: runtime}

        # now leave
        return EPLaunch3WorkflowResponse(
            success=True,
            message="Ran EnergyPlus OK for file: %s!" % file_name,
            column_data=column_data
        )


class EnergyPlusWorkflowIP(BaseEPLaunch3Workflow):

    def name(self):
        return "EnergyPlus IP"

    def description(self):
        return "Run EnergyPlus with IP unit system"

    def get_file_types(self):
        return ["*.idf", "*.imf"]

    def get_extra_data(self):
        return {"Hey, it's extra": "data"}

    def get_interface_columns(self):
        return [ColumnNames.Errors, ColumnNames.Warnings, ColumnNames.Runtime]

    def main(self, run_directory, file_name, args):

        full_file_path = os.path.join(run_directory, file_name)

        # run E+ and gather (for now fake) data
        status_code = subprocess.call([EPlusRunManager.EnergyPlusBinary, '-D', file_name], cwd=run_directory)
        # for i in range(5):
        #     time.sleep(1)
        #     if self.abort:
        #         return EPLaunch3WorkflowResponse(
        #             success=False,
        #             message="Abort command accepted!",
        #             column_data={}
        #         )
        if status_code != 0:
            return EPLaunch3WorkflowResponse(
                success=False,
                message="EnergyPlus failed for file: %s!" % full_file_path,
                column_data={}
            )

        end_file_path = os.path.join(run_directory, 'eplusout.end')
        success, errors, warnings, runtime = EPlusRunManager.get_end_summary(end_file_path)
        column_data = {ColumnNames.Errors: errors, ColumnNames.Warnings: warnings, ColumnNames.Runtime: runtime}

        # now leave
        return EPLaunch3WorkflowResponse(
            success=True,
            message="Ran EnergyPlus OK for file: %s!" % file_name,
            column_data=column_data
        )