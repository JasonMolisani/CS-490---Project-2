import unittest

KEY_INPUT = "input"
KEY_EXPECTED = "expected"

class SplitTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: "",
                KEY_EXPECTED: ""
            }
        ]
        
        self.failure_test_params = [
            {
                KEY_INPUT: "",
                KEY_EXPECTED: ""
            }
        ]


    def test_success(self):
        for test in self.success_test_params:
            response = test[KEY_INPUT]
            expected = test[KEY_EXPECTED]
            
            self.assertEqual(response, expected)
            
    def test_failure(self):
        for test in self.failure_test_params:
            response = test[KEY_INPUT]
            expected = test[KEY_EXPECTED]
            
            self.assertNotEqual(response, expected)


if __name__ == '__main__':
    unittest.main()