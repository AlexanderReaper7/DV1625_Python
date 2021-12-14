import sys
import collections

class RBNode():
    """A node in the red black tree"""
    def __init__(self, item):
        self.item = item
        self.is_red = True
        self.parent = None
        self.left = None
        self.right = None

class RedBlackTree():
    """an arbitrary data structure for a red-black tree"""
    def __init__(self):
        self.nil = RBNode(None)
        self.nil.is_red = False
        self.nil.parent = None
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil

### INSERT ###

    def insert(self, key):
        """inserts an item into the tree"""
        z = RBNode(key)
        z.item = key
        z.parent = None
        z.left = self.nil
        z.right = self.nil
        z.is_red = True

        y = None
        x = self.root
        while x != self.nil:
            y = x
            if z.item < x.item:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y is None:
            self.root = z
        elif z.item < y.item:
            y.left = z
        else:
            y.right = z

        if z.parent is None:
            z.is_red = False
            return
        if z.parent.parent is None:
            return

        self.insert_fixup(z)

    def insert_fixup(self, z):
        """fixes the tree after an insertion"""
        while z.parent.is_red is True:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.is_red is True:
                    z.parent.is_red = False
                    y.is_red = False
                    z.parent.parent.is_red = True
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.is_red = False
                    z.parent.parent.is_red = True
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.is_red is True:
                    z.parent.is_red = False
                    y.is_red = False
                    z.parent.parent.is_red = True
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.is_red = False
                    z.parent.parent.is_red = True
                    self.left_rotate(z.parent.parent)
            if z == self.root:
                break
        self.root.is_red = False

### DELETE ###

    def transplant(self, u, v):
        """Transplants two nodes"""
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete_fixup(self, x):
        """fixes the tree after a deletion"""
        while x != self.root and x.is_red == False:
            if x == x.parent.left:
                w = x.parent.right
                if w.is_red == True:
                    w.is_red = False
                    x.parent.is_red = True
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.is_red == False and w.right.is_red == False:
                    w.is_red = True
                    x = x.parent
                else:
                    if w.right.is_red == False:
                        w.left.is_red = False
                        w.is_red = True
                        self.right_rotate(w)
                        w = x.parent.right
                    w.is_red = x.parent.is_red
                    x.parent.is_red = False
                    w.right.is_red = False
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.is_red == True:
                    w.is_red = False
                    x.parent.is_red = True
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.is_red == False and w.right.is_red == False:
                    w.is_red = True
                    x = x.parent
                else:
                    if w.left.is_red == False:
                        w.right.is_red = False
                        w.is_red = True
                        self.left_rotate(w)
                        w = x.parent.left
                    w.is_red = x.parent.is_red
                    x.parent.is_red = False
                    w.left.is_red = False
                    self.right_rotate(x.parent)
                    x = self.root
        x.is_red = False

    def delete(self, z):
        """deletes a node"""
        y = z
        y_original_color = y.is_red
        if z.left == self.nil:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.branch_minimum(z.right)
            y_original_color = y.is_red
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.is_red = z.is_red
        if y_original_color == False:
            self.delete_fixup(x)

    def remove(self, item):
        """removes an item"""
        z = self.nil
        node = self.root
        while node != self.nil:
            if node.item == item:
                z = node
            if node.item <= item:
                node = node.right
            else:
                node = node.left
        if z == self.nil:
            print("item not found")
            return
        self.delete(z)

### SEARCHING ###

    def search(self, item):
        """searches the tree for an item, returns true if found."""
        node = self.root
        while node != self.nil:
            if node.item == item:
                return True
            if item < node.item:
                node = node.left
            else:
                node = node.right
        return False

    def path(self, key):
        """returns the path to the item in the tree"""
        node = self.root
        output = list()
        while node != self.nil:
            output.append(node.item)
            if node.item == key:
                return output
            if key < node.item:
                node = node.left
            else:
                node = node.right

    def branch_maximum(self, node):
        """returns the largest node on this branch"""
        while node.right != self.nil:
            node = node.right
        return node

    def branch_minimum(self, node):
        """returns the smallest node on this branch"""
        while node.left != self.nil:
            node = node.left
        return node

    def min(self):
        """returns the smallest item in the tree"""
        if self.root == self.nil:
            print("tree is empty")
            return None
        node = self.root
        while node.left != self.nil:
            node = node.left
        return node.item

    def max(self):
        """returns the largest item in the tree"""
        if self.root == self.nil:
            print("tree is empty")
            return None
        node = self.root
        while node.right != self.nil:
            node = node.right
        return node.item

    def bfs(self):
        """returns a bfs tree-node list"""
        visited, queue = list(), collections.deque([self.root])
        visited.append(self.root)
        while queue:
            vertex = queue.popleft()
            for neighbour in [vertex.right, vertex.left]:
                if neighbour != self.nil and neighbour not in visited:
                    visited.append(neighbour)
                    queue.append(neighbour)
        output = list()
        i = len(visited)
        while i > 0:
            i -= 1
            if visited[i].is_red:
                output.append([visited[i].item, "RED", visited[i].left.item, visited[i].right.item])
            else:
                output.append([visited[i].item, "BLACK",
                 visited[i].left.item, visited[i].right.item])
        return output

### ROTATION ###

    def left_rotate(self, x):
        """rotates left"""
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        """rotates right"""
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
