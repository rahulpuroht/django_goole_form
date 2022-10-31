class Node:
    def __init__(self,d):
        self.data=d
        self.next=None

class LinkedList:
    def __init__(self):
        self.head=None

    def push(self,d):

        new_node=Node(d)
        if not self.head:
            self.head=new_node
        else:
            new_node.next=self.head
            self.head=new_node


    def swappair(self):
        this_node=self.head
        

        if not this_node:
            return

        while (this_node and this_node.next):

            if this_node.data != this_node.next.data:

                this_node.data,this_node.next.data=this_node.next.data,this_node.data
            this_node=this_node.next.next
            

    def display(self):
        if not self.head:
            print('the list is empty')
        else:
            iternode=self.head
            while iternode:
                print(iternode.data)
                iternode= iternode.next



llist = LinkedList()
llist.push(5)
llist.push(4)
llist.push(3)
llist.push(2)
llist.push(1)
 
print "Linked list before calling pairWiseSwap() "
llist.display()
 
llist.swappair()
 
print "\nLinked list after calling pairWiseSwap()"
llist.display()
 


    
