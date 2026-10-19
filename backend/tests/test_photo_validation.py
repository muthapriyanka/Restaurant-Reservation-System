import unittest

from fastapi import HTTPException

from app.routes import photos


class PhotoValidationTest(unittest.TestCase):
    def test_accepts_supported_image_signatures(self):
        self.assertTrue(
            photos._matches_declared_image_type(b"\xff\xd8\xffpayload", "image/jpeg")
        )
        self.assertTrue(
            photos._matches_declared_image_type(
                b"\x89PNG\r\n\x1a\npayload", "image/png"
            )
        )
        self.assertTrue(
            photos._matches_declared_image_type(
                b"RIFF\x04\x00\x00\x00WEBPpayload", "image/webp"
            )
        )

    def test_rejects_mismatched_image_signature(self):
        self.assertFalse(
            photos._matches_declared_image_type(b"<script>alert(1)</script>", "image/jpeg")
        )

    def test_media_route_rejects_non_image_prefix(self):
        with self.assertRaises(HTTPException) as error:
            photos.read_media("private/config.json")

        self.assertEqual(error.exception.status_code, 404)


if __name__ == "__main__":
    unittest.main()
