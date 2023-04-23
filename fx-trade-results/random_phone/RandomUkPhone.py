import random

class RandomUkPhone():
    area_codes = [
        {"code": "0113", "min": 4960000, "max": 4960999}, #Leeds
        {"code": "0114", "min": 4960000, "max": 4960999}, #Sheffield
        {"code": "0115", "min": 4960000, "max": 4960999}, #Nottingham
        {"code": "0116", "min": 4960000, "max": 4960999}, #Leicster
        {"code": "0117", "min": 4960000, "max": 4960999}, #Bristol
        {"code": "0118", "min": 4960000, "max": 4960999}, #Reading
        {"code": "0121", "min": 4960000, "max": 4960999}, #Birmingham
        {"code": "0131", "min": 4960000, "max": 4960999}, #Edinburgh
        {"code": "0141", "min": 4960000, "max": 4960999}, #Glasgow
        {"code": "0151", "min": 4960000, "max": 4960999}, #Liverpool
        {"code": "0161", "min": 4960000, "max": 4960999}, #Manchester
        {"code": "202", "min": 79460000, "max": 79460999}, #London
        {"code": "0191", "min": 4980000, "max": 4980999}, #Tyneside/Durham/Sunderland
        {"code": "028", "min": 96496000, "max": 96496999}, #Northern Ireland
        {"code": "029", "min": 20180000, "max": 20180999}, #Cardiff
        {"code": "01632", "min": 960000, "max": 960999} #No area
    ]

    mobile = {"code": "07700", "min": 900000, "max": 900999}
    freephone = {"code": "08081", "min": 570000, "max": 570999}
    premium = {"code": "0909", "min": 8790000, "max": 8790999}
    ukwide = {"code": "03069", "min": 990000, "max": 990999}

    def _random_number(self, template, international):
        number = random.randint(template['min'], template['max'])
        phoneno = "{}{}".format(template['code'], number)
        if international:
            phoneno = "{}{}".format("+44", phoneno[1:])
        return phoneno

    def random_landline(self, international=False):
        area = random.randint(1, len(self.area_codes))
        template = self.area_codes[area - 1]

        return self._random_number(template, international)
    
    def random_mobile(self, international=False):
        return self._random_number(self.mobile, international)
        
    def random_freephone(self, international=False):
        return self._random_number(self.freephone, international)
        
    def random_premium(self, international=False):
        return self._random_number(self.premium, international)
        
    def random_ukwide(self, international=False):
        return self._random_number(self.ukwide, international)