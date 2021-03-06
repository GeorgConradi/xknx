import unittest

from xknx.knxip import KNXIPFrame, KNXIPServiceType, SearchResponse, \
    HPAI, DIBDeviceInformation, DIBSuppSVCFamilies


class Test_KNXIP_Discovery(unittest.TestCase):
    # pylint: disable=too-many-public-methods,invalid-name

    def test_connect_request(self):

        raw = ((0x06, 0x10, 0x02, 0x02, 0x00, 0x50, 0x08, 0x01,
                0xc0, 0xa8, 0x2a, 0x0a, 0x0e, 0x57, 0x36, 0x01,
                0x02, 0x00, 0x11, 0x00, 0x00, 0x00, 0x11, 0x22,
                0x33, 0x44, 0x55, 0x66, 0xe0, 0x00, 0x17, 0x0c,
                0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x47, 0x69,
                0x72, 0x61, 0x20, 0x4b, 0x4e, 0x58, 0x2f, 0x49,
                0x50, 0x2d, 0x52, 0x6f, 0x75, 0x74, 0x65, 0x72,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x0c, 0x02, 0x02, 0x01,
                0x03, 0x02, 0x04, 0x01, 0x05, 0x01, 0x07, 0x01))

        knxipframe = KNXIPFrame()
        self.assertEqual(knxipframe.from_knx(raw), 80)
        self.assertEqual(knxipframe.to_knx(), list(raw))

        self.assertTrue(isinstance(knxipframe.body, SearchResponse))
        self.assertEqual(
            knxipframe.body.control_endpoint,
            HPAI("192.168.42.10", 3671))
        self.assertEqual(len(knxipframe.body.dibs), 2)
        # Specific testing of parsing and serializing of
        # DIBDeviceInformation and DIBSuppSVCFamilies is
        # done within knxip_dib_test.py
        self.assertTrue(isinstance(
            knxipframe.body.dibs[0], DIBDeviceInformation))
        self.assertTrue(isinstance(
            knxipframe.body.dibs[1], DIBSuppSVCFamilies))
        self.assertEqual(knxipframe.body.device_name, "Gira KNX/IP-Router")

        knxipframe2 = KNXIPFrame()
        knxipframe2.init(KNXIPServiceType.SEARCH_RESPONSE)
        knxipframe2.body.control_endpoint = \
            HPAI(ip_addr="192.168.42.10", port=3671)
        knxipframe2.body.dibs.append(knxipframe.body.dibs[0])
        knxipframe2.body.dibs.append(knxipframe.body.dibs[1])
        knxipframe2.normalize()
        self.assertEqual(knxipframe2.to_knx(), list(raw))


SUITE = unittest.TestLoader().loadTestsFromTestCase(Test_KNXIP_Discovery)
unittest.TextTestRunner(verbosity=2).run(SUITE)
