"""Contains tests for orders."""
from front.base_test import BaseTestCase
from front.admin import OrderInline


class Orders(BaseTestCase):
    """Tests orders."""

    def setUp(self):
        """
        Set up order test pre-conditions.
        """
        super(Orders, self).setUp()

    def test_shipping_address(self):
        '''
        Test that a shippig address only allows one order
        '''
        self.assertEqual(OrderInline.max_num, 1)
        get_response = self.elena.get("/admin/front/order/add/")
        self.assertContains(get_response, "Shipping address")
