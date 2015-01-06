class Diff:
    def __init__(self, expected, actual):
        self.expected = expected
        self.actual = actual
    
    def OutputResult(self):
        ret = ''
        if self.expected == self.actual:
            ret += 'Equal. Both collections have ' + str(len(self.expected)) + ' items.\n'
        else:
            ret += 'The expected collection has ' + str(len(self.expected)) + ' items, while the actual collection has ' + str(len(self.actual))+ ' items.\n'
            ret += 'Expected diff actual: ' + str([i for i in self.expected if i not in self.actual]) + '\n'
            ret += 'Actual diff expected: ' + str([i for i in self.actual if i not in self.expected]) + '\n'
        return ret
            
if __name__ == "__main__":
    d = Diff([1, 2, 3], [3, 4])
    print d.OutputResult()
    
    d = Diff([1, 2, 3], [1, 2, 3])
    print d.OutputResult()
