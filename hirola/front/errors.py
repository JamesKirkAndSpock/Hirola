"""Contains custom error messages for predicted scenarios."""
landing_page_error = (
    'The dimensions of your image are {} pixels (width) by {} pixels (height).'
    '\nThe landing page has to have a width of 1280 pixels or more and a '
    'height of 700 pixels or more for clear images'
    )

phone_category_error = (
    'The maximum phone categories can only be four. Adding a fifth option will'
    ' displace the items on the top grid. You can only edit the four options'
    ' that already exist.'
)

phone_category_error_2 = (
    'The phone category {} already exists.'
)

category_image_error = (
    'The image needs to have an equal height and width dimension. The image '
    'you entered has a height of {} pixels and a width of {} pixels'
)

hot_deal_error = (
    'A hot deal of the phone {} already exists'
)
