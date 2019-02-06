class Beam:

    def __init__(self, power, waist, label, detuning=0):
        """

        :param power:
        :param waist:
        :param label:
        :param detuning:
        """
        self.power = power
        self.waist = waist
        self.label = label
        self.detuning = detuning

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, val):
        try:
            self.__label
            q = input("Are you sure you want to change permissions (y/n)?")
            if q in ["Yes", "yes", "Y", "y", "True", "true"]:
                self.__label = val
            else:
                pass
        except:
            self.__label = val


class Atom:

    def __init__(self, decay_rates, dipole_moments, lower_splittings, upper_splittings, detuning=0):
        """

        :param decay_rates:
        :param dipole_moments:
        :param lower_splittings:
        :param upper_splittings:
        :param detuning:
        """
        self.decay_rates = decay_rates
        self.dipole_moments = dipole_moments
        self.lower_splittings = lower_splittings
        self.upper_splittings = upper_splittings
        self.detuning = detuning

        self.n_lower = len(lower_splittings) + 1
        self.n_upper = len(upper_splittings) + 1
        self.classes = self._generate_classes_list()
        self._generate_transition_list()

    def _generate_classes_list(self):
        """

        :return:
        """
        classes = {}
        for l in range(self.n_lower):
            for u in range(self.n_upper):
                classes.update({"class " + str(l + 1) + "-" + str(u + 1 + self.n_upper): [[l + 1, u + 1 + self.n_upper], []]})
        return classes

    def _generate_transition_list(self):
        """
        Fill classes dictionary.  Format is {'class l-u':[[l, u], [[tran_l, tran_u], frequency, 'permission']]}
        :return:
        """
        for ion_class in self.classes:
            for i in range(self.n_lower):
                for j in range(self.n_upper):
                    lower_target = self.classes[ion_class][0][0] - 1
                    upper_target = self.classes[ion_class][0][1] - 1 - self.n_upper
                    if i == lower_target and j != upper_target:
                        limits = sorted([j, upper_target])
                        up_down = (j - upper_target) / (abs(j - upper_target))
                        frequency = up_down * sum(self.upper_splittings[limits[0]:limits[1]])
                    elif i == lower_target and j == upper_target:
                        frequency = 0
                    elif i != lower_target and j == upper_target:
                        limits = sorted([i, lower_target])
                        up_down = (lower_target - i) / (abs(lower_target - i))
                        frequency = up_down * sum(self.lower_splittings[limits[0]:limits[1]])
                    else:
                        limits_lower = sorted([i, lower_target])
                        limits_upper = sorted([j, upper_target])
                        up_down_lower = (lower_target - i) / (abs(lower_target - i))
                        up_down_upper = (j - upper_target) / (abs(j - upper_target))
                        frequency = up_down_lower * sum(
                            self.lower_splittings[limits_lower[0]:limits_lower[1]]) + up_down_upper * sum(
                            self.upper_splittings[limits_upper[0]:limits_upper[1]])
                    self.classes[ion_class][1].append([[i + 1, j + 1 + self.n_upper], round(frequency, 1), 'none'])
        return None

    def print_classes(self):
        """

        :return:
        """
        for classs in self.classes:
            print(classs, self.classes[classs][0])
            for tran in self.classes[classs][1]:
                print("    ", tran)

# fuck = Atom(1, 1, [148.9, 76.4], [183, 114])
# fuck.print_classes()
