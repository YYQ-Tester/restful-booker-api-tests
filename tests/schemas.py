
BOOKING_SCHEMA = {
    "type": "object",
    "required": ["firstname", "lastname", "totalprice",
                 "depositpaid", "bookingdates"],
    "properties": {
        "firstname":   {"type": "string"},
        "lastname":    {"type": "string"},
        "totalprice":  {"type": "number"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": {
            "type": "object",
            "required": ["checkin", "checkout"],
            "properties": {
                "checkin":  {"type": "string", "format": "date"},
                "checkout": {"type": "string", "format": "date"},
            },
        },
        "additionalneeds": {"type": "string"},
    },
}

BOOK_ID_SCHEMAS={
    "type":"array",
    "items":{
        "type":"object",
        "required":["bookingid"],
        "properties":{"bookingid":{"type":"integer"}}
    }
}
