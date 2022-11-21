import copy
import Engine
x = Engine.Process()
print(x.events)
copy = copy.deepcopy(x)
copy.add_event("A")
print(x.events)
