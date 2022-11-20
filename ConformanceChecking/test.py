import Engine


def Show(P):
    print("    Enabled: {}".format(P.enabled()))
    print("    Accepting: {}".format(P.is_accepting()))
    print("    Included: {}".format(P.included))


def Execute(P, e):
    print("Executing {}".format(e))
    P.execute(e)
    Show(P)


def Header(P, title):
    print("* New graph: {}".format(title))
    Show(P)


def main():
    print("DCR Process Test")

    # Construct A -->* B
    P = Engine.Process()
    P.add_event("A")
    P.add_event("B")
    P.add_relation("A", "condition", "B")

    Header(P, "A-->* B")
    Execute(P, "A")

    # Construct A *--> B
    P = Engine.Process()
    P.add_event("A")
    P.add_event("B")
    P.add_relation("A", "response", "B")

    Header(P, "A *--> B")
    Execute(P, "A")
    Execute(P, "B")

    # Construct process A-->% B-->* C
    P = Engine.Process()
    P.add_event("A")
    P.add_event("B")
    P.add_event("C")
    P.add_relation("A", "exclude", "B")
    P.add_relation("B", "condition", "C")

    Header(P, "A -->% B -->* C")
    Execute(P, "A")

    # construct process A -->% !B --<> C
    P = Engine.Process()
    P.add_event("A")
    P.add_event("B")
    P.included.remove("B")
    P.pending.add("B")
    P.add_event("C")
    P.add_relation("A", "exclude", "B")
    P.add_relation("B", "milestone", "C")

    Header(P, "A -->% !B --<> C")
    Execute(P, "A")

    # construct process A -->+ %B
    P = Engine.Process()
    P.add_event("A")
    P.add_event("B")
    P.add_relation("A", "include", "B")
    P.included.remove("B")

    Header(P, "A -->+ %B")
    Execute(P, "A")


if __name__ == "__main__":
    main()
