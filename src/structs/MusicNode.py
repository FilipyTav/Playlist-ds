from structs.Music import Music


class SMusicNode:
    def __init__(self, data: Music):
        self.data = data

        self.next: SMusicNode | None = None
