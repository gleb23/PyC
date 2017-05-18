from bricks import Function, Int, Void
from errs import ClassCastError


class BuiltInFunction(Function):
    def __init__(self, name = None, parentBlock=None, params=None, return_type=None):
        super(BuiltInFunction, self).__init__(name, parentBlock, params, return_type)


class Function_get(BuiltInFunction):
    def __init__(self):
        super(Function_get, self).__init__(name='get', parentBlock=None, params=None, return_type=Int)

    def execute(self):
        try:
            return Int(int(raw_input()))
        except ValueError:
            raise ClassCastError()


class Function_put(BuiltInFunction):
    def __init__(self):
        super(Function_put, self).__init__(name='put', parentBlock=None, params=[Int()], return_type=Void)

    def execute(self):
        print self.params[0].execute().value
        return Void()

builtins_map = {
    'get': Function_get(),
    'put': Function_put(),
}
