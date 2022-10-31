class BinarySearchNode():
    def __init__(self,data):
        self.data=data
        self.right=None
        self.left=None

    def add_child(self,data):

        if self.data == data:
            return
        print(11,'self.data>>',self.data,'data>>',data)
        if  data < self.data :
            #print(1,'self.data>>',self.data,'data>>',data)
            if self.left is not None:
                self.left.add_child(data)

            else:
                #print(2, 'self.data>>',self.data)
                self.left=BinarySearchNode(data)
        else:
            if self.right is not None:
                self.right.add_child(data)
            
            else:
                self.right=BinarySearchNode(data)


    def in_order_traversal(self):
        elements=[]

        #visit left sub tree
        if self.left:
            print(1,'elements before left traversal')
            elements += self.left.in_order_traversal()
            print(2,elements)
        #visit base node
        elements.append(self.data)

        #visit right sub tree
        if self.right:
            print(3,'elements before right traversal')
            elements += self.right.in_order_traversal()
            print(4,elements)
        
        return elements


    def pre_order_traversal(self):
        elements=[]

        if self.data:
            elements.append(self.data)

        if self.left:
            elements += self.left.pre_order_traversal()

        if self.right:
            elements += self.right.pre_order_traversal()

       

        return elements

    def post_order_traversal(self):
        elements=[]

        if self.left:
            elements += self.left.post_order_traversal()

        if self.right:
            elements += self.right.post_order_traversal()

        if self.data:
            elements.append(self.data)

        return elements


    def search(self,data):
        if self.data==data:
            return True

        if data < self.data:#val might be left subtree

            if self.left:
                return self.left.search(data)
            
            else:
                return False
        else:#val might be right subtree

            if self.right:
                return self.right.search(data)
            else:
                return False

def build_tree(numbers):
    root=BinarySearchNode(numbers[0])
    for i in range(1, len(numbers)):
        root.add_child(numbers[i])

    return root


numbers=[22,4,6,12,87,34,23,56]
numbers_tree= build_tree(numbers)
print(numbers_tree)
print(numbers_tree.in_order_traversal())
print(numbers_tree.search(87))
print('pre_order_traversal>>>',numbers_tree.pre_order_traversal())
print('post_order_traversal>>>',numbers_tree.post_order_traversal())



