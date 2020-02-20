import unittest
exec(open("./data_process.py").read())

root = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
data_path = os.path.join(root, "data")
file = os.path.join(data_path,"test")

class TestCheckAnnotation(unittest.TestCase):
    def test_basic_true(self):
        self.assertTrue(check_annotation(file+"_annotated"))
    def test_dict_true(self):
        self.assertTrue(check_annotation(file+"2_annotated"))
    def test_empty(self):
        self.assertFalse(check_annotation(file+"5_annotated"))
    def test_basic_false(self):
        self.assertFalse(check_annotation(file+"3_annotated"))
    def test_dict_false(self):
        self.assertFalse(check_annotation(file+"4_annotated"))
        
if __name__=='__main__':
      unittest.main()