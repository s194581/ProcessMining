class Relation:
    src = ''
    tgt = ''
    rel = ''

    def __init__(self, src, rel, tgt):
        self.src = src
        self.rel = rel
        self.tgt = tgt


class Process:
    events = set()
    relations = set()

    executed = set()
    included = set()
    pending = set()

    def add_event(self, name):
        self.events.add(name)
        self.included.add(name)

    def add_relation(self, src, arr, tgt):
        self.relations.add(Relation(src, arr, tgt))

    def enabled(self):
        result = set(self.events)

        for r in self.relations:
            if r.rel == "condition":
                if r.src in self.included and not r.src in self.executed:
                    result.remove(r.tgt)
                break
            elif r.rel == "milestone":
                if r.src in self.included and r.src in self.pending:
                    result.remove(r.tgt)
                break
            else:
                break

        return result

    def execute(self, e):
        if e in self.pending:
            self.pending.remove(e)
        self.executed.add(e)

        for r in self.relations:
            if r.rel != e:
                continue

            if r.rel == 'exclude':
                self.included.remove(r.tgt)
            elif r.rel == "include":
                self.included.add(r.tgt)
            elif r.rel == "response":
                self.pending.add(r.tgt)

    def is_accepting(self):
        for e in self.pending:
            if e in self.included:
                return False
        return True
