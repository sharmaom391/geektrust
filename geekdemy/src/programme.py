class Programme():
    programmes={
            'certification':3000.0,
            'degree':5000.0,
            'diploma':2500.0
    }
    def __init__(self,programme_name,programme_quantity) -> None:
        self.programme_name=programme_name
        self.programme_fee=self.programmes[programme_name]*programme_quantity
        self.programme_qty=programme_quantity