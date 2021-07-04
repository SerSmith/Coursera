class TestFactorize(unittest.TestCase):

    def test_wrong_types_raise_exception(self):
        cases = ['string', 1.5]

        for case in cases:
            with self.subTest(i=case):
                with self.assertRaises(TypeError):
                    factorize(x=case)
    
    def test_negative(self):
        cases = [-1,  -10,  -100]
        for case in cases:
            with self.subTest(i=case):
                with self.assertRaises(ValueError):
                    factorize(x=case)
    
    def test_zero_and_one_cases(self):
        cases = [0, 1]
        for case in cases:
            with self.subTest(i=case):
                res = factorize(x=case)
                self.assertTupleEqual(res, (case,))

    def test_simple_numbers(self):
        cases = [3, 13, 29]
        for case in cases:
            with self.subTest(i=case):
                res = factorize(x=case)
                self.assertTupleEqual(res, (case,))

    def test_two_simple_multipliers(self):
        cases = [6, 26, 121]
        answers = [(2, 3), (2, 13), (11, 11)]
        for case, answer in zip(cases, answers):
            with self.subTest(i=case):
                res = factorize(x=case)
                self.assertTupleEqual(res, answer)

    def test_many_multipliers(self):
        cases = [1001, 9699690]
        answers = [(7, 11, 13), (2, 3, 5, 7, 11, 13, 17, 19)]
        for case, answer in zip(cases, answers):
            with self.subTest(i=case):
                res = factorize(x=case)
                self.assertTupleEqual(res, answer)
