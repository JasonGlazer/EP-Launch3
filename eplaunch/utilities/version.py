class Version:

    def check_energyplus_version(self, file_path):
        found = False
        current_version = ''
        with open(file_path, "r") as f:
            cur_line = f.readline()
            while cur_line:
                cur_line = cur_line.strip()
                if cur_line:
                    if cur_line[0] != "!":
                        cur_line = cur_line.upper()
                        if "VERSION" in cur_line:
                            cur_line = self.line_with_no_comment(cur_line)
                            if ";" in cur_line:
                                poss_obj = cur_line
                            else:
                                next_line = f.readline()
                                next_line = next_line.strip()
                                next_line = self.line_with_no_comment(next_line)
                                poss_obj = cur_line + next_line
                            if poss_obj[-1] == ";":
                                poss_obj = poss_obj[:-1]
                            fields = poss_obj.split(',')
                            current_version = fields[1]
                            found = True
                            break
                cur_line = f.readline()  # get the next line
        # print("The current version is {} which is {}".format(current_version,
        #                                          self.numeric_version_from_string(current_version)))
        return found, current_version, self.numeric_version_from_string(current_version)

    def line_with_no_comment(self, in_string):
        exclamation_point_pos = in_string.find("!")
        if exclamation_point_pos >= 0:
            out_string = in_string[0:exclamation_point_pos]
            out_string = out_string.strip()
        else:  # no explanation point found
            out_string = in_string.strip()
        return out_string

    def numeric_version_from_string(self, string_version):
        # if the version string has sha1 hash at the end remove it
        words = string_version.split("-")
        # the rest of the version number should just be separated by periods
        parts = words[0].split(".")
        numeric_version = 0
        parts = parts[:3]
        # if only a two part version number add a zero.
        if len(parts) == 2:
            parts.append("0")
        for part in parts:
            numeric_version = numeric_version * 100 + int(part)
        return numeric_version
