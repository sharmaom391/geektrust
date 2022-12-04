class Coupon():
    coupons={
        'B4G1':'n-1',
        'DEAL_G20':0.2,
        'DEAL_G5':0.05
    }
    def __init__(self,coupon_name=None) -> None:
        self.coupon_name=coupon_name
        self.coupon_discount=self.coupons.get(coupon_name,0.0)
