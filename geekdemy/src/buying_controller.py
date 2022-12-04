from .coupon import Coupon
class BuyingController():
    ENROLMENT_FEE_CONSTANT=500.0
    ENROLMENT_THRESHOLD=6666.0
    DISCOUNT_THRESHOLD=10000.0
    PRO_MEMBERSHIP_FEE_CONSTANT=200.0
    PRO_MEMBERSHIP_DISCOUNT={
        'certification':0.02,
        'degree':0.03,
        'diploma':0.01
    }
    def __init__(self) -> None:
        self.programmes=[]
        self.coupons=[]
        self.total_programmes=0
        self.pro_membership_applied=False

    def add_pro_membership(self):
        self.pro_membership_applied=True

    def add_programme(self,programme):
        self.programmes.append(programme)
        self.total_programmes+=programme.programme_qty

    def add_coupon(self,coupon):
        self.coupons.append(coupon)

    def print_bill(self):
        self.total_programmes_fees()
        print(f'SUB_TOTAL {self.sub_total():.2f}')
        print(f'COUPON_DISCOUNT {self.applicable_coupon().coupon_name} {self.coupon_discount():.2f}')
        print(f'TOTAL_PRO_DISCOUNT {self.total_pro_discount():.2f}')
        print(f'PRO_MEMBERSHIP_FEE {self.get_pro_membership_fee():.2f}')
        print(f'ENROLLMENT_FEE {self.enrolment_fee():.2f}')
        print(f'TOTAL {self.total():.2f}')

    def total_programmes_fees(self):
        return sum(programme.programme_fee for programme in self.programmes)

    def cheapest_programme(self):
        cheapest_fee=float('inf')
        cheapest_programme=self.programmes[0].programme_name
        for programme in self.programmes:
            cheapest_fee=min(programme.programme_fee/programme.programme_qty,cheapest_fee)
            cheapest_programme=programme.programme_name
        return cheapest_programme,cheapest_fee

    def sub_total(self):
        return self.get_pro_membership_fee()-self.total_pro_discount()+self.total_programmes_fees()

    def total_pro_discount(self):
        total_pro_discount=0.0
        if self.pro_membership_applied:
            for programme in self.programmes:
                total_pro_discount+=(self.PRO_MEMBERSHIP_DISCOUNT[programme.programme_name]*programme.programme_fee)
        return total_pro_discount

    def get_pro_membership_fee(self):
        pro_membership_fee=0.0
        if self.pro_membership_applied:
            pro_membership_fee=self.PRO_MEMBERSHIP_FEE_CONSTANT
        return pro_membership_fee

    def enrolment_fee(self):
        enrolment_fee=0.0
        if self.total_programmes_fees()<self.ENROLMENT_THRESHOLD:
            enrolment_fee=self.ENROLMENT_FEE_CONSTANT
        return enrolment_fee

    def total(self):
        return self.sub_total()+self.enrolment_fee()-self.coupon_discount()

    def coupon_discount(self):
        coupon=self.applicable_coupon()
        if coupon.coupon_name=='B4G1':
            cheapest_programme,cheapest_programme_fee=self.cheapest_programme()
            pro_discount=0.0
            if self.pro_membership_applied:
                pro_discount=self.PRO_MEMBERSHIP_DISCOUNT[cheapest_programme]*cheapest_programme_fee
            coupon_discount=cheapest_programme_fee-pro_discount
        else:
            coupon_discount=self.sub_total()*coupon.coupon_discount
        return coupon_discount

    def applicable_coupon(self):
        if self.total_programmes>=4:
            return Coupon('B4G1')
        elif self.sub_total()>=self.DISCOUNT_THRESHOLD and 'DEAL_G20' in self.coupons:
            return Coupon('DEAL_G20')
        elif self.total_programmes>=2 and 'DEAL_G5' in self.coupons and 'DEAL_G20' not in self.coupons:
            return Coupon('DEAL_G5')
        elif self.total_programmes>2 and 'DEAL_G5' in self.coupons and 'DEAL_G20' in self.coupons:
            return Coupon('DEAL_G20')
        else:
            return Coupon()
