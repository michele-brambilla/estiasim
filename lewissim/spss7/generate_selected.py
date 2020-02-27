template = """
@property
def selected_%d(self):
    return selected_impl(%d, self._values)
"""

for i in range(1,37):
    print(template%(i,i))