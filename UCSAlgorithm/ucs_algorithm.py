from graph import Node, Graph
  

class UCS:
  """
    This class used to represent the Greedy algorithm
    ...
    Attributes
    ----------
    graph : Graph
      Represent the graph (search space of the problem) 
    start : str
      Represent the starting point 
    target : str
      Represent the destination (target) node
    opened : list
      Represent the list with the available nodes in the search process
    closed : list
      Represent the list with the closed (visited) nodes
    number_of_steps : int
      Keep the number of steps of the algorithm
    ...
    Methods
    -------
    calculate_distance(self, parent, child) -> int
      Calculate the distance from the starting node to the child node
    insert_to_list(self, list_category, node) -> None
      Insert a new node either ot opened or to closed list according to list_category parameter 
    remove_from_opened(self) -> Node
      Remove from the opened list the node with the smallest heuristic value
    opened_is_empty(self) -> Boolean
      Check if the opened list is empty or not
    get_old_node(self, node_value) -> Node
      Return the node from the opened list in case of a new node with the same value
    calculate_path(self, target_node) -> list
      Calculate and return the path from the stat node to target node
    search(self)
        Implements the core of algorithm. This method searches, in the search space of the problem, a solution 
    """

  def __init__(self, graph, start_position, target):
    self.graph = graph
    self.start = graph.find_node(start_position)
    self.target = graph.find_node(target)
    self.opened = []
    self.closed = []
    self.number_of_steps = 0


  def calculate_distance(self, parent, child):
    """
      Calculate and return the distance from the start to child node. If the heuristic value has already calculated
      and is smaller than the new value, the method return theold value. Otherwise the method return the new value
      and note the parent as the parent node of child
      Parameters
      ----------
      parent : Node
        Represent the parent node
      child : Node
        Represent the child node
      ...
      Return 
      ------
        int
    """
    for neighbor in parent.neighbors:
      if neighbor[0] == child:
        distance = parent.heuristic_value + neighbor[1]
        if distance < child.heuristic_value:
          child.parent = parent
          return distance
        
        return child.heuristic_value

  
  def insert_to_list(self, list_category, node):
    """
      Insert a node in the proper list (opened or closed) according to list_category
      Parameters
      ----------
      list_category : str
          Determines the list in which the node will be appened. If the value is 'open' 
          the node is appended in the opened list. Otherwise, the node is appended in the closed list
      node : Node
          The node of the problem that will be added to the frontier
    """
    if list_category == "open":
      self.opened.append(node)
    else:
      self.closed.append(node)
  

  def remove_from_opened(self):
    """
      Remove the node with the smallest heuristic value from the opened list
      Then add the removed node to the closed list
      Returns
      -------
        Node
    """
    self.opened.sort()
    # for n in self.opened:
    #   print(f"({n},{n.heuristic_value})", end = " ")
    # print("\n")
    node = self.opened.pop(0)
    self.closed.append(node)
    return node


  def opened_is_empty(self):
    """
      Check if the the list opened is empty, so no solution found
      Returns
      -------
      Boolean
        True if the list opened is empty
        False if the list opened is not empty
    """
    return len(self.opened) == 0


  def get_old_node(self, node_value):
    """
      Return the node with the given value from the opened list,
      to compare its heuristic_value with a node with the same value
      ...
      Parameters
      ----------
        node_value : Node
        Represent the value of the node
      Returns
      -------
        Node
    """
    for node in self.opened:
      if node.value == node_value:
        return node
    return None 
      

  def calculate_path(self, target_node):
    """
      Calculate and return the path (solution) of the problem
      ...
      Parameters
      ----------
        target_node : Node
        Represent final (destination) node of the problem
      Returns
      -------
        list
    """
    path = [target_node.value]
    node = target_node.parent
    while True:
      path.append(node.value)
      if node.parent is None:
        break
      node = node.parent
    path.reverse()
    return path
  
  
  def search(self):
    """
      Is the main algorithm. Search for a solution in the solution space of the problem
      Stops if the opened list is empty, so no solution found or if it find a solution. 
      ...
      Return
      ------
        list
    """
    # The heuristic value of the starting node is zero
    self.start.heuristic_value = 0
    # Add the starting point to opened list
    self.opened.append(self.start)

    while True:
      self.number_of_steps += 1

      if self.opened_is_empty():
        print(f"No Solution Found after {self.number_of_steps} steps!!!")
        break
        
      selected_node = self.remove_from_opened()
      # print(f"Selected Node {selected_node}")
      # check if the selected_node is the solution
      if selected_node == self.target:
        path = self.calculate_path(selected_node)
        return path, self.number_of_steps

      # extend the node
      new_nodes = selected_node.extend_node()

      # add the extended nodes in the list opened
      if len(new_nodes) > 0:
        for new_node in new_nodes:
          
          new_node.heuristic_value = self.calculate_distance(selected_node, new_node)
          if new_node not in self.closed and new_node not in self.opened:
            self.insert_to_list("open", new_node)
          elif new_node in self.opened and new_node.parent != selected_node:
            old_node = self.get_old_node(new_node.value)
            if new_node.heuristic_value < old_node.heuristic_value:
              new_node.parent = selected_node
              self.insert_to_opened(new_node)

def run():
  graph = Graph()
  graph.add_node(Node('V1'))
  graph.add_node(Node('V2'))
  graph.add_node(Node('V3'))
  graph.add_node(Node('V4'))
  graph.add_node(Node('V5'))
  graph.add_node(Node('V6'))

  graph.add_edge('V1', 'V2', 9)
  graph.add_edge('V1', 'V3', 4)
  graph.add_edge('V2', 'V3', 2)
  graph.add_edge('V2', 'V4', 7)
  graph.add_edge('V2', 'V5', 3)
  graph.add_edge('V3', 'V4', 1)
  graph.add_edge('V3', 'V5', 6)
  graph.add_edge('V4', 'V5', 4)
  graph.add_edge('V4', 'V6', 8)
  graph.add_edge('V5', 'V6', 2)

  alg = UCS(graph, "V1", "V6")
  path, path_length = alg.search()
  print(" -> ".join(path))
  print(f"Lenghth of the path: {path_length}")

if __name__ == '__main__':
  run()