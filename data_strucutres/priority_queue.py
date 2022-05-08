class PriorityQueue:
    """
    Models priority queue.\n
    Implemented using min heap data structure.\n
    Time complexities:
        element addition: O(log(n))
        element search: O(1)
    """
    def __init__(self, optimization_key_extractor = lambda x: x):
        self.lookup_dict = {}
        self.optimization_key_extractor = optimization_key_extractor
        self.size = 0
        self.data = [None]


    def minHeapify(self, pos: int) -> None:
        """Prepare smallest element for get operation

        Args:
            pos (int): Position where smallest element of all its descendants will be placed
        """
        lookup_dict = self.lookup_dict
        data = self.data
        #if leaf not reached
        while(pos*2 <= self.size):
            if(pos*2 + 1 > self.size):
                #if there is no right child
                if(data[pos*2][1] < data[pos][1]):
                    lookup_dict[self.optimization_key_extractor(data[pos][0])] = pos*2
                    lookup_dict[self.optimization_key_extractor(data[pos*2][0])] = pos
                    data[pos*2], data[pos] = data[pos], data[pos*2]
                return
            if(data[pos][1] <= data[pos*2][1] and data[pos][1] <= data[pos*2 + 1][1]):
                return
            if(data[pos*2][1] <= data[pos*2 + 1][1]):
                #left child is smaller than current
                lookup_dict[self.optimization_key_extractor(data[pos][0])] = pos*2
                lookup_dict[self.optimization_key_extractor(data[pos*2][0])] = pos
                data[pos*2], data[pos] = data[pos], data[pos*2]
                pos = pos * 2
            else:
                #right child is smaller than current
                lookup_dict[self.optimization_key_extractor(data[pos][0])] = pos*2 + 1
                lookup_dict[self.optimization_key_extractor(data[pos*2 + 1][0])] = pos
                data[pos*2 + 1], data[pos] = data[pos], data[pos*2 + 1]
                pos = pos * 2 + 1
        

    def insert(self, element: object, priority: object) -> None:
        """Insert element with specific priority
        
        Args:
            element (object): element to be added
            priority (object): comparable value used to compare elements in priority queue
        """
        lookup_dict = self.lookup_dict
        data = self.data
        self.size += 1
        data.append((element, priority))
        current_index = self.size
        lookup_dict[self.optimization_key_extractor(element)] = current_index

        while(current_index > 1 and data[current_index][1] < data[current_index//2][1]):
            lookup_dict[self.optimization_key_extractor(data[current_index][0])] = current_index//2
            lookup_dict[self.optimization_key_extractor(data[current_index//2][0])] = current_index
            data[current_index//2], data[current_index] = data[current_index], data[current_index//2]
            current_index = current_index//2

    def get(self) -> object:
        """Gets next element from priority queue
        
        Returns:
            object: Next element if not empty, None otherwise
        """
        lookup_dict = self.lookup_dict
        data = self.data
        if(len(data) > 1):
            first_h_element = data[1]
            last_h_element = data[-1]
            lookup_dict[self.optimization_key_extractor(last_h_element[0])] = 1
            data[1] = last_h_element
            del data[-1]
            del lookup_dict[self.optimization_key_extractor(first_h_element[0])]
            self.size -= 1
            self.minHeapify(1)
            return first_h_element[0]
        else:
            return None


    def getIndex(self, element: object) -> int:
        """Gets index of the element with the same extracted feature according to optimization_key_extractor
        
        Args:
            element (object): Element containing a feature based on which to find the element in priority queue

        Returns:
            int: Index of element with same feature according to optimization_key_extractor if found, -1 otherwise
        """
        try:
            index = self.lookup_dict[self.optimization_key_extractor(element)]
            return index
        except KeyError as e:
            return -1
    

    def getElement(self, element: object) -> object:
        """Gets extracted_element with the same extracted feature as element according to optimization_key_extractor
        
        Args:
            element (object): Element containing a feature based on which to find the element in priority queue

        Returns:
            object: Extracted element with same feature as element according to optimization_key_extractor if found, None otherwise
        """
        
        try:
            index = self.lookup_dict[self.optimization_key_extractor(element)]
            extracted_element = self.data[index][0]
            return extracted_element
        except KeyError as e:
            return None

    def contains(self, element: object) -> bool:
        """Checks if priority queue contains element based on extracted feature extracted according to optimization_key_extractor
        
        Args:
            element (object): Element containing feature based on which to find element in priority queue

        Returns:
            bool: True if element with feature found, False otherwise
        """
        try:
            extracted_element = self.lookup_dict[self.optimization_key_extractor(element)]
            return True
        except KeyError as e:
            return False
    

    def empty(self) -> bool:
        """Checks if priority queue is empty
        
        Returns:
            bool: True if empty, False otherwise
        """
        return self.size == 0


    def size(self) -> int:
        """Gets number of elements in priority queue
        
        Returns:
            int: number of elements in priority queue
        """
        return self.size
    

    def modifyElement(self, element, new_element, new_priority) -> object:
        """Replaces element found in priority queue based on feature extracted based on optimization_key_extractor with new_element
        
        Args:
            element (object): Element containing feature based on which to find element to replace in priority queue
            new_element (object): Element to replace the existing element in priority queue

        Returns:
            object: Element which has been replaced if found, None otherwise
        """
        index = self.getIndex(element)
        if(index == -1):
            return None
        old_h_element = self.data[index]
        #del self.data[index]
        self.data[index] = (new_element, new_priority)
        #del self.lookup_dict[self.optimization_key_extractor(element)]
        #self.lookup_dict[self.optimization_key_extractor(element)] = 1
        while(index >= 1):
            self.minHeapify(index)
            index //=2

        return old_h_element


    def __str__(self) -> str:
        return [f'{element.__str__()} {priority.__str__()}' for element, priority in self.data[1:]].__str__()
