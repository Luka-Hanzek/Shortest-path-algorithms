from data_strucutres.priority_queue import PriorityQueue
import random

tests = [1,1]
if(tests[0]):
    p_q = PriorityQueue()
    test_data = []
    for i in range(100):
        test_data.append((i, random.randint(0, 1000)))

    for element, priority in test_data:
        p_q.insert(element, priority)

    test_passed = True
    for element, priority in test_data:
        extracted_element = p_q._data[p_q.getIndex(element)][0]
        
        if(extracted_element != element):
            print(f"expected: {element} actual: {extracted_element}")
            test_passed = False

    print(f"Test passed: {test_passed}")

if(tests[1]):
    p_q = PriorityQueue()
    input_data = []
    input_data.append(("e0", 7))
    input_data.append(("e1", 4))
    input_data.append(("e2", 10))
    input_data.append(("e3", 2))
    input_data.append(("e4", 3))
    input_data.append(("e5", 9))
    input_data.append(("e6", 8))
    input_data.append(("e7", 5))
    input_data.append(("e8", 6))
    input_data.append(("e9", 1))
    
    expected_output_data = [ "e1", "e9", "e3", "e4", "e7", "e8", "e0", "e6", "e5", "e2"]
    for value, priority in input_data:
        p_q.insert(value, priority)

    p_q.modifyElement("e1", "e1", 0)
    print(p_q)
    test_passed = True
    for expected in expected_output_data:
        actual = p_q.get()
        if(expected != actual):
            print(f"expected: {expected} actual: {actual}")
            test_passed = False
    
    print(f"Test passed: {test_passed}")