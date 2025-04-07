class Parameters:
    final_dict = {"pretty": True}
    def __init__(self,filters = None, format = "JSON", fields = None, expand = None, size = 10000, from_param = 0, sort = None, facets = None):
        if filters is not None: self.final_dict["filters"] = filters
        self.final_dict.update({"format": format})
        if fields is not None: self.final_dict.update({"fields": fields})
        if expand is not None: self.final_dict.update({"expand": expand})
        self.final_dict.update({"size": size})
        self.final_dict.update({"from": from_param})
        if sort is not None: self.final_dict.update({"sort": sort})
        if facets is not None: self.final_dict.update({"facets": facets})

    def get_parameters(self):
        return self.final_dict

    def add_parameters(self, parameters: dict):
        self.final_dict.update(parameters)

    def change_parameters(self, parameter, value):
        if parameter in self.final_dict:
            self.final_dict[parameter] = value
        else:
            print(f"\033[91mWarning\033[0m: parameter \"\033[93m{parameter}\033[0m\" does not exist")




test = Parameters(format="CSV")
print(test.get_parameters())
test.change_parameters("formsat", "TSV")
print(test.get_parameters())
