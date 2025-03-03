# This example deviates from Mesa's ForestFire in that it uses BaseScheduler
# instead of RandomActivation.

from mesa import Model
from mesa import Agent
from mesa.space import SingleGrid
from mesa.time import BaseScheduler

class TreeCell(Agent):
    """
    A tree cell.
    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.
    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """

    def __init__(self, pos, model):
        """
        Create a new tree.
        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        if self.condition == "On Fire":
            for neighbor in self.model.grid.iter_neighbors(self.pos, moore=False):
                if neighbor.condition == "Fine":
                    neighbor.condition = "On Fire"
            self.condition = "Burned Out"

class ForestFire(Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, seed, height, width, density):
        """
        Create a new forest fire model.
        Args:
            height, width: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        super().__init__(seed=seed)
        # Set up model objects
        self.schedule = BaseScheduler(self)
        self.grid = SingleGrid(height, width, torus=False)

        # Place a tree in each cell with Prob = density
        for cont, pos in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell(pos, self)
                # Set all trees in the first column on fire.
                if pos[0] == 0:
                    new_tree.condition = "On Fire"
                self.grid.place_agent(new_tree, pos)
                self.schedule.add(new_tree)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
