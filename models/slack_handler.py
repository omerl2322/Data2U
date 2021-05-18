from interfaces.delivery_method import DeliveryMethod


class ViaSlack(DeliveryMethod):
    def send_report(self, report):
        return None
