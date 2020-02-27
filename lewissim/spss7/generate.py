
##########################

# template = """
# @property
# def selected_%d(self):
#     return self._selected_impl(%d)
# """

#for i in range(1,37):
#    print(template%(i,i))
###########################

template = """
@property
def select_%d(self):
    return r_select_impl(%d, self._mask)

@select_%d.setter
def select_%d(self, value):
    if value:
        self._values, self._mask = select_impl(%d, self._values, self._mask)
"""

for i in range(1,37):
    print(template%(i,i,i,i,i))